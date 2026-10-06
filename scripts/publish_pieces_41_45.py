#!/usr/bin/env python3
"""Publish Night Windows pieces 41–45 into the Prompt Framed site.

Expects PNG masters already present under gallery/:
  gallery/41-dolomites-tre-cime-moon.png
  gallery/42-lofoten-reine-moon.png
  gallery/43-cinque-terre-manarola-moon.png
  gallery/44-lake-bled-island-moon.png
  gallery/45-guilin-li-river-moon.png

Run from repo root:
  python3 scripts/publish_pieces_41_45.py

Before running: check the copy in NEW_PIECES (alt / description / card_blurb /
keywords) and the HUB_* / BUY_* strings against the real images. They were
written from the prompt briefs, before the images existed.

Idempotent: skips catalog/products rows and HTML cards that already exist.
New piece pages ship with GA4 + Product/Offer/ImageObject/BreadcrumbList JSON-LD.
Also refreshes the night-windows.html hub (forty-five pieces), the buy.html hero
copy, the piece-40 next link, and "More windows like this" related-piece
cross-links in both directions.
Buy blocks are filled from products.json by scripts/apply_stripe_links.py.
Does NOT git commit or push, and never watermarks gallery/*.png or print masters.
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
GA_ID = "G-663R8VD62L"
GA_TAG = f"""  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>"""

STYLE = (
    "Dreamy cinematic fantasy realism, photorealistic landscape photography, "
    "ethereal moonlight, dramatic clouds, lush vegetation and wildflowers, "
    "deep atmospheric perspective, rich blue-green nighttime tones, subtle warm lights, "
    "romantic landscape aesthetic, peaceful dreamlike atmosphere, highly detailed, "
    "realistic natural textures, volumetric haze, dramatic but believable lighting."
)

NEW_PIECES = [
    {
        "id": "41-dolomites-tre-cime-moon",
        "slug": "dolomites-tre-cime-moon",
        "title": "Dolomites Tre Cime Moon",
        "photoNumber": 41,
        "file": "41-dolomites-tre-cime-moon.png",
        "asset": "41-dolomites-tre-cime-moon.jpg",
        "alt": (
            "Moonlit Tre Cime di Lavaredo peaks in the Dolomites above a wildflower alpine meadow, "
            "a small wooden hut with glowing windows, mist in the valley, and a full moon"
        ),
        "description": (
            "The three peaks of Tre Cime rise over a wildflower meadow while a lone hut keeps its "
            "windows lit and valley mist drifts under a full Dolomites moon."
        ),
        "card_blurb": "Three peaks, a lit mountain hut, and a moon over the Dolomites.",
        "keywords": [
            "Dolomites night",
            "Tre Cime di Lavaredo moonlight",
            "alpine hut wall art",
            "Italian Alps print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "42-lofoten-reine-moon",
        "slug": "lofoten-reine-moon",
        "title": "Lofoten Reine Moon",
        "photoNumber": 42,
        "file": "42-lofoten-reine-moon.png",
        "asset": "42-lofoten-reine-moon.jpg",
        "alt": (
            "Moonlit Reine fishing village in the Lofoten Islands with red rorbu cabins on stilts and "
            "warm lights over a mirror-still fjord, jagged peaks behind, and the full moon reflected in the water"
        ),
        "description": (
            "Red rorbu cabins on stilts glow along a mirror-still Lofoten fjord while jagged peaks stand "
            "over Reine and the full moon lays its reflection on the water."
        ),
        "card_blurb": "Red fishing cabins, a still fjord, and a moon over Reine.",
        "keywords": [
            "Lofoten Islands night",
            "Reine Norway moonlight",
            "red fishing cabin wall art",
            "Nordic fjord print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "43-cinque-terre-manarola-moon",
        "slug": "cinque-terre-manarola-moon",
        "title": "Cinque Terre Manarola Moon",
        "photoNumber": 43,
        "file": "43-cinque-terre-manarola-moon.png",
        "asset": "43-cinque-terre-manarola-moon.jpg",
        "alt": (
            "Moonlit Manarola in the Cinque Terre with pastel cliffside houses and lit windows above the sea, "
            "magenta bougainvillea and a lantern-lit path in the foreground, and a full moon over the Ligurian Sea"
        ),
        "description": (
            "Manarola’s pastel houses stack up the cliff with their windows lit while magenta "
            "bougainvillea frames a glowing path and a full moon silvers the Ligurian Sea."
        ),
        "card_blurb": "Pastel cliff houses, bougainvillea, and a moon over Manarola.",
        "keywords": [
            "Cinque Terre night",
            "Manarola moonlight",
            "Italian coast wall art",
            "Liguria cliffside village print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "44-lake-bled-island-moon",
        "slug": "lake-bled-island-moon",
        "title": "Lake Bled Island Moon",
        "photoNumber": 44,
        "file": "44-lake-bled-island-moon.png",
        "asset": "44-lake-bled-island-moon.jpg",
        "alt": (
            "Moonlit Lake Bled with the island church and its tall bell tower, Bled Castle on its cliff, "
            "snowy Julian Alps beyond, a covered wooden pletna boat with lanterns, and wildflowers on the shore"
        ),
        "description": (
            "Bled’s island church and bell tower glow on the moonlit lake while the castle keeps watch "
            "from its cliff and a lantern-lit pletna boat waits by the flowered shore."
        ),
        "card_blurb": "Island church, castle cliff, and a moon over Lake Bled.",
        "keywords": [
            "Lake Bled night",
            "Slovenia island church moonlight",
            "alpine lake wall art",
            "Julian Alps print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "45-guilin-li-river-moon",
        "slug": "guilin-li-river-moon",
        "title": "Guilin Li River Moon",
        "photoNumber": 45,
        "file": "45-guilin-li-river-moon.png",
        "asset": "45-guilin-li-river-moon.jpg",
        "alt": (
            "Moonlit Li River near Guilin with misty karst peaks, a bamboo raft carrying a glowing "
            "lantern, bamboo groves along the banks, and a full moon in the night sky"
        ),
        "description": (
            "Karst peaks fade into mist along the Li River while a lantern glows on a bamboo raft "
            "and a full moon rises over the bamboo banks near Guilin."
        ),
        "card_blurb": "Misty karst peaks, a lantern raft, and a moon over the Li River.",
        "keywords": [
            "Guilin Li River night",
            "karst mountains moonlight",
            "bamboo raft wall art",
            "China river landscape print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
]

# ---- Hub / buy copy (edit here once the real images are checked) ----
# Kept out of the templates below so tweaks after the image check are one-line edits.
COUNT_WORD = "forty-five"
COUNT_WORD_CAP = "Forty-five"
HUB_META_DESC = (
    "Night Windows is forty-five dreamy moonlit landscape prints — the Dolomites, Lofoten, "
    "Cinque Terre, Lake Bled, Guilin’s Li River, and more. Want a poster? Buy at the link."
)
HUB_INTRO = (
    "Windows into places you wish you were. Dreamy moonlit landscapes — the three peaks of Tre Cime "
    "above a lit mountain hut, Reine’s red cabins on a still Lofoten fjord, Manarola’s pastel houses "
    "over the Ligurian Sea, Lake Bled’s island church, and a lantern raft drifting down the Li River "
    "— printed as posters."
)
HUB_THEMES = [
    (
        "Castles and old towns",
        [
            ("neuschwanstein-castle-moon", "Neuschwanstein"),
            ("lake-bled-island-moon", "Lake Bled’s island church and castle"),
            ("mont-saint-michel-moon", "Mont Saint-Michel"),
            ("hallstatt-lake-moon", "Hallstatt"),
            ("chefchaouen-blue-moon", "Chefchaouen"),
            ("moroccan-kasbah-night", "a Moroccan kasbah"),
        ],
    ),
    (
        "Temples by moonlight",
        [
            ("angkor-wat-moon", "Angkor Wat"),
            ("bagan-temples-night", "Bagan"),
            ("bali-jungle-temple", "a Bali jungle temple"),
            ("japanese-temple-pond", "a Japanese temple pond"),
            ("petra-treasury-night", "Petra’s Treasury"),
        ],
    ),
    (
        "Mountains and river valleys",
        [
            ("dolomites-tre-cime-moon", "the Dolomites’ Tre Cime"),
            ("matterhorn-alpine-moon", "the Matterhorn"),
            ("guilin-li-river-moon", "Guilin’s Li River"),
            ("zhangjiajie-pillars-moon", "Zhangjiajie’s stone pillars"),
            ("yosemite-half-dome-moon", "Yosemite’s Half Dome"),
        ],
    ),
    (
        "Waterfalls, lakes and wild coasts",
        [
            ("plitvice-lakes-moon", "Plitvice Lakes"),
            ("faroe-gasadalur-moon", "Gásadalur in the Faroes"),
            ("lofoten-reine-moon", "Reine in the Lofoten Islands"),
            ("cinque-terre-manarola-moon", "Manarola in the Cinque Terre"),
            ("iceland-black-sand-moon", "Iceland’s black sand"),
            ("banff-lake-louise-moon", "Lake Louise"),
            ("moonlit-waterfall", "a moonlit waterfall"),
        ],
    ),
]
BUY_META_DESC = (
    "Buy Night Windows moonlit landscape prints — forty-five windows including the Dolomites, "
    "Lofoten, Cinque Terre, Lake Bled, and Guilin’s Li River. $29 poster or $69 framed, 12×18, "
    "shipping included. Stripe checkout."
)
BUY_HERO = (
    "Forty-five moonlit windows, printed for your wall — from the three peaks of the Dolomites and "
    "Reine’s red cabins in Lofoten to Manarola’s cliffside houses, Lake Bled’s island church, and "
    "the karst peaks of Guilin’s Li River. Choose a 12×18 enhanced matte poster or the same print "
    "in a black frame. Shipping is included, and each button opens secure Stripe checkout."
)

NEXT_BY_SLUG = {
    "faroe-gasadalur-moon": "dolomites-tre-cime-moon",
    "dolomites-tre-cime-moon": "lofoten-reine-moon",
    "lofoten-reine-moon": "cinque-terre-manarola-moon",
    "cinque-terre-manarola-moon": "lake-bled-island-moon",
    "lake-bled-island-moon": "guilin-li-river-moon",
    "guilin-li-river-moon": "moonlit-alpine-meadow",
}

NEXT_LABEL = {
    "moonlit-alpine-meadow": "First window",
}

# SEO (5 Oct 2026, kept for 41–45): thematic "More windows like this" links, both directions,
# so each new URL gets contextual internal links from older, already-crawled pages.
RELATED = {
    "dolomites-tre-cime-moon": ["matterhorn-alpine-moon", "wildflower-meadow-cabin"],
    "lofoten-reine-moon": ["norwegian-stave-church-fjord", "northern-lights-fjord"],
    "cinque-terre-manarola-moon": ["amalfi-terrace-night", "coastal-cliffside-town"],
    "lake-bled-island-moon": ["hallstatt-lake-moon", "moonlit-mediterranean-village"],
    "guilin-li-river-moon": ["ha-long-bay-moon", "zhangjiajie-pillars-moon"],
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
    ("chefchaouen-blue-moon", "Chefchaouen Blue Moon"),
    ("plitvice-lakes-moon", "Plitvice Lakes Moon"),
    ("neuschwanstein-castle-moon", "Neuschwanstein Castle Moon"),
    ("angkor-wat-moon", "Angkor Wat Moon"),
    ("faroe-gasadalur-moon", "Faroe Gásadalur Moon"),
    ("dolomites-tre-cime-moon", "Dolomites Tre Cime Moon"),
    ("lofoten-reine-moon", "Lofoten Reine Moon"),
    ("cinque-terre-manarola-moon", "Cinque Terre Manarola Moon"),
    ("lake-bled-island-moon", "Lake Bled Island Moon"),
    ("guilin-li-river-moon", "Guilin Li River Moon"),
]

TITLES = dict(SERIES_LINKS)


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



def product_jsonld(piece: dict, meta_desc: str) -> str:
    slug = piece["slug"]
    page = f"{BASE_URL}/pieces/{slug}.html"
    img = f"{BASE_URL}/assets/{piece['asset']}"
    sku = f"nw-{piece['photoNumber']:02d}-{slug}"
    seller = {"@type": "Organization", "name": "Joshua Israel Ventures LLC"}

    def offer(variant: str, label: str, price: str) -> dict:
        return {
            "@type": "Offer",
            "@id": f"{page}#offer-{variant}",
            "name": f"{piece['title']} \u2014 {label} 12x18",
            "price": price,
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition",
            "url": page,
            "seller": seller,
        }

    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "@id": f"{page}#product",
                "name": piece["title"],
                "description": meta_desc,
                "sku": sku,
                "mpn": sku,
                "category": "Home & Garden > Decor > Artwork > Posters, Prints, & Visual Artwork",
                "brand": {"@type": "Brand", "name": "Night Shade Art"},
                "isPartOf": {
                    "@type": "CreativeWorkSeries",
                    "name": "Night Windows",
                    "url": f"{BASE_URL}/night-windows.html",
                },
                "image": [
                    {
                        "@type": "ImageObject",
                        "@id": f"{page}#image",
                        "url": img,
                        "contentUrl": img,
                        "caption": piece["alt"],
                        "name": piece["title"],
                        "representativeOfPage": True,
                    }
                ],
                "offers": [
                    offer("poster", "poster", "29.00"),
                    offer("framed", "framed print", "69.00"),
                ],
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{page}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Night Windows", "item": f"{BASE_URL}/night-windows.html"},
                    {"@type": "ListItem", "position": 3, "name": piece["title"], "item": page},
                ],
            },
        ],
    }
    return '  <script type="application/ld+json">\n' + json.dumps(data, indent=2) + "\n  </script>"


def related_para(slugs: list[str]) -> str:
    links = " · ".join(f'<a href="./{s}.html">{TITLES[s]}</a>' for s in slugs)
    return f'        <p class="note related-windows">More windows like this: {links}</p>'


def piece_html(piece: dict, width: int, height: int) -> str:
    slug = piece["slug"]
    next_slug = NEXT_BY_SLUG[slug]
    next_label = NEXT_LABEL.get(next_slug, "Next window")
    dw, dh = display_dims(width, height)
    num = f"{piece['photoNumber']:02d}"
    meta_desc = (
        f"{piece['title']} from the Night Windows series. Poster and framed print options. "
        f"{piece['description']}"
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{GA_TAG}
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{piece['title']} — Night Windows print | Prompt Framed</title>
  <meta name="description" content="{meta_desc}" />
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
{product_jsonld(piece, meta_desc)}
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
{related_para(RELATED[slug])}
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
    if path.exists() and "<!-- buy:start -->" in path.read_text(encoding="utf-8"):
        # Already converted by apply_stripe_links.py; don't clobber live buy buttons.
        print(f"  piece page: keep existing {path.relative_to(ROOT)} (buy block applied)")
        return
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


def buy_card(piece: dict, orientation: str) -> str:
    landscape_class = " landscape" if orientation == "landscape" else ""
    return f"""      <article class="card{landscape_class}" id="{piece['slug']}">
        <a href="./pieces/{piece['slug']}.html"><img src="./assets/{piece['asset']}" alt="{piece['title']}" loading="lazy"></a>
        <div class="meta">
          <h2>{piece['title']}</h2>
          <p>{piece['description']}</p>
          <p class="note">This window opens for orders soon.</p>
        </div>
      </article>"""


def update_buy(pieces_meta: list[tuple[dict, str]]) -> None:
    """Add placeholder cards inside the buy:start/buy:end grid (apply_stripe_links.py
    regenerates the whole grid from products.json afterwards) + refresh hero copy."""
    html = BUY_PATH.read_text(encoding="utf-8")
    if pieces_meta[0][0]["slug"] not in html:
        cards = "\n".join(buy_card(p, ori) for p, ori in pieces_meta)
        if "<!-- buy:end -->" not in html:
            die("buy.html missing <!-- buy:end --> marker")
        html = html.replace("\n      <!-- buy:end -->", "\n" + cards + "\n      <!-- buy:end -->", 1)
        print("  buy.html: appended 5 product cards")
    else:
        print("  buy.html: cards already present")
    html, n_meta = re.subn(
        r'<meta name="description" content="Buy Night Windows moonlit landscape prints[^"]*">',
        lambda _: f'<meta name="description" content="{BUY_META_DESC}">',
        html,
        count=1,
    )
    html, n_hero = re.subn(
        r"(<section class=\"hero left\">.*?<h1>Buy the print</h1>\s*<p>)[^<]*(</p>)",
        lambda m: m.group(1) + BUY_HERO + m.group(2),
        html,
        count=1,
        flags=re.S,
    )
    if not (n_meta and n_hero):
        die(f"buy.html meta/hero pattern not found (meta={n_meta}, hero={n_hero})")
    BUY_PATH.write_text(html, encoding="utf-8")
    print(f"  buy.html: hero/meta → {COUNT_WORD} windows")


def update_piece40_next() -> None:
    path = PIECES / "faroe-gasadalur-moon.html"
    html = path.read_text(encoding="utf-8")
    if "dolomites-tre-cime-moon.html" in html.split("related-windows")[0]:
        print("  piece 40: next link already updated")
        return
    new_html, n = re.subn(
        r'<a class="btn secondary" href="\./moonlit-alpine-meadow\.html">[^<]*</a>',
        '<a class="btn secondary" href="./dolomites-tre-cime-moon.html">Next window</a>',
        html,
    )
    if n == 0:
        die("Could not update Next window on faroe-gasadalur-moon.html")
    path.write_text(new_html, encoding="utf-8")
    print("  piece 40: Next window → dolomites-tre-cime-moon")


def update_related_backlinks() -> None:
    """Older related pieces link forward to the new windows (merged, idempotent)."""
    back: dict[str, list[str]] = {}
    for new_slug, olds in RELATED.items():
        for old in olds:
            back.setdefault(old, []).append(new_slug)
    for old, news in back.items():
        path = PIECES / f"{old}.html"
        html = path.read_text(encoding="utf-8")
        m = re.search(r'\n        <p class="note related-windows">.*?</p>', html)
        existing = re.findall(r'href="\./([a-z0-9-]+)\.html"', m.group(0)) if m else []
        slugs = existing + [s for s in news if s not in existing]
        para = "\n" + related_para(slugs)
        if m:
            new_html = html[: m.start()] + para + html[m.end() :]
        else:
            anchor = "\n      </div>\n    </article>"
            if anchor not in html:
                die(f"No insertion point for related links in {path.name}")
            new_html = html.replace(anchor, para + anchor, 1)
        if new_html != html:
            path.write_text(new_html, encoding="utf-8")
            print(f"  related: {old} → {', '.join(slugs)}")


def update_series_hub() -> None:
    """SEO: unique intro + full cross-links for every piece + ItemList schema."""
    def link(slug: str, text: str) -> str:
        return f'<a href="./pieces/{slug}.html">{text}</a>'

    def oxford(parts: list[str]) -> str:
        return ", ".join(parts[:-1]) + ", and " + parts[-1] if len(parts) > 1 else parts[0]

    new_drop = oxford([link(p["slug"], p["title"]) for p in NEW_PIECES])
    themes = "\n".join(
        f"    <p>{label}: {oxford([link(s, t) for s, t in links])}.</p>"
        for label, links in HUB_THEMES
    )
    items = "\n".join(
        f'      <li><a href="./pieces/{slug}.html">{title}</a></li>'
        for slug, title in SERIES_LINKS
    )
    item_list = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Night Windows",
        "url": f"{BASE_URL}/night-windows.html",
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(SERIES_LINKS),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i,
                    "name": title,
                    "url": f"{BASE_URL}/pieces/{slug}.html",
                }
                for i, (slug, title) in enumerate(SERIES_LINKS, 1)
            ],
        },
    }
    ld = json.dumps(item_list, indent=2, ensure_ascii=False)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
{GA_TAG}
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Night Windows series — moonlit landscape prints | Prompt Framed</title>
  <meta name="description" content="{HUB_META_DESC}">
  <link rel="canonical" href="{BASE_URL}/night-windows.html">
  <meta property="og:title" content="Night Windows — {COUNT_WORD} moonlit windows | Prompt Framed">
  <meta property="og:description" content="A growing series of dreamy moonlit landscapes from Night Shade Art. Each picture is a window into a place you wish you were.">
  <meta property="og:url" content="{BASE_URL}/night-windows.html">
  <meta property="og:image" content="{BASE_URL}/assets/night-windows-contact-sheet.jpg">
  <meta property="og:image:alt" content="Contact sheet of Night Windows landscapes">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Night Windows — Prompt Framed">
  <meta name="twitter:description" content="{COUNT_WORD_CAP} windows into places you wish you were.">
  <meta name="twitter:image" content="{BASE_URL}/assets/night-windows-contact-sheet.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=Outfit:wght@380;560;650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json">
{ld}
  </script>
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
    <p>{HUB_INTRO}</p>
    <p>{COUNT_WORD_CAP} windows so far. Each piece page has its own mood, alt text, and buy link. A social post shows the art; the line under it stays the same.</p>
    <p class="soft-cta"><a class="btn" href="./buy.html">Want a poster? Buy at the link.</a></p>
    <figure class="series-sheet">
      <img src="./assets/night-windows-contact-sheet.jpg" width="1400" height="933" alt="Contact sheet of Night Windows moonlit landscapes">
    </figure>
    <h2>Open windows</h2>
    <ol class="series-list">
{items}
    </ol>
    <p>New this drop: {new_drop}.</p>
    <h2>Find your window</h2>
{themes}
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
    print(f"  night-windows.html: refreshed hub ({len(SERIES_LINKS)} pieces + intro + ItemList schema + themed links)")


def copy_print_masters() -> None:
    """Clean print masters for fulfilment: byte-for-byte copies, never watermarked."""
    import shutil

    dst_dir = GALLERY / "print-masters"
    dst_dir.mkdir(parents=True, exist_ok=True)
    for p in NEW_PIECES:
        src, dst = GALLERY / p["file"], dst_dir / p["file"]
        if dst.exists() and dst.read_bytes() == src.read_bytes():
            continue
        shutil.copy2(src, dst)
        print(f"  print master: {dst.relative_to(ROOT)}")


def check_copy() -> None:
    """Public hero copy must not name AI/ChatGPT (keywords follow the existing pattern)."""
    texts = [HUB_META_DESC, HUB_INTRO, BUY_META_DESC, BUY_HERO]
    for p in NEW_PIECES:
        texts += [p["title"], p["alt"], p["description"], p["card_blurb"]]
    bad = [t for t in texts if re.search(r"\bAI\b|ChatGPT", t)]
    if bad:
        die("AI/ChatGPT in public copy: " + " | ".join(bad))
    known = set(TITLES)
    for slug, olds in RELATED.items():
        for s in [slug, *olds]:
            if s not in known:
                die(f"RELATED slug not in SERIES_LINKS: {s}")
            if not (PIECES / f"{s}.html").exists() and s not in {p['slug'] for p in NEW_PIECES}:
                die(f"RELATED slug has no page: {s}")
    for _, links in HUB_THEMES:
        for s, _t in links:
            if s not in known:
                die(f"HUB_THEMES slug not in SERIES_LINKS: {s}")


def main() -> None:
    print(f"Repo: {ROOT}")
    check_copy()
    check_pngs()
    copy_print_masters()
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
    update_piece40_next()
    update_related_backlinks()
    update_series_hub()
    print("\nDone. Next: python3 scripts/watermark_for_social.py 41-dolomites-tre-cime-moon 42-lofoten-reine-moon \\")
    print("  43-cinque-terre-manarola-moon 44-lake-bled-island-moon 45-guilin-li-river-moon, push, Stripe links,")
    print("then python3 scripts/apply_stripe_links.py && --check.")


if __name__ == "__main__":
    main()
