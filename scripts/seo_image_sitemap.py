#!/usr/bin/env python3
"""SEO: Google image-sitemap entries for every Night Windows piece page.

Art prints are found through image search as much as web search, but until now
Google could only discover our pictures by rendering each page. This adds an
<image:image><image:loc> for each piece URL in sitemap.xml (and the contact
sheet on the series hub), using the WATERMARKED public previews in assets/
only, never gallery/*.png or gallery/print-masters/.

Only <image:loc> is written: Google dropped image:title / caption / license
in 2022, so the alt text on the page carries the description.

Idempotent: safe to run after every drop (publish scripts call it at the end).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap.xml"
PRODUCTS = ROOT / "products.json"
BASE = "https://moonlitwindows.com"
NS = 'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'


def main() -> None:
    xml = SITEMAP.read_text(encoding="utf-8")
    if NS not in xml:
        xml = xml.replace(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n        {NS}>',
            1,
        )
    images = {
        f"{BASE}/night-windows.html": f"{BASE}/assets/night-windows-contact-sheet.jpg",
    }
    for item in json.loads(PRODUCTS.read_text(encoding="utf-8")):
        asset = item.get("asset", "")
        if not re.fullmatch(r"\d\d-[a-z0-9-]+\.jpg", asset):
            continue  # only watermarked public previews
        if not (ROOT / "assets" / asset).is_file():
            continue
        images[f"{BASE}/pieces/{item['slug']}.html"] = f"{BASE}/assets/{asset}"

    added = 0
    for page, img in images.items():
        plain = f"<url><loc>{page}</loc></url>"
        if plain not in xml:
            continue  # already has an image entry (or page not in sitemap)
        rich = (
            f"<url>\n    <loc>{page}</loc>\n"
            f"    <image:image><image:loc>{img}</image:loc></image:image>\n  </url>"
        )
        xml = xml.replace(plain, rich, 1)
        added += 1
    for bad in ("print-masters", ".png<"):
        if bad in xml:
            raise SystemExit(f"sitemap would expose a non-public image ({bad})")
    SITEMAP.write_text(xml, encoding="utf-8")
    total = xml.count("<image:image>")
    print(f"image sitemap: added {added}; {total} image entries total")


if __name__ == "__main__":
    main()
