"""SEO pass (2026-10-07): commercial titles/meta, sale lines, shop nav, JSON-LD, sitemap lastmod."""
import json, re, glob, html, datetime, subprocess
SITE="https://moonlitwindows.com"
P=json.load(open("products.json"))
by={p["slug"]:p for p in P}
SALE="12×18 posters ($29) and framed prints ($69), shipping included"
def sub1(pat,rep,s,flags=0):
    n=re.sub(pat,rep,s,count=1,flags=flags); return n
def setmeta(s,attr,key,val):
    v=html.escape(val,quote=True)
    pat=r'<meta %s="%s" content="[^"]*"\s*/?>'%(attr,re.escape(key))
    tag='<meta %s="%s" content="%s" />'%(attr,key,v)
    if re.search(pat,s): return re.sub(pat,lambda m:tag,s,count=1)
    return s.replace("</title>","</title>\n  "+tag,1)
def head(s,title,desc,img=None,ogdesc=None):
    s=re.sub(r"<title>.*?</title>","<title>%s</title>"%html.escape(title,quote=False),s,count=1)
    s=setmeta(s,"name","description",desc)
    for a,k,v in [("property","og:title",title),("property","og:description",ogdesc or desc),
                  ("name","twitter:card","summary_large_image"),("name","twitter:title",title),("name","twitter:description",ogdesc or desc)]:
        s=setmeta(s,a,k,v)
    if img:
        s=setmeta(s,"property","og:image",img); s=setmeta(s,"name","twitter:image",img)
    s=setmeta(s,"property","og:site_name","Moonlit Windows")
    return s
def nav(s):
    s=re.sub(r'(<a href="(?:\.\./|\./)buy\.html">)(Buy a print|Buy)(</a>)',r'\1Shop Posters &amp; Framed Prints\3',s)
    return s
def footer(s,pre):
    if 'class="footer-shop"' in s: return s
    return re.sub(r'(<footer class="site-footer">.*?<div class="wrap">)',r'\1<div class="footer-shop"><a href="%sbuy.html">Shop Posters &amp; Framed Prints</a> · $29 poster · $69 framed · 12×18 · shipping included</div>'%pre,s,count=1,flags=re.S)
def setld(s,obj,marker):
    block='<script type="application/ld+json" data-ld="%s">\n%s\n  </script>'%(marker,json.dumps(obj,indent=2,ensure_ascii=False))
    pat=r'<script type="application/ld\+json" data-ld="%s">.*?</script>'%marker
    if re.search(pat,s,re.S): return re.sub(pat,lambda m:block,s,flags=re.S)
    return s.replace("</head>","  "+block+"\n</head>",1)
def trim(t,n=158):
    return t if len(t)<=n else t[:n].rsplit(" ",1)[0].rstrip(",;—- ")+"…"
changed=[]
# pieces
for f in sorted(glob.glob("pieces/*.html")):
    s=o=open(f).read(); slug=f.split("/")[1][:-5]; p=by[slug]; t=p["title"]
    m=re.search(r'<p class="desc">(.*?)</p>',s,re.S); d=html.unescape(m.group(1)).strip()
    img=re.search(r'og:image" content="([^"]+)"',s).group(1)
    s=head(s,f"{t} Poster & Framed Print | Moonlit Windows",
           trim(f"Buy {t} as a 12×18 poster ($29) or black framed print ($69), shipping included. {d}"),img,
           f"{t}: Night Windows poster $29 · framed print $69 (12×18, shipping included). {d}")
    s=nav(s); s=footer(s,"../")
    if 'class="sale-line"' not in s:
        s=re.sub(r'(<h1>.*?</h1>)',r'\1\n        <p class="sale-line">Poster and framed print for sale · $29 poster · $69 framed · 12×18 · shipping included · <a href="#buy">Buy now</a></p>',s,count=1)
    # enrich Product JSON-LD
    m=re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',s,re.S)
    ld=json.loads(m.group(2)); prod=[g for g in ld["@graph"] if g["@type"]=="Product"][0]
    url=f"{SITE}/pieces/{slug}.html"; prod["url"]=url
    prod["description"]=f"{t} from the Night Windows series, for sale as a 12×18 enhanced matte poster ($29) or black framed print ($69), shipping included. {d}"
    prod["offers"]=[{**of,"url":url,"seller":{"@type":"Organization","name":"Moonlit Windows","url":SITE+"/"},
        "shippingDetails":{"@type":"OfferShippingDetails","shippingRate":{"@type":"MonetaryAmount","value":"0","currency":"USD"}}} for of in prod["offers"]]
    for of,kind in zip(prod["offers"],["poster","framed"]):
        assert of["price"]==("29.00" if kind=="poster" else "69.00") and p["stripe"][kind+"Price"]==(2900 if kind=="poster" else 6900)
    s=s[:m.start(2)]+"\n"+json.dumps(ld,indent=2)+"\n  "+s[m.end(2):]
    if s!=o: open(f,"w").write(s); changed.append(f)
items=[{"@type":"ListItem","position":i+1,"name":f'{p["title"]} poster & framed print',"url":f'{SITE}/pieces/{p["slug"]}.html'} for i,p in enumerate(P)]
img_sheet=SITE+"/assets/night-windows-contact-sheet.jpg"
# index
s=o=open("index.html").read()
s=head(s,"Night Windows Art Posters & Framed Prints for Sale | Moonlit Windows",
 "Shop 50 moonlit landscape art prints: 12×18 posters $29, framed prints $69, shipping included. Night Windows by Night Shade Art, secure Stripe checkout.",img_sheet,
 "Moonlit landscape posters ($29) and framed prints ($69), 12×18, shipping included.")
s=nav(s); s=footer(s,"./")
s=s.replace('<p>Windows into places you wish you were. Dreamy moonlit landscapes, printed as posters.</p>\n      <p class="soft-cta"><a class="btn" href="./buy.html">Want a poster? Buy at the link.</a>',
 '<p>Windows into places you wish you were. Dreamy moonlit landscapes, printed as posters.</p>\n      <p class="sale-line">Art posters and framed prints for sale: $29 poster · $69 framed · 12×18 · shipping included.</p>\n      <p class="soft-cta"><a class="btn" href="./buy.html">Shop Posters &amp; Framed Prints</a>',1)
s=setld(s,{"@context":"https://schema.org","@graph":[
 {"@type":"Organization","@id":SITE+"/#org","name":"Moonlit Windows","alternateName":["Night Shade Art","Prompt Framed"],"url":SITE+"/","logo":SITE+"/assets/brand/night-shade-art-avatar-1080.png","sameAs":["https://www.instagram.com/moonnightshadeart/"],"legalName":"Joshua Israel Ventures LLC"},
 {"@type":"WebSite","@id":SITE+"/#website","name":"Moonlit Windows","url":SITE+"/","publisher":{"@id":SITE+"/#org"}},
 {"@type":"ItemList","name":"Night Windows posters & framed prints","numberOfItems":len(items),"itemListElement":items}]},"shop")
if s!=o: open("index.html","w").write(s); changed.append("index.html")
# buy
s=o=open("buy.html").read()
s=head(s,"Shop Posters & Framed Prints: 50 Night Windows Art Prints | Moonlit Windows",
 "Shop Night Windows art posters ($29) and framed prints ($69), 12×18, shipping included. 50 moonlit landscapes incl. Meteora, Mount Fuji, Isle of Skye. Stripe checkout.",img_sheet)
s=nav(s); s=footer(s,"./")
s=s.replace("<h1>Buy the print</h1>","<h1>Shop Posters &amp; Framed Prints</h1>\n      <p class=\"sale-line\">Night Windows art posters and framed prints for sale: $29 poster · $69 framed · 12×18 · shipping included.</p>",1)
s=setld(s,{"@context":"https://schema.org","@graph":[
 {"@type":"CollectionPage","name":"Shop Posters & Framed Prints","url":SITE+"/buy.html","mainEntity":{"@type":"ItemList","numberOfItems":len(items),"itemListElement":items}},
 {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Shop Posters & Framed Prints","item":SITE+"/buy.html"}]}]},"shop")
if s!=o: open("buy.html","w").write(s); changed.append("buy.html")
# series
s=o=open("night-windows.html").read()
s=head(s,"Night Windows Moonlit Landscape Posters & Framed Prints | Moonlit Windows",
 "The Night Windows series: 50 moonlit landscape art prints for sale as 12×18 posters ($29) or framed prints ($69), shipping included. Meteora, Mount Fuji, Skye and more.",img_sheet)
s=nav(s); s=footer(s,"./")
s=s.replace('<h1>Night Windows</h1>','<h1>Night Windows</h1>\n    <p class="sale-line">Moonlit landscape posters and framed prints for sale: $29 poster · $69 framed · 12×18 · shipping included. <a href="./buy.html">Shop now</a></p>',1) if 'sale-line' not in s else s
s=setld(s,{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Night Windows","item":SITE+"/night-windows.html"}]},"crumb")
if s!=o: open("night-windows.html","w").write(s); changed.append("night-windows.html")
# other pages: nav + footer
for f in ["about.html","contact.html","how-it-works.html","guide-print-sizes.html","thanks.html","how-to-turn-chatgpt-art-into-a-framed-poster.html"]:
    s=o=open(f).read(); s=nav(s); s=footer(s,"./")
    if s!=o: open(f,"w").write(s); changed.append(f)
# sitemap lastmod (real last-commit date or today if changed now)
today=datetime.date.today().isoformat()
sm=open("sitemap.xml").read()
def lm(m):
    loc=m.group(1); path=loc.replace(SITE+"/","") or "index.html"
    return f"<loc>{loc}</loc><lastmod>{today}</lastmod>" if path in changed else f"<loc>{loc}</loc>"
sm=re.sub(r"<lastmod>[^<]*</lastmod>","",sm)
sm=re.sub(r"<loc>([^<]+)</loc>",lm,sm)
open("sitemap.xml","w").write(sm)
print(len(changed),"files changed")
