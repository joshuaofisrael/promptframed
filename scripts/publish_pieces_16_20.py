#!/usr/bin/env python3
"""Publish Night Windows pieces 16–20 into the Prompt Framed site.

Expects PNG masters already present under gallery/:
  gallery/16-provence-lavender-moon.png
  gallery/17-amalfi-terrace-night.png
  gallery/18-patagonia-lake-peaks.png
  gallery/19-bali-jungle-temple.png
  gallery/20-iceland-black-sand-moon.png

Run from repo root:
  python3 scripts/publish_pieces_16_20.py

Idempotent: skips catalog/products rows and HTML cards that already exist.
Also refreshes night-windows.html series list + piece-15 next link.
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
        "id": "16-provence-lavender-moon",
        "slug": "provence-lavender-moon",
        "title": "Provence Lavender Moon",
        "photoNumber": 16,
        "file": "16-provence-lavender-moon.png",
        "asset": "16-provence-lavender-moon.jpg",
        "alt": (
            "Moonlit Provence lavender fields in long purple rows under a full moon, "
            "distant stone farmhouse with warm window lights, wildflowers in the foreground"
        ),
        "description": (
            "Rows of moonlit lavender stretch toward a warm stone farmhouse while a full moon "
            "glows through dramatic clouds over the Provence fields."
        ),
        "card_blurb": "Lavender rows, a farmhouse glow, and a moon over Provence.",
        "keywords": [
            "Provence lavender",
            "moonlit fields",
            "French countryside night",
            "lavender wall art",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "17-amalfi-terrace-night",
        "slug": "amalfi-terrace-night",
        "title": "Amalfi Terrace Night",
        "photoNumber": 17,
        "file": "17-amalfi-terrace-night.png",
        "asset": "17-amalfi-terrace-night.jpg",
        "alt": (
            "Cliffside Amalfi coast terraces at night with warm glowing windows, lemon trees, "
            "and a silver moonlight path across the Mediterranean sea"
        ),
        "description": (
            "Stacked Amalfi terraces glow with warm windows above a moonlit sea path, lemon trees "
            "and wildflowers lining the cliffside stone."
        ),
        "card_blurb": "Cliffside terraces, warm windows, and a moonpath on the sea.",
        "keywords": [
            "Amalfi coast",
            "Italian terrace night",
            "Mediterranean moonlight",
            "cliffside wall art",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "18-patagonia-lake-peaks",
        "slug": "patagonia-lake-peaks",
        "title": "Patagonia Lake Peaks",
        "photoNumber": 18,
        "file": "18-patagonia-lake-peaks.png",
        "asset": "18-patagonia-lake-peaks.jpg",
        "alt": (
            "Turquoise glacial lake in Patagonia under moonlight with jagged snow-dusted peaks, "
            "moon haze, and wildflowers along the shore"
        ),
        "description": (
            "A turquoise Patagonian lake mirrors jagged moonlit peaks while haze and wildflowers "
            "soften the glacial shore."
        ),
        "card_blurb": "Glacial turquoise water, jagged peaks, and moon haze.",
        "keywords": [
            "Patagonia lake",
            "glacial peaks",
            "moonlit mountains",
            "turquoise lake print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "19-bali-jungle-temple",
        "slug": "bali-jungle-temple",
        "title": "Bali Jungle Temple",
        "photoNumber": 19,
        "file": "19-bali-jungle-temple.png",
        "asset": "19-bali-jungle-temple.jpg",
        "alt": (
            "Mossy Balinese temple stone steps in jungle mist at night with soft lantern light "
            "and moonlight through a dense canopy"
        ),
        "description": (
            "Mossy temple steps climb through jungle mist as lanterns and moonbeams filter through "
            "the canopy in a quiet Balinese night."
        ),
        "card_blurb": "Mossy temple steps, lanterns, and moon through jungle mist.",
        "keywords": [
            "Bali temple",
            "jungle night",
            "lantern stone steps",
            "tropical temple print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "20-iceland-black-sand-moon",
        "slug": "iceland-black-sand-moon",
        "title": "Iceland Black Sand Moon",
        "photoNumber": 20,
        "file": "20-iceland-black-sand-moon.png",
        "asset": "20-iceland-black-sand-moon.jpg",
        "alt": (
            "Iceland black sand beach at night with basalt sea stacks and northern moonlight "
            "gleaming on wet sand under dramatic clouds"
        ),
        "description": (
            "Northern moonlight gleams across wet black sand and basalt stacks while dramatic clouds "
            "sweep an Icelandic shore."
        ),
        "card_blurb": "Black sand, basalt stacks, and northern moonlight on the wet shore.",
        "keywords": [
            "Iceland black sand",
            "basalt stacks",
            "northern moonlight",
            "beach night print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
]

# Next-window chain for the new batch; piece 20 loops to first series piece.
NEXT_BY_SLUG = {
    "scottish-highlands-loch": "provence-lavender-moon",
    "provence-lavender-moon": "amalfi-terrace-night",
    "amalfi-terrace-night": "patagonia-lake-peaks",
    "patagonia-lake-peaks": "bali-jungle-temple",
    "bali-jungle-temple": "iceland-black-sand-moon",
    "iceland-black-sand-moon": "moonlit-alpine-meadow",
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
    """PNG → watermarked website JPG in assets/. Print masters stay clean."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import watermark_for_social as wm

    src = GALLERY / piece["file"]
    dst = ASSETS / piece["asset"]
    w, h = wm.export_website_jpg(src, dst)
    orientation = "portrait" if h >= w else "landscape"
    print(f"  JPG {dst.relative_to(ROOT)} ({w}x{h}, {orientation}, watermarked)")
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


def update_piece15_next() -> None:
    path = PIECES / "scottish-highlands-loch.html"
    html = path.read_text(encoding="utf-8")
    if "provence-lavender-moon.html" in html:
        print("  piece 15: next link already updated")
        return
    new_html, n = re.subn(
        r'<a class="btn secondary" href="\./moonlit-alpine-meadow\.html">[^<]*</a>',
        '<a class="btn secondary" href="./provence-lavender-moon.html">Next window</a>',
        html,
    )
    if n == 0:
        die("Could not update Next window on scottish-highlands-loch.html")
    path.write_text(new_html, encoding="utf-8")
    print("  piece 15: Next window → provence-lavender-moon")


def update_series_hub() -> None:
    """SEO: unique intro + full cross-links for all 20 pieces."""
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
  <meta name="description" content="Night Windows is twenty dreamy moonlit landscape prints — Provence lavender, Amalfi terraces, Patagonia peaks, Bali temples, Iceland black sand, and more. Want a poster? Buy at the link.">
  <link rel="canonical" href="{BASE_URL}/night-windows.html">
  <meta property="og:title" content="Night Windows — twenty moonlit windows | Prompt Framed">
  <meta property="og:description" content="A growing series of dreamy moonlit landscapes from Night Shade Art. Each picture is a window into a place you wish you were.">
  <meta property="og:url" content="{BASE_URL}/night-windows.html">
  <meta property="og:image" content="{BASE_URL}/assets/night-windows-contact-sheet.jpg">
  <meta property="og:image:alt" content="Contact sheet of Night Windows landscapes">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Night Windows — Prompt Framed">
  <meta name="twitter:description" content="Twenty windows into places you wish you were.">
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
    <p>Windows into places you wish you were. Dreamy moonlit landscapes — Provence lavender fields, Amalfi cliff terraces, Patagonian peaks, Balinese jungle temples, Icelandic black sand — printed as posters.</p>
    <p>Twenty windows so far. Each piece page has its own mood, alt text, and buy link. A social post shows the art; the line under it stays the same.</p>
    <p class="soft-cta"><a class="btn" href="./buy.html">Want a poster? Buy at the link.</a></p>
    <figure class="series-sheet">
      <img src="./assets/night-windows-contact-sheet.jpg" width="1400" height="933" alt="Contact sheet of Night Windows moonlit landscapes">
    </figure>
    <h2>Open windows</h2>
    <ol class="series-list">
{items}
    </ol>
    <p>New this drop: <a href="./pieces/provence-lavender-moon.html">Provence Lavender Moon</a>, <a href="./pieces/amalfi-terrace-night.html">Amalfi Terrace Night</a>, <a href="./pieces/patagonia-lake-peaks.html">Patagonia Lake Peaks</a>, <a href="./pieces/bali-jungle-temple.html">Bali Jungle Temple</a>, and <a href="./pieces/iceland-black-sand-moon.html">Iceland Black Sand Moon</a>.</p>
    <p>Follow Night Shade Art on Instagram: <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a>. Nothing here charges a card until Stripe checkout is approved.</p>
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
    print("  night-windows.html: refreshed hub (20 pieces + unique intro)")


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
    update_piece15_next()
    update_series_hub()
    print("\nDone. Review diffs, then commit + push when ready.")
    print("Buy CTAs remain buy.html#slug (Stripe/Printful urls stay null/placeholder).")


if __name__ == "__main__":
    main()
