"""2026-10-07 buyer-keyword pass. Only real products: poster $29, framed print $69 (12x18). No canvas/wallpaper."""
import re,glob,json,html
P={p["slug"]:p for p in json.load(open("products.json"))}
for f in glob.glob("pieces/*.html"):
    s=open(f).read(); slug=f[7:-5]; t=P[slug]["title"]
    s=s.replace(f"<title>{html.escape(t,quote=False)} Poster &amp; Framed Print | Moonlit Windows</title>",
                f"<title>{html.escape(t,quote=False)} Wall Art Poster &amp; Framed Print | Moonlit Windows</title>")
    s=s.replace(f"<title>{t} Poster & Framed Print | Moonlit Windows</title>",f"<title>{t} Wall Art Poster & Framed Print | Moonlit Windows</title>")
    s=re.sub(r'content="Buy ([^"]*?) as a 12×18 poster \(\$29\) or black framed print \(\$69\), shipping included\.',
             r'content="Moon poster wall art: buy \1 as a 12×18 art print poster ($29) or framed print ($69), shipping included.',s)
    s=re.sub(r'(<meta (?:property|name)="(?:og|twitter):title" content=")[^"]*"',lambda m:m.group(1)+html.escape(f"{t} Wall Art Poster & Framed Print | Moonlit Windows")+'"',s)
    s=s.replace("Poster and framed print for sale ·","Moonlit wall art poster and framed print for sale ·")
    # alt text: main image + og alt
    s=re.sub(r'(<article class="piece">\s*<img [^>]*alt=")([^"]*?)(")',lambda m:m.group(1)+(m.group(2) if "wall art" in m.group(2) else m.group(2)+", night landscape wall art print")+m.group(3),s,count=1)
    s=re.sub(r'(og:image:alt" content=")([^"]*?)(")',lambda m:m.group(1)+(m.group(2) if "wall art" in m.group(2) else m.group(2)+", night landscape wall art print")+m.group(3),s,count=1)
    m=re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',s,re.S); ld=json.loads(m.group(2))
    pr=[g for g in ld["@graph"] if g["@type"]=="Product"][0]
    pr["name"]=f"{t} Wall Art Print (Poster or Framed Print, 12x18)"
    pr["description"]=re.sub(r"^.*?shipping included\. ",f"{t} moonlit night landscape wall art from the Night Windows series, sold as a 12×18 art print poster ($29) or framed wall art print ($69), shipping included. A home decor print for living rooms and bedrooms. ",pr["description"],count=1)
    for o in pr["offers"]:
        o["name"]=f"{t} wall art poster 12x18" if o["price"]=="29.00" else f"{t} framed wall art print 12x18"
    s=s[:m.start(2)]+"\n"+json.dumps(ld,indent=2)+"\n  "+s[m.end(2):]
    open(f,"w").write(s)
def rep(f,pairs):
    s=open(f).read()
    for a,b in pairs: s=s.replace(a,b)
    open(f,"w").write(s)
rep("index.html",[("Night Windows Art Posters &amp; Framed Prints for Sale | Moonlit Windows","Moonlit Wall Art Posters &amp; Framed Prints for Sale | Moonlit Windows"),
 ("Night Windows Art Posters & Framed Prints for Sale | Moonlit Windows","Moonlit Wall Art Posters & Framed Prints for Sale | Moonlit Windows"),
 ("Shop 50 moonlit landscape art prints: 12×18 posters $29, framed prints $69, shipping included. Night Windows by Night Shade Art, secure Stripe checkout.",
  "Shop 50 moonlit night landscape wall art prints: 12×18 moon posters $29, framed wall art $69, shipping included. Home decor art prints with secure Stripe checkout."),
 ("Art posters and framed prints for sale:","Moonlit wall art posters and framed prints for sale:")])
rep("buy.html",[("Shop Posters &amp; Framed Prints: 50 Night Windows Art Prints | Moonlit Windows","Shop Wall Art Posters &amp; Framed Prints | Moonlit Windows"),
 ("Shop Posters & Framed Prints: 50 Night Windows Art Prints | Moonlit Windows","Shop Wall Art Posters & Framed Prints | Moonlit Windows"),
 ("Shop Night Windows art posters ($29) and framed prints ($69), 12×18, shipping included. 50 moonlit landscapes incl. Meteora, Mount Fuji, Isle of Skye. Stripe checkout.",
  "Shop moon posters and framed wall art: 50 night landscape art prints, 12×18 poster $29 or framed print $69, shipping included. Meteora, Mount Fuji, Isle of Skye posters."),
 ("Night Windows art posters and framed prints for sale:","Night landscape wall art posters and framed art prints for sale:")])
rep("night-windows.html",[("Night Windows Moonlit Landscape Posters &amp; Framed Prints | Moonlit Windows","Night Windows Moon Posters &amp; Framed Wall Art Prints | Moonlit Windows"),
 ("Night Windows Moonlit Landscape Posters & Framed Prints | Moonlit Windows","Night Windows Moon Posters & Framed Wall Art Prints | Moonlit Windows"),
 ("Moonlit landscape posters and framed prints for sale:","Moonlit landscape wall art posters and framed prints for sale:")])
# buy grid alt text
s=open("buy.html").read()
s=re.sub(r'(<article class="card" id="[^"]+">\s*<a [^>]*><img [^>]*alt=")([^"]*?)(")',lambda m:m.group(1)+(m.group(2) if "poster" in m.group(2) else m.group(2)+" wall art poster and framed print")+m.group(3),s)
open("buy.html","w").write(s)
