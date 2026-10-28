#!/usr/bin/env python3
"""Build waterfall-wall-art.html: a buyer-intent collection page for waterfall wall art
(posters $35, framed prints $69, 4x6 ft peel and stick wall murals $149), and wire internal
links to it. Idempotent. Written 19 Oct 2026, modelled on build_collection_lakes.py (whose
waterfalls group stays; lake-wall-art.html links here for the full waterfall set).

Cards reuse the live Stripe links from products.json and the card blurbs already on buy.html.
Images are the public watermarked previews (assets/thumbs + assets), never masters.

  python3 scripts/build_collection_waterfalls.py          # write page + wire links + sitemap/llms.txt
  python3 scripts/build_collection_waterfalls.py --check  # dry run: exit 1 if anything would change
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = "--check" in sys.argv
FILE = "waterfall-wall-art.html"
PAGE = ROOT / FILE
SITE = "https://moonlitwindows.com"
URL = f"{SITE}/{FILE}"
TODAY = "2026-10-28"
OG_SLUG = "plitvice-lakes-moon"
MARK = 'data-collection="waterfalls"'

GROUPS = [
    ("iceland-north-atlantic", "Iceland and North Atlantic waterfalls", "waterfall wall art poster and framed print",
     "Mossy cliffs, black rock and long northern nights: falls that drop straight out of green walls toward the sea.", [
        ("skogafoss-waterfall-moon", "Skógafoss pouring a wide white curtain over mossy cliffs in south Iceland beside its staircase path under a full moon"),
        ("seljalandsfoss-waterfall-moon", "Seljalandsfoss dropping from a mossy cliff into silver mist in south Iceland, its footpath curving behind the falls, under a full moon"),
        ("gullfoss-waterfall-moon", "Gullfoss plunging in wide tiers into its misty Hvítá canyon on Iceland’s Golden Circle, a turf-roofed farmhouse lit on the rim under a full moon"),
        ("kirkjufell-waterfall-moon", "Kirkjufellsfoss cascading over mossy rocks below cone-shaped Kirkjufell on a moonlit Icelandic fjord"),
        ("faroe-gasadalur-moon", "Múlafossur waterfall dropping from green sea cliffs at Gásadalur in the Faroe Islands under a full moon"),
    ]),
    ("europe", "European waterfalls", "waterfall wall art poster and framed print",
     "Alpine valleys and terraced forest lakes, with a few lit windows and boardwalks close to the water.", [
        ("plitvice-lakes-moon", "Plitvice’s turquoise lakes spilling over terraced falls, a lit boardwalk threading the Croatian forest under moonlight"),
        ("rhine-falls-moon", "The Rhine Falls thundering around their rock pillar below the lit windows of Schloss Laufen in Switzerland under a full moon"),
        ("lauterbrunnen-valley-moon", "Staubbach Falls pouring down the cliff above Lauterbrunnen’s lit chalets and church in the Swiss Alps"),
    ]),
    ("north-america", "North American waterfalls", "waterfall wall art poster and framed print",
     "From Oregon’s mossy Columbia River Gorge to a desert canyon oasis in Arizona, falls lit by the moon and a few warm windows.", [
        ("multnomah-falls-moon", "Multnomah Falls pouring in two tiers past the arched Benson Bridge in Oregon’s Columbia River Gorge under a full moon"),
        ("havasu-falls-moon", "Havasu Falls plunging from red canyon rock into a turquoise travertine pool in the Grand Canyon under a full moon"),
    ]),
    ("rainforest-canyon-river", "Rainforest, canyon and river waterfalls", "waterfall wall art poster and framed print",
     "The big ones: rainforest gorges and the Zambezi, all wrapped in moonlit spray.", [
        ("iguazu-falls-moon", "Tier after tier of Iguazu’s waterfalls thundering into a misty rainforest gorge under a full moon"),
        ("victoria-falls-moon", "Victoria Falls pouring into its misty gorge on the Zambezi with a moonbow arcing through the spray"),
        ("moonlit-waterfall", "A tall waterfall pouring through a deep, misty gorge among ferns and mossy rock under moonlight"),
    ]),
]
SLUGS = [s for _, _, _, _, items in GROUPS for s, _ in items]
N = len(SLUGS)

TITLE = "Waterfall Wall Art: Moonlit Waterfall Posters & Framed Prints | Moonlit Windows"
DESC = f"Waterfall wall art: {N} moonlit waterfall posters, from Skógafoss to Iguazu and Victoria Falls. Poster $35, framed $69, mural $149, shipping included."
H1 = "Waterfall Wall Art: Moonlit Waterfall Posters and Framed Prints"

FAQ = [
    ("What sizes and formats are available?",
     "Every piece comes as a 12×18 in enhanced matte poster ($35), the same 12×18 print in a black frame ($69), or a 4×6 ft (48×72 in) peel and stick wall mural on removable polyester ($149). Shipping is included on all three."),
    ("Are these real waterfalls?",
     "Eight are named falls reimagined at night: Skógafoss and Kirkjufellsfoss in Iceland, Múlafossur at Gásadalur in the Faroe Islands, Staubbach Falls above Lauterbrunnen in Switzerland, the terraced falls of Plitvice in Croatia, Iguazu on the Argentina–Brazil border, Havasu Falls in the Grand Canyon in Arizona, and Victoria Falls on the Zambezi between Zambia and Zimbabwe. Moonlit Waterfall is an imagined gorge rather than one exact place."),
    ("Can you see a waterfall by moonlight?",
     "Yes. Near a full moon, white water and spray catch a surprising amount of light, and at big falls such as Victoria Falls the spray can even form a lunar rainbow, or moonbow. Victoria Falls Moon shows one. The prints keep that soft, silvery night light rather than a bright daytime look."),
    ("Which waterfall print suits a bedroom?",
     "The calmest are the Icelandic and Faroese falls, Skógafoss, Kirkjufellsfoss and Múlafossur, with cool greens and soft white water, and Plitvice, where the falls are small and gentle. Iguazu, Havasu and Victoria Falls have more power and colour, so they suit a living room, an office or a hallway."),
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
        {"@type": "CollectionPage", "name": "Waterfall Wall Art: Moonlit Waterfall Posters and Framed Prints",
         "url": URL, "description": DESC,
         "isPartOf": {"@type": "WebSite", "name": "Moonlit Windows", "url": SITE + "/"},
         "publisher": {"@type": "Organization", "@id": SITE + "/#org", "name": "Moonlit Windows", "url": SITE + "/",
                       "brand": {"@type": "Brand", "name": "Moonlit Windows", "alternateName": ["Night Shade Art", "Night Windows", "Prompt Framed"]}},
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": f"{it['title']} poster & framed print",
              "url": f"{SITE}/pieces/{it['slug']}.html"} for i, it in enumerate(items)]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Shop", "item": SITE + "/buy.html"},
            {"@type": "ListItem", "position": 3, "name": "Waterfall Wall Art", "item": URL}]}]}
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
  <meta property="og:image:alt" content="{og_item['title']} waterfall wall art poster" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{T}" />
  <meta name="twitter:description" content="{DESC}" />
  <meta name="twitter:image" content="{og}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=Outfit:wght@380;560;650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json" data-ld="collection-waterfalls">
{ld(sel)}
  </script>
  <script type="application/ld+json" data-ld="faq-waterfalls">
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
    <p class="note breadcrumb"><a href="./">Home</a> › <a href="./buy.html">Shop</a> › Waterfall wall art</p>
    <section class="hero left">
      <div class="kicker">Collection</div>
      <h1>{H1}</h1>
      <p class="sale-line">{N} waterfall art prints · $35 poster · $69 framed · 12×18 · $149 peel &amp; stick wall mural (4×6 ft) · shipping included</p>
      <p class="answer-first">These are {N} moonlit waterfall prints, each sold as a 12×18 in poster for $35, a black-framed print for $69, or a 4×6 ft peel and stick wall mural for $149, with shipping included. Most show real falls at night, among them Skógafoss, Gullfoss and Kirkjufellsfoss in Iceland, Plitvice in Croatia, Iguazu, Havasu Falls in the Grand Canyon, Multnomah Falls in Oregon, the Rhine Falls in Switzerland and Victoria Falls, with a full moon over the spray.</p>
      <p>Falling water is the brightest thing in a moonlit landscape. White water and mist hold the moonlight while the cliffs, moss and forest around them stay dark, so a waterfall print reads clearly from across a room and still feels quiet up close. Tall falls also suit the portrait 12×18 format and a 4×6 ft wall panel naturally.</p>
      <p class="note">Jump to: <a href="#iceland-north-atlantic">Iceland and North Atlantic</a> · <a href="#europe">Europe</a> · <a href="#north-america">North America</a> · <a href="#rainforest-canyon-river">Rainforest, canyon and river</a> · <a href="#choose">Choosing a piece</a> · <a href="#faq">FAQ</a></p>
    </section>

{grids}

    <section class="prose">
      <h2 id="choose">How to choose waterfall wall art for your room</h2>
      <p><strong>Hallway, stair wall or a narrow space.</strong> A tall waterfall fills a slim wall the way a window would: {P("skogafoss-waterfall-moon", "Skógafoss")} with its staircase path climbing beside the spray, {P("lauterbrunnen-valley-moon", "Staubbach Falls above Lauterbrunnen")}, or {P("faroe-gasadalur-moon", "Múlafossur at Gásadalur")} dropping straight toward the sea.</p>
      <p><strong>Bedroom.</strong> Cool greens and soft white water read calmest at night: {P("kirkjufell-waterfall-moon", "Kirkjufellsfoss below Kirkjufell")} or the gentle terraced falls of {P("plitvice-lakes-moon", "Plitvice")}. More bedroom picks and size tips are in the <a data-guide="bedroom" href="./moon-poster-bedroom.html">moon poster for bedroom</a> guide.</p>
      <p><strong>Living room, office or a feature wall.</strong> The big falls have the most energy: {P("iguazu-falls-moon", "Iguazu")} tier after tier, {P("victoria-falls-moon", "Victoria Falls")} with a moonbow in its spray, and {P("havasu-falls-moon", "Havasu Falls")}, where red canyon rock frames a turquoise pool. To let a waterfall fill the wall, the same artwork comes as a 4×6 ft (48×72 in) peel and stick wall mural; the <a href="./peel-and-stick-wall-murals.html">peel and stick wall murals collection</a> covers measuring and wall prep.</p>
      <p><strong>Bathroom or spa corner.</strong> Water suits water. A framed print of {P("moonlit-waterfall", "Moonlit Waterfall")} or Plitvice brings the sound of a gorge to mind without adding colour that fights the tiles; hang it away from direct splashes.</p>
      <p><strong>A trip to remember.</strong> If you drove Iceland’s Ring Road, hiked down to Havasupai or stood in the spray at Victoria Falls, the place-named prints are made for that. Pairs work well too: Skógafoss with Kirkjufellsfoss for Iceland, or Iguazu with Victoria Falls for the world’s great falls.</p>
      <p>Prefer still water? The <a href="./lake-wall-art.html">lake and waterfall wall art collection</a> has Lake Como, Lake Bled, Hallstatt and Moraine Lake, and the <a href="./mountain-wall-art.html">mountain wall art collection</a> has the Matterhorn, the Dolomites and Mount Fuji. For sea cliffs and harbours, see the <a href="./coastal-wall-art.html">coastal wall art collection</a>. Not sure about size? The <a href="./guide-print-sizes.html">print size guide</a> compares the poster, framed print and mural.</p>
    </section>

    <section class="prose" id="faq">
      <h2>Questions about these waterfall prints</h2>
{faq_html()}
      <p>Looking for something else? Browse <a href="./night-windows.html">every Night Windows piece</a> or the <a href="./buy.html">full shop</a>.</p>
    </section>
  </div>
  <footer class="site-footer">
    <div class="wrap"><div class="footer-shop"><a href="./buy.html">Shop Posters, Prints &amp; Wall Murals</a> · $35 poster · $69 framed · 12×18 · shipping included</div>
      <div><a href="./">Gallery</a> · <a href="./mountain-wall-art.html">Mountain wall art</a> · <a href="./lake-wall-art.html">Lake and waterfall wall art</a> · <a href="./waterfall-wall-art.html">Waterfall wall art</a> · <a href="./coastal-wall-art.html">Coastal wall art</a> · <a href="./asian-wall-art.html">Asian wall art</a> · <a href="./european-wall-art.html">European wall art</a> · <a href="./peel-and-stick-wall-murals.html">Peel and stick wall murals</a> · Night Shade Art on Instagram: <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a></div>
    </div>
    <div class="operated-by footer-legal"><p class="footer-legal-links"><a href="./terms.html">Terms</a> · <a href="./privacy.html">Privacy</a> · <a href="./disclaimer.html">Disclaimer</a> · <a href="./contact.html">Contact</a></p></div>
  </footer>
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "899375a6262144aabf5184589abd580c"}}'></script>
</body>
</html>
'''

PIECE_LINK = (f'<p class="note collection-link" {MARK}>See more falls in the '
              '<a href="../waterfall-wall-art.html">waterfall wall art collection</a>: '
              f'{N} moonlit waterfall posters, framed prints and wall murals.</p>')
# Same text publish_pieces_76_80.py carries in HUB_THEMES (WATERFALLS_SUFFIX), so either order works.
HUB_LINK = (f' Every waterfall is also in the <a {MARK} href="./waterfall-wall-art.html">'
            'waterfall wall art collection</a>.')

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
        a = '<a data-collection="lakes" href="./lake-wall-art.html">Lake &amp; waterfall wall art</a>'
        if a in src: put(rel, src, src.replace(a, a + f' · <a {MARK} href="./waterfall-wall-art.html">Waterfall wall art</a>', 1))
        else: print("WARN buy.html theme anchor not found")
    rel = "night-windows.html"; src = (ROOT / rel).read_text(encoding="utf-8")
    if MARK not in src:
        a = 'href="./lake-wall-art.html">lake and waterfall wall art collection</a>.'
        if a in src: put(rel, src, src.replace(a, a + HUB_LINK, 1))
        else: print("WARN night-windows anchor not found")
    rel = "llms.txt"; src = (ROOT / rel).read_text(encoding="utf-8")
    line = (f"- [Waterfall wall art]({URL}): {N} moonlit waterfall posters ($35), framed prints ($69) and wall murals "
            "($149), from Skógafoss, Kirkjufellsfoss and Plitvice to Iguazu, Havasu Falls and Victoria Falls, with a room guide and FAQ\n")
    if URL in src:
        put(rel, src, re.sub(rf"- \[Waterfall wall art\]\({re.escape(URL)}\):[^\n]*\n", lambda m: line, src, count=1))
    else:
        m = re.search(r"- \[Lake and waterfall wall art\]\([^)]*\):[^\n]*\n", src)
        if m: put(rel, src, src[:m.end()] + line + src[m.end():])
        else: print("WARN llms.txt anchor not found")
    return out

def sitemap(changed):
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8"); n = sm
    if f"<loc>{URL}</loc>" not in n:
        asset = json.loads((ROOT / "products.json").read_text())
        asset = next(i["asset"] for i in asset if i["slug"] == OG_SLUG)
        entry = f'  <url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><image:image><image:loc>{SITE}/assets/{asset}</image:loc></image:image></url>\n'
        i = n.find(f"<url><loc>{SITE}/lake-wall-art.html</loc>")
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
