---
name: latex-thesis-build-debug
description: Build and debug this TongjiThesis LaTeX repository (XeLaTeX + biblatex/biber). Use when compilation fails, bibliography breaks, fonts are missing, or images can’t be found.
license: Apache-2.0
---

You are working in a TongjiThesis-based LaTeX repo. Follow this workflow to build and fix build failures with minimal, targeted edits.

## 1) Pick the correct entry file
Prefer the file the user is actively editing. In this repository, likely entry points are:

- `main.tex` (repo root; includes the Word→LaTeX export workflow)

If unsure, search for `\\documentclass` and choose the top-level file that inputs the main body (e.g., `\\input{...}`) and prints bibliography.

## 2) Build with latexmk (XeLaTeX)
Use XeLaTeX because the class uses `xeCJK`.

- Fast build:
  - `latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex`

- If bibliography is wrong or missing, force a full rebuild:
  - `latexmk -xelatex -interaction=nonstopmode -file-line-error -gg main.tex`

If `latexmk` is unavailable, fall back to the explicit sequence:

1. `xelatex -interaction=nonstopmode -file-line-error main.tex`
2. `biber main`
3. `xelatex -interaction=nonstopmode -file-line-error main.tex`
4. `xelatex -interaction=nonstopmode -file-line-error main.tex`

## 3) Locate the real error quickly
When a build fails:

- Prefer the first error (the one right after the first `!`).
- Use `-file-line-error` output to jump to the file and line.
- If you have a `.log`, scan it:
  - `Select-String -Path *.log -Pattern "^! |LaTeX Error|Package .* Error" -CaseSensitive:$false`

## 4) Common fixes in this repo
### Fonts (xeCJK)
`tongjithesis.cls` uses 方正 fonts by default. On machines without these fonts you may see missing glyphs or font-not-found errors.

- Prefer a minimal override in the entry `.tex` (as done in `main.tex`): use `\\IfFontExistsTF{SimSun}{...}{}` to switch to SimSun/SimHei/KaiTi when available.
- If SimSun is also missing, ask the user what fonts are installed or suggest installing a CJK font set.

### Bibliography (biblatex + biber)
This template enforces GB/T 7714-2015 via `biblatex`.

- Confirm the entry `.tex` includes `\\addbibresource{...}` and ends with `\\printbibliography`.
- If citations don’t appear, verify `biber` ran and the `.bcf`/`.bbl` files are generated.
- If `.bib` path issues appear, check whether it is relative to the entry file.

### Images
For the Word-export pipeline, images typically live under `word/media/` and `main.tex` sets `\\graphicspath{{word/}}`.

- If an image is missing, confirm the file exists and the path matches case and extension.

## 5) Keep fixes minimal
- Change the smallest surface area possible (usually the entry `.tex`).
- Rebuild after each change.
- Don’t refactor unrelated LaTeX.

## Optional helper script
If you’re in VS Code/terminal on Windows, you can use `scripts/build.ps1` from this skill folder to run a consistent `latexmk` command.

Defaults:
- If `main.tex` exists, it is used.
