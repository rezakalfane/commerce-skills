#!/usr/bin/env python3
"""Crop a horizontal row of image tiles (e.g. an Instagram feed, a gallery strip) out of a
screenshot, for sections whose images only exist after JavaScript runs.

Finds the tiles by scanning one row of pixels for runs that differ from the page
background, then finds each tile's top and bottom edges. A tile whose scan row hits
background-coloured content (e.g. white logo text on a dark tile) is missed by the
scan; with --count, missing tiles are inferred from the spacing of the detected ones.

Usage:
  python3 crop_tiles.py "screens/*2.57.37*" --y 0.67 --count 4 --out assets --name gallery
     --y     scan row, as a fraction of image height (or an absolute pixel value if > 1)
     --bg    background colour as hex (default ffffff); --tol colour tolerance (default 10)
     --min   minimum tile width in px (default 200)
Writes <out>/<name>-1.jpg … and prints the boxes. Always look at the crops afterwards.
"""
import argparse
import glob
from pathlib import Path

from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("screenshot", help="path or glob (screenshot names often contain U+202F)")
    ap.add_argument("--y", type=float, required=True)
    ap.add_argument("--count", type=int)
    ap.add_argument("--out", default=".")
    ap.add_argument("--name", default="tile")
    ap.add_argument("--bg", default="ffffff")
    ap.add_argument("--tol", type=int, default=10)
    ap.add_argument("--min", type=int, default=200)
    a = ap.parse_args()

    paths = glob.glob(a.screenshot) or [a.screenshot]
    im = Image.open(paths[0]).convert("RGB")
    W, H = im.size
    y = int(a.y * H) if a.y <= 1 else int(a.y)
    bg = tuple(int(a.bg[i:i + 2], 16) for i in (0, 2, 4))
    is_bg = lambda p: all(abs(c - b) <= a.tol for c, b in zip(p, bg))  # noqa: E731

    runs, start = [], None
    for x in range(W):
        b = is_bg(im.getpixel((x, y)))
        if not b and start is None:
            start = x
        elif b and start is not None:
            runs.append((start, x))
            start = None
    if start is not None:
        runs.append((start, W))
    runs = [r for r in runs if r[1] - r[0] >= a.min]
    if not runs:
        raise SystemExit("no tiles found on that row; try another --y")

    # vertical extent from the first tile's centre column
    cx = (runs[0][0] + runs[0][1]) // 2
    top = bot = y
    while top > 0 and not is_bg(im.getpixel((cx, top - 1))):
        top -= 1
    while bot < H - 1 and not is_bg(im.getpixel((cx, bot + 1))):
        bot += 1

    # infer missing tiles from the typical width and gap
    if a.count and len(runs) < a.count and len(runs) >= 2:
        w = round(sum(r[1] - r[0] for r in runs) / len(runs))
        gap = round(sum(runs[i + 1][0] - runs[i][1] for i in range(len(runs) - 1)) / (len(runs) - 1))
        while len(runs) < a.count:
            x0 = runs[-1][1] + gap
            if x0 + w > W:
                break
            runs.append((x0, x0 + w))

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for i, (x0, x1) in enumerate(runs, 1):
        box = (x0 + 2, top + 2, x1 - 2, bot - 1)  # trim anti-aliased edges
        p = out / f"{a.name}-{i}.jpg"
        im.crop(box).save(p, quality=92)
        print(p, box, f"{box[2] - box[0]}×{box[3] - box[1]}")


if __name__ == "__main__":
    main()
