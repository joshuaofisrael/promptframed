#!/usr/bin/env python3
"""Publish Night Windows pieces 46–50 into the Prompt Framed site.

Expects PNG masters already present under gallery/:
  gallery/46-meteora-monasteries-moon.png
  gallery/47-lauterbrunnen-valley-moon.png
  gallery/48-mount-fuji-pagoda-moon.png
  gallery/49-iguazu-falls-moon.png
  gallery/50-isle-of-skye-storr-moon.png

Run from repo root:
  python3 scripts/publish_pieces_46_50.py

Copy in NEW_PIECES (alt / description / card_blurb / keywords) and the HUB_* / BUY_*
strings was written after checking the real images.

Idempotent: skips catalog/products rows and HTML cards that already exist.
New piece pages ship with GA4 + Product/Offer/ImageObject/BreadcrumbList JSON-LD.
Also refreshes the night-windows.html hub (fifty pieces), the buy.html hero
copy, the piece-45 next link, and "More windows like this" related-piece
cross-links in both directions.
Buy blocks are filled from products.json by scripts/apply_stripe_links.py; then
scripts/build_grid_thumbs.py adds watermarked grid thumbnails + srcset.
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
        "id": "46-meteora-monasteries-moon",
        "slug": "meteora-monasteries-moon",
        "title": "Meteora Monasteries Moon",
        "photoNumber": 46,
        "file": "46-meteora-monasteries-moon.png",
        "asset": "46-meteora-monasteries-moon.jpg",
        "alt": (
            'Moonlit Meteora in Greece with lit monasteries perched on sheer sandstone pillars, mist filling the valley below, village lights along the river plain, and a full moon over the mountains'
        ),
        "description": (
            'Meteora’s monasteries glow on top of sheer stone pillars while mist pools in the valley below and a full moon rises over the mountains of Thessaly.'
        ),
        "card_blurb": 'Cliff-top monasteries, a misty valley, and a moon over Meteora.',
        "keywords": [
            "Meteora Greece night",
            "Meteora monasteries moonlight",
            "Greek monastery wall art",
            "Thessaly rock pillars print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "47-lauterbrunnen-valley-moon",
        "slug": "lauterbrunnen-valley-moon",
        "title": "Lauterbrunnen Valley Moon",
        "photoNumber": 47,
        "file": "47-lauterbrunnen-valley-moon.png",
        "asset": "47-lauterbrunnen-valley-moon.jpg",
        "alt": (
            'Moonlit Lauterbrunnen Valley in Switzerland with Staubbach Falls pouring off a sheer cliff, a white church steeple and lit chalets in the village, a stream under a stone bridge, wildflowers by a wooden fence, and snowy Alps under a full moon'
        ),
        "description": (
            'Staubbach Falls pours down the cliff above Lauterbrunnen while chalet windows and the church glow in the valley and snowy Alps shine under a full moon.'
        ),
        "card_blurb": 'A cliff waterfall, lit chalets, and a moon over Lauterbrunnen.',
        "keywords": [
            "Lauterbrunnen night",
            "Staubbach Falls moonlight",
            "Swiss village wall art",
            "Swiss Alps valley print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "48-mount-fuji-pagoda-moon",
        "slug": "mount-fuji-pagoda-moon",
        "title": "Mount Fuji Pagoda Moon",
        "photoNumber": 48,
        "file": "48-mount-fuji-pagoda-moon.png",
        "asset": "48-mount-fuji-pagoda-moon.jpg",
        "alt": (
            'Moonlit Mount Fuji behind the red five-story Chureito Pagoda with lantern-lit stairs, cherry blossoms in bloom, a lake town glowing below, and a full moon in the night sky'
        ),
        "description": (
            'The red Chureito Pagoda glows among cherry blossoms while lake-town lights shimmer below and snow-capped Mount Fuji rises under a full moon.'
        ),
        "card_blurb": 'A red pagoda, cherry blossoms, and a moon over Mount Fuji.',
        "keywords": [
            "Mount Fuji night",
            "Chureito Pagoda moonlight",
            "cherry blossom wall art",
            "Japan landscape print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "49-iguazu-falls-moon",
        "slug": "iguazu-falls-moon",
        "title": "Iguazu Falls Moon",
        "photoNumber": 49,
        "file": "49-iguazu-falls-moon.png",
        "asset": "49-iguazu-falls-moon.jpg",
        "alt": (
            'Moonlit Iguazu Falls on the Argentina and Brazil border with tiers of waterfalls pouring through lush rainforest, mist rising from the gorge, and a full moon above the river'
        ),
        "description": (
            'Tier after tier of Iguazu’s waterfalls thunders into a misty gorge while the rainforest stays dark and green under a bright full moon.'
        ),
        "card_blurb": 'Rainforest waterfalls, rising mist, and a moon over Iguazu.',
        "keywords": [
            "Iguazu Falls night",
            "Iguazu waterfalls moonlight",
            "rainforest waterfall wall art",
            "Argentina Brazil landscape print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
    {
        "id": "50-isle-of-skye-storr-moon",
        "slug": "isle-of-skye-storr-moon",
        "title": "Isle of Skye Storr Moon",
        "photoNumber": 50,
        "file": "50-isle-of-skye-storr-moon.png",
        "asset": "50-isle-of-skye-storr-moon.jpg",
        "alt": (
            'Moonlit Old Man of Storr on the Isle of Skye with jagged rock pinnacles above green slopes, small lochans and a sea loch catching the moonlight, heather in the foreground, and a full moon over the Scottish Highlands'
        ),
        "description": (
            'The Old Man of Storr stands over green Skye slopes while lochans and the sea loch catch silver light under a full Highland moon.'
        ),
        "card_blurb": 'Rock pinnacles, silver lochans, and a moon over the Isle of Skye.',
        "keywords": [
            "Isle of Skye night",
            "Old Man of Storr moonlight",
            "Scottish Highlands wall art",
            "Scotland landscape print",
            "AI wall art",
            "ChatGPT art print",
        ],
    },
]

# ---- Hub / buy copy (edit here once the real images are checked) ----
# Kept out of the templates below so tweaks after the image check are one-line edits.
COUNT_WORD = "fifty"
COUNT_WORD_CAP = "Fifty"
HUB_META_DESC = (
    "Night Windows is fifty dreamy moonlit landscape prints — Meteora, Lauterbrunnen, "
    "Mount Fuji, Iguazu Falls, the Isle of Skye, and more. Want a poster? Buy at the link."
)
HUB_INTRO = (
    "Windows into places you wish you were. Dreamy moonlit landscapes — Meteora’s monasteries on "
    "their stone pillars, Staubbach Falls above Lauterbrunnen’s chalets, the Chureito Pagoda under "
    "Mount Fuji, the misty falls of Iguazu, and the Old Man of Storr on the Isle of Skye "
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
        "Temples, pagodas and monasteries",
        [
            ("angkor-wat-moon", "Angkor Wat"),
            ("mount-fuji-pagoda-moon", "the Chureito Pagoda below Mount Fuji"),
            ("meteora-monasteries-moon", "Meteora’s cliff-top monasteries"),
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
            ("lauterbrunnen-valley-moon", "Switzerland’s Lauterbrunnen Valley"),
            ("matterhorn-alpine-moon", "the Matterhorn"),
            ("isle-of-skye-storr-moon", "the Old Man of Storr on Skye"),
            ("guilin-li-river-moon", "Guilin’s Li River"),
            ("zhangjiajie-pillars-moon", "Zhangjiajie’s stone pillars"),
            ("yosemite-half-dome-moon", "Yosemite’s Half Dome"),
        ],
    ),
    (
        "Waterfalls, lakes and wild coasts",
        [
            ("iguazu-falls-moon", "Iguazu Falls"),
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
    "Buy Night Windows moonlit landscape prints — fifty windows including Meteora, "
    "Lauterbrunnen, Mount Fuji, Iguazu Falls, and the Isle of Skye. $29 poster or $69 framed, 12×18, "
    "shipping included. Stripe checkout."
)
BUY_HERO = (
    "Fifty moonlit windows, printed for your wall — from Meteora’s cliff-top monasteries and "
    "the Lauterbrunnen waterfall to the Chureito Pagoda under Mount Fuji, the falls of Iguazu, and "
    "the Old Man of Storr on the Isle of Skye. Choose a 12×18 enhanced matte poster or the same print "
    "in a black frame. Shipping is included, and each button opens secure Stripe checkout."
)

NEXT_BY_SLUG = {
    "guilin-li-river-moon": "meteora-monasteries-moon",
    "meteora-monasteries-moon": "lauterbrunnen-valley-moon",
    "lauterbrunnen-valley-moon": "mount-fuji-pagoda-moon",
    "mount-fuji-pagoda-moon": "iguazu-falls-moon",
    "iguazu-falls-moon": "isle-of-skye-storr-moon",
    "isle-of-skye-storr-moon": "moonlit-alpine-meadow",
}

NEXT_LABEL = {
    "moonlit-alpine-meadow": "First window",
}

# SEO (5 Oct 2026, kept for 46–50): thematic "More windows like this" links, both directions,
# so each new URL gets contextual internal links from older, already-crawled pages.
RELATED = {
    "meteora-monasteries-moon": ["cappadocia-fairy-chimneys", "santorini-caldera-moon"],
    "lauterbrunnen-valley-moon": ["matterhorn-alpine-moon", "moonlit-waterfall"],
    "mount-fuji-pagoda-moon": ["japanese-temple-pond", "kyoto-bamboo-moon"],
    "iguazu-falls-moon": ["plitvice-lakes-moon", "machu-picchu-mist"],
    "isle-of-skye-storr-moon": ["scottish-highlands-loch", "faroe-gasadalur-moon"],
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
    ("meteora-monasteries-moon", "Meteora Monasteries Moon"),
    ("lauterbrunnen-valley-moon", "Lauterbrunnen Valley Moon"),
    ("mount-fuji-pagoda-moon", "Mount Fuji Pagoda Moon"),
    ("iguazu-falls-moon", "Iguazu Falls Moon"),
    ("isle-of-skye-storr-moon", "Isle of Skye Storr Moon"),
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


def update_piece45_next() -> None:
    path = PIECES / "guilin-li-river-moon.html"
    html = path.read_text(encoding="utf-8")
    if "meteora-monasteries-moon.html" in html.split("related-windows")[0]:
        print("  piece 45: next link already updated")
        return
    new_html, n = re.subn(
        r'<a class="btn secondary" href="\./moonlit-alpine-meadow\.html">[^<]*</a>',
        '<a class="btn secondary" href="./meteora-monasteries-moon.html">Next window</a>',
        html,
    )
    if n == 0:
        die("Could not update Next window on guilin-li-river-moon.html")
    path.write_text(new_html, encoding="utf-8")
    print("  piece 45: Next window → meteora-monasteries-moon")


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
    update_piece45_next()
    update_related_backlinks()
    update_series_hub()
    # SEO (7 Oct 2026): image-sitemap entries (watermarked assets only) for new + old pieces.
    sys.path.insert(0, str(ROOT / "scripts"))
    import seo_image_sitemap
    seo_image_sitemap.main()
    print("\nDone. Next: python3 scripts/watermark_for_social.py 46-meteora-monasteries-moon 47-lauterbrunnen-valley-moon \\")
    print("  48-mount-fuji-pagoda-moon 49-iguazu-falls-moon 50-isle-of-skye-storr-moon, push, Stripe links,")
    print("then python3 scripts/apply_stripe_links.py && --check, then python3 scripts/build_grid_thumbs.py.")


if __name__ == "__main__":
    main()
