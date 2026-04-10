#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PAPER_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

INPUT_DIR="${1:-${PAPER_DIR}/figures}"
OUTPUT_DIR="${2:-${PAPER_DIR}/figures-cropped}"
MARGINS="${PDFCROP_MARGINS:-0}"

if [[ ! -d "$INPUT_DIR" ]]; then
  echo "[auto-pdfcrop] input directory not found: $INPUT_DIR" >&2
  exit 1
fi

if ! command -v pdfcrop >/dev/null 2>&1; then
  echo "[auto-pdfcrop] pdfcrop not found; skip auto-cropping." >&2
  exit 0
fi

mkdir -p "$OUTPUT_DIR"

total=0
cropped=0
skipped=0

while IFS= read -r -d '' src; do
  ((total += 1))

  rel="${src#"$INPUT_DIR"/}"
  dst="$OUTPUT_DIR/$rel"
  mkdir -p "$(dirname -- "$dst")"

  if [[ -f "$dst" && "$dst" -nt "$src" ]]; then
    ((skipped += 1))
    continue
  fi

  if ! pdfcrop --margins "$MARGINS" --clip "$src" "$dst" >/dev/null 2>&1; then
    echo "[auto-pdfcrop] failed: $rel" >&2
    exit 1
  fi

  ((cropped += 1))
done < <(find "$INPUT_DIR" -type f -iname '*.pdf' -print0)

if ((total == 0)); then
  echo "[auto-pdfcrop] no PDF files found in $INPUT_DIR"
elif ((cropped == 0)); then
  echo "[auto-pdfcrop] up to date ($total PDFs, $skipped skipped)"
else
  echo "[auto-pdfcrop] done ($total PDFs, $cropped cropped, $skipped skipped)"
fi
