#!/usr/bin/env python3
"""
Make a private 9:16 (1080x1920) generation input from a clean gallery master.
Output goes to /tmp/reelsrc/ (never into gallery/ or anywhere public).

Usage: python3 scripts/prep_reel_source.py 26-banff-lake-louise-moon [--x-offset 60]
  --x-offset: left edge of the 9:16 crop in master pixels (default: centred).
"""
import argparse
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("piece")
ap.add_argument("--x-offset", type=int, default=None)
a = ap.parse_args()
src = ROOT / "gallery" / f"{a.piece.removesuffix('.png')}.png"
im = Image.open(src).convert("RGB")
w, h = im.size
cw = round(h * 9 / 16)
if cw <= w:
    x = (w - cw) // 2 if a.x_offset is None else max(0, min(a.x_offset, w - cw))
    im = im.crop((x, 0, x + cw, h))
else:  # wider-than-tall masters: crop height instead
    ch = round(w * 16 / 9); y = (h - ch) // 2
    im = im.crop((0, y, w, y + ch))
out = Path("/tmp/reelsrc") / f"{src.stem}-9x16.png"
out.parent.mkdir(parents=True, exist_ok=True)
im.resize((1080, 1920), Image.Resampling.LANCZOS).save(out)
print(out)
