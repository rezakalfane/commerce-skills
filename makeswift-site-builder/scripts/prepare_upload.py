#!/usr/bin/env python3
"""Flatten page assets into one folder ready to drag into the Makeswift file library.

Files are copied (not moved) as  <prefix>-<NN>-<name>.<ext>, in the order given by a
simple ordering file or by sorted path. The folder holds images ONLY, because it is
uploaded as-is with Makeswift's Files > New > "Upload folder". Name --out after the
client (e.g. assets/Dunlop) so the library folder gets that name. A manifest
(file -> section -> size) is written NEXT TO the folder as MAKESWIFT_MANIFEST.md.

Usage:
  python3 prepare_upload.py --src assets --out assets/Dunlop --prefix dunlop \
      [--order order.txt]      # optional: lines "relative/path.jpg | Section label"

Files listed in --order come first, in that order; everything else follows sorted.
Hidden files and the output folder itself are skipped.
"""
import argparse
import re
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # dimensions are optional
    Image = None

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--order")
    a = ap.parse_args()
    src, out = Path(a.src).resolve(), Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    for old in out.iterdir():
        if old.is_file():
            old.unlink()

    labels, ordered = {}, []
    if a.order:
        for line in Path(a.order).read_text().splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            path, _, label = (x.strip() for x in line.partition("|"))
            ordered.append((src / path).resolve())
            labels[(src / path).resolve()] = label
    rest = sorted(p.resolve() for p in src.rglob("*")
                  if p.is_file() and p.suffix.lower() in EXTS and not p.name.startswith(".")
                  and out not in p.resolve().parents)
    files = ordered + [p for p in rest if p not in ordered]

    rows = []
    for i, p in enumerate(files, 1):
        if not p.exists():
            raise SystemExit(f"missing: {p}")
        name = f"{a.prefix}-{i:02d}-{slug(p.stem)}{p.suffix.lower()}"
        shutil.copy2(p, out / name)
        dims = ""
        if Image and p.suffix.lower() != ".svg":
            with Image.open(p) as im:
                dims = f"{im.width}×{im.height}"
        rows.append((name, labels.get(p, ""), dims, f"{p.stat().st_size // 1024} KB", p.relative_to(src)))

    with open(out.parent / "MAKESWIFT_MANIFEST.md", "w") as f:
        f.write(f"# Makeswift upload manifest ({a.prefix})\n\n"
                f"Upload `{out.name}/` via Makeswift Files > Workspace > New > Upload folder, then "
                f"search `{a.prefix}-` in any image picker.\n\n"
                "| File | Section | Size | Weight | Source |\n|---|---|---|---|---|\n")
        for r in rows:
            f.write("| " + " | ".join(str(x) for x in r) + " |\n")
    print(f"{len(rows)} files -> {out}")


if __name__ == "__main__":
    main()
