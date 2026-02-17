import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence


@dataclass(frozen=True)
class CitationField:
    raw_marker: str
    item_keys: List[str]


def _latex_escape(value: str) -> str:
    # Minimal escaping for BibTeX/BibLaTeX values.
    # We keep this conservative to avoid mangling CJK text.
    return (
        value.replace("\\", "\\\\")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("%", "\\%")
        .replace("&", "\\&")
        .replace("$", "\\$")
        .replace("#", "\\#")
        .replace("_", "\\_")
        .replace("~", "\\textasciitilde{}")
        .replace("^", "\\textasciicircum{}")
    )


def _find_pandoc_explicit() -> Optional[Path]:
    """Find pandoc.exe without relying on PATH refresh."""
    candidates: List[Path] = []

    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        candidates.append(
            Path(local_app_data)
            / "Microsoft"
            / "WinGet"
            / "Packages"
            / "JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe"
            / "pandoc-3.8.3"
            / "pandoc.exe"
        )

        # Fallback: look for any pandoc.exe under this package dir
        pkg_root = (
            Path(local_app_data)
            / "Microsoft"
            / "WinGet"
            / "Packages"
            / "JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe"
        )
        if pkg_root.exists():
            candidates.extend(pkg_root.rglob("pandoc.exe"))

    candidates.extend(
        [
            Path(os.environ.get("ProgramFiles", "C:\\Program Files"))
            / "Pandoc"
            / "pandoc.exe",
            Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"))
            / "Pandoc"
            / "pandoc.exe",
        ]
    )

    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    return None


def _run(cmd: Sequence[str], *, cwd: Optional[Path] = None) -> None:
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def _rewrite_markdown_for_tongjithesis(md_text: str) -> str:
    """Make pandoc markdown headings align with tongjithesis chapter/section structure.

    - Drops the first title line like "# 题目：..." (Word title is already in main.tex).
    - Removes manual numbering prefixes (e.g. "第1章 ", "1.2.3 ").
    """
    lines = md_text.splitlines()
    out: List[str] = []

    # Drop a leading "题目" heading if present.
    i = 0
    if i < len(lines) and re.match(r"^#\s*题目[:：]", lines[i].strip()):
        i += 1
        # Skip following blank lines.
        while i < len(lines) and lines[i].strip() == "":
            i += 1

    for line in lines[i:]:
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not m:
            out.append(line)
            continue

        hashes = m.group(1)
        title = m.group(2).strip()

        # "第1章 引言" -> "引言"
        title = re.sub(r"^第\s*\d+\s*章\s+", "", title)
        # "1.2.3 标题" -> "标题"
        title = re.sub(r"^\d+(?:\.\d+)*\s+", "", title)

        out.append(f"{hashes} {title}".rstrip())

    return "\n".join(out) + "\n"


def _convert_wmf_to_png(media_dir: Path) -> None:
    """Convert any .wmf images to .png for PDFLaTeX compatibility."""
    if not media_dir.exists():
        return

    wmf_files = list(media_dir.rglob("*.wmf"))
    if not wmf_files:
        return

    magick = shutil.which("magick")
    if not magick:
        raise RuntimeError("Found .wmf images but ImageMagick 'magick' is not available")

    for wmf in wmf_files:
        png = wmf.with_suffix(".png")
        # Use a decent density to keep text legible.
        _run([magick, "-density", "300", str(wmf), str(png)])



def _read_docx_xml(docx_path: Path, inner_path: str) -> str:
    with zipfile.ZipFile(docx_path, "r") as zf:
        data = zf.read(inner_path)
    # Word XML is UTF-8.
    return data.decode("utf-8", errors="strict")


def _extract_instr_text(xml_text: str) -> str:
    """Concatenate all Word field instruction texts (w:instrText) in document order."""
    # WordprocessingML namespace
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    root = ET.fromstring(xml_text)
    parts: List[str] = []
    for el in root.iterfind(".//w:instrText", ns):
        if el.text:
            parts.append(el.text)
    return "".join(parts)


def _extract_csl_json_objects_from_instr(instr_text: str) -> List[str]:
    """Extract CSL_CITATION JSON objects from concatenated instruction text.

    We locate occurrences of 'CSL_CITATION' then parse a JSON object by matching
    braces while respecting quoted strings and escape sequences.
    """
    results: List[str] = []
    idx = 0
    token = "CSL_CITATION"
    while True:
        pos = instr_text.find(token, idx)
        if pos == -1:
            break

        brace_start = instr_text.find("{", pos)
        if brace_start == -1:
            idx = pos + len(token)
            continue

        depth = 0
        in_string = False
        escape = False
        end = None
        for i in range(brace_start, len(instr_text)):
            ch = instr_text[i]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue

            if ch == '"':
                in_string = True
                continue

            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break

        if end is None:
            idx = brace_start + 1
            continue

        raw_json = instr_text[brace_start:end]
        results.append(raw_json)
        idx = end

    return results


def _citation_item_keys_from_csl_json(csl_json_text: str) -> List[str]:
    # The JSON is typically XML-escaped.
    unescaped = html.unescape(csl_json_text)
    obj = json.loads(unescaped)

    keys: List[str] = []
    for item in obj.get("citationItems", []) or []:
        # Prefer explicit item keys when present in uris.
        uris = item.get("uris") or []
        for uri in uris:
            # Example: http://zotero.org/users/local/XXXX/items/ABCD1234
            if isinstance(uri, str) and "/items/" in uri:
                k = uri.rsplit("/items/", 1)[-1].strip()
                if k:
                    keys.append(k)
                    break

        # Sometimes the Zotero internal numeric id is present; we can't
        # deterministically map it to a BibTeX key without talking to Zotero.
        # We skip it here.

    # Preserve order, de-dup.
    seen = set()
    out: List[str] = []
    for k in keys:
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out


def _iter_citation_items(csl_json_text: str):
    """Yield (item_key, item_data) from a CSL_CITATION JSON block."""
    unescaped = html.unescape(csl_json_text)
    obj = json.loads(unescaped)
    for item in obj.get("citationItems", []) or []:
        uris = item.get("uris") or []
        item_key = None
        for uri in uris:
            if isinstance(uri, str) and "/items/" in uri:
                item_key = uri.rsplit("/items/", 1)[-1].strip() or None
                break
        if item_key is None:
            continue
        item_data = item.get("itemData") or {}
        if not isinstance(item_data, dict):
            item_data = {}
        yield item_key, item_data


def _csl_date_to_year(item_data: dict) -> Optional[str]:
    issued = item_data.get("issued")
    if isinstance(issued, dict):
        parts = issued.get("date-parts")
        if isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]:
            y = parts[0][0]
            if isinstance(y, int):
                return str(y)
            if isinstance(y, str) and y.isdigit():
                return y
    # Sometimes there is a plain 'year'
    y = item_data.get("year")
    if isinstance(y, int):
        return str(y)
    if isinstance(y, str) and y.strip():
        return y.strip()
    return None


def _csl_names_to_bib(names) -> Optional[str]:
    if not isinstance(names, list) or not names:
        return None
    out = []
    for n in names:
        if not isinstance(n, dict):
            continue
        literal = n.get("literal")
        if isinstance(literal, str) and literal.strip():
            out.append(literal.strip())
            continue
        family = n.get("family")
        given = n.get("given")
        if isinstance(family, str) and family.strip() and isinstance(given, str) and given.strip():
            out.append(f"{family.strip()}, {given.strip()}")
        elif isinstance(family, str) and family.strip():
            out.append(family.strip())
        elif isinstance(given, str) and given.strip():
            out.append(given.strip())
    if not out:
        return None
    return " and ".join(out)


def _csl_type_to_biblatex_entry_type(csl_type: str) -> str:
    mapping = {
        "book": "book",
        "article-journal": "article",
        "paper-conference": "inproceedings",
        "chapter": "incollection",
        "report": "report",
        "thesis": "thesis",
        "webpage": "online",
        "post-weblog": "online",
    }
    return mapping.get(csl_type, "misc")


def _itemdata_to_biblatex_fields(item_data: dict) -> dict:
    fields: dict = {}
    # Core
    title = item_data.get("title")
    if isinstance(title, str) and title.strip():
        fields["title"] = title.strip()

    author = _csl_names_to_bib(item_data.get("author"))
    if author:
        fields["author"] = author

    editor = _csl_names_to_bib(item_data.get("editor"))
    if editor:
        fields["editor"] = editor

    year = _csl_date_to_year(item_data)
    if year:
        fields["year"] = year

    # Container / publication
    container = item_data.get("container-title") or item_data.get("containerTitle")
    if isinstance(container, str) and container.strip():
        fields["journaltitle"] = container.strip()

    publisher = item_data.get("publisher")
    if isinstance(publisher, str) and publisher.strip():
        fields["publisher"] = publisher.strip()

    location = item_data.get("publisher-place") or item_data.get("publisherPlace")
    if isinstance(location, str) and location.strip():
        fields["location"] = location.strip()

    volume = item_data.get("volume")
    if isinstance(volume, str) and volume.strip():
        fields["volume"] = volume.strip()
    elif isinstance(volume, int):
        fields["volume"] = str(volume)

    number = item_data.get("issue") or item_data.get("number")
    if isinstance(number, str) and number.strip():
        fields["number"] = number.strip()
    elif isinstance(number, int):
        fields["number"] = str(number)

    pages = item_data.get("page") or item_data.get("pages")
    if isinstance(pages, str) and pages.strip():
        fields["pages"] = pages.strip()

    doi = item_data.get("DOI") or item_data.get("doi")
    if isinstance(doi, str) and doi.strip():
        fields["doi"] = doi.strip()

    url = item_data.get("URL") or item_data.get("url")
    if isinstance(url, str) and url.strip():
        fields["url"] = url.strip()

    return fields


def _write_biblatex(bib_path: Path, itemdata_by_key: dict) -> None:
    lines: List[str] = []
    for key in sorted(itemdata_by_key.keys()):
        item = itemdata_by_key[key]
        csl_type = item.get("type") if isinstance(item, dict) else None
        entry_type = _csl_type_to_biblatex_entry_type(csl_type) if isinstance(csl_type, str) else "misc"
        fields = _itemdata_to_biblatex_fields(item if isinstance(item, dict) else {})

        lines.append(f"@{entry_type}{{{key},")
        for fname, fval in fields.items():
            escaped = _latex_escape(str(fval))
            lines.append(f"  {fname} = {{{escaped}}},")
        # Remove trailing comma by adding a harmless note if empty? Keep as-is; biblatex tolerates.
        lines.append("}\n")

    bib_path.write_text("\n".join(lines), encoding="utf-8")


def _extract_citations_from_docx(docx_path: Path) -> List[CitationField]:
    # Citations can exist in the main document and sometimes in footnotes/endnotes.
    xml_paths = ["word/document.xml", "word/footnotes.xml", "word/endnotes.xml"]
    instr_chunks: List[str] = []
    for p in xml_paths:
        try:
            xml_text = _read_docx_xml(docx_path, p)
        except KeyError:
            continue
        try:
            instr_chunks.append(_extract_instr_text(xml_text))
        except ET.ParseError:
            continue

    instr_text = "".join(instr_chunks)
    csl_jsons = _extract_csl_json_objects_from_instr(instr_text)

    citations: List[CitationField] = []
    for j in csl_jsons:
        keys = _citation_item_keys_from_csl_json(j)
        citations.append(CitationField(raw_marker=j[:64], item_keys=keys))

    return citations


def _extract_itemdata_by_key_from_docx(docx_path: Path) -> dict:
    xml_paths = ["word/document.xml", "word/footnotes.xml", "word/endnotes.xml"]
    instr_chunks: List[str] = []
    for p in xml_paths:
        try:
            xml_text = _read_docx_xml(docx_path, p)
        except KeyError:
            continue
        try:
            instr_chunks.append(_extract_instr_text(xml_text))
        except ET.ParseError:
            continue
    instr_text = "".join(instr_chunks)
    csl_jsons = _extract_csl_json_objects_from_instr(instr_text)

    itemdata_by_key: dict = {}
    for j in csl_jsons:
        for item_key, item_data in _iter_citation_items(j):
            # First seen wins (later should be identical).
            itemdata_by_key.setdefault(item_key, item_data)
    return itemdata_by_key


def _replace_pandoc_numeric_cites_in_markdown(md_text: str, citations: Sequence[CitationField]) -> str:
    """Replace pandoc's numeric citation markers like ^\[1\]^ with \cite{...}.

    This assumes the markers appear in the same order as the Zotero fields.
    """
    marker_re = re.compile(r"\^\\\[[^\]]+\\\]\^")
    matches = list(marker_re.finditer(md_text))

    if len(matches) != len(citations):
        raise RuntimeError(
            f"Citation count mismatch: markdown has {len(matches)} markers, "
            f"but docx has {len(citations)} Zotero citation fields. "
            "If your Word document contains a generated bibliography field or "
            "custom formatting, we may need a more robust alignment strategy."
        )

    parts: List[str] = []
    last = 0
    for match, citation in zip(matches, citations):
        parts.append(md_text[last : match.start()])
        if citation.item_keys:
            keys = ",".join(citation.item_keys)
            parts.append(f"\\cite{{{keys}}}")
        else:
            # Fallback: keep the original marker if we couldn't resolve keys.
            parts.append(match.group(0))
        last = match.end()
    parts.append(md_text[last:])
    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--docx",
        type=Path,
        default=Path(r"C:\\Users\\Lenovo\\Desktop\\graduation_thesis\\word\\thesis.docx"),
        help="Path to the source .docx",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(r"C:\\Users\\Lenovo\\Desktop\\graduation_thesis\\word"),
        help="Output directory",
    )
    args = parser.parse_args()

    docx_path: Path = args.docx
    out_dir: Path = args.out_dir

    if not docx_path.exists():
        print(f"Missing docx: {docx_path}", file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)

    pandoc = _find_pandoc_explicit()
    if pandoc is None:
        print("pandoc.exe not found. Install it with: winget install --id JohnMacFarlane.Pandoc -e", file=sys.stderr)
        return 3

    citations = _extract_citations_from_docx(docx_path)
    itemdata_by_key = _extract_itemdata_by_key_from_docx(docx_path)

    raw_md = out_dir / "thesis.raw.md"
    cited_md = out_dir / "thesis.cited.md"
    out_tex = out_dir / "thesis.from_md.tex"
    keys_txt = out_dir / "thesis.zotero_item_keys.txt"
    out_bib = out_dir / "thesis.references.bib"
    tongji_md = out_dir / "thesis.tongji.md"
    tongji_tex = out_dir / "thesis.tongji.tex"
    media_root = out_dir / "media"

    # 1) docx -> markdown
    _run([
        str(pandoc),
        "-f",
        "docx",
        "-t",
        "markdown",
        "--extract-media",
        str(out_dir),
        "--wrap=none",
        "-o",
        str(raw_md),
        str(docx_path),
    ])

    md_text = raw_md.read_text(encoding="utf-8")

    # 2) replace numeric markers with \cite{ITEMKEY,...}
    md_with_cites = _replace_pandoc_numeric_cites_in_markdown(md_text, citations)
    cited_md.write_text(md_with_cites, encoding="utf-8")

    # 3) markdown -> latex
    _run([
        str(pandoc),
        "-f",
        "markdown+raw_tex",
        "-t",
        "latex",
        "--wrap=none",
        "-o",
        str(out_tex),
        str(cited_md),
    ])

    # 3.1) tongjithesis-friendly outputs (chapters/sections, image handling)
    tongji_md_text = _rewrite_markdown_for_tongjithesis(md_with_cites)
    tongji_md.write_text(tongji_md_text, encoding="utf-8")

    # Convert WMF to PNG (after extract-media, before LaTeX conversion).
    try:
        _convert_wmf_to_png(media_root)
    except Exception:
        # If conversion fails, keep going; users can manually convert later.
        pass

    _run([
        str(pandoc),
        "-f",
        "markdown+raw_tex",
        "-t",
        "latex",
        "--wrap=none",
        "--top-level-division=chapter",
        "-o",
        str(tongji_tex),
        str(tongji_md),
    ])

    # Post-process the LaTeX snippet so it can be \input into an existing document.
    tex_lines = tongji_tex.read_text(encoding="utf-8").splitlines()
    out_lines: List[str] = []
    for line in tex_lines:
        # Replace \hl{...} with plain text to avoid missing macro errors
        line = re.sub(r"\\hl\{([^}]*)\}", r"\1", line)

        # Unwrap pandocbounded images: \pandocbounded{...} -> ...
        if "\\pandocbounded{" in line:
            line = line.replace("\\pandocbounded{", "")
            if line.endswith("}}"):
                line = line[:-1]

        # Fix media paths to be relative to the project root
        line = line.replace("{media/", "{word/media/")
        # Prefer PNG over WMF for PDF output
        line = line.replace(".wmf}", ".png}")

        out_lines.append(line)

    tongji_tex.write_text("\n".join(out_lines) + "\n", encoding="utf-8")

    # 4) write keys list (unique)
    all_keys: List[str] = []
    for c in citations:
        all_keys.extend(c.item_keys)
    uniq = []
    seen = set()
    for k in all_keys:
        if k not in seen:
            seen.add(k)
            uniq.append(k)

    keys_txt.write_text("\n".join(uniq) + ("\n" if uniq else ""), encoding="utf-8")

    # 5) write a BibLaTeX file derived from embedded Zotero CSL itemData.
    _write_biblatex(out_bib, itemdata_by_key)

    print(
        f"OK\n- raw md: {raw_md}\n- cited md: {cited_md}\n- latex: {out_tex}\n- tongji latex: {tongji_tex}\n- item keys: {keys_txt}\n- references: {out_bib}"
    )
    print(
        "\nNotes:\n"
        "- This .bib is generated from the CSL metadata embedded in the Word/Zotero fields.\n"
        "- If you want higher-fidelity BibLaTeX fields (GB/T 7714 specifics), export via Zotero + Better BibTeX and replace the .bib.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
