#!/usr/bin/env python3
"""Build asian-wall-art.html: a buyer-intent collection page for Asian and Japanese wall art
(posters $35, framed prints $69, 4x6 ft peel and stick wall murals $149), and wire internal
links to it. Idempotent. Modelled on build_collection_coastal.py.

Cards reuse the live Stripe links from products.json and the card blurbs already on buy.html.
Images are the public watermarked previews (assets/thumbs + assets), never masters.

  python3 scripts/build_collection_asian.py        # write page + wire links + sitemap/llms.txt
  python3 scripts/build_collection_asian.py --check # dry run: exit 1 if anything would change
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = "--check" in sys.argv
FILE = "asian-wall-art.html"
PAGE = ROOT / FILE
SITE = "https://moonlitwindows.com"
URL = f"{SITE}/{FILE}"
TODAY = "2026-10-16"
OG_SLUG = "mount-fuji-pagoda-moon"
MARK = 'data-collection="asian"'

GROUPS = [
    ("japan", "Japanese wall art", "Japanese wall art poster and framed print",
     "Mount Fuji, a Kyoto bamboo grove and a temple garden pond: the quietest corner of the series.", [
        ("mount-fuji-pagoda-moon", "The red Chureito Pagoda among cherry blossoms with snow-capped Mount Fuji under a full moon"),
        ("kyoto-bamboo-moon", "A misty Kyoto bamboo grove path lit by filtered moonlight"),
        ("japanese-temple-pond", "A still Japanese temple pond reflecting the full moon, with stone lanterns, pines and maples"),
    ]),
    ("china", "Chinese landscape wall art", "Chinese landscape wall art poster and framed print",
     "Karst peaks, sandstone pillars and the Great Wall, each wrapped in moonlit mist.", [
        ("great-wall-mutianyu-moon", "The Great Wall at Mutianyu winding over forested ridges with warm watchtowers under a full moon"),
        ("guilin-li-river-moon", "Karst peaks along the Li River near Guilin with a lantern on a bamboo raft under a full moon"),
        ("zhangjiajie-pillars-moon", "Zhangjiajie’s sandstone pillars rising through forest mist in moonlight"),
    ]),
    ("southeast-asia-india", "South and Southeast Asian temple wall art", "temple wall art poster and framed print",
     "Temples, stupas, a rock fortress, rice terraces and a lantern-lit bay, from Agra, Sigiriya and Angkor to Bali and Ha Long.", [
        ("taj-mahal-moon", "The white marble Taj Mahal above its reflecting pool and cypress gardens under a full moon"),
        ("sigiriya-rock-moon", "Sigiriya’s flat-topped Lion Rock in Sri Lanka rising above the jungle, its terraced water gardens and pools mirroring a full moon"),
        ("angkor-wat-moon", "Angkor Wat’s towers above a lotus pond with palms and the full moon reflected in the water"),
        ("bagan-temples-night", "Brick stupas scattered across the misty plain of Bagan under moonlight"),
        ("bali-jungle-temple", "Mossy temple steps climbing through Balinese jungle mist with lanterns and moonbeams"),
        ("ha-long-bay-moon", "Limestone karsts and lantern-lit junks on calm, moonlit Ha Long Bay"),
        ("moonlit-rice-terraces", "Cascading rice terraces and warm village lights under a full moon"),
    ]),
]
SLUGS = [s for _, _, _, _, items in GROUPS for s, _ in items]
N = len(SLUGS)

TITLE = "Asian Wall Art: Japanese & Temple Posters, Framed Prints | Moonlit Windows"
DESC = (f"Asian wall art: {N} moonlit Japanese, Chinese and temple posters and framed prints, from Mount Fuji, Kyoto "
        "and the Great Wall to the Taj Mahal, Sigiriya, Angkor Wat and Bagan. 12×18 poster $35, framed $69, "
        "4×6 ft wall mural $149, shipping included.")
H1 = "Asian Wall Art: Moonlit Japanese, Chinese and Temple Prints"

FAQ = [
    ("What sizes and formats are available?",
     "Every piece comes as a 12×18 in enhanced matte poster ($35), the same 12×18 print in a black frame ($69), or a 4×6 ft (48×72 in) peel and stick wall mural on removable polyester ($149). Shipping is included on all three."),
    ("Are these real places?",
     "Most are named places reimagined at night: the Chureito Pagoda below Mount Fuji, a Kyoto bamboo grove, the Great Wall at Mutianyu, the Li River near Guilin, Zhangjiajie, the Taj Mahal, Sigiriya’s Lion Rock in Sri Lanka, Angkor Wat, Bagan and Ha Long Bay. Japanese Temple Pond, Bali Jungle Temple and Moonlit Rice Terraces evoke those landscapes rather than one exact viewpoint."),
    ("Is there Japanese wall art for a bedroom?",
     "Yes. Kyoto Bamboo Moon and Japanese Temple Pond are the calmest pieces in the collection, with soft greens, still water and mist. Mount Fuji Pagoda Moon has more colour from the cherry blossoms and pagoda, so it suits a living room or hallway as well."),
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
        {"@type": "CollectionPage", "name": "Asian Wall Art: Moonlit Japanese, Chinese and Temple Prints",
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
            {"@type": "ListItem", "position": 3, "name": "Asian Wall Art", "item": URL}]}]}
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
  <meta property="og:image:alt" content="{og_item['title']} Japanese wall art poster" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{T}" />
  <meta name="twitter:description" content="{DESC}" />
  <meta name="twitter:image" content="{og}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=Outfit:wght@380;560;650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json" data-ld="collection-asian">
{ld(sel)}
  </script>
  <script type="application/ld+json" data-ld="faq-asian">
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
    <p class="note breadcrumb"><a href="./">Home</a> › <a href="./buy.html">Shop</a> › Asian wall art</p>
    <section class="hero left">
      <div class="kicker">Collection</div>
      <h1>{H1}</h1>
      <p class="sale-line">{N} Asian and Japanese art prints · $35 poster · $69 framed · 12×18 · $149 peel &amp; stick wall mural (4×6 ft) · shipping included</p>
      <p class="answer-first">These are {N} moonlit Asian landscape and temple prints, each sold as a 12×18 in poster for $35, a black-framed print for $69, or a 4×6 ft peel and stick wall mural for $149, with shipping included. Most show real places at night, among them Mount Fuji, Kyoto, the Great Wall, Guilin, the Taj Mahal, Angkor Wat and Bagan, with a full moon in the sky and warm lantern light below.</p>
      <p>Mist does a lot of the work here: it softens karst peaks and bamboo, settles over temple plains and lifts off still ponds, so even the busiest scenes stay calm. That makes this the most meditative group in the Night Windows series, with deep greens and blues rather than bright colour.</p>
      <p class="note">Jump to: <a href="#japan">Japan</a> · <a href="#china">China</a> · <a href="#southeast-asia-india">South and Southeast Asia</a> · <a href="#choose">Choosing a piece</a> · <a href="#faq">FAQ</a></p>
    </section>

{grids}

    <section class="prose">
      <h2 id="choose">How to choose Asian wall art for your room</h2>
      <p><strong>Bedroom.</strong> Go for stillness: {P("kyoto-bamboo-moon", "Kyoto Bamboo Moon")} with its soft green grove, {P("japanese-temple-pond", "Japanese Temple Pond")} with the moon in the water, or the lantern-lit junks of {P("ha-long-bay-moon", "Ha Long Bay")}. More bedroom picks and size tips are in the <a data-guide="bedroom" href="./moon-poster-bedroom.html">moon poster for bedroom</a> guide.</p>
      <p><strong>Living room or a feature wall.</strong> Big, recognisable scenes carry across a room: {P("mount-fuji-pagoda-moon", "Mount Fuji and the Chureito Pagoda")}, {P("great-wall-mutianyu-moon", "the Great Wall at Mutianyu")} and {P("taj-mahal-moon", "the Taj Mahal")}. To make one fill the wall, the same artwork comes as a 4×6 ft (48×72 in) peel and stick wall mural; the <a href="./peel-and-stick-wall-murals.html">peel and stick wall murals collection</a> covers measuring and wall prep.</p>
      <p><strong>Meditation corner, yoga room or study.</strong> The temple pieces are the most contemplative: {P("angkor-wat-moon", "Angkor Wat")} reflected in its lotus pond, the stupas of {P("bagan-temples-night", "Bagan")}, or mossy steps in {P("bali-jungle-temple", "Bali Jungle Temple")}.</p>
      <p><strong>Office or hallway.</strong> Layered mountain scenes read well from a distance: {P("guilin-li-river-moon", "the Li River near Guilin")}, {P("zhangjiajie-pillars-moon", "Zhangjiajie’s pillars")} or {P("moonlit-rice-terraces", "Moonlit Rice Terraces")}.</p>
      <p><strong>A trip to remember.</strong> If you hiked to the Chureito Pagoda, walked the wall at Mutianyu or visited Angkor, the place-named prints are made for that. Pairs work well too: Fuji with Kyoto for a Japan wall, or Guilin with Ha Long Bay for karst country.</p>
      <p>Prefer high peaks, still lakes or the sea? See the <a href="./mountain-wall-art.html">mountain wall art collection</a>, the <a href="./lake-wall-art.html">lake and waterfall wall art collection</a> and the <a href="./coastal-wall-art.html">coastal wall art collection</a>. For castles, canals and old towns, see the <a data-collection="european" href="./european-wall-art.html">European wall art collection</a>. Not sure about size? The <a href="./guide-print-sizes.html">print size guide</a> compares the poster, framed print and mural.</p>
    </section>

    <section class="prose" id="faq">
      <h2>Questions about these Asian and Japanese prints</h2>
{faq_html()}
      <p>Looking for something else? Browse <a href="./night-windows.html">every Night Windows piece</a> or the <a href="./buy.html">full shop</a>.</p>
    </section>
  </div>
  <footer class="site-footer">
    <div class="wrap"><div class="footer-shop"><a href="./buy.html">Shop Posters, Prints &amp; Wall Murals</a> · $35 poster · $69 framed · 12×18 · shipping included</div>
      <div><a href="./">Gallery</a> · <a href="./mountain-wall-art.html">Mountain wall art</a> · <a href="./lake-wall-art.html">Lake and waterfall wall art</a> · <a href="./coastal-wall-art.html">Coastal wall art</a> · <a href="./asian-wall-art.html">Asian wall art</a> · <a href="./european-wall-art.html">European wall art</a> · <a href="./peel-and-stick-wall-murals.html">Peel and stick wall murals</a> · Night Shade Art on Instagram: <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a></div>
    </div>
    <div class="operated-by footer-legal"><p>© 2026 Joshua Israel Ventures LLC. All rights reserved. Moonlit Windows is owned and operated by Joshua Israel Ventures LLC.</p><p class="footer-legal-links"><a href="./terms.html">Terms</a> · <a href="./privacy.html">Privacy</a> · <a href="./disclaimer.html">Disclaimer</a> · <a href="./contact.html">Contact</a></p></div>
  </footer>
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "899375a6262144aabf5184589abd580c"}}'></script>
</body>
</html>
'''

PIECE_LINK = (f'<p class="note collection-link" {MARK}>Part of the '
              '<a href="../asian-wall-art.html">Asian wall art collection</a>: '
              f'{N} moonlit Japanese, Chinese and temple posters, framed prints and wall murals.</p>')

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
        a = '<a data-collection="coastal" href="./coastal-wall-art.html">Coastal wall art</a>'
        if a in src: put(rel, src, src.replace(a, a + f' · <a {MARK} href="./asian-wall-art.html">Asian wall art</a>', 1))
        else: print("WARN buy.html theme anchor not found")
    rel = "night-windows.html"; src = (ROOT / rel).read_text(encoding="utf-8")
    if MARK not in src:
        a = 'href="./coastal-wall-art.html">coastal wall art collection</a>.</p>'
        if a in src: put(rel, src, src.replace(a, a[:-4] + f' Mount Fuji, Kyoto, the Great Wall and the temples of Angkor, Bagan and Agra are in the <a {MARK} href="./asian-wall-art.html">Asian wall art collection</a>.</p>', 1))
        else: print("WARN night-windows anchor not found")
    rel = "llms.txt"; src = (ROOT / rel).read_text(encoding="utf-8")
    if URL in src:
        put(rel, src, re.sub(rf"(- \[Asian\ wall\ art\]\({re.escape(URL)}\): )\d+ ", rf"\g<1>{N} ", src, count=1))
    if URL not in src:
        m = re.search(r"- \[Coastal wall art\]\([^)]*\):[^\n]*\n", src)
        line = (f"- [Asian wall art]({URL}): {N} moonlit Japanese, Chinese and temple posters ($35), framed prints ($69) "
                "and wall murals ($149), from Mount Fuji, Kyoto and the Great Wall to the Taj Mahal, Angkor Wat and Bagan, with a room guide and FAQ\n")
        if m: put(rel, src, src[:m.end()] + line + src[m.end():])
        else: print("WARN llms.txt anchor not found")
    return out

def sitemap(changed):
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8"); n = sm
    if f"<loc>{URL}</loc>" not in n:
        asset = json.loads((ROOT / "products.json").read_text())
        asset = next(i["asset"] for i in asset if i["slug"] == OG_SLUG)
        entry = f'  <url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><image:image><image:loc>{SITE}/assets/{asset}</image:loc></image:image></url>\n'
        i = n.find(f"<url><loc>{SITE}/coastal-wall-art.html</loc>")
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
