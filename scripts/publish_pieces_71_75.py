#!/usr/bin/env python3
"""Publish Night Windows pieces 71–75 into the Prompt Framed / Moonlit Windows site.

Written 16 Oct 2026 for pieces 71–75, adapted from publish_pieces_66_70.py (written 15 Oct 2026)
for the CURRENT site structure (after seo_commercial_pass.py,
seo_keywords_pass.py, apply_mural_links.py, the owner footer, the nav rename,
mountain-wall-art.html, the european/asian/lakes/coastal/murals collection pages,
seo_image_sitemap.py and build_grid_thumbs.py). New piece pages
are rendered directly in that final shape (same head/meta/JSON-LD/buy block/footer as
pieces/bora-bora-lagoon-moon.html), and every other page is patched IN PLACE, so the
site-wide passes never need to be re-run.

Expects clean PNG masters under gallery/ (never watermarked, never committed):
  gallery/71-colmar-petite-venise-moon.png
  gallery/72-glenfinnan-viaduct-moon.png
  gallery/73-monument-valley-moon.png
  gallery/74-sigiriya-rock-moon.png
  gallery/75-cradle-mountain-dove-lake-moon.png

Run from anywhere:
  python3 scripts/publish_pieces_71_75.py               # publish (refuses while TODO copy remains)
  python3 scripts/publish_pieces_71_75.py --allow-todo  # dry runs only
  python3 scripts/publish_pieces_71_75.py --check       # read-only structural checks
  python3 scripts/publish_pieces_71_75.py --ping        # AFTER commit+push: wait for deploy, IndexNow-ping new + changed URLs
Without all five masters every mode except --check/--ping stops at check_pngs() BEFORE writing anything.

Re-run the SAME command after the Stripe links (posterUrl, framedUrl, muralUrl) are in
products.json: it rewires the buy blocks of pieces 71–75 (piece pages + buy.html cards)
in the live format, touching nothing else. Do NOT run apply_stripe_links.py or
apply_mural_links.py in write mode: on today's site they strip the mountain
collection-link note from piece pages and revert the buy.html card price lines
and alt text. Their --check modes are read-only and fine.

What one run does (idempotent):
  * print masters: byte copies into gallery/print-masters/ (clean)
  * watermarked public previews: assets/NN-slug.jpg (website/og) + gallery/social/NN-slug.jpg
    (Instagram + Stripe product image) via watermark_for_social.export_piece
  * gallery/catalog.json + products.json rows (stripe placeholder until links exist)
  * pieces/<slug>.html (final head/JSON-LD incl. #offer-mural, buy block, window-nav, related,
    mountain collection-link note on Monument Valley and Cradle Mountain)
  * index.html: gallery cards + shop ItemList JSON-LD + "Shop NN" meta
  * buy.html: cards inside buy:start/buy:end + hero + meta/OG/Twitter count + shop ItemList
  * night-windows.html: count, intro, ol list, ItemList, "New this drop", themes (keeps the
    european, mountain, murals, lakes, coastal and asian collection links)
  * mountain-wall-art.html: "all seventy Night Windows" -> "all seventy-five" count line
  * about.html + llms.txt: series count 70 -> 75
  * next chain bora-bora-lagoon -> 71 -> ... -> 75 -> moonlit-alpine-meadow ("First window")
  * RELATED "More windows like this" links both directions
  * sitemap.xml: new URLs, image entries (seo_image_sitemap), lastmod today on touched pages
  * grid thumbnails + srcset for new cards (build_grid_thumbs)
Does NOT git commit/push and never touches Stripe.

Collection pages are hand-curated by their own build scripts. Prepared edits for 71–75 live in
/workspace/promptframed-private/collections_71_75.patch (git apply it, then run each builder with
--check, then for real, ONLY after the Stripe links land: the european, asian and lakes builders
assert live Stripe links; mountain and murals show 'opens for orders soon' while Stripe is a placeholder).
Re-runs of this script keep any european/asian/lakes/murals collection-link notes on the new piece pages.
Notes (16 Oct 2026 plan; re-check against the real images):
  * peel-and-stick-wall-murals.html — all five IF each preview is 1024×1536 (2:3 portrait):
    Colmar, Glenfinnan, Sigiriya -> castles (castles and landmarks); Monument Valley -> mountains
    (mountain and canyon); Cradle Mountain -> lakes-waterfalls. Drop any that is not 2:3 from the patch.
  * european-wall-art.html — colmar-petite-venise-moon (old towns), glenfinnan-viaduct-moon (countryside).
  * asian-wall-art.html — sigiriya-rock-moon (southeast-asia-india group, renamed South and Southeast Asian).
  * lake-wall-art.html — cradle-mountain-dove-lake-moon (lakes group).
  * mountain-wall-art.html — monument-valley-moon and cradle-mountain-dove-lake-moon (MOUNTAIN_COLLECTION
    below + build_collection_mountain.py SLUGS in the patch; keep both in step).
  * coastal-wall-art.html — not applicable.
"""
from __future__ import annotations

import datetime
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

GALLERY = ROOT / "gallery"
ASSETS = ROOT / "assets"
PIECES = ROOT / "pieces"
CATALOG_PATH = GALLERY / "catalog.json"
PRODUCTS_PATH = ROOT / "products.json"
INDEX_PATH = ROOT / "index.html"
BUY_PATH = ROOT / "buy.html"
SITEMAP_PATH = ROOT / "sitemap.xml"
SERIES_PATH = ROOT / "night-windows.html"
MOUNTAIN_PATH = ROOT / "mountain-wall-art.html"
BASE_URL = "https://moonlitwindows.com"
GA_ID = "G-663R8VD62L"
TODAY = datetime.date.today().isoformat()

STYLE = (
    "Dreamy cinematic fantasy realism, photorealistic landscape photography, "
    "ethereal moonlight, dramatic clouds, lush vegetation and wildflowers, "
    "deep atmospheric perspective, rich blue-green nighttime tones, subtle warm lights, "
    "romantic landscape aesthetic, peaceful dreamlike atmosphere, highly detailed, "
    "realistic natural textures, volumetric haze, dramatic but believable lighting. "
    "Idyllic, calm, natural moonlit night that invites the viewer to step into the scene: soft silvery moonlight, "
    "gentle cool night tones, warm natural window and lantern light, true-to-life colours, recognizably real place. "
    "No neon, no magenta/purple/cyan glow, no glowing or fluorescent lights, no daylight-bright night, not oversaturated. "
    "thin wispy clouds veiling the moon without dimming the moonlight."
)

# ---------------------------------------------------------------------------------------
# COPY. Final copy written 16 Oct 2026 BEFORE the images existed; re-check alt text against the real
# images and adjust any detail that is not in the picture.
# Use typographic apostrophes (’) and no double quotes. No AI/ChatGPT/Higgsfield/canvas. Never neon.
# alt: what is literally in the picture (the site appends ", night landscape wall art print").
# description: one sentence, ~110–140 chars (piece page, buy card, meta, JSON-LD).
# card_blurb: short homepage line, pattern "A, B, and a moon over X."
# ---------------------------------------------------------------------------------------
NEW_PIECES = [
    {
        "slug": "colmar-petite-venise-moon",
        "title": "Colmar Petite Venise Moon",
        "photoNumber": 71,
        "alt": "Moonlit Petite Venise quarter of Colmar in Alsace, France, pastel half-timbered houses with flower-filled window boxes and warm lit windows lining a calm canal on the left, a weeping willow on the right bank, a small arched stone bridge beyond and flowers in the foreground, the full moon behind thin wispy clouds reflected in the water",
        "description": "Half-timbered houses in Colmar’s Petite Venise lean over a calm canal, flower boxes and warm windows mirrored beneath a cloud-veiled Alsace moon.",
        "card_blurb": "Half-timbered houses, a quiet canal, and a moon over Colmar.",
        "keywords": [
            "Colmar Petite Venise night",
            "Colmar canal moonlight",
            "Alsace half-timbered houses wall art",
            "France old town print",
        ],
    },
    {
        "slug": "glenfinnan-viaduct-moon",
        "title": "Glenfinnan Viaduct Moon",
        "photoNumber": 72,
        "alt": "Moonlit Glenfinnan Viaduct in the Scottish Highlands, Scotland, its curving stone arches spanning a green glen, Loch Shiel and misty mountains beyond, purple heather, grass and mossy rocks in the foreground and a full moon behind thin wispy clouds shining over the loch",
        "description": "The Glenfinnan Viaduct curves its stone arches across a Highland glen toward Loch Shiel and misty mountains beneath a cloud-veiled moon.",
        "card_blurb": "Curving stone arches, a Highland glen, and a moon over Glenfinnan.",
        "keywords": [
            "Glenfinnan Viaduct night",
            "Loch Shiel moonlight",
            "Scottish Highlands wall art",
            "Scotland railway viaduct print",
        ],
    },
    {
        "slug": "monument-valley-moon",
        "title": "Monument Valley Moon",
        "photoNumber": 73,
        "alt": "Moonlit Monument Valley in the Navajo Nation on the Arizona–Utah border, USA, red sandstone buttes and mesas rising from the desert floor, a winding red dirt road through sagebrush, scrub and red boulders in the foreground, silvery moonlight on the rock and a bright full moon in thin wispy clouds",
        "description": "Red sandstone buttes rise from the desert floor of Monument Valley, silvered by a full moon veiled in thin cloud on the Arizona–Utah border.",
        "card_blurb": "Sandstone buttes, a winding desert road, and a moon over Monument Valley.",
        "keywords": [
            "Monument Valley night",
            "Monument Valley buttes moonlight",
            "desert southwest wall art",
            "Arizona Utah landscape print",
        ],
    },
    {
        "slug": "sigiriya-rock-moon",
        "title": "Sigiriya Rock Moon",
        "photoNumber": 74,
        "alt": "Moonlit Sigiriya Lion Rock in Sri Lanka, the flat-topped rock fortress rising sheer above the jungle, palm trees on either side, and the terraced water gardens with a small cascade and lily-pad pools reflecting the moon in the foreground, a full moon behind thin wispy clouds",
        "description": "Sigiriya’s flat-topped Lion Rock rises sheer above Sri Lankan jungle and its terraced water gardens, all silvered by a cloud-veiled moon.",
        "card_blurb": "An ancient rock fortress, terraced water gardens, and a moon over Sigiriya.",
        "keywords": [
            "Sigiriya Lion Rock night",
            "Sigiriya fortress moonlight",
            "Sri Lanka landscape wall art",
            "Sigiriya rock print",
        ],
    },
    {
        "slug": "cradle-mountain-dove-lake-moon",
        "title": "Cradle Mountain Dove Lake Moon",
        "photoNumber": 75,
        "alt": "Moonlit Cradle Mountain in Tasmania, Australia, its jagged dolerite peaks mirrored in still Dove Lake, the old timber boatshed on the right shore, golden buttongrass, flowering shrubs and boulders in the foreground and a full moon behind thin wispy clouds",
        "description": "Cradle Mountain’s jagged peaks mirror in still Dove Lake beside the old timber boatshed, beneath a cloud-veiled Tasmanian moon.",
        "card_blurb": "A timber boatshed, a mirrored peak, and a moon over Dove Lake.",
        "keywords": [
            "Cradle Mountain night",
            "Dove Lake boatshed moonlight",
            "Tasmania landscape wall art",
            "Australia mountain lake print",
        ],
    },
]
for _p in NEW_PIECES:
    _p["id"] = f"{_p['photoNumber']:02d}-{_p['slug']}"
    _p["file"] = f"{_p['id']}.png"
    _p["asset"] = f"{_p['id']}.jpg"
NEW_SLUGS = [p["slug"] for p in NEW_PIECES]

COUNT = 75
PREV_COUNT = 70
COUNT_WORD_CAP = "Seventy-five"
COUNT_WORD = "seventy-five"
PREV_COUNT_WORD = "seventy"

# night-windows.html intro paragraph.
HUB_INTRO = (
    "Windows into places you wish you were. Dreamy moonlit landscapes — the half-timbered canals of Colmar’s "
    "Petite Venise, the Glenfinnan Viaduct above Loch Shiel, the sandstone buttes of Monument Valley, "
    "Sigiriya’s Lion Rock, and Cradle Mountain over Dove Lake "
    "— printed as posters."
)
# buy.html hero paragraph (the <p> after the sale-line).
BUY_HERO = (
    "Seventy-five moonlit windows, printed for your wall — from Colmar’s half-timbered canals and the Glenfinnan "
    "Viaduct to Monument Valley, Sigiriya’s Lion Rock, and Cradle Mountain above Dove Lake. Choose a 12×18 "
    "enhanced matte poster or the same print in a black frame. Shipping is included, and each button "
    "opens secure Stripe checkout."
)
# Tails of the hub / buy meta descriptions (place names searchers type). OLD = what 66–70 left live.
HUB_META_TAIL_OLD, HUB_META_TAIL_NEW = (
    "Eilean Donan, Dubrovnik, Pamukkale, Rothenburg, Bora Bora and more.",
    "Colmar, Glenfinnan, Monument Valley, Sigiriya, Cradle Mountain and more.",
)
BUY_META_TAIL_OLD, BUY_META_TAIL_NEW = (
    "Eilean Donan, Dubrovnik, Pamukkale, Rothenburg, Bora Bora posters.",
    "Colmar, Glenfinnan, Monument Valley, Sigiriya, Cradle Mountain posters.",
)
# night-windows.html "Find your window" (full replacement; suffix keeps the mountain link).
MOUNTAIN_SUFFIX = (
    ' See them together in the <a data-collection="mountain" href="./mountain-wall-art.html">'
    "mountain wall art collection</a>."
)
# Same markup build_collection_murals.py inserts, so re-running this script keeps the murals links.
MURALS_PIECE_LINK = ('<p class="note collection-link" data-collection="murals">Planning a feature wall? See the '
                     '<a href="../peel-and-stick-wall-murals.html">peel and stick wall murals collection</a> '
                     'for measuring and wall-prep tips.</p>')
MURALS_SUFFIX = (' For a whole feature wall, see the <a data-collection="murals" '
                 'href="./peel-and-stick-wall-murals.html">peel and stick wall murals collection</a>.')
# Added to the hub by build_collection_lakes.py (12 Oct 2026); the themes block is fully
# rewritten below, so it must be carried here or the lakes link would be dropped.
LAKES_SUFFIX = (' The lakes and waterfalls are gathered in the <a data-collection="lakes" '
                'href="./lake-wall-art.html">lake and waterfall wall art collection</a>.')
# Added to the hub by build_collection_coastal.py (13 Oct 2026, right after the lakes link); carried
# here for the same reason (the first 56–60 run dropped it).
COASTAL_SUFFIX = (' Seaside villages, ocean cliffs and fjords are in the <a data-collection="coastal" '
                  'href="./coastal-wall-art.html">coastal wall art collection</a>.')
# Added to the hub by build_collection_asian.py (14 Oct 2026, right after the coastal link). The 61–65
# publish run dropped it from the live hub (build_collection_asian.py --check said WOULD CHANGE on
# 15 Oct); carrying it here restores it and keeps it on every re-run.
ASIAN_SUFFIX = (' Mount Fuji, Kyoto, the Great Wall and the temples of Angkor, Bagan and Agra are in the '
                '<a data-collection="asian" href="./asian-wall-art.html">Asian wall art collection</a>.')
# Added to the hub castles line by build_collection_european.py (15 Oct 2026); carried here so the
# full themes rewrite below keeps it.
EUROPEAN_SUFFIX = (' See them together in the <a data-collection="european" '
                   'href="./european-wall-art.html">European wall art collection</a>.')
HUB_THEMES = [
    (
        "Castles and old towns",
        [
            ("neuschwanstein-castle-moon", "Neuschwanstein"),
            ("eilean-donan-castle-moon", "Eilean Donan Castle on Loch Duich"),
            ("dubrovnik-old-town-moon", "Dubrovnik’s walled old town"),
            ("rothenburg-old-town-moon", "Rothenburg’s lamplit cobblestone lanes"),
            ("colmar-petite-venise-moon", "Colmar’s Petite Venise canals"),
            ("prague-charles-bridge-moon", "Prague’s Charles Bridge"),
            ("bruges-canal-moon", "Bruges’ Rozenhoedkaai and Belfry"),
            ("bibury-arlington-row-moon", "Arlington Row in Bibury"),
            ("sintra-pena-palace-moon", "Sintra’s Pena Palace"),
            ("lake-bled-island-moon", "Lake Bled’s island church and castle"),
            ("mont-saint-michel-moon", "Mont Saint-Michel"),
            ("lake-como-bellagio-moon", "Bellagio on Lake Como"),
            ("hallstatt-lake-moon", "Hallstatt"),
            ("chefchaouen-blue-moon", "Chefchaouen"),
            ("moroccan-kasbah-night", "a Moroccan kasbah"),
        ],
        EUROPEAN_SUFFIX,
    ),
    (
        "Temples, monuments, pagodas and monasteries",
        [
            ("taj-mahal-moon", "the Taj Mahal"),
            ("angkor-wat-moon", "Angkor Wat"),
            ("sigiriya-rock-moon", "Sigiriya’s Lion Rock fortress"),
            ("mount-fuji-pagoda-moon", "the Chureito Pagoda below Mount Fuji"),
            ("meteora-monasteries-moon", "Meteora’s cliff-top monasteries"),
            ("bagan-temples-night", "Bagan"),
            ("bali-jungle-temple", "a Bali jungle temple"),
            ("japanese-temple-pond", "a Japanese temple pond"),
            ("petra-treasury-night", "Petra’s Treasury"),
        ],
        "",
    ),
    (
        "Mountains and river valleys",
        [
            ("dolomites-tre-cime-moon", "the Dolomites’ Tre Cime"),
            ("lauterbrunnen-valley-moon", "Switzerland’s Lauterbrunnen Valley"),
            ("matterhorn-alpine-moon", "the Matterhorn"),
            ("isle-of-skye-storr-moon", "the Old Man of Storr on Skye"),
            ("glenfinnan-viaduct-moon", "the Glenfinnan Viaduct above Loch Shiel"),
            ("kirkjufell-waterfall-moon", "Kirkjufell and Kirkjufellsfoss"),
            ("great-wall-mutianyu-moon", "the Great Wall at Mutianyu"),
            ("guilin-li-river-moon", "Guilin’s Li River"),
            ("zhangjiajie-pillars-moon", "Zhangjiajie’s stone pillars"),
            ("yosemite-half-dome-moon", "Yosemite’s Half Dome"),
        ],
        MOUNTAIN_SUFFIX,
    ),
    (
        "Canyons, waterfalls, lakes, lagoons, salt flats and wild coasts",
        [
            ("pamukkale-terraces-moon", "Pamukkale’s travertine terraces"),
            ("bora-bora-lagoon-moon", "Bora Bora’s lagoon"),
            ("cradle-mountain-dove-lake-moon", "Cradle Mountain above Dove Lake"),
            ("lake-tekapo-church-moon", "Lake Tekapo’s Church of the Good Shepherd"),
            ("na-pali-coast-moon", "Kauai’s Na Pali Coast"),
            ("victoria-falls-moon", "Victoria Falls"),
            ("salar-de-uyuni-moon", "the mirrored Salar de Uyuni"),
            ("grand-canyon-rim-moon", "the Grand Canyon’s South Rim"),
            ("monument-valley-moon", "Monument Valley’s sandstone buttes"),
            ("cliffs-of-moher-moon", "the Cliffs of Moher"),
            ("big-sur-bixby-bridge-moon", "Bixby Creek Bridge on Big Sur"),
            ("iguazu-falls-moon", "Iguazu Falls"),
            ("plitvice-lakes-moon", "Plitvice Lakes"),
            ("faroe-gasadalur-moon", "Gásadalur in the Faroes"),
            ("lofoten-reine-moon", "Reine in the Lofoten Islands"),
            ("cinque-terre-manarola-moon", "Manarola in the Cinque Terre"),
            ("iceland-black-sand-moon", "Iceland’s black sand"),
            ("banff-lake-louise-moon", "Lake Louise"),
            ("moonlit-waterfall", "a moonlit waterfall"),
        ],
        MURALS_SUFFIX + LAKES_SUFFIX + COASTAL_SUFFIX + ASIAN_SUFFIX,
    ),
]

NEXT_BY_SLUG = {
    "bora-bora-lagoon-moon": "colmar-petite-venise-moon",
    "colmar-petite-venise-moon": "glenfinnan-viaduct-moon",
    "glenfinnan-viaduct-moon": "monument-valley-moon",
    "monument-valley-moon": "sigiriya-rock-moon",
    "sigiriya-rock-moon": "cradle-mountain-dove-lake-moon",
    "cradle-mountain-dove-lake-moon": "moonlit-alpine-meadow",
}
NEXT_LABEL = {"moonlit-alpine-meadow": "First window"}
PREV_LAST = "bora-bora-lagoon-moon"  # piece 70, currently links to "First window"

# "More windows like this" (both directions). Re-check against the real images.
RELATED = {
    "colmar-petite-venise-moon": ["venetian-canal-moonrise", "rothenburg-old-town-moon"],
    "glenfinnan-viaduct-moon": ["eilean-donan-castle-moon", "scottish-highlands-loch"],
    "monument-valley-moon": ["grand-canyon-rim-moon", "cappadocia-fairy-chimneys"],
    "sigiriya-rock-moon": ["angkor-wat-moon", "meteora-monasteries-moon"],
    "cradle-mountain-dove-lake-moon": ["banff-lake-louise-moon", "lake-tekapo-church-moon"],
}
# Slugs listed here get the mountain collection-link note on their page. They must also be in
# build_collection_mountain.py SLUGS (added by collections_71_75.patch; mountain-wall-art.html is
# hand-written) or the note points at a page that does not list them.
MOUNTAIN_COLLECTION: set[str] = {"monument-valley-moon", "cradle-mountain-dove-lake-moon"}

GA_TAG = f"""  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>"""
IG = '<a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a>'
PRICE_LINE = "$35 poster · $69 framed (12×18)"
PRICE_LINE_MURAL = "$35 poster · $69 framed (12×18) · $149 peel &amp; stick wall mural (4×6 ft)"
PIECE_NOTE = ("Enhanced matte poster or black-framed print, 12×18 in. Shipping included. "
              "Secure checkout by Stripe; your receipt arrives by email.")
MURAL_NOTE = ('<p class="note mural-note">Peel &amp; stick wall mural: 4×6 ft (48×72 in) removable wallpaper on '
              'peel-and-stick polyester. No paste; removes cleanly from most smooth painted walls. Each mural is '
              'printed to order and ships in 1–2 weeks, shipping included.</p>')
START, END = "<!-- buy:start -->", "<!-- buy:end -->"
BANNED = r"\bAI\b|ChatGPT|Higgsfield|github\.io|canvas"

ALLOW_TODO = "--allow-todo" in sys.argv
CHANGED_URLS: set[str] = set()  # for sitemap lastmod


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_if_changed(path: Path, new: str, url: str | None = None) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if new == old:
        return False
    path.write_text(new, encoding="utf-8")
    if url:
        CHANGED_URLS.add(url)
    return True


def page_url(slug: str) -> str:
    return f"{BASE_URL}/pieces/{slug}.html"


def titles() -> dict[str, str]:
    t = {p["slug"]: p["title"] for p in load_json(PRODUCTS_PATH)}
    t.update({p["slug"]: p["title"] for p in NEW_PIECES})
    return t


def is_live(u) -> bool:
    return isinstance(u, str) and u.startswith("https://buy.stripe.com/")


def stripe_for(slug: str) -> dict:
    for it in load_json(PRODUCTS_PATH):
        if it["slug"] == slug:
            return it.get("stripe") or {}
    return {}


# ------------------------------- checks -------------------------------
def check_copy() -> None:
    texts = [HUB_INTRO, BUY_HERO, HUB_META_TAIL_NEW, BUY_META_TAIL_NEW]
    for p in NEW_PIECES:
        texts += [p["title"], p["alt"], p["description"], p["card_blurb"], *p["keywords"]]
    texts += [lbl for _, links, _ in HUB_THEMES for _, lbl in links]
    bad = [t for t in texts if re.search(BANNED, t)]
    if bad:
        die("banned word (AI/ChatGPT/Higgsfield/github.io/canvas) in public copy: " + " | ".join(bad))
    quotes = [t for t in texts if '"' in t or "'" in t or "<" in t or "&" in t]
    if quotes:
        die("use ’ (not straight quotes) and no <, & in copy: " + " | ".join(quotes))
    todo = [t for t in texts if "TODO" in t]
    if todo and not ALLOW_TODO:
        die(f"{len(todo)} copy field(s) still marked TODO; finalize them from the real images "
            "(or pass --allow-todo for a dry run).")
    known = set(titles())
    for slug, olds in RELATED.items():
        for s in [slug, *olds]:
            if s not in known:
                die(f"RELATED slug unknown: {s}")
            if s not in NEW_SLUGS and not (PIECES / f"{s}.html").exists():
                die(f"RELATED slug has no page: {s}")
    themed = [s for _, links, _ in HUB_THEMES for s, _ in links]
    for s in themed:
        if s not in known:
            die(f"HUB_THEMES slug unknown: {s}")
    for s in NEW_SLUGS:
        if s not in themed:
            die(f"new piece missing from HUB_THEMES: {s}")
    prods = load_json(PRODUCTS_PATH)
    old = [p for p in prods if p["slug"] not in NEW_SLUGS]
    if len(old) != PREV_COUNT:
        die(f"expected {PREV_COUNT} existing products, found {len(old)}")


def check_pngs() -> None:
    missing = [f"gallery/{p['file']}" for p in NEW_PIECES if not (GALLERY / p["file"]).is_file()]
    if missing:
        die("Missing PNG masters (do not invent files). Copy them in, then re-run:\n  - " + "\n  - ".join(missing))


# ------------------------------- images -------------------------------
def export_images(piece: dict) -> tuple[int, int, int, int]:
    """Clean master -> print-masters byte copy + watermarked social + website JPGs."""
    from PIL import Image
    import watermark_for_social as wm

    src = GALLERY / piece["file"]
    before = src.read_bytes()
    outs = [ASSETS / piece["asset"], GALLERY / "social" / piece["asset"], GALLERY / "print-masters" / piece["file"]]
    if all(o.exists() and o.stat().st_mtime >= src.stat().st_mtime for o in outs):
        print(f"  previews: up to date for {piece['id']}")
    else:
        wm.ensure_dirs()
        wm.export_piece(src, wm.load_watermark(), social=True, website=True)
    pm = GALLERY / "print-masters" / piece["file"]
    if pm.read_bytes() != before:  # belt and braces (export_piece already asserts)
        shutil.copy2(src, pm)
    if src.read_bytes() != before:
        die(f"print master modified: {src}")
    with Image.open(src) as im:
        mw, mh = im.size
    with Image.open(ASSETS / piece["asset"]) as im:
        aw, ah = im.size
    return mw, mh, aw, ah


# ------------------------------- data rows -------------------------------
# Generation details (tool name, style prompt) are private: they never go into the public
# gallery/catalog.json, only into this file outside the repo.
CATALOG_PRIVATE = Path(__import__("os").environ.get(
    "PUBLISH_71_75_PRIVATE_CATALOG", "/workspace/promptframed-private/catalog_private.json"))
PRIVATE_FIELDS = ("source", "stylePrompt")


def save_private_catalog(slug: str) -> None:
    data = load_json(CATALOG_PRIVATE) if CATALOG_PRIVATE.exists() else {}
    rec = {"source": "ChatGPT", "stylePrompt": STYLE}
    if data.get(slug, {}).get("source") != rec["source"] or data.get(slug, {}).get("stylePrompt") != STYLE:
        data.setdefault(slug, {}).update(rec)
        CATALOG_PRIVATE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_catalog(piece: dict, width: int, height: int) -> None:
    catalog = load_json(CATALOG_PATH)
    row = {
        "id": piece["id"],
        "slug": piece["slug"],
        "title": piece["title"],
        "photoNumber": piece["photoNumber"],
        "file": piece["file"],
        "width": width,
        "height": height,
        "orientation": "portrait" if height >= width else "landscape",
        "alt": piece["alt"],
        "description": piece["description"],
        "keywords": piece["keywords"],
        "products": ["poster", "framed_print"],
        "status": "ready",
    }
    save_private_catalog(piece["slug"])
    for i, e in enumerate(catalog):
        if e.get("slug") == piece["slug"]:
            if e != row:  # refresh copy edits on re-run
                catalog[i] = row
                dump_json(CATALOG_PATH, catalog)
                print(f"  catalog: refreshed {piece['id']}")
            return
    catalog.append(row)
    dump_json(CATALOG_PATH, catalog)
    print(f"  catalog: appended {piece['id']}")


def append_products(piece: dict) -> None:
    products = load_json(PRODUCTS_PATH)
    for e in products:
        if e.get("slug") == piece["slug"]:
            if e.get("title") != piece["title"]:
                e["title"] = piece["title"]
                dump_json(PRODUCTS_PATH, products)
            return
    products.append(
        {
            "slug": piece["slug"],
            "title": piece["title"],
            "series": "Night Windows",
            "photoNumber": piece["photoNumber"],
            "printful": {"posterUrl": None, "framedUrl": None, "status": "placeholder"},
            "stripe": {"posterUrl": None, "framedUrl": None, "status": "placeholder"},
            "asset": piece["asset"],
            "printSource": f"gallery/{piece['file']}",
        }
    )
    products.sort(key=lambda e: e.get("photoNumber", 0))
    dump_json(PRODUCTS_PATH, products)
    print(f"  products: appended {piece['slug']} (stripe placeholder)")


# ------------------------------- piece page -------------------------------
def trim(t: str, n: int = 158) -> str:  # same as seo_commercial_pass.trim
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",;—- ") + "…"


def wall_alt(alt: str) -> str:  # same as seo_keywords_pass
    return alt if "wall art" in alt else alt + ", night landscape wall art print"


def meta_description(t: str, d: str) -> str:
    """Reproduces commercial pass -> keyword pass -> mural pass on <meta name=description>."""
    s = html.escape(trim(f"Buy {t} as a 12×18 poster ($35) or black framed print ($69), shipping included. {d}"), quote=True)
    s = re.sub(r"^Buy (.*?) as a 12×18 poster \(\$35\) or black framed print \(\$69\), shipping included\.",
               r"Moon poster wall art: buy \1 as a 12×18 art print poster ($35) or framed print ($69), shipping included.", s)
    return s.replace("shipping included.", "shipping included, or a $149 peel and stick wall mural (removable wallpaper).", 1)


def buy_block(slug: str, ind: str = "        ") -> str:
    st = stripe_for(slug)
    i2 = ind + "  "
    lines = [START, f'{ind}<section class="buy-box" id="buy">']
    if is_live(st.get("posterUrl")) and is_live(st.get("framedUrl")):
        mural = is_live(st.get("muralUrl"))
        lines += [
            f'{i2}<p class="price-line">{PRICE_LINE_MURAL if mural else PRICE_LINE}</p>',
            f'{i2}<div class="actions buy-actions">',
            f'{i2}  <a class="btn" data-buy="{slug}" data-sku="poster" href="{st["posterUrl"]}">Buy this print · Poster $35</a>',
            f'{i2}  <a class="btn secondary" data-buy="{slug}" data-sku="framed" href="{st["framedUrl"]}">Buy framed · $69</a>',
        ]
        if mural:
            lines.append(f'{i2}  <a class="btn secondary" data-buy="{slug}" data-sku="mural" href="{st["muralUrl"]}">Peel &amp; Stick Wall Mural · $149</a>')
        lines.append(f"{i2}</div>")
        lines.append(f'{i2}<p class="note">{PIECE_NOTE}</p>')
        if mural:
            lines.append(f"{i2}{MURAL_NOTE}")
    else:
        lines += [
            f'{i2}<p class="price-line">{PRICE_LINE}</p>',
            f'{i2}<p class="note">This window opens for orders soon.</p>',
            f'{i2}<p class="note">{PIECE_NOTE}</p>',
        ]
    lines += [f"{ind}</section>", f"{ind}{END}"]
    return "\n".join(lines)


def product_jsonld(piece: dict) -> str:
    t, d, slug = piece["title"], piece["description"], piece["slug"]
    page = page_url(slug)
    img = f"{BASE_URL}/assets/{piece['asset']}"
    sku = f"nw-{piece['photoNumber']:02d}-{slug}"
    ship = {"@type": "OfferShippingDetails",
            "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "USD"}}
    # seller = the LLC (Moonlit Windows is only a brand of Joshua Israel Ventures LLC)
    mw = {"@type": "Organization", "@id": f"{BASE_URL}/#org", "name": "Joshua Israel Ventures LLC", "url": f"{BASE_URL}/"}

    def offer(variant: str, name: str, price: str) -> dict:
        return {"@type": "Offer", "@id": f"{page}#offer-{variant}", "name": name, "price": price,
                "priceCurrency": "USD", "availability": "https://schema.org/InStock",
                "itemCondition": "https://schema.org/NewCondition", "url": page,
                "seller": mw, "shippingDetails": ship}

    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "@id": f"{page}#product",
                "name": f"{t} Wall Art Print (Poster or Framed Print, 12x18)",
                "description": (
                    f"{t} moonlit night landscape wall art from the Night Windows series, sold as a 12×18 art print "
                    f"poster ($35) or framed wall art print ($69), shipping included. A home decor print for living "
                    f"rooms and bedrooms. {d} Also available as a 4×6 ft peel and stick wall mural ($149): removable "
                    f"wallpaper, printed to order."
                ),
                "sku": sku,
                "mpn": sku,
                "category": "Home & Garden > Decor > Artwork > Posters, Prints, & Visual Artwork",
                "brand": {"@type": "Brand", "name": "Moonlit Windows"},
                "isPartOf": {"@type": "CreativeWorkSeries", "name": "Night Windows",
                             "url": f"{BASE_URL}/night-windows.html"},
                "image": [{"@type": "ImageObject", "@id": f"{page}#image", "url": img, "contentUrl": img,
                           "caption": piece["alt"], "name": t, "representativeOfPage": True}],
                "offers": [
                    offer("poster", f"{t} wall art poster 12x18", "35.00"),
                    offer("framed", f"{t} framed wall art print 12x18", "69.00"),
                    {"@type": "Offer", "@id": f"{page}#offer-mural",
                     "name": f"{t} peel and stick wall mural 4x6 ft (48x72 in), removable wallpaper",
                     "price": "149.00", "priceCurrency": "USD", "availability": "https://schema.org/InStock",
                     "itemCondition": "https://schema.org/NewCondition", "url": page, "shippingDetails": ship,
                     "seller": mw},
                ],
                "url": page,
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{page}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Night Windows", "item": f"{BASE_URL}/night-windows.html"},
                    {"@type": "ListItem", "position": 3, "name": t, "item": page},
                ],
            },
        ],
    }
    return '  <script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False) + "\n  </script>"


def related_para(slugs: list[str], tt: dict[str, str]) -> str:
    links = " · ".join(f'<a href="./{s}.html">{tt[s]}</a>' for s in slugs)
    return f'        <p class="note related-windows">More windows like this: {links}</p>'


def window_nav(slug: str) -> str:
    nxt = NEXT_BY_SLUG[slug]
    return f'        <p class="window-nav"><a class="btn secondary" href="./{nxt}.html">{NEXT_LABEL.get(nxt, "Next window")}</a></p>'


def piece_html(piece: dict, aw: int, ah: int, tt: dict[str, str]) -> str:
    slug, t, d = piece["slug"], piece["title"], piece["description"]
    t_esc = html.escape(t, quote=True)
    head_title = f"{t_esc} Poster, Framed Print &amp; Wall Mural | Moonlit Windows"
    social_desc = html.escape(f"{t}: Night Windows poster $35 · framed print $69 (12×18, shipping included). {d}", quote=True)
    dw, dh = (900, 1350) if ah >= aw else (900, 822)
    img = f"{BASE_URL}/assets/{piece['asset']}"
    alt = wall_alt(piece["alt"])
    collection = ""
    if slug in MOUNTAIN_COLLECTION:
        collection = ('        <p class="note collection-link" data-collection="mountain">Part of the '
                      '<a href="../mountain-wall-art.html">mountain wall art collection</a>: moonlit mountain '
                      'posters, framed prints and wall murals.</p>\n')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{GA_TAG}
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{head_title}</title>
  <meta property="og:site_name" content="Moonlit Windows" />
  <meta name="description" content="{meta_description(t, d)}" />
  <link rel="canonical" href="{page_url(slug)}" />
  <meta property="og:title" content="{head_title}" />
  <meta property="og:description" content="{social_desc}" />
  <meta property="og:url" content="{page_url(slug)}" />
  <meta property="og:image" content="{img}" />
  <meta property="og:image:alt" content="{alt}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{head_title}" />
  <meta name="twitter:description" content="{social_desc}" />
  <meta name="twitter:image" content="{img}" />
  <link rel="stylesheet" href="../styles.css" />
{product_jsonld(piece)}
</head>
<body>
  <div class="wrap">
    <header class="site-header">
      <a class="brand" href="../">Prompt <span>Framed</span></a>
      <nav class="nav">
        <a href="../#gallery">Gallery</a>
        <a href="../night-windows.html">The series</a>
        <a href="../buy.html">Shop Posters, Prints &amp; Wall Murals</a>
        <a href="../about.html">About</a>
        {IG}
      </nav>
    </header>
    <article class="piece">
      <img src="../assets/{piece['asset']}" width="{dw}" height="{dh}" alt="{alt}" />
      <div>
        <div class="kicker">Night Windows · {piece['photoNumber']:02d}</div>
        <h1>{t}</h1>
        <p class="sale-line">Moonlit wall art poster, framed print and peel &amp; stick wall mural for sale · $35 poster · $69 framed · 12×18 · $149 wall mural (4×6 ft) · shipping included · <a href="#buy">Buy now</a></p>
        <p class="desc">{d}</p>
        {buy_block(slug)}
        {MURALS_PIECE_LINK}
{window_nav(slug)}
{related_para(RELATED[slug], tt)}
{collection}        <p class="note"><a href="../night-windows.html">Browse the full Night Windows series</a> · Night Shade Art on Instagram: {IG}</p>
      </div>
    </article>
  </div>
  <footer class="site-footer"><div class="wrap"><div class="footer-shop"><a href="../buy.html">Shop Posters, Prints &amp; Wall Murals</a> · $35 poster · $69 framed · 12×18 · shipping included</div><div><a href="../">Back to gallery</a> · {IG}</div></div>  <div class="operated-by footer-legal"><p>© 2026 Joshua Israel Ventures LLC. All rights reserved. Moonlit Windows is owned and operated by Joshua Israel Ventures LLC.</p><p class="footer-legal-links"><a href="../terms.html">Terms</a> · <a href="../privacy.html">Privacy</a> · <a href="../disclaimer.html">Disclaimer</a> · <a href="../contact.html">Contact</a></p></div>
  </footer>
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "899375a6262144aabf5184589abd580c"}}'></script>
</body>
</html>
"""


def write_piece_page(piece: dict, aw: int, ah: int, tt: dict[str, str]) -> None:
    path = PIECES / f"{piece['slug']}.html"
    new = piece_html(piece, aw, ah, tt)
    if path.exists():
        # Keep related links other pages may have merged in since the first run.
        old = path.read_text(encoding="utf-8")
        m = re.search(r'<p class="note related-windows">.*?</p>', old)
        if m:
            extra = [s for s in re.findall(r'href="\./([a-z0-9-]+)\.html"', m.group(0)) if s not in RELATED[piece["slug"]]]
            if extra:
                new = new.replace(related_para(RELATED[piece["slug"]], tt), related_para(RELATED[piece["slug"]] + extra, tt))
        # Keep collection-link notes added by build_collection_*.py (lakes, coastal, ...) that this
        # template does not render itself, in their old order, right after the murals note.
        have = set(re.findall(r'<p class="note collection-link" data-collection="([a-z-]+)">', new))
        keep = [m.group(0) for m in re.finditer(r'<p class="note collection-link" data-collection="([a-z-]+)">.*?</p>', old)
                if m.group(1) not in have]
        if keep:
            anchor = re.search(r'(\n(\s*)<p class="note collection-link" data-collection="murals">.*?</p>)', new)
            if anchor:
                ins = "".join("\n" + anchor.group(2) + k for k in keep)
                new = new[:anchor.end()] + ins + new[anchor.end():]
    if write_if_changed(path, new, page_url(piece["slug"])):
        print(f"  piece page: pieces/{piece['slug']}.html")


# ------------------------------- index.html -------------------------------
def index_card(piece: dict, landscape: bool) -> str:
    wh = 'width="900" height="822"' if landscape else 'width="900" height="1350"'
    s = piece["slug"]
    return f"""      <article class="card{' landscape' if landscape else ''}">
        <a href="./pieces/{s}.html"><img src="./assets/{piece['asset']}" {wh} alt="{piece['alt']}" loading="lazy" /></a>
        <div class="meta">
          <h2><a href="./pieces/{s}.html">{piece['title']}</a></h2>
          <p>{piece['card_blurb']}</p>
          <p class="soft-cta"><a href="./pieces/{s}.html">Want a poster? Buy at the link.</a></p>
        </div>
      </article>"""


def card_re(slug: str, with_id: bool) -> re.Pattern:
    if with_id:
        return re.compile(rf'      <article class="card[^"]*" id="{re.escape(slug)}">.*?</article>', re.S)
    return re.compile(rf'      <article class="card[^"]*">\s*<a href="\./pieces/{re.escape(slug)}\.html">.*?</article>', re.S)


def keep_srcset(new_card: str, old_card: str) -> str:
    """Re-use the thumb-rewritten <img> head from an existing card (build_grid_thumbs output)."""
    m_old = re.search(r'<img src="\./assets/thumbs/[^"]+" srcset="[^"]+" sizes="[^"]+"(?: decoding="async")?', old_card)
    if not m_old:
        return new_card
    return re.sub(r'<img src="\./assets/[0-9][0-9]-[^"]+\.jpg"', lambda _: m_old.group(0), new_card, count=1)


def shop_itemlist(s: str, path_in_ld) -> str:
    m = re.search(r'(<script type="application/ld\+json" data-ld="shop">\n)(.*?)(\n  </script>)', s, re.S)
    if not m:
        die("shop JSON-LD not found")
    ld = json.loads(m.group(2))
    lst = path_in_ld(ld)
    have = {e["url"] for e in lst["itemListElement"]}
    for p in NEW_PIECES:
        u = page_url(p["slug"])
        if u not in have:
            lst["itemListElement"].append({"@type": "ListItem", "position": len(lst["itemListElement"]) + 1,
                                           "name": f"{p['title']} poster & framed print", "url": u})
    lst["numberOfItems"] = len(lst["itemListElement"])
    return s[: m.start(2)] + json.dumps(ld, indent=2, ensure_ascii=False) + s[m.end(2):]


def count_sub(s: str, old: str, new: str, label: str, expect_min: int = 1) -> str:
    if new in s and old not in s:
        return s
    n = s.count(old)
    if n < expect_min:
        die(f"{label}: pattern not found: {old!r}")
    return s.replace(old, new)


def update_index(meta: list[tuple[dict, bool]]) -> None:
    s = INDEX_PATH.read_text(encoding="utf-8")
    m = re.search(r'(<section id="gallery"[^>]*>)(.*?)(\n    </section>)', s, re.S)
    if not m:
        die("index.html: #gallery section not found")
    body = m.group(2)
    for piece, land in meta:
        card = index_card(piece, land)
        old = card_re(piece["slug"], False).search(body)
        if old:
            body = body[: old.start()] + keep_srcset(card, old.group(0)) + body[old.end():]
        else:
            body = body.rstrip() + "\n" + card
    s = s[: m.start(2)] + body + s[m.end(2):]
    s = count_sub(s, f"Shop {PREV_COUNT} moonlit night landscape", f"Shop {COUNT} moonlit night landscape", "index meta")
    s = count_sub(s, f"Choose from {PREV_COUNT} night scenes", f"Choose from {COUNT} night scenes", "index answer-first")
    s = shop_itemlist(s, lambda ld: next(g for g in ld["@graph"] if g["@type"] == "ItemList"))
    if write_if_changed(INDEX_PATH, s, f"{BASE_URL}/"):
        print("  index.html: cards + meta + shop ItemList")


# ------------------------------- buy.html -------------------------------
def buy_card(piece: dict, landscape: bool) -> str:
    s = piece["slug"]
    st = stripe_for(s)
    ind = "          "
    lines = [
        f'      <article class="card{" landscape" if landscape else ""}" id="{s}">',
        f'        <a href="./pieces/{s}.html"><img src="./assets/{piece["asset"]}" alt="{html.escape(piece["title"])} wall art poster and framed print" loading="lazy"></a>',
        '        <div class="meta">',
        f"{ind}<h2>{html.escape(piece['title'])}</h2>",
        f"{ind}<p>{piece['description']}</p>",
    ]
    if is_live(st.get("posterUrl")) and is_live(st.get("framedUrl")):
        mural = is_live(st.get("muralUrl"))
        lines += [
            f'{ind}<p class="price-line">{PRICE_LINE_MURAL if mural else PRICE_LINE}</p>',
            f'{ind}<div class="actions buy-actions">',
            f'{ind}  <a class="btn" data-buy="{s}" data-sku="poster" href="{st["posterUrl"]}">Buy this print · Poster $35</a>',
            f'{ind}  <a class="btn secondary" data-buy="{s}" data-sku="framed" href="{st["framedUrl"]}">Buy framed · $69</a>',
        ]
        if mural:
            lines.append(f'{ind}  <a class="btn secondary" data-buy="{s}" data-sku="mural" href="{st["muralUrl"]}">Peel &amp; Stick Wall Mural · $149</a>')
        lines.append(f"{ind}</div>")
    else:
        lines += [f'{ind}<p class="price-line">{PRICE_LINE}</p>', f'{ind}<p class="note">This window opens for orders soon.</p>']
    lines += ["        </div>", "      </article>"]
    return "\n".join(lines)


def update_buy(meta: list[tuple[dict, bool]]) -> None:
    s = BUY_PATH.read_text(encoding="utf-8")
    if END not in s:
        die("buy.html missing buy:end marker")
    for piece, land in meta:
        card = buy_card(piece, land)
        old = card_re(piece["slug"], True).search(s)
        if old:
            s = s[: old.start()] + keep_srcset(card, old.group(0)) + s[old.end():]
        else:
            s = s.replace("\n      " + END, "\n" + card + "\n      " + END, 1)
    # meta / og / twitter descriptions (3x) + place names
    s = count_sub(s, f"wall art: {PREV_COUNT} night landscape art prints", f"wall art: {COUNT} night landscape art prints", "buy meta", 3)
    s = count_sub(s, f"Buy any of the {PREV_COUNT} Night Windows", f"Buy any of the {COUNT} Night Windows", "buy sale-line")
    if BUY_META_TAIL_OLD in s:
        s = s.replace(BUY_META_TAIL_OLD, BUY_META_TAIL_NEW)
    # hero paragraph right after the hero sale-line
    s, n = re.subn(r'(<section class="hero left">.*?<p class="sale-line">[^\n]*</p>\n      <p>)[^<]*(</p>)',
                   lambda m: m.group(1) + BUY_HERO + m.group(2), s, count=1, flags=re.S)
    if not n:
        die("buy.html hero paragraph not found")
    s = shop_itemlist(s, lambda ld: next(g for g in ld["@graph"] if g["@type"] == "CollectionPage")["mainEntity"])
    if write_if_changed(BUY_PATH, s, f"{BASE_URL}/buy.html"):
        print("  buy.html: cards + hero + meta + shop ItemList")


# ------------------------------- next / related -------------------------------
def update_prev_next() -> None:
    path = PIECES / f"{PREV_LAST}.html"
    s = path.read_text(encoding="utf-8")
    first = NEW_SLUGS[0]
    new, n = re.subn(r'<p class="window-nav"><a class="btn secondary" href="\./moonlit-alpine-meadow\.html">First window</a></p>',
                     f'<p class="window-nav"><a class="btn secondary" href="./{first}.html">Next window</a></p>', s)
    if n == 0 and f'href="./{first}.html">Next window' not in s:
        die(f"could not repoint Next window on {path.name}")
    if write_if_changed(path, new, page_url(PREV_LAST)):
        print(f"  {PREV_LAST}: Next window -> {first}")


def update_related_backlinks(tt: dict[str, str]) -> None:
    back: dict[str, list[str]] = {}
    for new_slug, olds in RELATED.items():
        for old in olds:
            back.setdefault(old, []).append(new_slug)
    for old, news in back.items():
        path = PIECES / f"{old}.html"
        s = path.read_text(encoding="utf-8")
        m = re.search(r"\n        <p class=\"note related-windows\">.*?</p>", s)
        existing = re.findall(r'href="\./([a-z0-9-]+)\.html"', m.group(0)) if m else []
        slugs = existing + [x for x in news if x not in existing]
        para = "\n" + related_para(slugs, tt)
        if m:
            new = s[: m.start()] + para + s[m.end():]
        else:
            # Put it after the window-nav / Next link (outside buy:start/end), before
            # collection-link or the "Browse the full series" note.
            anchor = re.search(r'\n        <p class="note collection-link"|\n        <p class="note"><a href="\.\./night-windows\.html">', s)
            if not anchor:
                die(f"no insertion point for related links in {path.name}")
            new = s[: anchor.start()] + para + s[anchor.start():]
        if write_if_changed(path, new, page_url(old)):
            print(f"  related: {old} -> {', '.join(slugs)}")


# ------------------------------- series hub -------------------------------
def update_series_hub(tt: dict[str, str]) -> None:
    s = SERIES_PATH.read_text(encoding="utf-8")

    def link(slug: str, text: str) -> str:
        return f'<a href="./pieces/{slug}.html">{text}</a>'

    def oxford(parts: list[str]) -> str:
        return ", ".join(parts[:-1]) + ", and " + parts[-1] if len(parts) > 1 else parts[0]

    # meta descriptions (3x)
    s = count_sub(s, f"The Night Windows series: {PREV_COUNT} moonlit", f"The Night Windows series: {COUNT} moonlit", "hub meta", 3)
    if HUB_META_TAIL_OLD in s:
        s = s.replace(HUB_META_TAIL_OLD, HUB_META_TAIL_NEW)
    # intro + count line
    s, n = re.subn(r"<p>Windows into places you wish you were\.[^<]*</p>", lambda _: f"<p>{HUB_INTRO}</p>", s, count=1)
    if not n:
        die("hub intro not found")
    s = re.sub(r"<p>[A-Z][a-z-]+ windows so far\.", f"<p>{COUNT_WORD_CAP} windows so far.", s, count=1)
    # ordered list
    m = re.search(r'(<ol class="series-list">\n)(.*?)(\n    </ol>)', s, re.S)
    items = m.group(2)
    for p in NEW_PIECES:
        if f'./pieces/{p["slug"]}.html"' not in items:
            items += f'\n      <li><a href="./pieces/{p["slug"]}.html">{p["title"]}</a></li>'
    s = s[: m.start(2)] + items + s[m.end(2):]
    # ItemList JSON-LD (first, unlabelled ld+json block)
    m = re.search(r'(<script type="application/ld\+json">\n)(.*?)(\n  </script>)', s, re.S)
    ld = json.loads(m.group(2))
    lst = ld["mainEntity"]
    have = {e["url"] for e in lst["itemListElement"]}
    for p in NEW_PIECES:
        if page_url(p["slug"]) not in have:
            lst["itemListElement"].append({"@type": "ListItem", "position": len(lst["itemListElement"]) + 1,
                                           "name": p["title"], "url": page_url(p["slug"])})
    lst["numberOfItems"] = len(lst["itemListElement"])
    s = s[: m.start(2)] + json.dumps(ld, indent=2, ensure_ascii=False) + s[m.end(2):]
    # new drop line
    new_drop = oxford([link(p["slug"], p["title"]) for p in NEW_PIECES])
    s, n = re.subn(r"<p>New this drop: .*?</p>", lambda _: f"<p>New this drop: {new_drop}.</p>", s, count=1)
    if not n:
        die("hub 'New this drop' not found")
    # themes
    themes = "\n".join(f"    <p>{label}: {oxford([link(x, t) for x, t in links])}.{suffix}</p>" for label, links, suffix in HUB_THEMES)
    s, n = re.subn(r"(<h2>Find your window</h2>\n)(.*?)(\n    <p>Follow Night Shade Art)",
                   lambda m: m.group(1) + themes + m.group(3), s, count=1, flags=re.S)
    if not n:
        die("hub themes block not found")
    if write_if_changed(SERIES_PATH, s, f"{BASE_URL}/night-windows.html"):
        print(f"  night-windows.html: {COUNT} pieces, intro, list, ItemList, new drop, themes")


def update_mountain_page() -> None:
    if not MOUNTAIN_PATH.exists():
        return
    s = MOUNTAIN_PATH.read_text(encoding="utf-8")
    new = s.replace(f"all {PREV_COUNT_WORD} Night Windows</a>", f"all {COUNT_WORD} Night Windows</a>")
    if write_if_changed(MOUNTAIN_PATH, new, f"{BASE_URL}/mountain-wall-art.html"):
        print("  mountain-wall-art.html: series count")


def update_about_llms() -> None:
    """Series counts in about.html (answer-first paragraph) and llms.txt."""
    pairs = {
        ROOT / "about.html": (f"{BASE_URL}/about.html",
                              [(f"a series of {PREV_COUNT} moonlit", f"a series of {COUNT} moonlit")]),
        ROOT / "llms.txt": (f"{BASE_URL}/llms.txt",
                            [(f"a series of {PREV_COUNT} moonlit", f"a series of {COUNT} moonlit"),
                             (f"Gallery of all {PREV_COUNT} Night Windows", f"Gallery of all {COUNT} Night Windows"),
                             (f"index of all {PREV_COUNT} pieces", f"index of all {COUNT} pieces")]),
    }
    for path, (url, subs) in pairs.items():
        if not path.exists():
            continue
        s = path.read_text(encoding="utf-8")
        new = s
        for old, rep_ in subs:
            if old in new:
                new = new.replace(old, rep_)
            elif rep_ not in new:
                print(f"  WARN {path.name}: count text not found: {old!r}")
        if write_if_changed(path, new, url):
            print(f"  {path.name}: series count {COUNT}")


# ------------------------------- IndexNow -------------------------------
URLS_FILE = Path(__import__("os").environ.get("PUBLISH_71_75_URLS", "/workspace/promptframed-private/publish_71_75_urls.json"))
INDEXNOW = Path("/workspace/promptframed-private/indexnow_ping.py")


def save_urls() -> None:
    new = [page_url(s) for s in NEW_SLUGS]
    changed = set(CHANGED_URLS) | {f"{BASE_URL}/sitemap.xml"} | set(new)
    if URLS_FILE.exists():  # a re-run (e.g. after Stripe links land) keeps today's earlier URLs
        try:
            prev = load_json(URLS_FILE)
            if prev.get("date") == TODAY:
                changed |= set(prev.get("changed", []))
        except (OSError, ValueError):
            pass
    changed = sorted(changed)
    try:
        URLS_FILE.write_text(json.dumps({"date": TODAY, "new": new, "changed": changed}, indent=2) + "\n", encoding="utf-8")
        print(f"  IndexNow list: {len(changed)} URL(s) saved to {URLS_FILE}")
    except OSError as e:
        print(f"  WARN could not save IndexNow list: {e}")


def ping_indexnow() -> int:
    """--ping: run AFTER git commit + push. Waits for the new piece pages to go live, then pings IndexNow."""
    import subprocess, time, urllib.request
    if not URLS_FILE.exists():
        die(f"{URLS_FILE} not found: run the publish step first")
    data = load_json(URLS_FILE)
    pending = list(data["new"])
    deadline = time.time() + 600
    while pending and time.time() < deadline:
        still = []
        for u in pending:
            try:
                code = urllib.request.urlopen(urllib.request.Request(f"{u}?nc={int(time.time())}", method="HEAD"), timeout=20).status
            except Exception:
                code = 0
            if code != 200:
                still.append(u)
        pending = still
        if pending:
            time.sleep(15)
    if pending:
        die(f"not live after 10 min, IndexNow NOT pinged: {pending}")
    print(f"live: {len(data['new'])} new page(s); pinging {len(data['changed'])} URL(s)")
    r = subprocess.run([sys.executable, str(INDEXNOW), *data["changed"]], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    print(out)
    return 0 if re.search(r"IndexNow 20[02]\b", out) else 1


# ------------------------------- sitemap -------------------------------
def update_sitemap() -> None:
    xml = SITEMAP_PATH.read_text(encoding="utf-8")
    added = 0
    for p in NEW_PIECES:
        loc = page_url(p["slug"])
        if f"<loc>{loc}</loc>" in xml:
            continue
        entry = f"  <url><loc>{loc}</loc></url>\n"
        anchor = f"  <url><loc>{BASE_URL}/mountain-wall-art.html</loc>"
        xml = xml.replace(anchor, entry + anchor, 1) if anchor in xml else xml.replace("</urlset>", entry + "</urlset>", 1)
        added += 1
    SITEMAP_PATH.write_text(xml, encoding="utf-8")
    import seo_image_sitemap  # converts plain new entries to image entries (watermarked assets only)
    seo_image_sitemap.main()
    xml = SITEMAP_PATH.read_text(encoding="utf-8")
    for url in sorted(CHANGED_URLS):
        xml = re.sub(rf"(<loc>{re.escape(url)}</loc>)(<lastmod>[^<]*</lastmod>)?", rf"\g<1><lastmod>{TODAY}</lastmod>", xml)
    SITEMAP_PATH.write_text(xml, encoding="utf-8")
    print(f"  sitemap.xml: added {added} URL(s); lastmod {TODAY} on {len(CHANGED_URLS)} page(s)")


# ------------------------------- verification -------------------------------
def verify() -> int:
    """Read-only structural checks against the reference page (piece 70, PREV_LAST)."""
    problems: list[str] = []
    ref = (PIECES / f"{PREV_LAST}.html").read_text(encoding="utf-8")

    def skeleton(t: str) -> list[str]:
        t = re.sub(r'\n\s*<p class="note collection-link".*?</p>', "", t)
        return re.findall(r"<(?:meta|link|script|p|div|a|section|article|nav|header|footer|h1|img)\b[^>]*?(?:class|property|name|rel|type|data-sku)=\"([^\"]+)\"", t)

    for p in NEW_PIECES:
        path = PIECES / f"{p['slug']}.html"
        if not path.exists():
            problems.append(f"missing page {path.name}")
            continue
        t = path.read_text(encoding="utf-8")
        for needle in ["operated-by", "Shop Posters, Prints &amp; Wall Murals", 'class="footer-shop"', 'class="sale-line"',
                       "#offer-mural", START, END, 'class="window-nav"', 'class="note related-windows"',
                       "Poster, Framed Print &amp; Wall Mural | Moonlit Windows", 'og:site_name']:
            if needle not in t:
                problems.append(f"{path.name}: missing {needle}")
        for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', t, re.S):
            json.loads(m.group(1))
        if re.search(BANNED, re.sub(r"<script.*?</script>", "", t, flags=re.S)):
            problems.append(f"{path.name}: banned word in visible HTML")
        if "TODO" in t:
            problems.append(f"{path.name}: TODO copy")
        if "print-masters" in t or re.search(r'gallery/[0-9][0-9]-[^"]*\.png', t):
            problems.append(f"{path.name}: references a clean master")
        st = stripe_for(p["slug"])
        live = all(is_live(st.get(k)) for k in ("posterUrl", "framedUrl", "muralUrl"))
        if live and skeleton(t) != skeleton(ref):
            problems.append(f"{path.name}: structure differs from {PREV_LAST}.html")
        if not live:
            problems.append(f"{p['slug']}: Stripe poster/framed/mural links not live yet (buy block shows 'soon')")
        for f in [ASSETS / p["asset"], GALLERY / "social" / p["asset"], ASSETS / "thumbs" / p["asset"]]:
            if not f.exists():
                problems.append(f"missing public preview {f.relative_to(ROOT)}")
    for page in [INDEX_PATH, BUY_PATH, SERIES_PATH]:
        t = page.read_text(encoding="utf-8")
        for p in NEW_PIECES:
            if f"./pieces/{p['slug']}.html" not in t:
                problems.append(f"{page.name}: no link to {p['slug']}")
        for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', t, re.S):
            json.loads(m.group(1))
        if "TODO" in t:
            problems.append(f"{page.name}: TODO copy")
    sm = SITEMAP_PATH.read_text(encoding="utf-8")
    import xml.dom.minidom
    xml.dom.minidom.parseString(sm.encode())
    for p in NEW_PIECES:
        if f"<image:loc>{BASE_URL}/assets/{p['asset']}</image:loc>" not in sm:
            problems.append(f"sitemap: no image entry for {p['slug']}")
    cat = load_json(CATALOG_PATH)
    leaked = [e.get("slug") for e in cat if any(k in e for k in PRIVATE_FIELDS)]
    if leaked:
        problems.append(f"catalog.json: private fields (source/stylePrompt) on {len(leaked)} row(s)")
    if re.search(r"\bAI\b|ChatGPT|Higgsfield|OpenAI|DALL|Midjourney", json.dumps(cat, ensure_ascii=False), re.I):
        problems.append("catalog.json: banned word")
    n_prod = len(load_json(PRODUCTS_PATH))
    if n_prod != COUNT:
        problems.append(f"products.json has {n_prod} rows, expected {COUNT}")
    for line in problems:
        print("  ! " + line)
    print(f"verify: {len(problems)} issue(s)")
    return 1 if problems else 0


def main() -> int:
    print(f"Repo: {ROOT}")
    if "--check" in sys.argv:
        return verify()
    if "--ping" in sys.argv:
        return ping_indexnow()
    check_copy()
    check_pngs()
    meta: list[tuple[dict, bool]] = []
    for piece in NEW_PIECES:
        print(f"\n== {piece['id']} ==")
        mw, mh, aw, ah = export_images(piece)
        append_catalog(piece, mw, mh)
        append_products(piece)
        meta.append((piece, aw > ah))
    tt = titles()
    from PIL import Image
    for piece, _land in meta:
        with Image.open(ASSETS / piece["asset"]) as im:
            aw, ah = im.size
        write_piece_page(piece, aw, ah, tt)

    print("\n== site updates ==")
    update_index(meta)
    update_buy(meta)
    update_prev_next()
    update_related_backlinks(tt)
    update_series_hub(tt)
    update_mountain_page()
    update_about_llms()
    update_sitemap()
    save_urls()
    import build_grid_thumbs  # watermarked 600px thumbs + srcset for the new grid cards
    made = build_grid_thumbs.build_thumbs()
    pages = [p for p in build_grid_thumbs.PAGES if build_grid_thumbs.rewrite(p)]
    print(f"  grid thumbs: built {made}; srcset added on {pages or 'none'}")
    print()
    verify()
    print("\nNo git commit/push done. Stripe untouched.")
    print("After commit + push, run: python3 scripts/publish_pieces_71_75.py --ping  (waits for deploy, then IndexNow)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
