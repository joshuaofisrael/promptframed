#!/usr/bin/env python3
"""Build lake-wall-art.html: a buyer-intent collection page for lake and waterfall wall art
(posters $35, framed prints $69, 4x6 ft peel and stick wall murals $149), and wire internal
links to it. Idempotent. Modelled on build_collection_murals.py.

Cards reuse the live Stripe links from products.json and the card blurbs already on buy.html.
Images are the public watermarked previews (assets/thumbs + assets), never masters.

  python3 scripts/build_collection_lakes.py          # write page + wire links + sitemap/llms.txt
  python3 scripts/build_collection_lakes.py --check  # dry run: exit 1 if anything would change
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = "--check" in sys.argv
FILE = "lake-wall-art.html"
PAGE = ROOT / FILE
SITE = "https://moonlitwindows.com"
URL = f"{SITE}/{FILE}"
TODAY = "2026-10-19"
OG_SLUG = "lake-bled-island-moon"
MARK = 'data-collection="lakes"'

GROUPS = [
    ("lakes", "Lake wall art", "lake wall art poster and framed print",
     "Still water, mirrored peaks and a few warm windows on the shore: the calmest scenes in the series.", [
        ("lake-como-bellagio-moon", "Bellagio’s pastel villas and cypresses glowing along Lake Como below moonlit mountains"),
        ("lake-bled-island-moon", "Lake Bled’s island church and clifftop castle on the moonlit lake"),
        ("lake-tekapo-church-moon", "Lake Tekapo’s Church of the Good Shepherd above purple lupins and turquoise water under a full moon"),
        ("hallstatt-lake-moon", "Hallstatt’s church steeple and lit houses reflected in a still alpine lake at night"),
        ("banff-lake-louise-moon", "Turquoise Lake Louise mirroring snowy Rocky Mountain peaks under moonlight"),
        ("patagonia-lake-peaks", "A turquoise Patagonian lake mirroring jagged moonlit peaks above a wildflower shore"),
        ("scottish-highlands-loch", "Mist over a Highlands loch with castle ruins glowing on the far shore under a full moon"),
        ("lakeside-cabin", "A warm-lit cabin beside a quiet lake, reflected in the water between dark pines at night"),
        ("moonlit-mediterranean-village", "A lakeside village with a lit bell tower, cypresses and a sailboat on still water under a full moon"),
        ("japanese-temple-pond", "A still temple pond mirroring the full moon beside stone lanterns, pines and maples"),
        ("salar-de-uyuni-moon", "Bolivia’s Salar de Uyuni salt flat under a thin layer of water, mirroring distant mountains and a full moon"),
        ("pamukkale-terraces-moon", "Pamukkale’s white travertine terraces in Turkey, their turquoise pools mirroring a full moon"),
        ("cradle-mountain-dove-lake-moon", "Cradle Mountain mirrored in still Dove Lake beside the old timber boatshed in Tasmania under a full moon"),
        ("moraine-lake-moon", "Moraine Lake’s turquoise water mirroring the Valley of the Ten Peaks beside red canoes in Banff under a full moon"),
    ]),
    ("waterfalls", "Waterfall wall art", "waterfall wall art poster and framed print",
     "Falling water and mist catching the moonlight, from Iceland and Swiss valleys to the Grand Canyon, South American rainforest and the Zambezi. See them all in the <a href=\"./waterfall-wall-art.html\">waterfall wall art collection</a>.", [
        ("plitvice-lakes-moon", "Plitvice’s turquoise lakes and terraced falls with a lit boardwalk through the forest"),
        ("iguazu-falls-moon", "Tiers of Iguazu waterfalls falling into a misty rainforest gorge under a full moon"),
        ("victoria-falls-moon", "Victoria Falls pouring into a misty gorge on the Zambezi with a moonbow in the spray under a full moon"),
        ("kirkjufell-waterfall-moon", "Kirkjufellsfoss pouring over mossy rocks with cone-shaped Kirkjufell and a moonlit Icelandic fjord beyond"),
        ("skogafoss-waterfall-moon", "Skógafoss pouring a wide white curtain over mossy cliffs in south Iceland beside its staircase path"),
        ("havasu-falls-moon", "Havasu Falls plunging from red canyon rock into a turquoise travertine pool in the Grand Canyon"),
        ("lauterbrunnen-valley-moon", "Staubbach Falls pouring into the Lauterbrunnen valley with lit chalets and snowy Alps"),
        ("faroe-gasadalur-moon", "Múlafossur waterfall dropping from green sea cliffs at Gásadalur under a full moon"),
        ("moonlit-waterfall", "A luminous waterfall pouring through a deep, misty gorge under moonlight"),
    ]),
]
SLUGS = [s for _, _, _, _, items in GROUPS for s, _ in items]
N = len(SLUGS)

TITLE = "Lake Wall Art & Waterfall Posters, Framed Prints | Moonlit Windows"
DESC = (f"Lake and waterfall wall art: {N} moonlit lake posters and framed prints, from Lake Como, Lake Bled, "
        "Hallstatt and Lake Louise to Plitvice, Iguazu and Victoria Falls. 12×18 poster $35, framed $69, "
        "4×6 ft wall mural $149, shipping included.")
H1 = "Lake &amp; Waterfall Wall Art: Moonlit Lake Posters and Framed Prints"

FAQ = [
    ("What sizes and formats are available?",
     "Every piece comes as a 12×18 in enhanced matte poster ($35), the same 12×18 print in a black frame ($69), or a 4×6 ft (48×72 in) peel and stick wall mural on removable polyester ($149). Shipping is included on all three."),
    ("Are these real places?",
     "Most are named lakes and waterfalls, reimagined at night: Lake Como, Lake Bled, Hallstatt, Lake Louise, Lake Tekapo, Moraine Lake, Plitvice, Iguazu, Victoria Falls, Kirkjufellsfoss, Skógafoss, Havasu Falls, Staubbach Falls in Lauterbrunnen and Múlafossur in the Faroe Islands, plus the Salar de Uyuni salt flat in Bolivia, mirrored after rain, the travertine pools of Pamukkale in Turkey, and Dove Lake below Cradle Mountain in Tasmania. Patagonia Lake Peaks and Scottish Highlands Loch evoke those regions rather than one exact viewpoint, and Lakeside Cabin, Moonlit Waterfall, Moonlit Mediterranean Village and Japanese Temple Pond are imagined scenes."),
    ("Will the watermark be on my print?",
     "No. The previews on this site carry a small Night Shade Art watermark to discourage copying; your print is made from a clean file without it."),
    ("How long does delivery take?",
     "Every order is printed to order after checkout and shipped by post. Wall murals ship in 1–2 weeks."),
    ("How do I pay?",
     "Every button opens secure Stripe checkout, and your receipt arrives by email."),
]

def blurbs():
    b = (ROOT / "buy.html").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<article class="(card[^"]*)" id="([^"]+)">.*?\.jpg (\d+)w".*?<h2>.*?</h2>\s*<p>(.*?)</p>', b, re.S):
        out[m.group(2)] = (m.group(1), m.group(3), m.group(4))
    return out

def is_live(st):
    return st.get("status") == "live" and all(str(st.get(k) or "").startswith("https://buy.stripe.com/")
                                              for k in ("posterUrl", "framedUrl", "muralUrl"))

def card(it, alt, suffix, info):
    cls, w, blurb = info
    s, t, st, a = it["slug"], html.escape(it["title"]), it["stripe"], it["asset"]
    if not is_live(st):  # new drop before its Stripe links exist: same 'soon' note as buy.html
        return f'''      <article class="{cls}" id="{s}">
        <a href="./pieces/{s}.html"><img src="./assets/thumbs/{a}" srcset="./assets/thumbs/{a} 600w, ./assets/{a} {w}w" sizes="(max-width: 640px) 92vw, (max-width: 1100px) 45vw, 22rem" decoding="async" alt="{html.escape(alt)}, {t} {suffix}" loading="lazy"></a>
        <div class="meta">
          <h3><a href="./pieces/{s}.html">{t}</a></h3>
          <p>{blurb}</p>
          <p class="price-line">$35 poster · $69 framed (12×18) · $149 peel &amp; stick wall mural (4×6 ft)</p>
          <p class="note">This window opens for orders soon.</p>
        </div>
      </article>'''
    return f'''      <article class="{cls}" id="{s}">
        <a href="./pieces/{s}.html"><img src="./assets/thumbs/{a}" srcset="./assets/thumbs/{a} 600w, ./assets/{a} {w}w" sizes="(max-width: 640px) 92vw, (max-width: 1100px) 45vw, 22rem" decoding="async" alt="{html.escape(alt)}, {t} {suffix}" loading="lazy"></a>
        <div class="meta">
          <h3><a href="./pieces/{s}.html">{t}</a></h3>
          <p>{blurb}</p>
          <p class="price-line">$35 poster · $69 framed (12×18) · $149 peel &amp; stick wall mural (4×6 ft)</p>
          <div class="actions buy-actions">
            <a class="btn" data-buy="{s}" data-sku="poster" href="{st['posterUrl']}">Poster · $35</a>
            <a class="btn secondary" data-buy="{s}" data-sku="framed" href="{st['framedUrl']}">Framed · $69</a>
            <a class="btn secondary" data-buy="{s}" data-sku="mural" href="{st['muralUrl']}">Wall mural · $149</a>
          </div>
        </div>
      </article>'''

def ld(items):
    g = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Lake & Waterfall Wall Art: Moonlit Lake Posters and Framed Prints",
         "url": URL, "description": DESC,
         "isPartOf": {"@type": "WebSite", "name": "Moonlit Windows", "url": SITE + "/"},
         "publisher": {"@type": "Organization", "@id": SITE + "/#org", "name": "Joshua Israel Ventures LLC", "url": SITE + "/",
                       "legalName": "Joshua Israel Ventures LLC",
                       "brand": {"@type": "Brand", "name": "Moonlit Windows", "alternateName": ["Night Shade Art", "Night Windows", "Prompt Framed"]}},
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": f"{it['title']} poster & framed print",
              "url": f"{SITE}/pieces/{it['slug']}.html"} for i, it in enumerate(items)]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Shop", "item": SITE + "/buy.html"},
            {"@type": "ListItem", "position": 3, "name": "Lake & Waterfall Wall Art", "item": URL}]}]}
    return json.dumps(g, ensure_ascii=False, indent=2)

def faq_ld():
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False, indent=2)

def faq_html():
    return "\n".join(f"      <p><strong>{html.escape(q, quote=False)}</strong> {html.escape(a, quote=False)}</p>" for q, a in FAQ)

def page(by_slug, bl):
    sections = []
    for gid, head, suffix, intro, items in GROUPS:
        cards = "\n".join(card(by_slug[s], alt, suffix, bl[s]) for s, alt in items)
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
    P = lambda s, label: f'<a href="./pieces/{s}.html">{label}</a>'
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
  <meta property="og:image:alt" content="{og_item['title']} lake wall art poster" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{T}" />
  <meta name="twitter:description" content="{DESC}" />
  <meta name="twitter:image" content="{og}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=Outfit:wght@380;560;650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json" data-ld="collection-lakes">
{ld(sel)}
  </script>
  <script type="application/ld+json" data-ld="faq-lakes">
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
    <p class="note breadcrumb"><a href="./">Home</a> › <a href="./buy.html">Shop</a> › Lake and waterfall wall art</p>
    <section class="hero left">
      <div class="kicker">Collection</div>
      <h1>{H1}</h1>
      <p class="sale-line">{N} lake and waterfall art prints · $35 poster · $69 framed · 12×18 · $149 peel &amp; stick wall mural (4×6 ft) · shipping included</p>
      <p class="answer-first">These are {N} moonlit lake and waterfall prints, each sold as a 12×18 in poster for $35, a black-framed print for $69, or a 4×6 ft peel and stick wall mural for $149, with shipping included. Most show real places at night, among them Lake Como, Lake Bled, Hallstatt, Lake Louise, Plitvice, Iguazu and Victoria Falls, with a full moon on the water and a few warm windows on the shore.</p>
      <p>Water is what makes a night scene glow: the moon doubles in a still lake, and mist over a waterfall catches its light. That makes these the softest, most restful pieces in the Night Windows series, a natural fit for a bedroom, a lake house or a cabin.</p>
      <p class="note">Jump to: <a href="#lakes">Lakes</a> · <a href="#waterfalls">Waterfalls</a> · <a href="#choose">Choosing a piece</a> · <a href="#faq">FAQ</a></p>
    </section>

{grids}

    <section class="prose">
      <h2 id="choose">How to choose lake wall art for your room</h2>
      <p><strong>Lake house or cabin.</strong> If the room already looks out on water, pick a scene that echoes it rather than competes with it: {P("lakeside-cabin", "Lakeside Cabin")} with its glowing window between the pines, or the misty {P("scottish-highlands-loch", "Scottish Highlands Loch")}. A framed 12×18 print suits a mantel, an entryway or the wall above a bunk.</p>
      <p><strong>Bedroom.</strong> The stillest water reads calmest: {P("banff-lake-louise-moon", "Lake Louise")} and {P("patagonia-lake-peaks", "Patagonia Lake Peaks")}, where turquoise water mirrors the mountains, {P("japanese-temple-pond", "Japanese Temple Pond")} with the moon reflected among stone lanterns, or {P("salar-de-uyuni-moon", "Salar de Uyuni")}, where a salt flat turns to a mirror after rain. More bedroom picks and size tips are in the <a data-guide="bedroom" href="./moon-poster-bedroom.html">moon poster for bedroom</a> guide.</p>
      <p><strong>Living room or a feature wall.</strong> Lit villages carry well across a room: {P("lake-como-bellagio-moon", "Bellagio on Lake Como")}, {P("hallstatt-lake-moon", "Hallstatt")} and {P("lake-bled-island-moon", "Lake Bled’s island church")}. To make the lake fill the wall, the same artwork comes as a 4×6 ft (48×72 in) peel and stick wall mural; the <a href="./peel-and-stick-wall-murals.html">peel and stick wall murals collection</a> covers measuring and wall prep.</p>
      <p><strong>Office or hallway.</strong> Waterfalls bring movement to a narrow wall: {P("iguazu-falls-moon", "Iguazu Falls")} tier after tier, {P("victoria-falls-moon", "Victoria Falls")} with a moonbow in its spray, {P("lauterbrunnen-valley-moon", "Staubbach Falls above Lauterbrunnen")}, or {P("plitvice-lakes-moon", "Plitvice’s terraced lakes")}.</p>
      <p><strong>A trip to remember.</strong> If you rowed out to Bled’s island, took the ferry to Bellagio or walked the Plitvice boardwalks, the place-named prints are made for that. Pairs work well too: Hallstatt with Lake Bled for an Alpine lakes wall, or Iguazu with Plitvice for waterfalls.</p>
      <p>Looking for peaks rather than water? The <a href="./mountain-wall-art.html">mountain wall art collection</a> has the Matterhorn, the Dolomites and Mount Fuji, and the <a href="./coastal-wall-art.html">coastal wall art collection</a> has the Amalfi Coast, Santorini and the Cliffs of Moher. For castles, canals and old towns, see the <a href="./european-wall-art.html">European wall art collection</a>; for Mount Fuji, Kyoto, the Taj Mahal and Angkor Wat, the <a href="./asian-wall-art.html">Asian wall art collection</a>. Not sure about size? The <a href="./guide-print-sizes.html">print size guide</a> compares the poster, framed print and mural.</p>
    </section>

    <section class="prose" id="faq">
      <h2>Questions about these lake and waterfall prints</h2>
{faq_html()}
      <p>Looking for something else? Browse <a href="./night-windows.html">every Night Windows piece</a> or the <a href="./buy.html">full shop</a>.</p>
    </section>
  </div>
  <footer class="site-footer">
    <div class="wrap"><div class="footer-shop"><a href="./buy.html">Shop Posters, Prints &amp; Wall Murals</a> · $35 poster · $69 framed · 12×18 · shipping included</div>
      <div><a href="./">Gallery</a> · <a href="./mountain-wall-art.html">Mountain wall art</a> · <a href="./lake-wall-art.html">Lake and waterfall wall art</a> · <a href="./waterfall-wall-art.html">Waterfall wall art</a> · <a href="./coastal-wall-art.html">Coastal wall art</a> · <a href="./asian-wall-art.html">Asian wall art</a> · <a href="./european-wall-art.html">European wall art</a> · <a href="./peel-and-stick-wall-murals.html">Peel and stick wall murals</a> · Night Shade Art on Instagram: <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a></div>
    </div>
    <div class="operated-by footer-legal"><p>© 2026 Joshua Israel Ventures LLC. All rights reserved. Moonlit Windows is owned and operated by Joshua Israel Ventures LLC.</p><p class="footer-legal-links"><a href="./terms.html">Terms</a> · <a href="./privacy.html">Privacy</a> · <a href="./disclaimer.html">Disclaimer</a> · <a href="./contact.html">Contact</a></p></div>
  </footer>
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "899375a6262144aabf5184589abd580c"}}'></script>
</body>
</html>
'''

PIECE_LINK = (f'<p class="note collection-link" {MARK}>Part of the '
              '<a href="../lake-wall-art.html">lake and waterfall wall art collection</a>: '
              f'{N} moonlit lake and waterfall posters, framed prints and wall murals.</p>')

def edits():
    out = {}
    def put(rel, old, new):
        if new != old: out[rel] = new
    for s in SLUGS:
        rel = f"pieces/{s}.html"; src = (ROOT / rel).read_text(encoding="utf-8")
        if MARK in src:
            new = re.sub(rf'<p class="note collection-link" {re.escape(MARK)}>.*?</p>', lambda m: PIECE_LINK, src, count=1)
        else:
            new, k = re.subn(r'(\n(\s*)<p class="note collection-link" data-collection="murals">.*?</p>\n)',
                             lambda m: m.group(1) + m.group(2) + PIECE_LINK + "\n", src, count=1)
            if not k: print("WARN no murals collection-link anchor on", s)
        put(rel, src, new)
    rel = "buy.html"; src = (ROOT / rel).read_text(encoding="utf-8")
    if MARK not in src:
        a = '<a data-collection="murals" href="./peel-and-stick-wall-murals.html">Peel and stick wall murals</a>'
        if a in src: put(rel, src, src.replace(a, a + f' · <a {MARK} href="./lake-wall-art.html">Lake &amp; waterfall wall art</a>', 1))
        else: print("WARN buy.html theme anchor not found")
    rel = "night-windows.html"; src = (ROOT / rel).read_text(encoding="utf-8")
    if MARK not in src:
        a = 'href="./peel-and-stick-wall-murals.html">peel and stick wall murals collection</a>.</p>'
        if a in src: put(rel, src, src.replace(a, a[:-4] + f' The lakes and waterfalls are gathered in the <a {MARK} href="./lake-wall-art.html">lake and waterfall wall art collection</a>.</p>', 1))
        else: print("WARN night-windows anchor not found")
    rel = "llms.txt"; src = (ROOT / rel).read_text(encoding="utf-8")
    if URL in src:  # keep count + place names in step
        put(rel, src, re.sub(rf"(- \[Lake and waterfall wall art\]\({re.escape(URL)}\): )\d+ (.*?) to Plitvice and Iguazu Falls,",
                             lambda m: m.group(1) + f"{N} " + m.group(2) + " to Plitvice, Iguazu and Victoria Falls,", src, count=1)
            if " to Plitvice and Iguazu Falls," in src else
            re.sub(rf"(- \[Lake and waterfall wall art\]\({re.escape(URL)}\): )\d+ ", rf"\g<1>{N} ", src, count=1))
    else:
        m = re.search(r"- \[Peel and stick wall murals\]\([^)]*\):[^\n]*\n", src)
        line = (f"- [Lake and waterfall wall art]({URL}): {N} moonlit lake and waterfall posters ($35), framed prints ($69) "
                "and wall murals ($149), from Lake Como, Lake Bled, Hallstatt and Lake Louise to Plitvice, Iguazu and Victoria Falls, with a room guide and FAQ\n")
        if m: put(rel, src, src[:m.end()] + line + src[m.end():])
        else: print("WARN llms.txt anchor not found")
    return out

def sitemap(changed):
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8"); n = sm
    if f"<loc>{URL}</loc>" not in n:
        asset = json.loads((ROOT / "products.json").read_text())
        asset = next(i["asset"] for i in asset if i["slug"] == OG_SLUG)
        entry = f'  <url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><image:image><image:loc>{SITE}/assets/{asset}</image:loc></image:image></url>\n'
        i = n.find(f"<url><loc>{SITE}/peel-and-stick-wall-murals.html</loc>")
        n = n[:n.index("\n", i) + 1] + entry + n[n.index("\n", i) + 1:] if i >= 0 else n.replace("</urlset>", entry + "</urlset>")
    for rel in changed:
        url = f"{SITE}/{rel}"
        n = re.sub(rf"(<loc>{re.escape(url)}</loc>)(\s*)(<lastmod>[^<]*</lastmod>)?",
                   lambda m: m.group(1) + (m.group(2) if m.group(3) else "") + f"<lastmod>{TODAY}</lastmod>", n)
    for bad in ("print-masters", ".png<", "github.io"):
        if bad in n: raise SystemExit(f"sitemap would expose {bad}")
    return n if n != sm else None

def main():
    items = {p["slug"]: p for p in json.loads((ROOT / "products.json").read_text())}
    assert len(set(SLUGS)) == N
    for s in SLUGS:
        st = items[s]["stripe"]
        if st.get("status") == "live":  # placeholder rows (new drop, Stripe pending) render a 'soon' card
            for k in ("muralUrl", "posterUrl", "framedUrl"):
                assert str(st.get(k, "")).startswith("https://buy.stripe.com/"), (s, k)
        else:
            print("note: Stripe not live yet, card shows 'opens for orders soon':", s)
        a = items[s]["asset"]
        assert re.fullmatch(r"\d\d-[a-z0-9-]+\.jpg", a) and (ROOT / "assets" / a).exists() and (ROOT / "assets" / "thumbs" / a).exists(), a
    new_page = page(items, blurbs())
    for bad in ("print-masters", ".png", "github.io", "ChatGPT", "Higgsfield", "canvas"):
        assert bad.lower() not in new_page.lower(), bad
    assert not re.search(r"\bAI\b", new_page), "AI"
    changes = edits()
    old = PAGE.read_text(encoding="utf-8") if PAGE.exists() else None
    if new_page != old: changes[FILE] = new_page
    sm = sitemap(list(changes))
    if sm is not None: changes["sitemap.xml"] = sm
    if CHECK:
        print(("WOULD CHANGE: " + ", ".join(sorted(changes))) if changes else "up to date")
        return 1 if changes else 0
    for rel, txt in changes.items(): (ROOT / rel).write_text(txt, encoding="utf-8")
    print(f"{N} pieces; changed {len(changes)} files:", " ".join(sorted(changes)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
