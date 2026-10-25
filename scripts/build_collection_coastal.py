#!/usr/bin/env python3
"""Build coastal-wall-art.html: a buyer-intent collection page for coastal, ocean and fjord wall art
(posters $35, framed prints $69, 4x6 ft peel and stick wall murals $149), and wire internal
links to it. Idempotent. Modelled on build_collection_lakes.py.

Cards reuse the live Stripe links from products.json and the card blurbs already on buy.html.
Images are the public watermarked previews (assets/thumbs + assets), never masters.

  python3 scripts/build_collection_coastal.py        # write page + wire links + sitemap/llms.txt
  python3 scripts/build_collection_coastal.py --check # dry run: exit 1 if anything would change
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = "--check" in sys.argv
FILE = "coastal-wall-art.html"
PAGE = ROOT / FILE
SITE = "https://moonlitwindows.com"
URL = f"{SITE}/{FILE}"
TODAY = "2026-10-16"
OG_SLUG = "amalfi-terrace-night"
MARK = 'data-collection="coastal"'

GROUPS = [
    ("mediterranean", "Mediterranean coast wall art", "coastal wall art poster and framed print",
     "Cliffside villages and a walled old town above a silver sea, with lit windows, bougainvillea and lemon trees.", [
        ("amalfi-terrace-night", "Amalfi Coast terraces with warm windows and lemon trees above a moonlit sea"),
        ("santorini-caldera-moon", "Santorini’s whitewashed terraces and blue domes above the moonlit caldera"),
        ("cinque-terre-manarola-moon", "Manarola’s pastel cliffside houses in the Cinque Terre above the moonlit Ligurian Sea"),
        ("dubrovnik-old-town-moon", "Dubrovnik’s medieval city walls and terracotta roofs above the moonlit Adriatic, with Fort Lovrijenac on its cliff"),
        ("coastal-cliffside-town", "A cliffside seaside town framed by purple flowers, with a glowing path down to the moonlit sea"),
        ("mediterranean-lantern-walk", "A lantern-lit stone walkway through Mediterranean houses toward a moonlit sea"),
    ]),
    ("atlantic-pacific", "Ocean cliffs and wild shores", "ocean wall art poster and framed print",
     "Surf, sea stacks, tidal water and a South Pacific lagoon under a full moon, from the west of Ireland to Kauai and Bora Bora.", [
        ("cliffs-of-moher-moon", "O’Brien’s Tower on the Cliffs of Moher above moonlit Atlantic surf and a sea stack"),
        ("big-sur-bixby-bridge-moon", "Bixby Creek Bridge above a Big Sur cove with silver Pacific surf under a full moon"),
        ("na-pali-coast-moon", "Emerald Na Pali Coast cliffs on Kauai plunging into a turquoise Pacific under a full moon"),
        ("bora-bora-lagoon-moon", "Overwater bungalows on Bora Bora’s turquoise lagoon, with palms and Mount Otemanu under a full moon"),
        ("iceland-black-sand-moon", "Moonlight on wet black sand and basalt sea stacks on an Icelandic shore"),
        ("mont-saint-michel-moon", "Mont Saint-Michel abbey rising from silver tidal water with warm windows at night"),
        ("faroe-gasadalur-moon", "Múlafossur waterfall dropping from Gásadalur’s green sea cliffs into the moonlit Atlantic"),
    ]),
    ("fjords-bays", "Fjord and bay wall art", "fjord wall art poster and framed print",
     "Sheltered northern water, a Highland sea loch and a calm Asian bay: mirror-still reflections between steep walls of rock.", [
        ("lofoten-reine-moon", "Red rorbu cabins on stilts along a mirror-still Lofoten fjord at Reine under a full moon"),
        ("norwegian-stave-church-fjord", "A wooden stave church glowing above a deep, misty Norwegian fjord at night"),
        ("northern-lights-fjord", "Northern lights over a calm fjord framed by snowy mountains and distant warm lights"),
        ("ha-long-bay-moon", "Limestone karsts and lantern-lit junks on calm, moonlit Ha Long Bay"),
        ("eilean-donan-castle-moon", "Eilean Donan Castle on its islet in Loch Duich, a Highland sea loch, with an arched stone bridge under a full moon"),
    ]),
]
SLUGS = [s for _, _, _, _, items in GROUPS for s, _ in items]
N = len(SLUGS)

TITLE = "Coastal Wall Art: Moonlit Ocean & Seaside Posters, Framed Prints | Moonlit Windows"
DESC = f"Coastal wall art: {N} moonlit seaside posters, from Amalfi and Santorini to Big Sur and Bora Bora. Poster $35, framed $69, mural $149, shipping included."
H1 = "Coastal Wall Art: Moonlit Ocean, Seaside and Fjord Prints"

FAQ = [
    ("What sizes and formats are available?",
     "Every piece comes as a 12×18 in enhanced matte poster ($35), the same 12×18 print in a black frame ($69), or a 4×6 ft (48×72 in) peel and stick wall mural on removable polyester ($149). Shipping is included on all three."),
    ("Are these real places?",
     "Most are named coasts reimagined at night: the Amalfi Coast, Santorini, Manarola in the Cinque Terre, Dubrovnik on the Adriatic, the Cliffs of Moher, Bixby Creek Bridge on Big Sur, the Na Pali Coast on Kauai, the lagoon of Bora Bora, Mont Saint-Michel, Gásadalur in the Faroe Islands, Reine in Lofoten, Eilean Donan Castle on Loch Duich and Ha Long Bay. Iceland Black Sand Moon and Norwegian Stave Church Fjord evoke those coastlines rather than one exact viewpoint, and Coastal Cliffside Town, Mediterranean Lantern Walk and Northern Lights Fjord are imagined scenes."),
    ("Is this beach decor?",
     "These are night scenes of seaside towns, ocean cliffs and fjords rather than sunny beach prints; Bora Bora Lagoon Moon comes closest to tropical decor, with palms and overwater bungalows on a moonlit lagoon, and Iceland Black Sand Moon shows a black-sand shore. If you want coastal decor that still feels calm in a bedroom, the moonlight keeps the palette soft and deep blue."),
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

def card(it, alt, suffix, info):
    cls, w, blurb = info
    s, t, st, a = it["slug"], html.escape(it["title"]), it["stripe"], it["asset"]
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
        {"@type": "CollectionPage", "name": "Coastal Wall Art: Moonlit Ocean, Seaside and Fjord Prints",
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
            {"@type": "ListItem", "position": 3, "name": "Coastal Wall Art", "item": URL}]}]}
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
  <meta property="og:image:alt" content="{og_item['title']} coastal wall art poster" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{T}" />
  <meta name="twitter:description" content="{DESC}" />
  <meta name="twitter:image" content="{og}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=Outfit:wght@380;560;650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json" data-ld="collection-coastal">
{ld(sel)}
  </script>
  <script type="application/ld+json" data-ld="faq-coastal">
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
    <p class="note breadcrumb"><a href="./">Home</a> › <a href="./buy.html">Shop</a> › Coastal wall art</p>
    <section class="hero left">
      <div class="kicker">Collection</div>
      <h1>{H1}</h1>
      <p class="sale-line">{N} coastal and ocean art prints · $35 poster · $69 framed · 12×18 · $149 peel &amp; stick wall mural (4×6 ft) · shipping included</p>
      <p class="answer-first">These are {N} moonlit coastal prints, each sold as a 12×18 in poster for $35, a black-framed print for $69, or a 4×6 ft peel and stick wall mural for $149, with shipping included. Most show real coastlines at night, among them the Amalfi Coast, Santorini, the Cinque Terre, the Cliffs of Moher, Big Sur and the Lofoten Islands, with a full moon on the sea and warm windows along the shore.</p>
      <p>The sea at night is mostly light on water: a moon path across the waves, surf turned silver, a village glowing above a cove. That makes these the most open, airy pieces in the Night Windows series, while the deep blues keep them calm enough for a bedroom.</p>
      <p class="note">Jump to: <a href="#mediterranean">Mediterranean</a> · <a href="#atlantic-pacific">Ocean cliffs</a> · <a href="#fjords-bays">Fjords and bays</a> · <a href="#choose">Choosing a piece</a> · <a href="#faq">FAQ</a></p>
    </section>

{grids}

    <section class="prose">
      <h2 id="choose">How to choose coastal wall art for your room</h2>
      <p><strong>Beach house or seaside flat.</strong> Echo the view without repeating it: the lit terraces of {P("amalfi-terrace-night", "Amalfi Terrace Night")} or {P("cinque-terre-manarola-moon", "Manarola")} bring the village, not just the water. A framed 12×18 print suits a hallway, a mantel or the wall beside a window.</p>
      <p><strong>Bedroom.</strong> Quiet water reads calmest: {P("lofoten-reine-moon", "Reine in Lofoten")} with its mirror-still fjord, {P("ha-long-bay-moon", "Ha Long Bay")} with lantern-lit junks, or the tidal shimmer around {P("mont-saint-michel-moon", "Mont Saint-Michel")}.</p>
      <p><strong>Living room or a feature wall.</strong> Big cliffs carry across a room: {P("cliffs-of-moher-moon", "the Cliffs of Moher")}, {P("big-sur-bixby-bridge-moon", "Bixby Creek Bridge on Big Sur")} and {P("santorini-caldera-moon", "Santorini’s caldera")}. To make the coast fill the wall, the same artwork comes as a 4×6 ft (48×72 in) peel and stick wall mural; the <a href="./peel-and-stick-wall-murals.html">peel and stick wall murals collection</a> covers measuring and wall prep.</p>
      <p><strong>Office or study.</strong> The northern scenes are moodier and less busy: {P("northern-lights-fjord", "Northern Lights Fjord")}, {P("norwegian-stave-church-fjord", "Norwegian Stave Church Fjord")} or {P("iceland-black-sand-moon", "Iceland Black Sand Moon")}.</p>
      <p><strong>A trip to remember.</strong> If you drove Highway 1, walked the Cinque Terre trail or stood on the Cliffs of Moher, the place-named prints are made for that. Pairs work well too: Amalfi with Santorini for a Mediterranean wall, or Lofoten with the Faroes for the North Atlantic.</p>
      <p>Prefer still lakes or high peaks? See the <a href="./lake-wall-art.html">lake and waterfall wall art collection</a> and the <a href="./mountain-wall-art.html">mountain wall art collection</a>. Castles, canals and old towns are in the <a href="./european-wall-art.html">European wall art collection</a>, and Mount Fuji, Kyoto and the temples of Angkor and Bagan in the <a href="./asian-wall-art.html">Asian wall art collection</a>. Not sure about size? The <a href="./guide-print-sizes.html">print size guide</a> compares the poster, framed print and mural.</p>
    </section>

    <section class="prose" id="faq">
      <h2>Questions about these coastal prints</h2>
{faq_html()}
      <p>Looking for something else? Browse <a href="./night-windows.html">every Night Windows piece</a> or the <a href="./buy.html">full shop</a>.</p>
    </section>
  </div>
  <footer class="site-footer">
    <div class="wrap"><div class="footer-shop"><a href="./buy.html">Shop Posters, Prints &amp; Wall Murals</a> · $35 poster · $69 framed · 12×18 · shipping included</div>
      <div><a href="./">Gallery</a> · <a href="./mountain-wall-art.html">Mountain wall art</a> · <a href="./lake-wall-art.html">Lake and waterfall wall art</a> · <a href="./coastal-wall-art.html">Coastal wall art</a> · <a href="./asian-wall-art.html">Asian wall art</a> · <a href="./european-wall-art.html">European wall art</a> · <a href="./peel-and-stick-wall-murals.html">Peel and stick wall murals</a> · Night Shade Art on Instagram: <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a></div>
    </div>
    <div class="operated-by footer-legal"><p class="footer-legal-links"><a href="./terms.html">Terms</a> · <a href="./privacy.html">Privacy</a> · <a href="./disclaimer.html">Disclaimer</a> · <a href="./contact.html">Contact</a></p></div>
  </footer>
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "899375a6262144aabf5184589abd580c"}}'></script>
</body>
</html>
'''

PIECE_LINK = (f'<p class="note collection-link" {MARK}>Part of the '
              '<a href="../coastal-wall-art.html">coastal wall art collection</a>: '
              f'{N} moonlit ocean, seaside and fjord posters, framed prints and wall murals.</p>')

def edits():
    out = {}
    def put(rel, old, new):
        if new != old: out[rel] = new
    for s in SLUGS:
        rel = f"pieces/{s}.html"; src = (ROOT / rel).read_text(encoding="utf-8")
        if MARK in src:
            new = re.sub(rf'<p class="note collection-link" {re.escape(MARK)}>.*?</p>', lambda m: PIECE_LINK, src, count=1)
        else:
            ms = list(re.finditer(r'\n(\s*)<p class="note collection-link" data-collection="[a-z]+">.*?</p>\n', src))
            if ms:
                m = ms[-1]; new = src[:m.end()] + m.group(1) + PIECE_LINK + "\n" + src[m.end():]
            else:
                new = src; print("WARN no collection-link anchor on", s)
        put(rel, src, new)
    rel = "buy.html"; src = (ROOT / rel).read_text(encoding="utf-8")
    if MARK not in src:
        a = '<a data-collection="lakes" href="./lake-wall-art.html">Lake &amp; waterfall wall art</a>'
        if a in src: put(rel, src, src.replace(a, a + f' · <a {MARK} href="./coastal-wall-art.html">Coastal wall art</a>', 1))
        else: print("WARN buy.html theme anchor not found")
    rel = "night-windows.html"; src = (ROOT / rel).read_text(encoding="utf-8")
    if MARK not in src:
        a = 'href="./lake-wall-art.html">lake and waterfall wall art collection</a>.</p>'
        if a in src: put(rel, src, src.replace(a, a[:-4] + f' Seaside villages, ocean cliffs and fjords are in the <a {MARK} href="./coastal-wall-art.html">coastal wall art collection</a>.</p>', 1))
        else: print("WARN night-windows anchor not found")
    rel = "llms.txt"; src = (ROOT / rel).read_text(encoding="utf-8")
    if URL in src:
        put(rel, src, re.sub(rf"(- \[Coastal\ wall\ art\]\({re.escape(URL)}\): )\d+ ", rf"\g<1>{N} ", src, count=1))
    if URL not in src:
        m = re.search(r"- \[Lake and waterfall wall art\]\([^)]*\):[^\n]*\n", src)
        line = (f"- [Coastal wall art]({URL}): {N} moonlit ocean, seaside and fjord posters ($35), framed prints ($69) "
                "and wall murals ($149), from the Amalfi Coast, Santorini and Cinque Terre to the Cliffs of Moher, Big Sur and Lofoten, with a room guide and FAQ\n")
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
        st = items[s]["stripe"]; assert st["status"] == "live", s
        for k in ("muralUrl", "posterUrl", "framedUrl"):
            assert str(st.get(k, "")).startswith("https://buy.stripe.com/"), (s, k)
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
