#!/usr/bin/env python3
"""Build european-wall-art.html: a buyer-intent collection page for European castle, old town and
village wall art (posters $35, framed prints $69, 4x6 ft peel and stick wall murals $149), and wire
internal links to it. Idempotent. Modelled on build_collection_asian.py.

Cards reuse the live Stripe links from products.json and the card blurbs already on buy.html.
Images are the public watermarked previews (assets/thumbs + assets), never masters.

  python3 scripts/build_collection_european.py        # write page + wire links + sitemap/llms.txt
  python3 scripts/build_collection_european.py --check # dry run: exit 1 if anything would change
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = "--check" in sys.argv
FILE = "european-wall-art.html"
PAGE = ROOT / FILE
SITE = "https://moonlitwindows.com"
URL = f"{SITE}/{FILE}"
TODAY = "2026-10-19"
OG_SLUG = "neuschwanstein-castle-moon"
MARK = 'data-collection="european"'

GROUPS = [
    ("castles", "Castle wall art", "castle wall art poster and framed print",
     "Fairy-tale towers, island strongholds and clifftop monasteries, each lit from within under a full moon.", [
        ("neuschwanstein-castle-moon", "Neuschwanstein Castle’s white towers on a forested crag above a misty valley, with a full moon over the Bavarian Alps"),
        ("hohenzollern-castle-moon", "Hohenzollern Castle’s towers and lit windows rising above a sea of valley mist in the Swabian Alb, Germany, beneath a cloud-veiled moon"),
        ("eilean-donan-castle-moon", "Eilean Donan Castle on its islet in Loch Duich, an arched stone bridge over still water below a cloud-veiled moon"),
        ("sintra-pena-palace-moon", "The golden Pena Palace above misty Sintra forests in Portugal under a cloud-veiled full moon"),
        ("mont-saint-michel-moon", "The abbey of Mont Saint-Michel rising from silver tidal water with warm windows under moonlight"),
        ("meteora-monasteries-moon", "Meteora’s monasteries on sheer stone pillars above a misty valley in Thessaly, Greece, under a full moon"),
    ]),
    ("old-towns", "European old town and city wall art", "European city wall art poster and framed print",
     "Canals, bridges, walls and cobbled lanes: Venice, Florence, Prague, Bruges, Colmar, Dubrovnik, Rothenburg and Hallstatt after dark.", [
        ("venetian-canal-moonrise", "A quiet Venetian canal with stone bridges, warm windows on the water and a lone gondola under moonlight"),
        ("ponte-vecchio-florence-moon", "Florence’s Ponte Vecchio and its lit shopfronts spanning the calm Arno on stone arches, Tuscany, Italy, beneath a cloud-veiled moon"),
        ("prague-charles-bridge-moon", "Prague’s Charles Bridge and its Gothic towers over the Vltava, with Prague Castle lit on the hill beneath a cloud-veiled moon"),
        ("bruges-canal-moon", "The Rozenhoedkaai in Bruges, Belgium, with stepped gables, a willow and the Belfry mirrored in the canal beneath a cloud-veiled moon"),
        ("dubrovnik-old-town-moon", "Dubrovnik’s medieval walls and terracotta roofs above the calm Adriatic, with Fort Lovrijenac on its cliff beneath a cloud-veiled moon"),
        ("rothenburg-old-town-moon", "Lamplit cobblestones forking around a half-timbered house in Rothenburg ob der Tauber, Germany, beneath a cloud-veiled moon"),
        ("colmar-petite-venise-moon", "Half-timbered houses and flower boxes mirrored in the canal of Colmar’s Petite Venise in Alsace, France, beneath a cloud-veiled moon"),
        ("hallstatt-lake-moon", "Hallstatt’s church steeple and lakeside houses mirrored in still alpine water in Austria under moonlight"),
    ]),
    ("countryside", "European countryside and village wall art", "countryside wall art poster and framed print",
     "Lavender fields, cypress roads, honey-stone cottages and a stone viaduct across a Highland glen: the gentlest scenes in the collection.", [
        ("provence-lavender-moon", "Rows of moonlit lavender in Provence, France, leading to a warm stone farmhouse under a full moon"),
        ("tuscany-cypress-hills", "A cypress-lined road winding through moonlit Tuscan hills toward a warm stone villa in Italy"),
        ("bibury-arlington-row-moon", "The honey-stone cottages of Arlington Row beside the River Coln in Bibury, England, under a cloud-veiled moon"),
        ("glenfinnan-viaduct-moon", "The curving stone arches of the Glenfinnan Viaduct across a Highland glen toward Loch Shiel, Scotland, beneath a cloud-veiled moon"),
    ]),
]
SLUGS = [s for _, _, _, _, items in GROUPS for s, _ in items]
N = len(SLUGS)

TITLE = "European Wall Art: Castle & Old Town Posters, Framed Prints | Moonlit Windows"
DESC = f"European wall art: {N} moonlit castle and old town posters, from Neuschwanstein to Venice and Prague. Poster $35, framed $69, mural $149, shipping included."
H1 = "European Wall Art: Moonlit Castles, Old Towns and Villages"

FAQ = [
    ("What sizes and formats are available?",
     "Every piece comes as a 12×18 in enhanced matte poster ($35), the same 12×18 print in a black frame ($69), or a 4×6 ft (48×72 in) peel and stick wall mural on removable polyester ($149). Shipping is included on all three."),
    ("Are these real places?",
     "Most are named places reimagined at night: Neuschwanstein, Hohenzollern Castle in the Swabian Alb, Eilean Donan, the Pena Palace in Sintra, Mont Saint-Michel, Meteora, Prague’s Charles Bridge, Florence’s Ponte Vecchio, the Rozenhoedkaai in Bruges, Colmar’s Petite Venise, Dubrovnik, Rothenburg, Hallstatt, Arlington Row in Bibury and the Glenfinnan Viaduct in the Scottish Highlands. Venetian Canal Moonrise, Provence Lavender Moon and Tuscany Cypress Hills evoke those places rather than one exact viewpoint."),
    ("Do you have castle wall art for a child’s room?",
     "Yes. Neuschwanstein Castle Moon is the most fairy-tale piece in the series, and Eilean Donan and Mont Saint-Michel have the same storybook feel with calmer, darker water. All of them are soft night scenes with a full moon rather than anything spooky."),
    ("Which pieces work as a travel souvenir?",
     "The place-named prints make a good reminder of a trip: Prague Charles Bridge Moon, Bruges Canal Moon, Dubrovnik Old Town Moon or Hallstatt Lake Moon for a city break, or Provence and Tuscany for a summer in the countryside."),
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
        {"@type": "CollectionPage", "name": H1,
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
            {"@type": "ListItem", "position": 3, "name": "European Wall Art", "item": URL}]}]}
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
  <meta property="og:image:alt" content="{og_item['title']} castle wall art poster" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{T}" />
  <meta name="twitter:description" content="{DESC}" />
  <meta name="twitter:image" content="{og}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=Outfit:wght@380;560;650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json" data-ld="collection-european">
{ld(sel)}
  </script>
  <script type="application/ld+json" data-ld="faq-european">
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
    <p class="note breadcrumb"><a href="./">Home</a> › <a href="./buy.html">Shop</a> › European wall art</p>
    <section class="hero left">
      <div class="kicker">Collection</div>
      <h1>{H1}</h1>
      <p class="sale-line">{N} European castle, city and village prints · $35 poster · $69 framed · 12×18 · $149 peel &amp; stick wall mural (4×6 ft) · shipping included</p>
      <p class="answer-first">These are {N} moonlit European castle, old town and countryside prints, each sold as a 12×18 in poster for $35, a black-framed print for $69, or a 4×6 ft peel and stick wall mural for $149, with shipping included. Most show real places at night, among them Neuschwanstein, Eilean Donan, Mont Saint-Michel, Venice, Prague, Bruges, Dubrovnik and Hallstatt, with a full moon overhead and warm light in the windows below.</p>
      <p>What ties this group together is lamplight on old stone: lit towers on their rocks, windows glowing over canals and cobbles, a farmhouse at the end of a lavender row. They are the warmest pieces in the Night Windows series, with gold and amber against deep blue rather than the cooler greens of the mountain and lake scenes.</p>
      <p class="note">Jump to: <a href="#castles">Castles</a> · <a href="#old-towns">Old towns and cities</a> · <a href="#countryside">Countryside and villages</a> · <a href="#choose">Choosing a piece</a> · <a href="#faq">FAQ</a></p>
    </section>

{grids}

    <section class="prose">
      <h2 id="choose">How to choose European wall art for your room</h2>
      <p><strong>Bedroom.</strong> Go for quiet water and soft light: {P("bruges-canal-moon", "Bruges Canal Moon")} with its mirrored gables, {P("hallstatt-lake-moon", "Hallstatt")} on its still lake, or the lavender rows of {P("provence-lavender-moon", "Provence Lavender Moon")}. More bedroom picks and size tips are in the <a data-guide="bedroom" href="./moon-poster-bedroom.html">moon poster for bedroom</a> guide.</p>
      <p><strong>Child’s room or nursery.</strong> Castles do the storytelling: {P("neuschwanstein-castle-moon", "Neuschwanstein")} above its misty valley, {P("eilean-donan-castle-moon", "Eilean Donan")} on its loch, or {P("mont-saint-michel-moon", "Mont Saint-Michel")} rising from the tide.</p>
      <p><strong>Living room or a feature wall.</strong> Wide, recognisable views carry across a room: {P("prague-charles-bridge-moon", "Prague’s Charles Bridge")}, {P("dubrovnik-old-town-moon", "Dubrovnik’s walled old town")} or {P("meteora-monasteries-moon", "the monasteries of Meteora")}. To make one fill the wall, the same artwork comes as a 4×6 ft (48×72 in) peel and stick wall mural; the <a href="./peel-and-stick-wall-murals.html">peel and stick wall murals collection</a> covers measuring and wall prep.</p>
      <p><strong>Kitchen, dining room or hallway.</strong> The countryside and village pieces feel homely: {P("tuscany-cypress-hills", "Tuscany Cypress Hills")}, the cottages of {P("bibury-arlington-row-moon", "Bibury’s Arlington Row")} or the lamplit lane in {P("rothenburg-old-town-moon", "Rothenburg Old Town Moon")}.</p>
      <p><strong>A trip to remember.</strong> If you crossed the Charles Bridge, walked Dubrovnik’s walls or drove through Tuscany, the place-named prints are made for that. Pairs work well too: {P("venetian-canal-moonrise", "Venice")} with Bruges or {P("colmar-petite-venise-moon", "Colmar")} for a canal wall, Neuschwanstein with Rothenburg for Bavaria, or {P("sintra-pena-palace-moon", "Sintra’s Pena Palace")} with Mont Saint-Michel for a castles pair.</p>
      <p>Prefer wild landscapes? See the <a href="./mountain-wall-art.html">mountain wall art collection</a>, the <a href="./lake-wall-art.html">lake and waterfall wall art collection</a>, the <a href="./coastal-wall-art.html">coastal wall art collection</a> and the <a href="./asian-wall-art.html">Asian wall art collection</a>. Not sure about size? The <a href="./guide-print-sizes.html">print size guide</a> compares the poster, framed print and mural.</p>
    </section>

    <section class="prose" id="faq">
      <h2>Questions about these European castle and old town prints</h2>
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
              '<a href="../european-wall-art.html">European wall art collection</a>: '
              f'{N} moonlit castle, old town and village posters, framed prints and wall murals.</p>')

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
        a = '<a data-collection="asian" href="./asian-wall-art.html">Asian wall art</a>'
        if a in src: put(rel, src, src.replace(a, a + f' · <a {MARK} href="./european-wall-art.html">European wall art</a>', 1))
        else: print("WARN buy.html theme anchor not found")
    rel = "night-windows.html"; src = (ROOT / rel).read_text(encoding="utf-8")
    if MARK not in src:
        m = re.search(r'(<p>Castles and old towns:.*?)(</p>)', src)
        if m: put(rel, src, src[:m.end(1)] + f' See them together in the <a {MARK} href="./european-wall-art.html">European wall art collection</a>.' + src[m.end(1):])
        else: print("WARN night-windows anchor not found")
    rel = "llms.txt"; src = (ROOT / rel).read_text(encoding="utf-8")
    if URL in src:
        put(rel, src, re.sub(rf"(- \[European\ wall\ art\]\({re.escape(URL)}\): )\d+ ", rf"\g<1>{N} ", src, count=1))
    if URL not in src:
        m = re.search(r"- \[Asian wall art\]\([^)]*\):[^\n]*\n", src)
        line = (f"- [European wall art]({URL}): {N} moonlit castle, old town and village posters ($35), framed prints ($69) "
                "and wall murals ($149), from Neuschwanstein, Venice and Prague to Bruges, Dubrovnik, Provence and Tuscany, with a room guide and FAQ\n")
        if m: put(rel, src, src[:m.end()] + line + src[m.end():])
        else: print("WARN llms.txt anchor not found")
    return out

def sitemap(changed):
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8"); n = sm
    if f"<loc>{URL}</loc>" not in n:
        asset = json.loads((ROOT / "products.json").read_text())
        asset = next(i["asset"] for i in asset if i["slug"] == OG_SLUG)
        entry = f'  <url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><image:image><image:loc>{SITE}/assets/{asset}</image:loc></image:image></url>\n'
        i = n.find(f"<url><loc>{SITE}/asian-wall-art.html</loc>")
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
