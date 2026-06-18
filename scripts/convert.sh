#!/usr/bin/env bash
# Convert draw.io diagrams to .webp images.
#
# Workflow (per diagram):
#   1. Edit the Mermaid source of truth: mermaid/articles/<slug>/<n>-name.mmd
#      (the .mmd holds the diagram's logic; it is kept in the repo but hidden from readers)
#   2. Reflect the change in the rich version: drawio/articles/<slug>/<n>-name.drawio
#   3. Run this script to render *.drawio -> images/articles/<slug>/<n>-name.webp
#   4. The article references only the .webp (see the single-line HTML comment next to each image)
#
# Usage:
#   scripts/convert.sh                       # convert every *.drawio under drawio/articles/
#   scripts/convert.sh path/to/file.drawio   # convert a single file
#   scripts/convert.sh drawio/articles/slug  # convert a directory
#   mise run drawio2webp                     # same as running with no arguments
#
# Output path mirrors the input: drawio/articles/<slug>/<n>.drawio -> images/articles/<slug>/<n>.webp
set -euo pipefail

DRAWIO_BIN="${DRAWIO_BIN:-/Applications/draw.io.app/Contents/MacOS/draw.io}"
SCALE="${SCALE:-2}"
BORDER="${BORDER:-20}"
QUALITY="${QUALITY:-85}"

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

convert_one() {
  local src="$1"
  local abs_src rel out tmpdir
  abs_src="$(cd "$(dirname "$src")" && pwd)/$(basename "$src")"
  rel="${abs_src#"$repo_root"/drawio/}"
  out="$repo_root/images/${rel%.drawio}.webp"
  mkdir -p "$(dirname "$out")"
  tmpdir="$(mktemp -d)"
  "$DRAWIO_BIN" --export --format png --scale "$SCALE" --border "$BORDER" \
    --output "$tmpdir/out.png" "$abs_src" >/dev/null
  cwebp -quiet -q "$QUALITY" "$tmpdir/out.png" -o "$out"
  rm -rf "$tmpdir"
  echo "✓ ${rel} -> images/${rel%.drawio}.webp"
}

targets=("$@")
[ ${#targets[@]} -eq 0 ] && targets=("$repo_root/drawio/articles")

for t in "${targets[@]}"; do
  if [ -d "$t" ]; then
    while IFS= read -r -d '' f; do convert_one "$f"; done \
      < <(find "$t" -name '*.drawio' -not -name '.*' -print0 | sort -z)
  else
    convert_one "$t"
  fi
done
