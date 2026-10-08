#!/usr/bin/env python3
"""AI-search readiness pass (8 Oct 2026). Idempotent, targeted string edits only.
Usage: ai_search_pass.py [--check]"""
import glob, json, re, sys
CHECK = '--check' in sys.argv
changed = []

def edit(path, pairs):
    s = open(path, encoding='utf-8').read(); o = s
    for old, new in pairs:
        if new in s: continue
        if old not in s: print('MISSING anchor in', path, ':', old[:70]); continue
        s = s.replace(old, new, 1)
    if s != o:
        changed.append(path)
        if not CHECK: open(path, 'w', encoding='utf-8').write(s)

MURAL_ANS = ('Moonlit Windows sells moonlit landscape wall art from the Night Windows series as '
             '$29 posters, $69 framed prints and $149 peel-and-stick wall murals.')

# Homepage: answer-first opener, unified WebSite node, mural in social descriptions
edit('index.html', [
    ('      <h1>Night Windows</h1>\n      <p>Windows into places',
     '      <h1>Night Windows</h1>\n      <p class="answer-first">' + MURAL_ANS +
     ' Choose from 50 night scenes, printed to order: 12×18 posters and black-framed prints, or 4×6 ft removable wall murals, with shipping included.</p>\n      <p>Windows into places'),
    ('''        "@type": "WebSite",
        "name": "Prompt Framed",
        "url": "https://moonlitwindows.com/",
        "description": "Night Windows: cinematic night landscapes as posters and framed prints.",
        "publisher": {
          "@type": "Organization",
          "name": "Joshua Israel Ventures LLC"
        }''',
     '''        "@type": "WebSite",
        "@id": "https://moonlitwindows.com/#website",
        "name": "Moonlit Windows",
        "alternateName": "Prompt Framed",
        "url": "https://moonlitwindows.com/",
        "description": "Night Windows: moonlit landscape wall art sold as posters, framed prints and peel-and-stick wall murals.",
        "publisher": {
          "@id": "https://moonlitwindows.com/#org"
        }'''),
    ('''        "isPartOf": {
          "@type": "WebSite",
          "name": "Prompt Framed",
          "url": "https://moonlitwindows.com/"
        },''',
     '''        "isPartOf": {
          "@id": "https://moonlitwindows.com/#website"
        },'''),
    ('<meta property="og:description" content="Moonlit landscape posters ($29) and framed prints ($69), 12×18, shipping included." />',
     '<meta property="og:description" content="Moonlit landscape posters ($29) and framed prints ($69), 12×18, plus 4×6 ft peel and stick wall murals ($149). Shipping included." />'),
    ('<meta name="twitter:description" content="Moonlit landscape posters ($29) and framed prints ($69), 12×18, shipping included." />',
     '<meta name="twitter:description" content="Moonlit landscape posters ($29) and framed prints ($69), 12×18, plus 4×6 ft peel and stick wall murals ($149). Shipping included." />'),
])

# Shop page: answer-first sale line including murals
edit('buy.html', [
    ('<p class="sale-line">Night landscape wall art posters and framed art prints for sale: $29 poster · $69 framed · 12×18 · shipping included.</p>',
     '<p class="sale-line">Buy any of the 50 Night Windows moonlit landscape prints as a $29 poster or $69 framed print (12×18 in) or as a $149 peel-and-stick wall mural (4×6 ft). Shipping is included.</p>'),
])

# Series page: mural in sale line
edit('night-windows.html', [
    ('<p class="sale-line">Moonlit landscape wall art posters and framed prints for sale: $29 poster · $69 framed · 12×18 · shipping included.',
     '<p class="sale-line">Moonlit landscape wall art posters, framed prints and peel &amp; stick wall murals for sale: $29 poster · $69 framed · 12×18 · $149 wall mural (4×6 ft) · shipping included.'),
])

# About page: clear title/description + answer-first opener
edit('about.html', [
    ('<title>About — Prompt Framed</title>',
     '<title>About Moonlit Windows: Night Windows Wall Art by Night Shade Art | Prompt Framed</title>'),
    ('<meta name="description" content="Prompt Framed is the Night Windows gallery of Joshua Israel Ventures LLC. Night pictures, printed as posters and shipped when you order.">',
     '<meta name="description" content="Moonlit Windows (Prompt Framed, Night Shade Art on Instagram) is the Night Windows wall art shop of Joshua Israel Ventures LLC: $29 posters, $69 framed prints and $149 peel-and-stick wall murals, printed to order and shipped.">'),
    ('    <h1>Night Windows</h1>\n    <p>Windows into places',
     '    <h1>Night Windows</h1>\n    <p class="answer-first">Moonlit Windows is the online shop for Night Windows, a series of 50 moonlit landscape pictures sold as $29 posters, $69 framed prints (12×18 in) and $149 peel-and-stick wall murals (4×6 ft). It is operated by Joshua Israel Ventures LLC and shares the series on Instagram as Night Shade Art.</p>\n    <p>Windows into places'),
])

# Piece pages: mural in the answer-first sale line
OLD_SL = '<p class="sale-line">Moonlit wall art poster and framed print for sale · $29 poster · $69 framed · 12×18 · shipping included · '
NEW_SL = '<p class="sale-line">Moonlit wall art poster, framed print and peel &amp; stick wall mural for sale · $29 poster · $69 framed · 12×18 · $149 wall mural (4×6 ft) · shipping included · '
for p in sorted(glob.glob('pieces/*.html')):
    edit(p, [(OLD_SL, NEW_SL)])

# Mountain collection: FAQPage JSON-LD mirroring the visible FAQ text
FAQ = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": "What sizes and formats are available?",
     "acceptedAnswer": {"@type": "Answer", "text": "A 12×18 inch enhanced matte poster ($29), the same 12×18 print in a black frame ($69), and a 4×6 ft (48×72 in) peel and stick wall mural on removable polyester ($149). Shipping is included on all three."}},
    {"@type": "Question", "name": "How long does a mural take?",
     "acceptedAnswer": {"@type": "Answer", "text": "Murals are printed to order and ship in 1–2 weeks."}},
    {"@type": "Question", "name": "Are these real places?",
     "acceptedAnswer": {"@type": "Answer", "text": "Most are named landmarks, reimagined at night. Patagonia Lake Peaks and Scottish Highlands Loch evoke those regions rather than one exact viewpoint, and Moonlit Alpine Meadow and Snowy Peaks Above Clouds are imagined alpine scenes."}},
    {"@type": "Question", "name": "How do I pay?",
     "acceptedAnswer": {"@type": "Answer", "text": "Every button opens secure Stripe checkout, and your receipt arrives by email."}},
]}
faq_tag = '  <script type="application/ld+json" data-ld="faq-mountain">\n' + json.dumps(FAQ, ensure_ascii=False, indent=2) + '\n  </script>\n</head>'
s = open('mountain-wall-art.html', encoding='utf-8').read()
if 'data-ld="faq-mountain"' not in s:
    edit('mountain-wall-art.html', [('</head>', faq_tag)])

print(('WOULD CHANGE' if CHECK else 'CHANGED'), len(changed), 'files')
for c in changed: print(' ', c)
