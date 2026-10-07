#!/usr/bin/env python3
"""Add the Peel & Stick Wall Mural ($149, 48x72 in) buy option to piece pages + buy.html.

Gated on products.json stripe.muralUrl (https://buy.stripe.com/...). Idempotent; safe to
re-run after apply_stripe_links.py (which regenerates the buy blocks and drops the mural button).
Does not touch poster/framed links. Mural print files live privately, never in this repo.

  python3 scripts/apply_mural_links.py          # apply
  python3 scripts/apply_mural_links.py --check  # count pieces with live mural links + buttons
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
items = json.loads((ROOT / "products.json").read_text())
live = lambda u: isinstance(u, str) and u.startswith("https://buy.stripe.com/")
LABEL = "Peel &amp; Stick Wall Mural · $149"
PL_OLD = "$29 poster · $69 framed (12×18)"
PL_NEW = "$29 poster · $69 framed (12×18) · $149 peel &amp; stick wall mural (4×6 ft)"
NOTE = ('<p class="note mural-note">Peel &amp; stick wall mural: 4×6 ft (48×72 in) removable wallpaper on '
        'peel-and-stick polyester. No paste; removes cleanly from most smooth painted walls. Each mural is printed to order and '
        'ships in 1–2 weeks, shipping included.</p>')
NAV_OLD, NAV_NEW = ">Shop Posters &amp; Framed Prints<", ">Shop Posters, Prints &amp; Wall Murals<"
OWNER = '<div class="operated-by">Operated by Joshua Israel Ventures LLC</div>'

def btn(slug, url, ind):
    return f'{ind}<a class="btn secondary" data-buy="{slug}" data-sku="mural" href="{url}">{LABEL}</a>\n'

def add_button(src, slug, url):
    if f'data-buy="{slug}" data-sku="mural"' in src:
        return re.sub(rf'(data-buy="{slug}" data-sku="mural" href=")[^"]*', rf'\g<1>{url}', src)
    pat = re.compile(rf'(\n(\s*)<a class="btn secondary" data-buy="{re.escape(slug)}" data-sku="framed"[^\n]*\n)')
    return pat.sub(lambda m: m.group(1) + btn(slug, url, m.group(2)), src, count=1)

def offer(slug, title):
    u = f"https://moonlitwindows.com/pieces/{slug}.html"
    return {"@type": "Offer", "@id": f"{u}#offer-mural",
            "name": f"{title} peel and stick wall mural 4x6 ft (48x72 in), removable wallpaper",
            "price": "149.00", "priceCurrency": "USD", "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition", "url": u,
            "shippingDetails": {"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "USD"}},
            "seller": {"@type": "Organization", "name": "Joshua Israel Ventures LLC", "url": "https://moonlitwindows.com/"}}

def fix_ld(src, slug, title):
    def f(m):
        d = json.loads(m.group(1)); ch = False
        for n in d.get("@graph", []):
            if n.get("@type") == "Product" and isinstance(n.get("offers"), list) and not any(o.get("@id", "").endswith("#offer-mural") for o in n["offers"]):
                n["offers"].append(offer(slug, title))
                n["description"] += " Also available as a 4×6 ft peel and stick wall mural ($149): removable wallpaper, printed to order."
                ch = True
        return '<script type="application/ld+json">\n' + json.dumps(d, indent=2, ensure_ascii=False) + "\n  </script>" if ch else m.group(0)
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', f, src, flags=re.S)

def piece(it):
    p = ROOT / "pieces" / f"{it['slug']}.html"; src = p.read_text(); url = it["stripe"]["muralUrl"]; t = it["title"]
    src = add_button(src, it["slug"], url)
    if PL_NEW not in src: src = src.replace(PL_OLD, PL_NEW)
    if "mural-note" not in src:
        src = re.sub(r'(\n(\s*)<p class="note">Enhanced matte poster[^\n]*\n)', lambda m: m.group(1) + m.group(2) + NOTE + "\n", src, count=1)
    src = fix_ld(src, it["slug"], t)
    src = src.replace("Wall Art Poster &amp; Framed Print | Moonlit Windows", "Poster, Framed Print &amp; Wall Mural | Moonlit Windows")
    src = re.sub(r'(<meta (?:name|property)="(?:og:|twitter:)?description" content=")((?:(?!mural)[^"])*?)(" />)',
                 lambda m: m.group(1) + m.group(2).replace("shipping included.", "shipping included, or a $149 peel and stick wall mural (removable wallpaper).", 1) + m.group(3), src)
    p.write_text(src)

def has_btn(it):
    return f'data-sku="mural" href="{it["stripe"]["muralUrl"]}"' in (ROOT / "pieces" / f"{it['slug']}.html").read_text()

def main():
    w = [i for i in items if live((i.get("stripe") or {}).get("muralUrl"))]
    if "--check" in sys.argv:
        b = (ROOT / "buy.html").read_text()
        ok = sum(1 for i in w if has_btn(i) and f'data-buy="{i["slug"]}" data-sku="mural"' in b)
        print(f"{len(w)}/{len(items)} pieces have live mural links; {ok} wired on piece page + buy.html"); return 0 if ok == len(items) else 1
    for it in w: piece(it)
    b = ROOT / "buy.html"; s = b.read_text()
    for it in w: s = add_button(s, it["slug"], it["stripe"]["muralUrl"])
    if PL_NEW not in s: s = s.replace(PL_OLD, PL_NEW)
    s = s.replace("Shop Wall Art Posters &amp; Framed Prints | Moonlit Windows", "Shop Wall Art Posters, Framed Prints &amp; Peel and Stick Wall Murals | Moonlit Windows")
    s = re.sub(r'(<meta (?:name|property)="(?:og:|twitter:)?description" content=")((?:(?!mural)[^"])*?)(" />)',
               lambda m: m.group(1) + m.group(2).replace("shipping included.", "shipping included. Peel and stick wall murals (4×6 ft removable wallpaper) $149.", 1) + m.group(3), s)
    if "mural-note" not in s:
        s = re.sub(r'(\n(\s*)<p class="price-line">)', lambda m: "\n" + m.group(2) + NOTE + m.group(1), s, count=1)
    b.write_text(s)
    for f in list(ROOT.glob("*.html")) + list((ROOT / "pieces").glob("*.html")):
        t = f.read_text(); n = t.replace(NAV_OLD, NAV_NEW)
        if "operated-by" not in n:
            n = n.replace("</footer>", "  " + OWNER + "\n  </footer>", 1) if "</footer>" in n else n.replace("</body>", f'<footer class="site-footer"><div class="wrap">{OWNER}</div></footer>\n</body>', 1)
        if n != t: f.write_text(n)
    print(f"mural option applied to {len(w)} pieces")
sys.exit(main())
