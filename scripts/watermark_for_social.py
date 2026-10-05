#!/usr/bin/env python3
"""
Apply the Night Shade Art watermark to public previews only.

Print masters stay clean forever (never opened for compositing, never overwritten
with a watermark):
  gallery/[0-9][0-9]-*.png       canonical clean masters (local, gitignored)
  gallery/print-masters/*.png    fulfillment / POD upload copies (local, gitignored)
  gallery/night-windows-contact-sheet.png   clean contact-sheet source (local)

Public previews (watermarked):
  gallery/social/*.jpg           Instagram / Stripe product image
  assets/[0-9][0-9]-*.jpg        website, piece pages, og/twitter
  assets/night-windows-contact-sheet.jpg

Usage:
  python3 scripts/watermark_for_social.py                  # social + website + sheet
  python3 scripts/watermark_for_social.py 02-moonlit...    # one basename
  python3 scripts/watermark_for_social.py --website        # website JPGs + sheet only
  python3 scripts/watermark_for_social.py --stamp path.jpg # one loose public JPEG
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
ASSETS = ROOT / "assets"
BRAND = ASSETS / "brand"
WATERMARK = BRAND / "watermark-corner.png"
# Fallback if corner missing
WATERMARK_ALT = BRAND / "watermark-logo-transparent.png"
CONTACT_SRC = GALLERY / "night-windows-contact-sheet.png"
CONTACT_DST = ASSETS / "night-windows-contact-sheet.jpg"
# Matches the width/height attributes on the series pages.
CONTACT_SITE_SIZE = (1400, 933)

# Opacity of watermark overlay (0–1). High enough to ruin casual screenshot prints,
# low enough the art still looks good on IG and on the site.
OPACITY = 0.72
# Scale watermark width as fraction of image width
WIDTH_FRAC = 0.42
# Padding from bottom-right edge as fraction of image size
PAD_FRAC = 0.035

# Website derivatives match the publish scripts: cap width, smaller JPEG.
WEBSITE_MAX_WIDTH = 1200
WEBSITE_JPEG_QUALITY = 85
SOCIAL_JPEG_QUALITY = 90


def ensure_dirs() -> None:
    PRINT.mkdir(parents=True, exist_ok=True)
    SOCIAL.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
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


def _assert_preview_dest(dest: Path) -> None:
    """Public previews are JPEGs. Print masters are PNGs and must stay clean."""
    if dest.suffix.lower() != ".jpg":
        raise SystemExit(
            f"Refusing to write a non-JPEG preview (print masters stay clean PNGs): {dest}"
        )
    if "print-masters" in dest.resolve().parts:
        raise SystemExit(f"Refusing to write into print-masters: {dest}")


def mark_geometry(width: int, height: int, mark: Image.Image) -> tuple[int, int, int, int]:
    target_w = max(120, int(width * WIDTH_FRAC))
    ratio = target_w / mark.width
    target_h = max(40, int(mark.height * ratio))
    pad_x = int(width * PAD_FRAC)
    pad_y = int(height * PAD_FRAC)
    x = width - target_w - pad_x
    y = height - target_h - pad_y
    return x, y, target_w, target_h


def composite_mark(base: Image.Image, mark: Image.Image) -> Image.Image:
    """Return an RGBA image with the corner mark. Does not touch the source file."""
    layer = base.convert("RGBA")
    w, h = layer.size
    x, y, target_w, target_h = mark_geometry(w, h, mark)
    mark_r = mark.resize((target_w, target_h), Image.Resampling.LANCZOS)
    mark_r = apply_opacity(mark_r, OPACITY)
    layer.alpha_composite(mark_r, (x, y))
    return layer


def _save_jpeg(im: Image.Image, dest: Path, *, quality: int, progressive: bool) -> None:
    _assert_preview_dest(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(
        dest,
        "JPEG",
        quality=quality,
        optimize=True,
        progressive=progressive,
    )


def watermark_one(src: Path, dest: Path, mark: Image.Image) -> Path:
    """Full-resolution social JPEG. `src` is read; print masters are not modified."""
    base = Image.open(src).convert("RGBA")
    layered = composite_mark(base, mark)
    _save_jpeg(layered, dest, quality=SOCIAL_JPEG_QUALITY, progressive=False)
    return dest


def _resize_max_width(im: Image.Image, max_width: int) -> Image.Image:
    w, h = im.size
    if w <= max_width:
        return im
    ratio = max_width / float(w)
    new_size = (max_width, max(1, int(round(h * ratio))))
    return im.resize(new_size, Image.Resampling.LANCZOS)


def export_website_jpg(src: Path, dest: Path, mark: Image.Image | None = None) -> tuple[int, int]:
    """Clean PNG → watermarked website JPEG. Returns saved (width, height).

    Resizes like the publish scripts (max width 1200) then applies the same
    corner mark used for gallery/social. Never writes a PNG.
    """
    if mark is None:
        mark = load_watermark()
    with Image.open(src) as raw:
        base = _resize_max_width(raw.convert("RGBA"), WEBSITE_MAX_WIDTH)
    layered = composite_mark(base, mark)
    _save_jpeg(layered, dest, quality=WEBSITE_JPEG_QUALITY, progressive=True)
    return layered.size


def _row_col_means(im: Image.Image) -> tuple[list[float], list[float]]:
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    rows = []
    for y in range(h):
        acc = 0.0
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            acc += (r + g + b) / 3
        rows.append(acc / ((w + 1) // 2))
    cols = []
    for x in range(w):
        acc = 0.0
        for y in range(0, h, 2):
            r, g, b = px[x, y]
            acc += (r + g + b) / 3
        cols.append(acc / ((h + 1) // 2))
    return rows, cols


def _gutter_spans(means: list[float], threshold: float = 180.0) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    start = None
    for i, m in enumerate(means):
        if m >= threshold:
            if start is None:
                start = i
        elif start is not None:
            spans.append((start, i))
            start = None
    if start is not None:
        spans.append((start, len(means)))
    # A bright frame around the whole sheet is not a cell gutter.
    return [(a, b) for a, b in spans if a > 2 and b < len(means) - 2]


def _intervals(length: int, gutters: list[tuple[int, int]]) -> list[tuple[int, int]]:
    cuts = [0]
    for a, b in gutters:
        cuts.append(a)
        cuts.append(b)
    cuts.append(length)
    intervals = []
    for i in range(0, len(cuts) - 1, 2):
        start, end = cuts[i], cuts[i + 1]
        if end - start > 8:
            intervals.append((start, end))
    return intervals


def _watermark_contact_cells(sheet: Image.Image, mark: Image.Image) -> Image.Image:
    """Stamp the corner mark on every panel so a crop of one window is not clean."""
    rows, cols = _row_col_means(sheet)
    row_gutters = _gutter_spans(rows)
    col_gutters = _gutter_spans(cols)
    y_iv = _intervals(sheet.height, row_gutters)
    x_iv = _intervals(sheet.width, col_gutters)
    if len(x_iv) < 2 or len(y_iv) < 2:
        return composite_mark(sheet, mark)
    out = sheet.convert("RGBA")
    for y0, y1 in y_iv:
        for x0, x1 in x_iv:
            cell = out.crop((x0, y0, x1, y1))
            marked = composite_mark(cell, mark)
            out.paste(marked, (x0, y0))
    return out


def export_contact_sheet(mark: Image.Image | None = None) -> Path | None:
    """Watermark each panel of the clean contact sheet into the public JPEG."""
    if not CONTACT_SRC.is_file():
        print(f"contact sheet source missing, skipped: {CONTACT_SRC.name}", file=sys.stderr)
        return None
    if mark is None:
        mark = load_watermark()
    with Image.open(CONTACT_SRC) as raw:
        sheet = raw.convert("RGBA")
        if sheet.size != CONTACT_SITE_SIZE:
            sheet = sheet.resize(CONTACT_SITE_SIZE, Image.Resampling.LANCZOS)
    marked = _watermark_contact_cells(sheet, mark)
    _save_jpeg(marked, CONTACT_DST, quality=WEBSITE_JPEG_QUALITY, progressive=True)
    return CONTACT_DST


def stamp_public_jpeg(path: Path, mark: Image.Image | None = None) -> Path:
    """Watermark one already-exported public JPEG in place.

    Refuses PNGs and anything under print-masters. Do not point this at a file
    that is already watermarked; it would stamp a second mark.
    """
    _assert_preview_dest(path)
    if not path.is_file():
        raise SystemExit(f"No such JPEG: {path}")
    if mark is None:
        mark = load_watermark()
    with Image.open(path) as raw:
        layered = composite_mark(raw.convert("RGBA"), mark)
    _save_jpeg(layered, path, quality=SOCIAL_JPEG_QUALITY, progressive=False)
    return path


def sync_print_master(src: Path) -> Path:
    """Guarantee a clean byte-for-byte copy exists under print-masters/."""
    dest = PRINT / src.name
    if dest.suffix.lower() != ".png":
        raise SystemExit(f"Refusing to sync a non-PNG print master: {src}")
    if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime or dest.stat().st_size != src.stat().st_size:
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


def export_piece(src: Path, mark: Image.Image, *, social: bool, website: bool) -> None:
    """Write public previews for one piece. The PNG master is only read and copied."""
    master_before = src.read_bytes()
    synced = sync_print_master(src)
    if social:
        watermark_one(src, SOCIAL / f"{src.stem}.jpg", mark)
    if website:
        export_website_jpg(src, ASSETS / f"{src.stem}.jpg", mark)
    if src.read_bytes() != master_before:
        raise SystemExit(f"Print master was modified (this is a bug): {src}")
    if synced.read_bytes() != master_before:
        raise SystemExit(f"print-masters copy is not a clean byte copy: {synced}")
    bits = []
    if social:
        bits.append("social")
    if website:
        bits.append("website")
    print(f"{' + '.join(bits)}: {src.stem}  |  print-master: {src.name} (clean)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pieces", nargs="*", help="Optional piece basenames")
    ap.add_argument("--opacity", type=float, default=None)
    ap.add_argument(
        "--website",
        action="store_true",
        help="Write website JPGs and the contact sheet only (do not re-encode social)",
    )
    ap.add_argument(
        "--stamp",
        action="append",
        default=[],
        metavar="JPEG",
        help="Watermark an extra public JPEG in place (not a print master)",
    )
    args = ap.parse_args()
    if args.opacity is not None:
        globals()["OPACITY"] = args.opacity

    ensure_dirs()
    mark = load_watermark()

    if args.stamp and not args.pieces and not args.website:
        for raw in args.stamp:
            dest = stamp_public_jpeg(Path(raw), mark)
            print(f"stamped: {dest}")
        return 0

    sources = piece_sources(args.pieces or None)
    if not sources:
        print("No gallery pieces found.", file=sys.stderr)
        return 1

    write_social = not args.website
    for src in sources:
        export_piece(src, mark, social=write_social, website=True)

    # The contact sheet is one series image; refresh it whenever masters are present.
    if not args.pieces:
        sheet = export_contact_sheet(mark)
        if sheet:
            print(f"contact sheet: {sheet.relative_to(ROOT)} (each panel watermarked)")

    for raw in args.stamp:
        dest = stamp_public_jpeg(Path(raw), mark)
        print(f"stamped: {dest}")

    print(
        f"Done. {len(sources)} public previews watermarked; print masters untouched."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
