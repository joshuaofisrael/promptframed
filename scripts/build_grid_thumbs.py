#!/usr/bin/env python3
"""Page-speed hygiene for grid pages (index.html, buy.html).

Grid cards were downloading the full 1024-1536px watermarked piece JPGs
(~400 KB each, ~17 MB for the whole wall). This makes 600px-wide
thumbnails from those SAME watermarked assets (never the print masters)
and gives each grid <img> a srcset so phones and laptops pull the small
file while high-density screens can still pick the full image.

Idempotent: safe to run every SEO run; new daily pieces get picked up.
"""
import glob, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
THUMBS = os.path.join(ASSETS, "thumbs")
THUMB_W = 600
PAGES = ["index.html", "buy.html"]
SIZES = "(max-width: 640px) 92vw, (max-width: 1100px) 45vw, 22rem"


def build_thumbs():
    os.makedirs(THUMBS, exist_ok=True)
    made = 0
    for src in sorted(glob.glob(os.path.join(ASSETS, "[0-9][0-9]-*.jpg"))):
        dst = os.path.join(THUMBS, os.path.basename(src))
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            continue
        im = Image.open(src).convert("RGB")
        w, h = im.size
        if w > THUMB_W:
            im = im.resize((THUMB_W, round(h * THUMB_W / w)), Image.LANCZOS)
        im.save(dst, "JPEG", quality=78, optimize=True, progressive=True)
        made += 1
    return made


IMG_RE = re.compile(r'<img src="\./assets/([0-9][0-9]-[^"/]+\.jpg)"([^>]*)>')


def rewrite(page):
    path = os.path.join(ROOT, page)
    html = open(path, encoding="utf-8").read()

    def sub(m):
        name, rest = m.group(1), m.group(2)
        if "srcset=" in rest or not os.path.exists(os.path.join(THUMBS, name)):
            return m.group(0)
        full_w = Image.open(os.path.join(ASSETS, name)).size[0]
        srcset = f'./assets/thumbs/{name} {THUMB_W}w, ./assets/{name} {full_w}w'
        extra = f' srcset="{srcset}" sizes="{SIZES}"'
        if "decoding=" not in rest:
            extra += ' decoding="async"'
        return f'<img src="./assets/thumbs/{name}"{extra}{rest}>'

    new = IMG_RE.sub(sub, html)
    if new != html:
        open(path, "w", encoding="utf-8").write(new)
        return True
    return False


if __name__ == "__main__":
    n = build_thumbs()
    changed = [p for p in PAGES if rewrite(p)]
    print(f"thumbs built: {n}; pages updated: {changed or 'none'}")
