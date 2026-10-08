#!/usr/bin/env python3
"""Build peel-and-stick-wall-murals.html: a buyer-intent collection page for the $149
4x6 ft (48x72 in) peel and stick wall mural, and wire internal links to it. Idempotent.

Modelled on build_collection_mountain.py. Cards reuse the live Stripe links from products.json
(stripe.muralUrl / posterUrl / framedUrl) and the card blurbs already on buy.html. Images are the
public watermarked previews (assets/thumbs + assets), never .png masters or print-masters.
Every product fact matches products.json, the piece pages' mural note, how-it-works.html,
guide-print-sizes.html, terms.html and disclaimer.html.

  python3 scripts/build_collection_murals.py          # write page + wire links + sitemap/llms.txt
  python3 scripts/build_collection_murals.py --check  # dry run: exit 1 if anything would change
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = "--check" in sys.argv
FILE = "peel-and-stick-wall-murals.html"
PAGE = ROOT / FILE
SITE = "https://moonlitwindows.com"
URL = f"{SITE}/{FILE}"
TODAY = "2026-10-08"
OG_SLUG = "dolomites-tre-cime-moon"
MARK = 'data-collection="murals"'

# Only pieces composed in the 2:3 proportion of the 48x72 in mural (1024x1536 previews).
GROUPS = [
    ("mountains", "Mountain wall murals", "Tall peaks suit a tall panel, with the summit high on the wall and the valley, lake or meadow below.", [
        ("matterhorn-alpine-moon", "The Matterhorn above a still alpine lake and wildflower meadow under moonlight"),
        ("dolomites-tre-cime-moon", "The three peaks of Tre Cime over a meadow with a lit mountain hut and a full moon"),
        ("mount-fuji-pagoda-moon", "Mount Fuji under a full moon behind the red Chureito Pagoda and cherry blossoms"),
        ("yosemite-half-dome-moon", "Half Dome rising through valley mist above the moonlit Merced River in Yosemite"),
        ("isle-of-skye-storr-moon", "The Old Man of Storr above green Isle of Skye slopes and lochans under a full moon"),
    ]),
    ("lakes-waterfalls", "Lake and waterfall wall murals", "Water scenes are the calmest choice for a bedroom wall: still reflections, falling water and soft mist.", [
        ("banff-lake-louise-moon", "Turquoise Lake Louise mirroring snowy Rocky Mountain peaks under moonlight"),
        ("lake-bled-island-moon", "Lake Bled’s island church and clifftop castle on the moonlit lake"),
        ("hallstatt-lake-moon", "Hallstatt’s church steeple and lit houses reflected in a still alpine lake at night"),
        ("lauterbrunnen-valley-moon", "Staubbach Falls pouring into the Lauterbrunnen valley with lit chalets and snowy Alps"),
        ("iguazu-falls-moon", "Tiers of Iguazu waterfalls falling into a misty rainforest gorge under a full moon"),
        ("plitvice-lakes-moon", "Plitvice’s turquoise lakes and terraced falls with a lit boardwalk through the forest"),
    ]),
    ("coasts", "Coastal and fjord wall murals", "Cliffs, harbours and sea light for a living room or a hallway you want to open up.", [
        ("santorini-caldera-moon", "Whitewashed Santorini terraces and blue domes above the moonlit caldera"),
        ("cinque-terre-manarola-moon", "Manarola’s pastel cliffside houses with lit windows above a moonlit sea"),
        ("faroe-gasadalur-moon", "Múlafossur waterfall dropping from green sea cliffs at Gásadalur under a full moon"),
        ("lofoten-reine-moon", "Red fishing cabins along a still Lofoten fjord below jagged peaks and a full moon"),
    ]),
    ("forests", "Forest wall murals", "Vertical trunks and stone pillars that fill a tall panel naturally.", [
        ("kyoto-bamboo-moon", "A Kyoto bamboo grove path softened by mist and filtered moonlight"),
        ("zhangjiajie-pillars-moon", "Zhangjiajie’s sandstone pillars rising through forest mist at night"),
    ]),
    ("castles", "Castle wall murals", "Storybook landmarks for a child’s room, a reading corner or a dramatic end wall.", [
        ("neuschwanstein-castle-moon", "Neuschwanstein Castle’s white towers on a forested crag under a full moon"),
        ("mont-saint-michel-moon", "Mont Saint-Michel abbey rising from silver tidal water under moonlight"),
    ]),
]
SLUGS = [s for _, _, _, items in GROUPS for s, _ in items]
N = len(SLUGS)

TITLE = "Peel and Stick Wall Murals: Moonlit Landscape Murals, $149 | Moonlit Windows"
DESC = (f"Peel and stick wall murals, $149: {N} moonlit mountain, lake, waterfall, coast and castle scenes "
        "as 4×6 ft (48×72 in) removable wallpaper murals. Printed to order, shipping included.")
H1 = "Peel and Stick Wall Murals: Moonlit Landscapes for a Feature Wall"

# Visible FAQ; the FAQPage JSON-LD is rendered from this same list (plain text answers).
FAQ = [
    ("How big is the wall mural?",
     "4×6 ft (48×72 in), in a tall format: 48 inches wide and 72 inches high. Every piece is offered in this one mural size for $149, shipping included."),
    ("What is it made of, and do I need paste?",
     "It is printed on removable peel-and-stick polyester, so no paste or glue is needed. It removes cleanly from most smooth painted walls."),
    ("How long does it take to arrive?",
     "Each mural is printed to order after checkout and ships by post in 1–2 weeks."),
    ("Will the watermark be on my mural?",
     "No. The previews on this site carry a small Night Shade Art watermark to discourage copying; your mural is printed from a clean file without it."),
    ("What if it arrives damaged or misprinted?",
     "Email joshuaofisrael@gmail.com within 30 days of delivery with your order details and a photo of the problem, and we will replace it or refund it."),
    ("Is there a smaller size?",
     "The mural comes in one size. For a smaller wall, every piece is also sold as a 12×18 in poster ($29) or the same print in a black frame ($69)."),
    ("How do I pay?",
     "Every button opens secure Stripe checkout, and your receipt arrives by email."),
]

def blurbs():
    b = (ROOT / "buy.html").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<article class="(card[^"]*)" id="([^"]+)">.*?\.jpg (\d+)w".*?<h2>.*?</h2>\s*<p>(.*?)</p>', b, re.S):
        out[m.group(2)] = (m.group(1), m.group(3), m.group(4))
    return out

def card(it, alt, info):
    cls, w, blurb = info
    s, t, st, a = it["slug"], html.escape(it["title"]), it["stripe"], it["asset"]
    return f'''      <article class="{cls}" id="{s}">
        <a href="./pieces/{s}.html"><img src="./assets/thumbs/{a}" srcset="./assets/thumbs/{a} 600w, ./assets/{a} {w}w" sizes="(max-width: 640px) 92vw, (max-width: 1100px) 45vw, 22rem" decoding="async" alt="{html.escape(alt)}, {t} peel and stick wall mural design" loading="lazy"></a>
        <div class="meta">
          <h3><a href="./pieces/{s}.html">{t}</a></h3>
          <p>{blurb}</p>
          <p class="price-line">$149 peel &amp; stick wall mural (4×6 ft) · or $29 poster · $69 framed (12×18)</p>
          <div class="actions buy-actions">
            <a class="btn" data-buy="{s}" data-sku="mural" href="{st['muralUrl']}">Wall mural · $149</a>
            <a class="btn secondary" data-buy="{s}" data-sku="poster" href="{st['posterUrl']}">Poster · $29</a>
            <a class="btn secondary" data-buy="{s}" data-sku="framed" href="{st['framedUrl']}">Framed · $69</a>
          </div>
        </div>
      </article>'''

def ld(items):
    g = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Peel and Stick Wall Murals: Moonlit Landscape Murals",
         "url": URL, "description": DESC,
         "isPartOf": {"@type": "WebSite", "name": "Moonlit Windows", "url": SITE + "/"},
         "publisher": {"@type": "Organization", "@id": SITE + "/#org", "name": "Joshua Israel Ventures LLC", "url": SITE + "/",
                       "legalName": "Joshua Israel Ventures LLC",
                       "brand": {"@type": "Brand", "name": "Moonlit Windows", "alternateName": ["Night Shade Art", "Night Windows", "Prompt Framed"]}},
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": f"{it['title']} peel and stick wall mural (4×6 ft)",
              "url": f"{SITE}/pieces/{it['slug']}.html"} for i, it in enumerate(items)]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Shop", "item": SITE + "/buy.html"},
            {"@type": "ListItem", "position": 3, "name": "Peel and Stick Wall Murals", "item": URL}]}]}
    return json.dumps(g, ensure_ascii=False, indent=2)

def faq_ld():
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False, indent=2)

def faq_html():
    out = []
    for q, a in FAQ:
        a = html.escape(a, quote=False).replace("joshuaofisrael@gmail.com", '<a href="mailto:joshuaofisrael@gmail.com">joshuaofisrael@gmail.com</a>')
        out.append(f"      <p><strong>{html.escape(q, quote=False)}</strong> {a}</p>")
    return "\n".join(out)

def page(by_slug, bl):
    sections = []
    for gid, head, intro, items in GROUPS:
        cards = "\n".join(card(by_slug[s], alt, bl[s]) for s, alt in items)
        sections.append(f'''    <h2 id="{gid}">{head}</h2>
    <p class="note">{intro}</p>
    <section class="grid" aria-label="{head}">
{cards}
    </section>''')
    grids = "\n\n".join(sections)
    sel = [by_slug[s] for s in SLUGS]
    og_item = by_slug[OG_SLUG]
    og = f"{SITE}/assets/{og_item['asset']}"
    T = TITLE.replace("&", "&amp;")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-663R8VD62L"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-663R8VD62L');</script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{T}</title>
  <meta name="description" content="{DESC}" />
  <link rel="canonical" href="{URL}">
  <meta property="og:site_name" content="Moonlit Windows" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{T}" />
  <meta property="og:description" content="{DESC}" />
  <meta property="og:url" content="{URL}">
  <meta property="og:image" content="{og}" />
  <meta property="og:image:alt" content="{og_item['title']} peel and stick wall mural design" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{T}" />
  <meta name="twitter:description" content="{DESC}" />
  <meta name="twitter:image" content="{og}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=Outfit:wght@380;560;650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json" data-ld="collection-murals">
{ld(sel)}
  </script>
  <script type="application/ld+json" data-ld="faq-murals">
{faq_ld()}
  </script>
</head>
<body data-products="products.json">
  <div class="wrap">
    <header class="site-header">
      <a class="brand" href="./"><span class="brand-series">Night Windows</span><span class="brand-studio">Prompt Framed</span></a>
            <nav class="nav" aria-label="Primary">
        <a href="./#gallery">Gallery</a>
        <a href="./night-windows.html">The series</a>
        <a href="./buy.html">Shop Posters, Prints &amp; Wall Murals</a>
        <a href="./guide-print-sizes.html">Print sizes</a>
        <a href="./how-it-works.html">How it works</a>
        <a href="./about.html">About</a>
        <a href="./contact.html">Contact</a>
        <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a>
      </nav>
    </header>
    <p class="note breadcrumb"><a href="./">Home</a> › <a href="./buy.html">Shop</a> › Peel and stick wall murals</p>
    <section class="hero left">
      <div class="kicker">Collection</div>
      <h1>{H1}</h1>
      <p class="sale-line">{N} wall mural designs · $149 peel &amp; stick wall mural · 4×6 ft (48×72 in) · removable · printed to order · shipping included</p>
      <p class="answer-first">Every Night Windows piece can be ordered as a 4×6 ft (48×72 in) peel and stick wall mural for $149, shipping included. It is printed to order on removable peel-and-stick polyester, needs no paste, removes cleanly from most smooth painted walls, and ships by post in 1–2 weeks. The {N} scenes below are the ones that work best at wall size: mountains, lakes and waterfalls, coasts, forests and castles, all under a full moon.</p>
      <p>The mural is a tall panel, 48 inches wide by 72 inches high, and each piece here is composed in that same tall 2:3 proportion, so the scene reads like a window cut into the wall: a peak at the top, a lit village, lake or path below. If you would rather hang a print, every design is also a 12×18 in poster ($29) or a black-framed print ($69).</p>
      <p class="note">Jump to: <a href="#mountains">Mountains</a> · <a href="#lakes-waterfalls">Lakes &amp; waterfalls</a> · <a href="#coasts">Coasts &amp; fjords</a> · <a href="#forests">Forests</a> · <a href="#castles">Castles</a> · <a href="#measure">How to measure</a> · <a href="#faq">FAQ</a></p>
    </section>

{grids}

    <section class="prose">
      <h2 id="measure">How to measure your wall for a 4×6 ft mural</h2>
      <p>The mural covers an area 48 inches (4 ft) wide and 72 inches (6 ft) high. Before you order, check that the wall has that much clear, smooth painted surface, with no switches, sockets, vents or trim inside the area.</p>
      <ul>
        <li><strong>Mark it out first.</strong> Use low-tack painter’s tape to outline a 48×72 in rectangle where the mural will go. Live with the outline for a day and look at it from the doorway and from where you sit.</li>
        <li><strong>Check the height.</strong> On a wall with a standard 8 ft (96 in) ceiling, a 72 in mural leaves 24 inches to split between the floor and the ceiling. Starting it just above a baseboard or headboard usually looks most deliberate.</li>
        <li><strong>Check the width.</strong> At 48 inches, the mural is narrower than a queen bed (60 in) or a typical sofa, so it reads as a tall, centred panel, like a window, rather than wall-to-wall wallpaper.</li>
      </ul>

      <h2>Which wall suits a 4×6 ft mural?</h2>
      <p><strong>Behind a bed.</strong> Centred above a headboard, a tall mural becomes the view from the pillow. The lake scenes (<a href="./pieces/banff-lake-louise-moon.html">Lake Louise</a>, <a href="./pieces/hallstatt-lake-moon.html">Hallstatt</a>, <a href="./pieces/lake-bled-island-moon.html">Lake Bled</a>) are the calmest choice for a bedroom.</p>
      <p><strong>A narrow wall or alcove.</strong> The space between two windows or doors, a nook beside a fireplace, or the end wall of a hallway is often close to four feet wide: exactly where a 48 in mural fits without crowding.</p>
      <p><strong>Behind a desk or in a reading corner.</strong> A tall mountain such as the <a href="./pieces/matterhorn-alpine-moon.html">Matterhorn</a> or <a href="./pieces/mount-fuji-pagoda-moon.html">Mount Fuji</a> gives a home office a backdrop that looks good on video calls.</p>
      <p><strong>A child’s room.</strong> Castles like <a href="./pieces/neuschwanstein-castle-moon.html">Neuschwanstein</a> and <a href="./pieces/mont-saint-michel-moon.html">Mont Saint-Michel</a> feel like storybook settings, and a peel-and-stick mural can come down when tastes change.</p>
      <p>Moonlit scenes are deep blue by nature. Walls that get good daylight or warm lamp light in the evening show them best; in a very dark corner, a lighter scene such as <a href="./pieces/santorini-caldera-moon.html">Santorini</a> or <a href="./pieces/cinque-terre-manarola-moon.html">Manarola</a> reads more clearly.</p>

      <h2>Wall prep, hanging and removal</h2>
      <p>These are general tips for peel-and-stick wall murals on painted walls:</p>
      <ul>
        <li><strong>Start with a smooth, clean, dry wall.</strong> Wipe off dust and grease and let the wall dry fully. Peel-and-stick materials hold best on smooth painted surfaces; heavily textured, damp, or already-wallpapered walls are not a good fit. If you have just painted, wait until the paint has fully cured.</li>
        <li><strong>Work from the top down.</strong> Draw a light pencil guideline with a level, peel back a short section of the backing at the top, line up the top edge, and smooth outward from the centre as you go, peeling the backing a little at a time.</li>
        <li><strong>Take it down slowly.</strong> To remove it, lift a top corner and peel back slowly at a low angle. The mural is made to remove cleanly from most smooth painted walls.</li>
      </ul>

      <h2>Wall mural, framed print or poster?</h2>
      <ul>
        <li><strong>Peel &amp; stick wall mural · $149.</strong> 4×6 ft (48×72 in) on removable polyester. Choose it when you want the scene to fill a wall and be seen from across the room.</li>
        <li><strong>Framed print · $69.</strong> 12×18 in in a black frame, ready to hang above a nightstand, desk or shelf.</li>
        <li><strong>Poster · $29.</strong> The same 12×18 in print on enhanced matte paper, for your own frame or a gallery wall of several pieces.</li>
      </ul>
      <p>All three include shipping and are printed to order. A wall-size print is meant to be seen from a few steps back; pressed close, fine detail is softer than on a 12×18 print, as with any image printed at wall size. The <a href="./guide-print-sizes.html">size guide</a> compares the formats in more detail, and <a href="./how-it-works.html">how it works</a> explains checkout and delivery.</p>
    </section>

    <section class="prose" id="faq">
      <h2>Wall mural questions</h2>
{faq_html()}
      <p>Looking for something else? Browse <a href="./mountain-wall-art.html">mountain wall art</a>, <a href="./night-windows.html">all fifty Night Windows</a> or the <a href="./buy.html">full shop</a>, where every piece has a wall mural button.</p>
    </section>
  </div>
  <footer class="site-footer">
    <div class="wrap"><div class="footer-shop"><a href="./buy.html">Shop Posters, Prints &amp; Wall Murals</a> · $29 poster · $69 framed · 12×18 · shipping included</div>
      <div><a href="./">Gallery</a> · <a href="./mountain-wall-art.html">Mountain wall art</a> · <a href="./peel-and-stick-wall-murals.html">Peel and stick wall murals</a> · Night Shade Art on Instagram: <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a></div>
    </div>
    <div class="operated-by footer-legal"><p>© 2026 Joshua Israel Ventures LLC. All rights reserved. Moonlit Windows is owned and operated by Joshua Israel Ventures LLC.</p><p class="footer-legal-links"><a href="./terms.html">Terms</a> · <a href="./privacy.html">Privacy</a> · <a href="./disclaimer.html">Disclaimer</a> · <a href="./contact.html">Contact</a></p></div>
  </footer>
</body>
</html>
'''

# ---------------- internal links ----------------
PIECE_LINK = (f'<p class="note collection-link" {MARK}>Planning a feature wall? See the '
              '<a href="../peel-and-stick-wall-murals.html">peel and stick wall murals collection</a> '
              'for measuring and wall-prep tips.</p>')

def edits():
    """Return {relpath: new_text} for files whose content would change."""
    out = {}
    def put(rel, old, new):
        if new != old:
            out[rel] = new

    # every piece page: one line right after the buy block (outside apply_stripe_links' regenerated region)
    for p in sorted((ROOT / "pieces").glob("*.html")):
        src = p.read_text(encoding="utf-8")
        if MARK in src:
            continue
        new, k = re.subn(r"(\n(\s*)<!-- buy:end -->\n)", lambda m: m.group(1) + m.group(2) + PIECE_LINK + "\n", src, count=1)
        if not k:
            print("WARN no buy:end anchor on", p.name)
        put(f"pieces/{p.name}", src, new)

    # buy.html hero "Browse by theme"
    rel = "buy.html"; src = (ROOT / rel).read_text(encoding="utf-8")
    if MARK not in src:
        a = 'Browse by theme: <a href="./mountain-wall-art.html">Mountain wall art</a>'
        if a in src:
            put(rel, src, src.replace(a, a + f' · <a {MARK} href="./peel-and-stick-wall-murals.html">Peel and stick wall murals</a>', 1))
        else:
            print("WARN buy.html theme anchor not found")

    # night-windows.html: waterfalls/lakes/coasts paragraph
    rel = "night-windows.html"; src = (ROOT / rel).read_text(encoding="utf-8")
    if MARK not in src:
        a = 'and <a href="./pieces/moonlit-waterfall.html">a moonlit waterfall</a>.</p>'
        if a in src:
            put(rel, src, src.replace(a, a[:-4] + f' For a whole feature wall, see the <a {MARK} href="./peel-and-stick-wall-murals.html">peel and stick wall murals collection</a>.</p>', 1))
        else:
            print("WARN night-windows anchor not found")

    # guide-print-sizes.html: mural section
    rel = "guide-print-sizes.html"; src = (ROOT / rel).read_text(encoding="utf-8")
    if MARK not in src:
        a = "check that the wall has that much clear, smooth painted surface before you order.</p>"
        if a in src:
            put(rel, src, src.replace(a, a[:-4] + f' The <a {MARK} href="./peel-and-stick-wall-murals.html">peel and stick wall murals collection</a> shows the scenes that work best at wall size, with measuring and wall-prep tips.</p>', 1))
        else:
            print("WARN guide anchor not found")

    # how-it-works.html: mural step
    rel = "how-it-works.html"; src = (ROOT / rel).read_text(encoding="utf-8")
    if MARK not in src:
        a = "No paste is needed, and it removes cleanly from most smooth painted walls.</li>"
        if a in src:
            put(rel, src, src.replace(a, a[:-5] + f' Browse the <a {MARK} href="./peel-and-stick-wall-murals.html">peel and stick wall murals collection</a> for scenes picked for a feature wall.</li>', 1))
        else:
            print("WARN how-it-works anchor not found")

    # llms.txt Shop section
    rel = "llms.txt"; src = (ROOT / rel).read_text(encoding="utf-8")
    if URL not in src:
        a = "with a room guide and FAQ\n"
        line = (f"- [Peel and stick wall murals]({URL}): {N} moonlit scenes picked for a feature wall as 4×6 ft (48×72 in) "
                "removable peel-and-stick wall murals ($149, shipping included), with measuring, wall prep and FAQ\n")
        if a in src:
            put(rel, src, src.replace(a, a + line, 1))
        else:
            print("WARN llms.txt anchor not found")
    return out

def sitemap(changed):
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    n = sm
    if f"<loc>{URL}</loc>" not in n:
        og = json.loads((ROOT / "products.json").read_text())
        asset = next(i["asset"] for i in og if i["slug"] == OG_SLUG)
        entry = (f'  <url><loc>{URL}</loc><lastmod>{TODAY}</lastmod>'
                 f'<image:image><image:loc>{SITE}/assets/{asset}</image:loc></image:image></url>\n')
        mt = f'<url><loc>{SITE}/mountain-wall-art.html</loc>'
        i = n.find(mt)
        if i >= 0:
            j = n.index("\n", i) + 1
            n = n[:j] + entry + n[j:]
        else:
            n = n.replace("</urlset>", entry + "</urlset>")
    for rel in changed:
        url = f"{SITE}/{rel}"
        n = re.sub(rf"(<loc>{re.escape(url)}</loc>)(\s*)(<lastmod>[^<]*</lastmod>)?",
                   lambda m: m.group(1) + (m.group(2) if m.group(3) else "") + f"<lastmod>{TODAY}</lastmod>", n)
    for bad in ("print-masters", ".png<", "github.io"):
        if bad in n:
            raise SystemExit(f"sitemap would expose {bad}")
    return n if n != sm else None

def main():
    items = {p["slug"]: p for p in json.loads((ROOT / "products.json").read_text())}
    assert len(set(SLUGS)) == N
    for s in SLUGS:
        it = items[s]
        st = it["stripe"]
        assert st["status"] == "live", s
        for k in ("muralUrl", "posterUrl", "framedUrl"):
            assert str(st.get(k, "")).startswith("https://buy.stripe.com/"), (s, k)
        assert re.fullmatch(r"\d\d-[a-z0-9-]+\.jpg", it["asset"]), it["asset"]
        assert (ROOT / "assets" / it["asset"]).exists() and (ROOT / "assets" / "thumbs" / it["asset"]).exists(), it["asset"]
    bl = blurbs()
    new_page = page(items, bl)
    for bad in ("print-masters", ".png", "github.io", "ChatGPT", "Higgsfield", "canvas"):
        assert bad.lower() not in new_page.lower(), bad
    assert not re.search(r"\bAI\b", new_page), "AI"

    changes = edits()
    old_page = PAGE.read_text(encoding="utf-8") if PAGE.exists() else None
    if new_page != old_page:
        changes[FILE] = new_page
    sm = sitemap(list(changes))
    if sm is not None:
        changes["sitemap.xml"] = sm

    if CHECK:
        print(("WOULD CHANGE: " + ", ".join(sorted(changes))) if changes else "up to date")
        return 1 if changes else 0
    for rel, txt in changes.items():
        (ROOT / rel).write_text(txt, encoding="utf-8")
    print(f"{N} pieces; changed {len(changes)} files:", " ".join(c for c in sorted(changes) if not c.startswith("pieces/")),
          f"+ {sum(c.startswith('pieces/') for c in changes)} piece pages")
    return 0

if __name__ == "__main__":
    sys.exit(main())
