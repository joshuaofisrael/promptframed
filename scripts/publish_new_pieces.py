#!/usr/bin/env python3
"""Publish Night Windows pieces 11–15 into the Prompt Framed site.

Expects PNG masters already present under gallery/:
  gallery/11-moonlit-rice-terraces.png
  gallery/12-venetian-canal-moonrise.png
  gallery/13-japanese-temple-pond.png
  gallery/14-moroccan-kasbah-night.png
  gallery/15-scottish-highlands-loch.png

Run from repo root or any cwd:
  python3 scripts/publish_new_pieces.py

Idempotent: skips catalog/products rows and HTML that already exist.
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
        "id": "11-moonlit-rice-terraces",
        "slug": "moonlit-rice-terraces",
        "title": "Moonlit Rice Terraces",
        "photoNumber": 11,
        "file": "11-moonlit-rice-terraces.png",
        "asset": "11-moonlit-rice-terraces.jpg",
        "alt": (
            "Moonlit rice terraces cascading down a misty hillside with warm village "
            "lights and a full moon reflected in flooded paddies"
        ),
        "description": (
            "Cascading moonlit rice terraces and warm village lights glow under a full moon, "
            "with mist, wildflowers, and deep blue-green night tones."
        ),
        "card_blurb": "Cascading paddies, village lights, and a moon in flooded water.",
        "keywords": [
            "rice terraces",
            "moonlit paddies",
            "Asian night landscape",
            "village lights print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "12-venetian-canal-moonrise",
        "slug": "venetian-canal-moonrise",
        "title": "Venetian Canal Moonrise",
        "photoNumber": 12,
        "file": "12-venetian-canal-moonrise.png",
        "asset": "12-venetian-canal-moonrise.jpg",
        "alt": (
            "Moonlit Venetian canal with ornate bridges, warm windows reflecting on still "
            "water, a quiet gondola, and hanging flowers"
        ),
        "description": (
            "A quiet Venetian canal under moonlight: stone bridges, warm windows on the water, "
            "a lone gondola, and flowers along the walls."
        ),
        "card_blurb": "Stone bridges, warm windows, and a quiet gondola under moonlight.",
        "keywords": [
            "Venice canal",
            "moonlit gondola",
            "Italian night landscape",
            "bridge wall art",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "13-japanese-temple-pond",
        "slug": "japanese-temple-pond",
        "title": "Japanese Temple Pond",
        "photoNumber": 13,
        "file": "13-japanese-temple-pond.png",
        "asset": "13-japanese-temple-pond.jpg",
        "alt": (
            "Moonlit Japanese temple garden with a still pond reflecting a full moon, "
            "stone lanterns, maple and pine trees"
        ),
        "description": (
            "A still temple pond mirrors the full moon while stone lanterns warm the misty "
            "garden path beneath pines and maples."
        ),
        "card_blurb": "Temple pond, stone lanterns, and a moon mirrored in still water.",
        "keywords": [
            "Japanese temple",
            "moonlit pond",
            "stone lantern garden",
            "Zen landscape print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "14-moroccan-kasbah-night",
        "slug": "moroccan-kasbah-night",
        "title": "Moroccan Kasbah Night",
        "photoNumber": 14,
        "file": "14-moroccan-kasbah-night.png",
        "asset": "14-moroccan-kasbah-night.jpg",
        "alt": (
            "Moonlit Moroccan kasbah at the edge of desert dunes with warm lantern light, "
            "palms, and wildflowers in an oasis"
        ),
        "description": (
            "A moonlit kasbah glows at the desert’s edge, lantern light in adobe windows, "
            "palms and wildflowers framing the dunes."
        ),
        "card_blurb": "Kasbah glow at the dune edge, palms, and oasis wildflowers.",
        "keywords": [
            "Moroccan kasbah",
            "desert night",
            "oasis landscape",
            "lantern adobe print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "15-scottish-highlands-loch",
        "slug": "scottish-highlands-loch",
        "title": "Scottish Highlands Loch",
        "photoNumber": 15,
        "file": "15-scottish-highlands-loch.png",
        "asset": "15-scottish-highlands-loch.jpg",
        "alt": (
            "Moonlit Scottish Highlands loch with castle ruins glowing on a distant shore, "
            "heather and wildflowers in the foreground"
        ),
        "description": (
            "Mist drifts over a Highlands loch as castle ruins glow on the far shore beneath "
            "a luminous moon and heather meadows."
        ),
        "card_blurb": "Misty Highlands loch, castle ruins, and heather under moonlight.",
        "keywords": [
            "Scottish Highlands",
            "moonlit loch",
            "castle ruins",
            "heather landscape print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
]

# Next-window chain by photo number; last loops to first series piece.
NEXT_BY_SLUG = {
    "mediterranean-lantern-walk": "moonlit-rice-terraces",
    "moonlit-rice-terraces": "venetian-canal-moonrise",
    "venetian-canal-moonrise": "japanese-temple-pond",
    "japanese-temple-pond": "moroccan-kasbah-night",
    "moroccan-kasbah-night": "scottish-highlands-loch",
    "scottish-highlands-loch": "moonlit-alpine-meadow",
}

NEXT_LABEL = {
    "moonlit-alpine-meadow": "First window",
}


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
            "asset": piece["asset"],
            "printSource": f"gallery/{piece['file']}",
        }
    )
    dump_json(PRODUCTS_PATH, products)
    print(f"  products: appended {piece['slug']}")


def display_dims(width: int, height: int) -> tuple[int, int]:
    """Match existing piece pages: portrait 900x1350, landscape 900x822-ish."""
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
  <meta property="og:image" content="{BASE_URL}/assets/{piece['asset']}" />
  <link rel="stylesheet" href="../styles.css" />
</head>
<body>
  <div class="wrap">
    <header class="site-header">
      <a class="brand" href="../">Prompt <span>Framed</span></a>
      <nav class="nav">
        <a href="../#gallery">Gallery</a>
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
        <p class="note">Want a poster? Buy at the link. Poster and framed sizes ship via print-on-demand after checkout. Buy links go live when the Printful Quick Store is published.</p>
      </div>
    </article>
  </div>
  <footer class="site-footer"><div class="wrap"><div>© Prompt Framed · Joshua Israel Ventures LLC</div><div><a href="../">Back to gallery</a> · <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a></div></div></footer>
</body>
</html>
"""


def write_piece_page(piece: dict, width: int, height: int) -> None:
    path = PIECES / f"{piece['slug']}.html"
    path.write_text(piece_html(piece, width, height), encoding="utf-8")
    print(f"  piece page: {path.relative_to(ROOT)}")


def index_card(piece: dict, orientation: str) -> str:
    landscape_class = " landscape" if orientation == "landscape" else ""
    # Match display dims used on index for existing cards
    if orientation == "landscape":
        wh = 'width="900" height="822"'
    else:
        wh = 'width="900" height="1350"'
    return f"""      <article class="card{landscape_class}">
        <a href="./pieces/{piece['slug']}.html"><img src="./assets/{piece['asset']}" {wh} alt="{piece['alt']}" loading="lazy" /></a>
        <div class="meta">
          <h2><a href="./pieces/{piece['slug']}.html">{piece['title']}</a></h2>
          <p>{piece['card_blurb']}</p>
        </div>
      </article>"""


def buy_card(piece: dict, orientation: str) -> str:
    landscape_class = " landscape" if orientation == "landscape" else ""
    return f"""      <article class="card{landscape_class}" id="{piece['slug']}">
        <img src="./assets/{piece['asset']}" alt="{piece['title']}" />
        <div class="meta">
          <h2>{piece['title']}</h2>
          <p>Poster &amp; framed options — link pending Printful publish.</p>
          <a class="btn secondary" href="./pieces/{piece['slug']}.html">View piece</a>
        </div>
      </article>"""


def upsert_cards_before_close(html: str, section_close: str, cards_html: str, slug_marker: str) -> str:
    """Insert cards before the gallery/grid closing tag if slug not already present."""
    if slug_marker in html:
        print(f"  HTML already contains {slug_marker}; skipping card insert")
        return html
    idx = html.rfind(section_close)
    if idx < 0:
        die(f"Could not find {section_close!r} to insert cards")
    return html[:idx] + cards_html + "\n" + html[idx:]


def update_index(pieces_meta: list[tuple[dict, str]]) -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")
    cards = "\n".join(index_card(p, ori) for p, ori in pieces_meta)
    # Insert before the gallery section close (first </section> after id="gallery")
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
    # Insert before the shop grid's closing </section>
    # Find the grid section that contains product cards
    m = re.search(
        r'(<section class="grid">)(.*?)(</section>\s*<p class="note">)',
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
    SITEMAP_PATH.write_text(xml, encoding="utf-8")
    print(f"  sitemap.xml: added {added} piece URL(s)")


def update_piece10_next() -> None:
    path = PIECES / "mediterranean-lantern-walk.html"
    html = path.read_text(encoding="utf-8")
    # Replace First window / alpine link with Next window → rice terraces
    new_html, n = re.subn(
        r'<a class="btn secondary" href="\./moonlit-alpine-meadow\.html">First window</a>',
        '<a class="btn secondary" href="./moonlit-rice-terraces.html">Next window</a>',
        html,
    )
    if n == 0:
        if "moonlit-rice-terraces.html" in html:
            print("  piece 10: next link already updated")
            return
        # Fallback: any secondary btn pointing at alpine
        new_html, n = re.subn(
            r'<a class="btn secondary" href="\./moonlit-alpine-meadow\.html">[^<]*</a>',
            '<a class="btn secondary" href="./moonlit-rice-terraces.html">Next window</a>',
            html,
        )
    if n == 0:
        die("Could not update Next window on mediterranean-lantern-walk.html")
    path.write_text(new_html, encoding="utf-8")
    print("  piece 10: Next window → moonlit-rice-terraces")


def main() -> None:
    print(f"Repo: {ROOT}")
    check_pngs()
    pieces_meta: list[tuple[dict, str]] = []
    # Convert + catalog/products/pages first so dims known for cards
    for piece in NEW_PIECES:
        print(f"\n== {piece['id']} ==")
        width, height, orientation = convert_jpg(piece)
        # Prefer master PNG dims for catalog (re-open master)
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
    update_piece10_next()
    print("\nDone. Review diffs, then commit + push when ready.")
    print("Buy CTAs remain buy.html#slug (Printful urls stay null/placeholder).")


if __name__ == "__main__":
    main()
