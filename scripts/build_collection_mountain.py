#!/usr/bin/env python3
"""Build mountain-wall-art.html: a themed collection page (mountain wall art posters,
framed prints, wall murals) and wire internal links to it. Idempotent.

Cards reuse the live Stripe links from products.json and the card blurbs already on buy.html.
Images are the public watermarked previews (assets/thumbs + assets), never masters.
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "mountain-wall-art.html"
URL = "https://moonlitwindows.com/mountain-wall-art.html"
SLUGS = [  # order = how they appear on the page
    "matterhorn-alpine-moon", "dolomites-tre-cime-moon", "mount-fuji-pagoda-moon",
    "lauterbrunnen-valley-moon", "isle-of-skye-storr-moon", "yosemite-half-dome-moon",
    "banff-lake-louise-moon", "patagonia-lake-peaks", "zhangjiajie-pillars-moon",
    "machu-picchu-mist", "scottish-highlands-loch", "snowy-peaks-above-clouds",
    "moonlit-alpine-meadow",
]
TITLE = "Mountain Wall Art Posters, Framed Prints &amp; Wall Murals | Moonlit Windows"
DESC = ("Mountain wall art for sale: 13 moonlit mountain posters and framed prints, from the "
        "Matterhorn, Dolomites and Mount Fuji to Yosemite and the Isle of Skye. 12×18 poster $29, "
        "framed print $69, 4×6 ft peel and stick wall mural $149, shipping included.")
LINK_MARK = 'data-collection="mountain"'

def blurbs():
    b = (ROOT / "buy.html").read_text()
    out = {}
    for m in re.finditer(r'<article class="(card[^"]*)" id="([^"]+)">.*?\.jpg (\d+)w".*?<h2>.*?</h2>\s*<p>(.*?)</p>', b, re.S):
        out[m.group(2)] = (m.group(1), m.group(3), m.group(4))
    return out

def card(it, info):
    cls, w, blurb = info
    s, t, st = it["slug"], html.escape(it["title"]), it["stripe"]
    a = it["asset"]
    return f'''      <article class="{cls}" id="{s}">
        <a href="./pieces/{s}.html"><img src="./assets/thumbs/{a}" srcset="./assets/thumbs/{a} 600w, ./assets/{a} {w}w" sizes="(max-width: 640px) 92vw, (max-width: 1100px) 45vw, 22rem" decoding="async" alt="{t} mountain wall art poster and framed print" loading="lazy"></a>
        <div class="meta">
          <h3><a href="./pieces/{s}.html">{t}</a></h3>
          <p>{blurb}</p>
          <p class="price-line">$29 poster · $69 framed (12×18) · $149 peel &amp; stick wall mural (4×6 ft)</p>
          <div class="actions buy-actions">
            <a class="btn" data-buy="{s}" data-sku="poster" href="{st['posterUrl']}">Poster · $29</a>
            <a class="btn secondary" data-buy="{s}" data-sku="framed" href="{st['framedUrl']}">Framed · $69</a>
            <a class="btn secondary" data-buy="{s}" data-sku="mural" href="{st['muralUrl']}">Wall mural · $149</a>
          </div>
        </div>
      </article>'''

def ld(items):
    g = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Mountain Wall Art Posters, Framed Prints & Wall Murals",
         "url": URL, "description": html.unescape(DESC),
         "isPartOf": {"@type": "WebSite", "name": "Moonlit Windows", "url": "https://moonlitwindows.com/"},
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": f"{it['title']} mountain poster & framed print",
              "url": f"https://moonlitwindows.com/pieces/{it['slug']}.html"} for i, it in enumerate(items)]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://moonlitwindows.com/"},
            {"@type": "ListItem", "position": 2, "name": "Shop", "item": "https://moonlitwindows.com/buy.html"},
            {"@type": "ListItem", "position": 3, "name": "Mountain Wall Art", "item": URL}]}]}
    return json.dumps(g, ensure_ascii=False, indent=2)

# FAQPage JSON-LD: must mirror the visible "Questions about these mountain prints" section word for word.
FAQ = [
    ("What sizes and formats are available?",
     "A 12×18 inch enhanced matte poster ($29), the same 12×18 print in a black frame ($69), and a 4×6 ft (48×72 in) peel and stick wall mural on removable polyester ($149). Shipping is included on all three."),
    ("How long does a mural take?", "Murals are printed to order and ship in 1–2 weeks."),
    ("Are these real places?",
     "Most are named landmarks, reimagined at night. Patagonia Lake Peaks and Scottish Highlands Loch evoke those regions rather than one exact viewpoint, and Moonlit Alpine Meadow and Snowy Peaks Above Clouds are imagined alpine scenes."),
    ("How do I pay?", "Every button opens secure Stripe checkout, and your receipt arrives by email."),
]

def faq_ld():
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False, indent=2)

def page(items, bl):
    cards = "\n".join(card(it, bl[it["slug"]]) for it in items)
    og = "https://moonlitwindows.com/assets/" + items[0]["asset"]
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-663R8VD62L"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-663R8VD62L');</script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLE}</title>
  <meta name="description" content="{DESC}" />
  <link rel="canonical" href="{URL}">
  <meta property="og:site_name" content="Moonlit Windows" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{TITLE}" />
  <meta property="og:description" content="{DESC}" />
  <meta property="og:url" content="{URL}">
  <meta property="og:image" content="{og}" />
  <meta property="og:image:alt" content="Matterhorn Alpine Moon mountain wall art poster" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{TITLE}" />
  <meta name="twitter:description" content="{DESC}" />
  <meta name="twitter:image" content="{og}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=Outfit:wght@380;560;650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json" data-ld="collection-mountain">
{ld(items)}
  </script>
  <script type="application/ld+json" data-ld="faq-mountain">
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
    <p class="note breadcrumb"><a href="./">Home</a> › <a href="./buy.html">Shop</a> › Mountain wall art</p>
    <section class="hero left">
      <div class="kicker">Collection</div>
      <h1>Mountain Wall Art: Moonlit Mountain Posters &amp; Framed Prints</h1>
      <p class="sale-line">13 mountain art prints · $29 poster · $69 framed · 12×18 · $149 peel &amp; stick wall mural (4×6 ft) · shipping included</p>
      <p>Every piece in this collection is a mountain scene at night: real peaks you can find on a map, seen under a full moon, often with a few warm windows glowing in the valley. The Matterhorn over a still alpine lake, the three towers of the Dolomites’ Tre Cime, Mount Fuji behind the Chureito Pagoda, Yosemite’s Half Dome, Lake Louise in the Canadian Rockies, and the Old Man of Storr on the Isle of Skye are all here, along with quieter scenes like a wildflower meadow above an alpine village and snowy peaks above the clouds.</p>
      <p>Each one comes three ways: a 12×18 inch enhanced matte poster, the same print in a black frame, or a 4×6 ft peel and stick wall mural for a whole feature wall.</p>
    </section>

    <section class="prose">
      <h2>How to choose mountain wall art for your room</h2>
      <p><strong>Bedroom.</strong> Moonlit scenes are dark and blue by nature, so they sit well where you want the room to feel calm. The stillest pieces are the lake scenes: <a href="./pieces/banff-lake-louise-moon.html">Banff Lake Louise Moon</a> and <a href="./pieces/patagonia-lake-peaks.html">Patagonia Lake Peaks</a>, where turquoise water mirrors the peaks, and the misty <a href="./pieces/scottish-highlands-loch.html">Scottish Highlands Loch</a>. A framed 12×18 print fits above a nightstand or a small dresser.</p>
      <p><strong>Living room or a feature wall.</strong> Big, recognisable silhouettes read best from across a room: <a href="./pieces/matterhorn-alpine-moon.html">the Matterhorn</a>, <a href="./pieces/mount-fuji-pagoda-moon.html">Mount Fuji</a> and <a href="./pieces/yosemite-half-dome-moon.html">Half Dome</a>. If you want the mountain to fill the wall rather than hang on it, the 4×6 ft (48×72 in) peel and stick wall mural uses the same artwork, needs no paste, and comes off most smooth painted walls cleanly.</p>
      <p><strong>Office or hallway.</strong> Detailed scenes reward a closer look: <a href="./pieces/lauterbrunnen-valley-moon.html">Lauterbrunnen Valley</a> with its waterfall, <a href="./pieces/zhangjiajie-pillars-moon.html">Zhangjiajie’s stone pillars</a>, and <a href="./pieces/machu-picchu-mist.html">Machu Picchu in the mist</a>.</p>
      <p><strong>A place you have been.</strong> Many people buy mountain art to remember a trip. If you hiked the Dolomites, skied near Zermatt or drove the Skye loop, the place-named prints are meant for exactly that. Pairs work well too: the Matterhorn with the Dolomites for an Alps wall, or Skye with the Highlands loch for Scotland.</p>
      <p>Not sure which size suits your wall? The <a href="./guide-print-sizes.html">print size guide</a> walks through 12×18 placement, and every piece page has larger previews.</p>
    </section>

    <section class="grid" aria-label="Mountain wall art prints">
      <!-- collection:start -->
{cards}
      <!-- collection:end -->
    </section>

    <section class="prose">
      <h2>Questions about these mountain prints</h2>
      <p><strong>What sizes and formats are available?</strong> A 12×18 inch enhanced matte poster ($29), the same 12×18 print in a black frame ($69), and a 4×6 ft (48×72 in) peel and stick wall mural on removable polyester ($149). Shipping is included on all three.</p>
      <p><strong>How long does a mural take?</strong> Murals are printed to order and ship in 1–2 weeks.</p>
      <p><strong>Are these real places?</strong> Most are named landmarks, reimagined at night. Patagonia Lake Peaks and Scottish Highlands Loch evoke those regions rather than one exact viewpoint, and <a href="./pieces/moonlit-alpine-meadow.html">Moonlit Alpine Meadow</a> and <a href="./pieces/snowy-peaks-above-clouds.html">Snowy Peaks Above Clouds</a> are imagined alpine scenes.</p>
      <p><strong>How do I pay?</strong> Every button opens secure Stripe checkout, and your receipt arrives by email.</p>
      <p>Looking for something other than mountains? Browse <a href="./night-windows.html">all fifty Night Windows</a> or the <a href="./buy.html">full shop</a>.</p>
    </section>
  </div>
  <footer class="site-footer">
    <div class="wrap"><div class="footer-shop"><a href="./buy.html">Shop Posters, Prints &amp; Wall Murals</a> · $29 poster · $69 framed · 12×18 · shipping included</div>
      <div>© 2026 Joshua Israel Ventures LLC · Night Windows by Prompt Framed · Night Shade Art</div>
      <div><a href="./">Gallery</a> · <a href="./mountain-wall-art.html">Mountain wall art</a> · Night Shade Art on Instagram: <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a></div>
    </div>
    <div class="operated-by">Operated by Joshua Israel Ventures LLC</div>
  </footer>
</body>
</html>
'''

def wire_links():
    n = 0
    # piece pages: one line after "More windows like this"
    for s in SLUGS:
        p = ROOT / "pieces" / f"{s}.html"; src = p.read_text()
        if LINK_MARK in src: continue
        line = f'\n        <p class="note collection-link" {LINK_MARK}>Part of the <a href="../mountain-wall-art.html">mountain wall art collection</a>: 13 moonlit mountain posters, framed prints and wall murals.</p>'
        new, k = re.subn(r'(<p class="note related-windows">.*?</p>)', r'\1' + line.replace('\\', r'\\'), src, count=1, flags=re.S)
        if not k:  # older pages: put it right under the mural note in the buy box
            new, k = re.subn(r'(<p class="note mural-note">.*?</p>)', lambda m: m.group(1) + line.replace('\n        ', '\n          '), src, count=1, flags=re.S)
        if k: p.write_text(new); n += 1
        else: print("WARN no anchor on", s)
    # hub: mountains paragraph
    hub = ROOT / "night-windows.html"; src = hub.read_text()
    if LINK_MARK not in src:
        src2 = src.replace("and <a href=\"./pieces/yosemite-half-dome-moon.html\">Yosemite’s Half Dome</a>.</p>",
            "and <a href=\"./pieces/yosemite-half-dome-moon.html\">Yosemite’s Half Dome</a>. See them together in the <a " + LINK_MARK + " href=\"./mountain-wall-art.html\">mountain wall art collection</a>.</p>", 1)
        if src2 != src: hub.write_text(src2); n += 1
        else: print("WARN hub anchor not found")
    # buy.html hero: after the mural note
    buy = ROOT / "buy.html"; src = buy.read_text()
    if LINK_MARK not in src:
        anchor = '</p>\n      <p class="price-line">$29 poster · $69 framed (12×18) · $149 peel &amp; stick wall mural (4×6 ft)</p>\n    </section>'
        src2 = src.replace(anchor, anchor[:-len('\n    </section>')] + '\n      <p class="note" ' + LINK_MARK + '>Browse by theme: <a href="./mountain-wall-art.html">Mountain wall art</a></p>\n    </section>', 1)
        if src2 != src: buy.write_text(src2); n += 1
        else: print("WARN buy hero anchor not found")
    return n

def sitemap():
    sm = ROOT / "sitemap.xml"; src = sm.read_text()
    if URL in src: return False
    entry = (f'  <url><loc>{URL}</loc><lastmod>2026-10-07</lastmod>'
             f'<image:image><image:loc>https://moonlitwindows.com/assets/35-matterhorn-alpine-moon.jpg</image:loc></image:image></url>\n')
    sm.write_text(src.replace("</urlset>", entry + "</urlset>")); return True

def main():
    items = {p["slug"]: p for p in json.load(open(ROOT / "products.json"))}
    sel = [items[s] for s in SLUGS]
    for it in sel:
        assert it["stripe"]["status"] == "live" and it["stripe"].get("muralUrl"), it["slug"]
        assert it["asset"].endswith(".jpg") and (ROOT / "assets" / it["asset"]).exists(), it["asset"]
    bl = blurbs()
    PAGE.write_text(page(sel, bl))
    print("page written; links wired:", wire_links(), "; sitemap added:", sitemap())

if __name__ == "__main__":
    sys.exit(main())
