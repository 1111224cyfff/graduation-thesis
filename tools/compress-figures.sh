#!/usr/bin/env bash
# 图片压缩脚本：压缩 figures/ 顶层的 PNG、JPG 与栅格底图 PDF
# - PNG: pngquant 质量 65-80
# - JPG: jpegoptim 质量 85（lossy，已是 -m 上限）
# - PDF: ghostscript /printer (300dpi)，仅在压缩后体积明显更小时替换
#
# 使用：
#   bash tools/compress-figures.sh              # 处理 figures/ 顶层
#   bash tools/compress-figures.sh path/to/dir  # 处理指定目录顶层
#   FORCE=1 bash tools/compress-figures.sh      # 忽略时间戳，重压全部

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PAPER_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

TARGET_DIR="${1:-${PAPER_DIR}/figures}"
STAMP_DIR="${TARGET_DIR}/.compress-stamps"
FORCE="${FORCE:-0}"

# 压缩参数（与询问选项中"高质量"对应）
PNG_QUALITY="${PNG_QUALITY:-65-80}"
JPG_QUALITY="${JPG_QUALITY:-85}"
PDF_PRESET="${PDF_PRESET:-/printer}"   # 300dpi，适合论文打印
# 仅当压缩 PDF 至少节省 PDF_PDF_MIN_GAIN_RATIO 时才替换原文件（保护矢量 PDF）
PDF_MIN_GAIN_RATIO="${PDF_MIN_GAIN_RATIO:-0.10}"   # 至少节省 10%

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "[compress] target directory not found: $TARGET_DIR" >&2
  exit 1
fi

need_tool() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "[compress] missing tool: $1 (brew install $2)" >&2
    exit 1
  fi
}

need_tool pngquant pngquant
need_tool jpegoptim jpegoptim
need_tool gs ghostscript

mkdir -p "$STAMP_DIR"

# 是否需要压缩（基于戳文件 mtime）
needs_compress() {
  local src="$1"
  local stamp="$STAMP_DIR/$(basename -- "$src").stamp"
  if [[ "$FORCE" == "1" ]]; then return 0; fi
  if [[ ! -f "$stamp" ]]; then return 0; fi
  if [[ "$src" -nt "$stamp" ]]; then return 0; fi
  return 1
}
mark_done() {
  local src="$1"
  local stamp="$STAMP_DIR/$(basename -- "$src").stamp"
  : > "$stamp"
  touch -r "$src" "$stamp"
}

human_size() {
  local bytes="$1"
  if (( bytes >= 1048576 )); then
    awk -v b="$bytes" 'BEGIN{printf "%.1fM", b/1048576}'
  elif (( bytes >= 1024 )); then
    awk -v b="$bytes" 'BEGIN{printf "%.1fK", b/1024}'
  else
    echo "${bytes}B"
  fi
}

bytes_of() {
  stat -f '%z' "$1" 2>/dev/null || stat -c '%s' "$1"
}

total_before=0
total_after=0
processed=0
skipped=0

compress_png() {
  local f="$1"
  local before after
  before=$(bytes_of "$f")
  # pngquant: --skip-if-larger 保证不会增大；--strip 去 metadata
  if pngquant --quality="$PNG_QUALITY" --skip-if-larger --strip --force --output "$f.tmp" -- "$f" 2>/dev/null; then
    after=$(bytes_of "$f.tmp")
    if (( after < before )); then
      mv "$f.tmp" "$f"
      echo "  PNG  $(basename -- "$f"): $(human_size "$before") -> $(human_size "$after")"
      total_before=$((total_before + before))
      total_after=$((total_after + after))
      ((processed += 1))
      return
    fi
    rm -f "$f.tmp"
  else
    rm -f "$f.tmp"
  fi
  echo "  PNG  $(basename -- "$f"): skipped (no gain)"
  ((skipped += 1))
}

compress_jpg() {
  local f="$1"
  local before after
  before=$(bytes_of "$f")
  # jpegoptim: --max 设置最大质量，--strip-all 去 metadata，--all-progressive 改为渐进式（通常更小）
  if jpegoptim --quiet --max="$JPG_QUALITY" --strip-all --all-progressive "$f"; then
    after=$(bytes_of "$f")
    if (( after < before )); then
      echo "  JPG  $(basename -- "$f"): $(human_size "$before") -> $(human_size "$after")"
      total_before=$((total_before + before))
      total_after=$((total_after + after))
      ((processed += 1))
      return
    fi
  fi
  echo "  JPG  $(basename -- "$f"): skipped (no gain)"
  ((skipped += 1))
}

compress_pdf() {
  local f="$1"
  local before after tmp
  before=$(bytes_of "$f")
  tmp="$f.tmp"
  if gs -q -dNOPAUSE -dBATCH -dSAFER \
        -sDEVICE=pdfwrite \
        -dPDFSETTINGS="$PDF_PRESET" \
        -dCompatibilityLevel=1.5 \
        -dDetectDuplicateImages=true \
        -dColorImageResolution=300 \
        -dGrayImageResolution=300 \
        -dMonoImageResolution=600 \
        -sOutputFile="$tmp" "$f" 2>/dev/null; then
    after=$(bytes_of "$tmp")
    local gain_ratio
    gain_ratio=$(awk -v b="$before" -v a="$after" 'BEGIN{ if(b<=0){print 0; exit} printf "%.4f", (b-a)/b }')
    # 防护：如果压缩后体积过小（<5% 且 <5KB），极可能是 gs 破坏了内容，跳过
    too_small=$(awk -v a="$after" -v b="$before" 'BEGIN{ if(a<5120 && a/b<0.05) print 1; else print 0 }')
    if [[ "$too_small" == "1" ]]; then
      rm -f "$tmp"
      echo "  PDF  $(basename -- "$f"): skipped (compressed too small, likely corrupted)"
      ((skipped += 1))
      return
    fi
    if awk -v g="$gain_ratio" -v m="$PDF_MIN_GAIN_RATIO" 'BEGIN{exit !(g >= m)}'; then
      mv "$tmp" "$f"
      echo "  PDF  $(basename -- "$f"): $(human_size "$before") -> $(human_size "$after")  [gain $(awk -v g="$gain_ratio" 'BEGIN{printf "%.0f%%", g*100}')]"
      total_before=$((total_before + before))
      total_after=$((total_after + after))
      ((processed += 1))
      return
    fi
    rm -f "$tmp"
  fi
  echo "  PDF  $(basename -- "$f"): skipped (no significant gain, likely vector)"
  ((skipped += 1))
}

echo "[compress] target = $TARGET_DIR"
echo "[compress] PNG quality=$PNG_QUALITY, JPG quality=$JPG_QUALITY, PDF preset=$PDF_PRESET"
echo

# 仅处理顶层（不递归子目录，避免压缩备份/素材）
while IFS= read -r -d '' f; do
  if ! needs_compress "$f"; then
    ((skipped += 1))
    continue
  fi
  ext_lower=$(printf '%s' "${f##*.}" | tr '[:upper:]' '[:lower:]')
  case "$ext_lower" in
    png) compress_png "$f" ;;
    jpg|jpeg) compress_jpg "$f" ;;
    pdf) compress_pdf "$f" ;;
    *) continue ;;
  esac
  mark_done "$f"
done < <(find "$TARGET_DIR" -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.pdf" \) -print0)

echo
if (( total_before > 0 )); then
  saved=$((total_before - total_after))
  ratio=$(awk -v s="$saved" -v b="$total_before" 'BEGIN{printf "%.1f", s/b*100}')
  echo "[compress] processed=$processed, skipped=$skipped"
  echo "[compress] saved $(human_size "$saved") of $(human_size "$total_before")  (-${ratio}%)"
else
  echo "[compress] processed=$processed, skipped=$skipped, no savings"
fi
