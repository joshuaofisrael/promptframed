#!/usr/bin/env python3
"""Publish Night Windows pieces 31–35 into the Prompt Framed site.

Expects PNG masters already present under gallery/:
  gallery/31-mont-saint-michel-moon.png
  gallery/32-hallstatt-lake-moon.png
  gallery/33-zhangjiajie-pillars-moon.png
  gallery/34-bagan-temples-night.png
  gallery/35-matterhorn-alpine-moon.png

Run from repo root:
  python3 scripts/publish_pieces_31_35.py

Idempotent: skips catalog/products rows and HTML cards that already exist.
Also refreshes night-windows.html series list + piece-30 next link.
Does NOT git commit or push.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as e:
    sys.exit(f"Pillow required: {e}")

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"
ASSETS = ROOT / "assets"
PIECES = ROOT / "pieces"
CATALOG_PATH = GALLERY / "catalog.json"
PRODUCTS_PATH = ROOT / "products.json"
INDEX_PATH = ROOT / "index.html"
BUY_PATH = ROOT / "buy.html"
SITEMAP_PATH = ROOT / "sitemap.xml"
SERIES_PATH = ROOT / "night-windows.html"
BASE_URL = "https://moonlitwindows.com"

STYLE = (
    "Dreamy cinematic fantasy realism, photorealistic landscape photography, "
    "ethereal moonlight, dramatic clouds, lush vegetation and wildflowers, "
    "deep atmospheric perspective, rich blue-green nighttime tones, subtle warm lights, "
    "romantic landscape aesthetic, peaceful dreamlike atmosphere, highly detailed, "
    "realistic natural textures, volumetric haze, dramatic but believable lighting."
)

NEW_PIECES = [
    {
        "id": "31-mont-saint-michel-moon",
        "slug": "mont-saint-michel-moon",
        "title": "Mont Saint-Michel Moon",
        "photoNumber": 31,
        "file": "31-mont-saint-michel-moon.png",
        "asset": "31-mont-saint-michel-moon.jpg",
        "alt": (
            "Moonlit Mont Saint-Michel abbey rising from reflective tidal flats, warm window "
            "glow on stone walls, wildflowers on the shore, and a full moon through dramatic night clouds"
        ),
        "description": (
            "The abbey rises from silver tidal water while moonlight and warm windows hush a "
            "quiet Mont Saint-Michel night."
        ),
        "card_blurb": "Tidal flats, abbey spire, and a moon over Mont Saint-Michel.",
        "keywords": [
            "Mont Saint-Michel night",
            "Normandy moonlight",
            "tidal island wall art",
            "abbey print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "32-hallstatt-lake-moon",
        "slug": "hallstatt-lake-moon",
        "title": "Hallstatt Lake Moon",
        "photoNumber": 32,
        "file": "32-hallstatt-lake-moon.png",
        "asset": "32-hallstatt-lake-moon.jpg",
        "alt": (
            "Moonlit Hallstatt lakeside village with church steeple reflected in still alpine water, "
            "timber houses, sheer mountains, and a full moon through dramatic night clouds"
        ),
        "description": (
            "Hallstatt’s steeple mirrors in still alpine water while moonlight and warm windows "
            "settle over a quiet lakeside night."
        ),
        "card_blurb": "Alpine lake mirror, church steeple, and a moon over Hallstatt.",
        "keywords": [
            "Hallstatt night",
            "Austrian lake moonlight",
            "alpine village wall art",
            "lakeside print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "33-zhangjiajie-pillars-moon",
        "slug": "zhangjiajie-pillars-moon",
        "title": "Zhangjiajie Pillars Moon",
        "photoNumber": 33,
        "file": "33-zhangjiajie-pillars-moon.png",
        "asset": "33-zhangjiajie-pillars-moon.jpg",
        "alt": (
            "Moonlit Zhangjiajie sandstone pillars rising from misty forest valleys with lush "
            "cliff vegetation, volumetric haze, and a full moon through dramatic night clouds"
        ),
        "description": (
            "Sandstone pillars rise through forest mist as moonlight and blue-green haze soften "
            "a quiet Zhangjiajie night."
        ),
        "card_blurb": "Stone pillars, forest mist, and a moon over Zhangjiajie.",
        "keywords": [
            "Zhangjiajie night",
            "Avatar mountains moonlight",
            "sandstone pillar wall art",
            "China landscape print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "34-bagan-temples-night",
        "slug": "bagan-temples-night",
        "title": "Bagan Temples Night",
        "photoNumber": 34,
        "file": "34-bagan-temples-night.png",
        "asset": "34-bagan-temples-night.jpg",
        "alt": (
            "Moonlit Bagan temple plain with countless brick stupas and pagodas across misty "
            "fields, soft warm temple lights, and a full moon through dramatic night clouds"
        ),
        "description": (
            "Brick stupas scatter across a misty plain while moonlight and soft temple glow hush "
            "a quiet Bagan night."
        ),
        "card_blurb": "Temple plain, mist, and a moon over Bagan.",
        "keywords": [
            "Bagan night",
            "Myanmar temples moonlight",
            "pagoda plain wall art",
            "stupa print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "35-matterhorn-alpine-moon",
        "slug": "matterhorn-alpine-moon",
        "title": "Matterhorn Alpine Moon",
        "photoNumber": 35,
        "file": "35-matterhorn-alpine-moon.png",
        "asset": "35-matterhorn-alpine-moon.jpg",
        "alt": (
            "Moonlit Matterhorn peak above alpine meadows with snow ridges reflected in a still "
            "lake, wildflowers, pines, and a full moon through dramatic night clouds"
        ),
        "description": (
            "The Matterhorn’s pyramid rises over a still alpine lake while moonlight silvers snow "
            "ridges and wildflower meadows."
        ),
        "card_blurb": "Pyramid peak, alpine lake, and a moon over the Matterhorn.",
        "keywords": [
            "Matterhorn night",
            "Zermatt moonlight",
            "Swiss Alps wall art",
            "alpine peak print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
]

NEXT_BY_SLUG = {
    "norwegian-stave-church-fjord": "mont-saint-michel-moon",
    "mont-saint-michel-moon": "hallstatt-lake-moon",
    "hallstatt-lake-moon": "zhangjiajie-pillars-moon",
    "zhangjiajie-pillars-moon": "bagan-temples-night",
    "bagan-temples-night": "matterhorn-alpine-moon",
    "matterhorn-alpine-moon": "moonlit-alpine-meadow",
}

NEXT_LABEL = {
    "moonlit-alpine-meadow": "First window",
}

SERIES_LINKS = [
    ("moonlit-alpine-meadow", "Moonlit Alpine Meadow"),
    ("moonlit-mediterranean-village", "Moonlit Mediterranean Village"),
    ("snowy-peaks-above-clouds", "Snowy Peaks Above Clouds"),
    ("coastal-cliffside-town", "Coastal Cliffside Town"),
    ("lakeside-cabin", "Lakeside Cabin"),
    ("hilltop-path-village", "Hilltop Path to Village"),
    ("moonlit-waterfall", "Moonlit Waterfall"),
    ("wildflower-meadow-cabin", "Wildflower Meadow Cabin"),
    ("northern-lights-fjord", "Northern Lights Fjord"),
    ("mediterranean-lantern-walk", "Mediterranean Lantern Walk"),
    ("moonlit-rice-terraces", "Moonlit Rice Terraces"),
    ("venetian-canal-moonrise", "Venetian Canal Moonrise"),
    ("japanese-temple-pond", "Japanese Temple Pond"),
    ("moroccan-kasbah-night", "Moroccan Kasbah Night"),
    ("scottish-highlands-loch", "Scottish Highlands Loch"),
    ("provence-lavender-moon", "Provence Lavender Moon"),
    ("amalfi-terrace-night", "Amalfi Terrace Night"),
    ("patagonia-lake-peaks", "Patagonia Lake Peaks"),
    ("bali-jungle-temple", "Bali Jungle Temple"),
    ("iceland-black-sand-moon", "Iceland Black Sand Moon"),
    ("cappadocia-fairy-chimneys", "Cappadocia Fairy Chimneys"),
    ("santorini-caldera-moon", "Santorini Caldera Moon"),
    ("tuscany-cypress-hills", "Tuscany Cypress Hills"),
    ("machu-picchu-mist", "Machu Picchu Mist"),
    ("ha-long-bay-moon", "Ha Long Bay Moon"),
    ("banff-lake-louise-moon", "Banff Lake Louise Moon"),
    ("petra-treasury-night", "Petra Treasury Night"),
    ("kyoto-bamboo-moon", "Kyoto Bamboo Moon"),
    ("yosemite-half-dome-moon", "Yosemite Half Dome Moon"),
    ("norwegian-stave-church-fjord", "Norwegian Stave Church Fjord"),
    ("mont-saint-michel-moon", "Mont Saint-Michel Moon"),
    ("hallstatt-lake-moon", "Hallstatt Lake Moon"),
    ("zhangjiajie-pillars-moon", "Zhangjiajie Pillars Moon"),
    ("bagan-temples-night", "Bagan Temples Night"),
    ("matterhorn-alpine-moon", "Matterhorn Alpine Moon"),
]


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def check_pngs() -> None:
    missing = []
    for p in NEW_PIECES:
        path = GALLERY / p["file"]
        if not path.is_file():
            missing.append(str(path.relative_to(ROOT)))
    if missing:
        die(
            "Missing PNG masters (do not invent files). Drop them then re-run:\n  - "
            + "\n  - ".join(missing)
        )


def convert_jpg(piece: dict) -> tuple[int, int, str]:
    src = GALLERY / piece["file"]
    dst = ASSETS / piece["asset"]
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        max_w = 1200
        if w > max_w:
            ratio = max_w / float(w)
            new_size = (max_w, max(1, int(round(h * ratio))))
            im = im.resize(new_size, Image.Resampling.LANCZOS)
            w, h = im.size
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, "JPEG", quality=85, optimize=True, progressive=True)
    orientation = "portrait" if h >= w else "landscape"
    print(f"  JPG {dst.relative_to(ROOT)} ({w}x{h}, {orientation})")
    return w, h, orientation


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, data) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def append_catalog(piece: dict, width: int, height: int, orientation: str) -> None:
    catalog = load_json(CATALOG_PATH)
    if any(e.get("id") == piece["id"] or e.get("slug") == piece["slug"] for e in catalog):
        print(f"  catalog: skip existing {piece['id']}")
        return
    catalog.append(
        {
            "id": piece["id"],
            "slug": piece["slug"],
            "title": piece["title"],
            "photoNumber": piece["photoNumber"],
            "source": "ChatGPT",
            "file": piece["file"],
            "width": width,
            "height": height,
            "orientation": orientation,
            "stylePrompt": STYLE,
            "alt": piece["alt"],
            "description": piece["description"],
            "keywords": piece["keywords"],
            "products": ["poster", "framed_print"],
            "status": "ready",
        }
    )
    dump_json(CATALOG_PATH, catalog)
    print(f"  catalog: appended {piece['id']}")


def append_products(piece: dict) -> None:
    products = load_json(PRODUCTS_PATH)
    if any(e.get("slug") == piece["slug"] for e in products):
        print(f"  products: skip existing {piece['slug']}")
        return
    products.append(
        {
            "slug": piece["slug"],
            "title": piece["title"],
            "series": "Night Windows",
            "photoNumber": piece["photoNumber"],
            "printful": {
                "posterUrl": None,
                "framedUrl": None,
                "status": "placeholder",
            },
            "stripe": {
                "posterUrl": None,
                "framedUrl": None,
                "status": "placeholder",
            },
            "asset": piece["asset"],
            "printSource": f"gallery/{piece['file']}",
        }
    )
    dump_json(PRODUCTS_PATH, products)
    print(f"  products: appended {piece['slug']}")


def display_dims(width: int, height: int) -> tuple[int, int]:
    if height >= width:
        return 900, 1350
    return 900, 822


def piece_html(piece: dict, width: int, height: int) -> str:
    slug = piece["slug"]
    next_slug = NEXT_BY_SLUG[slug]
    next_label = NEXT_LABEL.get(next_slug, "Next window")
    dw, dh = display_dims(width, height)
    num = f"{piece['photoNumber']:02d}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{piece['title']} — Night Windows print | Prompt Framed</title>
  <meta name="description" content="{piece['title']} from the Night Windows series. Poster and framed print options. {piece['description']}" />
  <link rel="canonical" href="{BASE_URL}/pieces/{slug}.html" />
  <meta property="og:title" content="{piece['title']} — Night Windows | Prompt Framed" />
  <meta property="og:description" content="{piece['description']}" />
  <meta property="og:url" content="{BASE_URL}/pieces/{slug}.html" />
  <meta property="og:image" content="{BASE_URL}/assets/{piece['asset']}" />
  <meta property="og:image:alt" content="{piece['alt']}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{piece['title']} — Night Windows | Prompt Framed" />
  <meta name="twitter:description" content="{piece['description']}" />
  <meta name="twitter:image" content="{BASE_URL}/assets/{piece['asset']}" />
  <link rel="stylesheet" href="../styles.css" />
</head>
<body>
  <div class="wrap">
    <header class="site-header">
      <a class="brand" href="../">Prompt <span>Framed</span></a>
      <nav class="nav">
        <a href="../#gallery">Gallery</a>
        <a href="../night-windows.html">The series</a>
        <a href="../buy.html">Buy a print</a>
        <a href="../about.html">About</a>
        <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a>
      </nav>
    </header>
    <article class="piece">
      <img src="../assets/{piece['asset']}" width="{dw}" height="{dh}" alt="{piece['alt']}" />
      <div>
        <div class="kicker">Night Windows · {num}</div>
        <h1>{piece['title']}</h1>
        <p class="desc">{piece['description']}</p>
        <div class="actions">
          <a class="btn" href="../buy.html#{slug}">Buy this print</a>
          <a class="btn secondary" href="./{next_slug}.html">{next_label}</a>
        </div>
        <p class="note">Want a poster? Buy at the link. Poster and framed sizes ship via print-on-demand after checkout.</p>
        <p class="note"><a href="../night-windows.html">Browse the full Night Windows series</a> · Night Shade Art on Instagram: <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a></p>
      </div>
    </article>
  </div>
  <footer class="site-footer"><div class="wrap"><div>© Prompt Framed · Joshua Israel Ventures LLC · Night Shade Art</div><div><a href="../">Back to gallery</a> · <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a></div></div></footer>
</body>
</html>
"""


def write_piece_page(piece: dict, width: int, height: int) -> None:
    path = PIECES / f"{piece['slug']}.html"
    path.write_text(piece_html(piece, width, height), encoding="utf-8")
    print(f"  piece page: {path.relative_to(ROOT)}")


def index_card(piece: dict, orientation: str) -> str:
    landscape_class = " landscape" if orientation == "landscape" else ""
    if orientation == "landscape":
        wh = 'width="900" height="822"'
    else:
        wh = 'width="900" height="1350"'
    return f"""      <article class="card{landscape_class}">
        <a href="./pieces/{piece['slug']}.html"><img src="./assets/{piece['asset']}" {wh} alt="{piece['alt']}" loading="lazy" /></a>
        <div class="meta">
          <h2><a href="./pieces/{piece['slug']}.html">{piece['title']}</a></h2>
          <p>{piece['card_blurb']}</p>
          <p class="soft-cta"><a href="./pieces/{piece['slug']}.html">Want a poster? Buy at the link.</a></p>
        </div>
      </article>"""


def buy_card(piece: dict, orientation: str) -> str:
    landscape_class = " landscape" if orientation == "landscape" else ""
    return f"""      <article class="card{landscape_class}" id="{piece['slug']}">
        <img src="./assets/{piece['asset']}" alt="{piece['title']}" />
        <div class="meta">
          <h2>{piece['title']}</h2>
          <p>Poster &amp; framed options — Stripe checkout pending connect approval.</p>
          <a class="btn secondary" href="./pieces/{piece['slug']}.html">View piece</a>
        </div>
      </article>"""


def update_index(pieces_meta: list[tuple[dict, str]]) -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")
    cards = "\n".join(index_card(p, ori) for p, ori in pieces_meta)
    m = re.search(r'(<section id="gallery"[^>]*>)(.*?)(</section>)', html, re.S)
    if not m:
        die("Could not find #gallery section in index.html")
    body = m.group(2)
    if pieces_meta[0][0]["slug"] in body:
        print("  index.html: cards already present")
        return
    new_body = body.rstrip() + "\n" + cards + "\n    "
    html = html[: m.start(2)] + new_body + html[m.end(2) :]
    INDEX_PATH.write_text(html, encoding="utf-8")
    print("  index.html: appended 5 gallery cards")


def update_buy(pieces_meta: list[tuple[dict, str]]) -> None:
    html = BUY_PATH.read_text(encoding="utf-8")
    cards = "\n".join(buy_card(p, ori) for p, ori in pieces_meta)
    m = re.search(
        r'(<section class="grid">)(.*?)(</section>\s*<p class="note")',
        html,
        re.S,
    )
    if not m:
        die("Could not find shop grid in buy.html")
    body = m.group(2)
    if pieces_meta[0][0]["slug"] in body:
        print("  buy.html: cards already present")
        return
    new_body = body.rstrip() + "\n" + cards + "\n    "
    html = html[: m.start(2)] + new_body + html[m.end(2) :]
    BUY_PATH.write_text(html, encoding="utf-8")
    print("  buy.html: appended 5 product cards")


def update_sitemap() -> None:
    xml = SITEMAP_PATH.read_text(encoding="utf-8")
    added = 0
    for p in NEW_PIECES:
        loc = f"{BASE_URL}/pieces/{p['slug']}.html"
        if loc in xml:
            continue
        entry = f"  <url><loc>{loc}</loc></url>\n"
        if "</urlset>" not in xml:
            die("sitemap.xml missing </urlset>")
        xml = xml.replace("</urlset>", entry + "</urlset>")
        added += 1
    if "night-windows.html" not in xml:
        entry = f"  <url><loc>{BASE_URL}/night-windows.html</loc></url>\n"
        xml = xml.replace("</urlset>", entry + "</urlset>")
        added += 1
    SITEMAP_PATH.write_text(xml, encoding="utf-8")
    print(f"  sitemap.xml: added {added} URL(s)")


def update_piece30_next() -> None:
    path = PIECES / "norwegian-stave-church-fjord.html"
    html = path.read_text(encoding="utf-8")
    if "mont-saint-michel-moon.html" in html:
        print("  piece 30: next link already updated")
        return
    new_html, n = re.subn(
        r'<a class="btn secondary" href="\./moonlit-alpine-meadow\.html">[^<]*</a>',
        '<a class="btn secondary" href="./mont-saint-michel-moon.html">Next window</a>',
        html,
    )
    if n == 0:
        die("Could not update Next window on norwegian-stave-church-fjord.html")
    path.write_text(new_html, encoding="utf-8")
    print("  piece 30: Next window → mont-saint-michel-moon")


def update_series_hub() -> None:
    """SEO: unique intro + full cross-links for all 35 pieces."""
    items = "\n".join(
        f'      <li><a href="./pieces/{slug}.html">{title}</a></li>'
        for slug, title in SERIES_LINKS
    )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Night Windows series — moonlit landscape prints | Prompt Framed</title>
  <meta name="description" content="Night Windows is thirty-five dreamy moonlit landscape prints — Mont Saint-Michel, Hallstatt, Zhangjiajie pillars, Bagan temples, the Matterhorn, and more. Want a poster? Buy at the link.">
  <link rel="canonical" href="{BASE_URL}/night-windows.html">
  <meta property="og:title" content="Night Windows — thirty-five moonlit windows | Prompt Framed">
  <meta property="og:description" content="A growing series of dreamy moonlit landscapes from Night Shade Art. Each picture is a window into a place you wish you were.">
  <meta property="og:url" content="{BASE_URL}/night-windows.html">
  <meta property="og:image" content="{BASE_URL}/assets/night-windows-contact-sheet.jpg">
  <meta property="og:image:alt" content="Contact sheet of Night Windows landscapes">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Night Windows — Prompt Framed">
  <meta name="twitter:description" content="Thirty-five windows into places you wish you were.">
  <meta name="twitter:image" content="{BASE_URL}/assets/night-windows-contact-sheet.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=Outfit:wght@380;560;650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="wrap prose">
    <header class="site-header">
      <a class="brand" href="./"><span class="brand-series">Night Windows</span><span class="brand-studio">Prompt Framed</span></a>
      <nav class="nav" aria-label="Primary">
        <a href="./#gallery">Gallery</a>
        <a href="./night-windows.html">The series</a>
        <a href="./buy.html">Buy</a>
        <a href="./guide-print-sizes.html">Print sizes</a>
        <a href="./how-it-works.html">How it works</a>
        <a href="./about.html">About</a>
        <a href="./contact.html">Contact</a>
        <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a>
      </nav>
    </header>
    <p class="kicker">Prompt Framed presents · Night Shade Art</p>
    <h1>Night Windows</h1>
    <p>Windows into places you wish you were. Dreamy moonlit landscapes — Mont Saint-Michel’s tidal abbey, Hallstatt’s alpine lake, Zhangjiajie’s stone pillars, Bagan’s temple plain, the Matterhorn above a still lake — printed as posters.</p>
    <p>Thirty-five windows so far. Each piece page has its own mood, alt text, and buy link. A social post shows the art; the line under it stays the same.</p>
    <p class="soft-cta"><a class="btn" href="./buy.html">Want a poster? Buy at the link.</a></p>
    <figure class="series-sheet">
      <img src="./assets/night-windows-contact-sheet.jpg" width="1400" height="933" alt="Contact sheet of Night Windows moonlit landscapes">
    </figure>
    <h2>Open windows</h2>
    <ol class="series-list">
{items}
    </ol>
    <p>New this drop: <a href="./pieces/mont-saint-michel-moon.html">Mont Saint-Michel Moon</a>, <a href="./pieces/hallstatt-lake-moon.html">Hallstatt Lake Moon</a>, <a href="./pieces/zhangjiajie-pillars-moon.html">Zhangjiajie Pillars Moon</a>, <a href="./pieces/bagan-temples-night.html">Bagan Temples Night</a>, and <a href="./pieces/matterhorn-alpine-moon.html">Matterhorn Alpine Moon</a>.</p>
    <p>Follow Night Shade Art on Instagram: <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a>. Stripe checkout is live for poster and framed prints.</p>
    <p><a class="btn secondary" href="./guide-print-sizes.html">Print size guide</a> · <a class="btn secondary" href="./#gallery">Full gallery</a></p>
  </div>
  <footer class="site-footer">
    <div class="wrap">
      <div>© 2026 Joshua Israel Ventures LLC · Night Windows by Prompt Framed · Night Shade Art</div>
      <div><a href="./buy.html">Want a poster? Buy at the link.</a> · <a href="./">Gallery</a> · Night Shade Art on Instagram: <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a></div>
    </div>
  </footer>
</body>
</html>
"""
    SERIES_PATH.write_text(html, encoding="utf-8")
    print("  night-windows.html: refreshed hub (35 pieces + unique intro)")


def main() -> None:
    print(f"Repo: {ROOT}")
    check_pngs()
    pieces_meta: list[tuple[dict, str]] = []
    for piece in NEW_PIECES:
        print(f"\n== {piece['id']} ==")
        width, height, orientation = convert_jpg(piece)
        with Image.open(GALLERY / piece["file"]) as im:
            mw, mh = im.size
        append_catalog(piece, mw, mh, "portrait" if mh >= mw else "landscape")
        append_products(piece)
        write_piece_page(piece, width, height)
        pieces_meta.append((piece, orientation))

    print("\n== site updates ==")
    update_index(pieces_meta)
    update_buy(pieces_meta)
    update_sitemap()
    update_piece30_next()
    update_series_hub()
    print("\nDone. Review diffs, then commit + push when ready.")
    print("Buy CTAs remain buy.html#slug until Stripe links are applied.")


if __name__ == "__main__":
    main()
