#!/usr/bin/env python3
"""
Apply Night Shade Art watermark to SOCIAL/preview images only.

Print masters stay clean forever:
  gallery/print-masters/*.png   (fulfillment / Stripe / POD upload)
  gallery/*.png                 (canonical clean masters; do not watermark)

Social (Instagram etc.) only:
  gallery/social/*.jpg          (watermarked)

Usage:
  python3 scripts/watermark_for_social.py                 # all pieces
  python3 scripts/watermark_for_social.py 02-moonlit...   # one basename
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"
PRINT = GALLERY / "print-masters"
SOCIAL = GALLERY / "social"
BRAND = ROOT / "assets" / "brand"
WATERMARK = BRAND / "watermark-corner.png"
# Fallback if corner missing
WATERMARK_ALT = BRAND / "watermark-logo-transparent.png"

# Opacity of watermark overlay (0–1). High enough to ruin casual screenshot prints,
# low enough the art still looks good on IG.
OPACITY = 0.72
# Scale watermark width as fraction of image width
WIDTH_FRAC = 0.42
# Padding from bottom-right edge as fraction of image size
PAD_FRAC = 0.035


def ensure_dirs() -> None:
    PRINT.mkdir(parents=True, exist_ok=True)
    SOCIAL.mkdir(parents=True, exist_ok=True)
    BRAND.mkdir(parents=True, exist_ok=True)


def load_watermark() -> Image.Image:
    path = WATERMARK if WATERMARK.exists() else WATERMARK_ALT
    if not path.exists():
        raise SystemExit(f"Missing watermark asset: {WATERMARK}")
    return Image.open(path).convert("RGBA")


def apply_opacity(im: Image.Image, opacity: float) -> Image.Image:
    if opacity >= 0.999:
        return im
    r, g, b, a = im.split()
    a = a.point(lambda p: int(p * opacity))
    out = Image.merge("RGBA", (r, g, b, a))
    return out


def watermark_one(src: Path, dest: Path, mark: Image.Image) -> Path:
    base = Image.open(src).convert("RGBA")
    w, h = base.size
    target_w = max(120, int(w * WIDTH_FRAC))
    ratio = target_w / mark.width
    target_h = max(40, int(mark.height * ratio))
    mark_r = mark.resize((target_w, target_h), Image.Resampling.LANCZOS)
    mark_r = apply_opacity(mark_r, OPACITY)

    pad_x = int(w * PAD_FRAC)
    pad_y = int(h * PAD_FRAC)
    x = w - mark_r.width - pad_x
    y = h - mark_r.height - pad_y

    layered = base.copy()
    layered.alpha_composite(mark_r, (x, y))
    # Also add a faint diagonal handle line so center crops still show ownership
    # (light, bottom-third only via the corner mark is enough for v1)

    rgb = layered.convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    rgb.save(dest, "JPEG", quality=90, optimize=True)
    return dest


def sync_print_master(src: Path) -> Path:
    """Guarantee a clean copy exists under print-masters/."""
    dest = PRINT / src.name
    if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
        dest.write_bytes(src.read_bytes())
    return dest


def piece_sources(only: list[str] | None) -> list[Path]:
    files = sorted(GALLERY.glob("[0-9][0-9]-*.png"))
    if only:
        wanted = set()
        for o in only:
            o = o.removesuffix(".png").removesuffix(".jpg")
            wanted.add(o)
        files = [f for f in files if f.stem in wanted or f.name in wanted]
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pieces", nargs="*", help="Optional piece basenames")
    ap.add_argument("--opacity", type=float, default=None)
    args = ap.parse_args()
    opacity = args.opacity if args.opacity is not None else OPACITY
    globals()["OPACITY"] = opacity

    ensure_dirs()
    mark = load_watermark()
    sources = piece_sources(args.pieces or None)
    if not sources:
        print("No gallery pieces found.", file=sys.stderr)
        return 1

    for src in sources:
        sync_print_master(src)
        out = SOCIAL / f"{src.stem}.jpg"
        watermark_one(src, out, mark)
        print(f"social: {out.name}  |  print-master: {src.name} (clean)")
    print(f"Done. {len(sources)} social watermarked; print masters untouched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
