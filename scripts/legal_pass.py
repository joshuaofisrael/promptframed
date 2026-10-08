#!/usr/bin/env python3
"""Brand/legal pass (8 Oct 2026). Idempotent; --check = dry run (prints what would change).
- Every page footer: LLC copyright + ownership line + Terms/Privacy/Disclaimer/Contact links
  (replaces the old 'Operated by' line and the old '© ... Prompt Framed' lines; keeps class operated-by).
- terms.html, privacy.html, disclaimer.html (WebPage + BreadcrumbList JSON-LD), sitemap + llms.txt entries.
- JSON-LD: Organization/publisher/seller = Joshua Israel Ventures LLC; Moonlit Windows = Brand.
- about.html: 'Moonlit Windows is a brand of Joshua Israel Ventures LLC.'
- site.js: mural buttons keep their mural Stripe link when products.json loads (was falling back to poster).
"""
import glob, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = "--check" in sys.argv
SITE = "https://moonlitwindows.com"
LLC = "Joshua Israel Ventures LLC"
EMAIL = "joshuaofisrael@gmail.com"
TODAY = "2026-10-08"
UPDATED = "8 October 2026"
changed = []

def write(rel, new):
    p = ROOT / rel
    old = p.read_text(encoding="utf-8") if p.exists() else None
    if new != old:
        changed.append(rel)
        if not CHECK:
            p.write_text(new, encoding="utf-8")

def legal_footer(p):
    return (f'<div class="operated-by footer-legal"><p>© 2026 {LLC}. All rights reserved. Moonlit Windows is owned and operated by {LLC}.</p>'
            f'<p class="footer-legal-links"><a href="{p}terms.html">Terms</a> · <a href="{p}privacy.html">Privacy</a> · '
            f'<a href="{p}disclaimer.html">Disclaimer</a> · <a href="{p}contact.html">Contact</a></p></div>')

OLD_OWNER = '<div class="operated-by">Operated by Joshua Israel Ventures LLC</div>'

def fix_footer(s, p):
    m = re.search(r"<footer.*?</footer>", s, re.S)
    if not m:
        return s
    f = re.sub(r"\s*<div>©[^<]*</div>", "", m.group(0))
    if OLD_OWNER in f:
        f = f.replace(OLD_OWNER, legal_footer(p))
    elif "footer-legal" not in f:
        f = f.replace("</footer>", "  " + legal_footer(p) + "\n  </footer>")
    return s[: m.start()] + f + s[m.end():]

BRAND = {"@type": "Brand", "name": "Moonlit Windows", "alternateName": ["Night Shade Art", "Night Windows", "Prompt Framed"]}
SELLER = {"@type": "Organization", "@id": SITE + "/#org", "name": LLC, "url": SITE + "/"}

def fix_ld(x, key=None):
    if isinstance(x, list):
        return [fix_ld(i, key) for i in x]
    if not isinstance(x, dict):
        return x
    t = x.get("@type")
    if key == "seller" and t == "Organization":
        return dict(SELLER)
    if t == "Organization" and (x.get("@id") == SITE + "/#org" or x.get("name") == "Moonlit Windows"):
        x["name"] = LLC
        x["legalName"] = LLC
        x.pop("alternateName", None)
        x["brand"] = dict(BRAND)
    if t == "Product" and "brand" in x:
        x["brand"] = {"@type": "Brand", "name": "Moonlit Windows"}
    return {k: (v if k == "brand" else fix_ld(v, k)) for k, v in x.items()}

LD_RE = re.compile(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S)

def fix_blocks(s):
    def sub(m):
        inner = m.group(2)
        d = json.loads(inner)
        nd = fix_ld(json.loads(inner))
        if nd == d:
            return m.group(0)
        lead = re.match(r"\s*", inner).group(0)
        trail = inner[len(inner.rstrip()):]
        return m.group(1) + lead + json.dumps(nd, ensure_ascii=False, indent=2) + trail + m.group(3)
    return LD_RE.sub(sub, s)

# ---------------- legal pages ----------------
def section(h, *paras):
    out = [f"    <h2>{h}</h2>"]
    for p in paras:
        out.append(p if p.lstrip().startswith("<ul") else f"    <p>{p}</p>")
    return "\n".join(out)

def ul(*items):
    return "    <ul>\n" + "\n".join(f"      <li>{i}</li>" for i in items) + "\n    </ul>"

MAIL = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'

TERMS = dict(
    slug="terms.html", crumb="Terms",
    title="Terms of Use and Sale | Moonlit Windows",
    h1="Terms of Use and Sale",
    desc=f"Terms for using moonlitwindows.com and buying Night Windows posters, framed prints and wall murals. Orders are contracts with {LLC}, which owns the Moonlit Windows brand.",
    lead=(f"These terms apply when you use moonlitwindows.com or buy from it. The shop is run by {LLC}. Moonlit Windows, Night Windows, "
          f"Night Shade Art and Prompt Framed are brands owned by {LLC}, not separate companies, so when you place an order your contract is with "
          f"{LLC} (“we”, “us”)."),
    body=[
        section("1. Orders and payment",
                "Orders are placed through Stripe Checkout, which opens when you press a buy button. Stripe processes your payment; we never see or store your full card number.",
                "Your order is accepted when payment is completed and Stripe emails you a receipt. If we cannot produce an item, or a price was shown in error, we will contact you and refund the order in full."),
        section("2. Prices and currency",
                "Prices on this site are in US dollars (USD) and include shipping as stated on each product. Stripe may show and charge the price in your local currency based on your location; the amount and currency shown at checkout are what you pay. Your bank or card issuer may add its own fees.",
                "Orders shipped outside the United States may be subject to import duties or taxes charged by the destination country. These are the buyer’s responsibility."),
        section("3. Made to order, printing and shipping",
                "Every poster, framed print and wall mural is made to order after you buy. Items are printed and shipped by third-party print partners, and delivered by postal or courier services.",
                "Delivery times are estimates. Peel-and-stick wall murals usually ship within 1–2 weeks. Because each item is made to order, please contact us as soon as possible if you need to change an order; once production has started we may not be able to change or cancel it."),
        section("4. The products",
                "Posters are 12×18 in on enhanced matte paper. Framed prints are the same 12×18 in print in a black frame. Wall murals are 4×6 ft (48×72 in) on removable peel-and-stick polyester.",
                "Murals need no paste and remove cleanly from most smooth painted walls, but results depend on the wall surface and paint. Test a small corner first; we are not responsible for damage to wall surfaces."),
        section("5. Damaged or misprinted items",
                f"If your item arrives damaged or misprinted, email {MAIL} within 30 days of delivery with your order details and a photo of the problem, and we will replace it or refund it.",
                "This does not affect any rights you have under the consumer laws that apply to you."),
        section("6. Images, copyright and permitted use",
                f"The artwork, images and text on this site are owned by or licensed to {LLC}. Images are offered for decor. Buying a print gives you the physical item for display; it does not transfer copyright or give you any right to reproduce, scan, copy, resell copies of, or commercially use the image.",
                "Please don’t copy, download for reuse, or redistribute images from this site or our social accounts without written permission."),
        section("7. Promo codes",
                "Promo codes apply only as shown at checkout, have no cash value, and may be changed or withdrawn at any time."),
        section("8. Warranty disclaimer",
                "Except for the promise in section 5 and any rights that cannot be excluded by law, the site and all products are provided “as is” and “as available”, without warranties of any kind, express or implied, including warranties of merchantability, fitness for a particular purpose and non-infringement."),
        section("9. Limitation of liability",
                f"To the fullest extent permitted by law, {LLC} will not be liable for any indirect, incidental, special, consequential or punitive damages, or for lost profits or data, arising from your use of the site or any product. Our total liability for any claim relating to an order is limited to the amount you paid for that order."),
        section("10. Governing law",
                "These terms are governed by the laws of the State of Florida, USA, without regard to its conflict-of-law rules. Any dispute will be handled by the state or federal courts located in Florida, unless the consumer laws of your country require otherwise."),
        section("11. Changes",
                "We may update these terms from time to time. The date at the top shows the latest version, and the terms in force when you place an order apply to that order."),
        section("12. Contact",
                f"Questions about these terms or an order: {MAIL}, or use the <a href=\"./contact.html\">contact page</a>."),
    ],
)

PRIVACY = dict(
    slug="privacy.html", crumb="Privacy",
    title="Privacy Policy | Moonlit Windows",
    h1="Privacy Policy",
    desc=f"How {LLC}, which owns the Moonlit Windows brand, handles personal data: Stripe checkout, order fulfilment by print partners, Google Analytics and email.",
    lead=(f"{LLC} is the data controller for moonlitwindows.com. Moonlit Windows is a brand of {LLC}. This policy explains what personal data "
          f"is collected when you visit or buy, why, and who it is shared with. Contact: {MAIL}."),
    body=[
        section("What we collect and why",
                ul("<strong>Purchases (Stripe).</strong> Checkout happens on Stripe. Stripe collects your payment details, email address, name and billing and shipping address to take payment and send your receipt. We receive the order details (name, email, shipping address, items and amount) but not your full card number. Stripe handles payment data under its own <a href=\"https://stripe.com/privacy\" rel=\"noopener\">privacy policy</a>.",
                   "<strong>Fulfilment.</strong> To make and deliver your order, we share your name, shipping address and order contents (and, where a carrier needs it, your email or phone number) with our third-party print partner and the delivery carrier.",
                   "<strong>Promo codes.</strong> If you enter a promo code at checkout, it is recorded with your order. This is how a referring creator’s commission is calculated.",
                   "<strong>Analytics (Google Analytics).</strong> Our pages load Google Analytics 4, which uses cookies to measure visits: pages viewed, approximate location, device and browser, and the site that referred you. We use this to understand which pages are useful. You can block it with your browser settings or the <a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"noopener\">Google Analytics opt-out add-on</a>. See <a href=\"https://policies.google.com/privacy\" rel=\"noopener\">Google’s privacy policy</a>.",
                   "<strong>Fonts.</strong> Most pages load fonts from Google Fonts, so your browser sends your IP address to Google when it fetches them.",
                   "<strong>Hosting.</strong> The site is hosted on GitHub Pages. GitHub may log visitors’ IP addresses to operate and secure the service.",
                   "<strong>Email and the contact form.</strong> The contact form does not send anything to our server; it opens your own email app with your message filled in. If you email us, we receive your email address and whatever you write, and use it only to reply and to handle your order.")),
        section("What we don’t do",
                "We don’t run advertising or AdSense, we don’t use affiliate tracking cookies, and we don’t sell or rent your personal data."),
        section("Legal bases",
                "We process order data to perform our contract with you and to meet tax and accounting obligations, and analytics data based on our legitimate interest in understanding how the site is used, or your consent where the law requires it."),
        section("How long we keep it",
                "Order records are kept for as long as needed to fulfil the order and to meet tax, accounting and legal obligations. Emails are kept for as long as needed to handle your request. Google Analytics data is kept according to the retention settings of our Analytics account."),
        section("International transfers",
                "Our service providers, including Stripe, Google, GitHub and our print partners, may process data in the United States and other countries."),
        section("Your rights",
                f"Depending on where you live (for example under the GDPR in the EU or UK, or California law), you may have the right to access, correct, delete or receive a copy of your personal data, to object to or restrict its use, and to complain to a data protection authority. To make a request, email {MAIL}."),
        section("Children",
                "This site is not directed at children under 13, and we do not knowingly collect their personal data."),
        section("Changes",
                "We may update this policy. The date at the top shows the latest version."),
        section("Contact",
                f"Data controller: {LLC}. Email: {MAIL}."),
    ],
)

DISCLAIMER = dict(
    slug="disclaimer.html", crumb="Disclaimer",
    title="Disclaimer | Moonlit Windows",
    h1="Disclaimer",
    desc=f"Colour and screen accuracy, watermarked previews, general information and creator promo code disclosure for Moonlit Windows, a brand of {LLC}.",
    lead=(f"Moonlit Windows is a brand of {LLC}. Please read these notes about how the artwork looks on screen and in print, what our guides are, "
          "and how creator promo codes work."),
    body=[
        section("Colour and screen accuracy",
                "Screens differ in brightness, colour and contrast, so a print can look slightly different from what you see on your device. This is especially true for dark night scenes, which can look brighter on a phone than on paper. Paper, framing and room lighting also change how colours read."),
        section("Images and previews",
                "The images on this site show the artwork itself. Website and social media previews carry a small Night Shade Art watermark to discourage copying; your print is made from a clean file without the watermark.",
                "Night Windows pieces are artistic interpretations of real and imagined places at night. They are not documentary photographs, and landmarks may be stylised."),
        section("General information only",
                "Our size guide, room suggestions and other content are general information to help you choose wall art. They are not professional interior design or other professional advice, and using this site does not create a professional relationship of any kind."),
        section("Third-party services and links",
                "Checkout is provided by Stripe, and some links lead to Instagram and other third-party sites. We are not responsible for the content or practices of those sites."),
        section("Creator promo codes",
                "Some creators share Moonlit Windows promo codes. When someone orders with a creator’s code, that creator may earn a commission on the sale. Creators who post about us are expected to disclose this relationship."),
        section("Contact",
                f"Questions: {MAIL}, or use the <a href=\"./contact.html\">contact page</a>."),
    ],
)

def legal_page(cfg, header, footer):
    url = f"{SITE}/{cfg['slug']}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#webpage", "name": cfg["h1"], "url": url, "description": cfg["desc"],
         "dateModified": TODAY, "inLanguage": "en",
         "isPartOf": {"@type": "WebSite", "@id": SITE + "/#website", "name": "Moonlit Windows", "url": SITE + "/"},
         "publisher": {"@type": "Organization", "@id": SITE + "/#org", "name": LLC, "legalName": LLC, "url": SITE + "/", "brand": BRAND}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": cfg["crumb"], "item": url}]}]}
    body = "\n\n".join(cfg["body"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-663R8VD62L"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-663R8VD62L');</script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{cfg['title']}</title>
  <meta name="description" content="{cfg['desc']}">
  <link rel="canonical" href="{url}">
  <meta property="og:site_name" content="Moonlit Windows">
  <meta property="og:title" content="{cfg['title']}">
  <meta property="og:description" content="{cfg['desc']}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/night-windows-contact-sheet.jpg">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=Outfit:wght@380;560;650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json" data-ld="page">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <div class="wrap prose legal">
{header}
    <p class="kicker">Legal</p>
    <h1>{cfg['h1']}</h1>
    <p class="answer-first">{cfg['lead']}</p>
    <p class="note">Last updated: {UPDATED}</p>

{body}
  </div>
  {footer}
</body>
</html>
"""

CSS = """
/* legal footer (brand of Joshua Israel Ventures LLC) */
.site-footer .footer-legal { width: min(var(--max), calc(100% - 2rem)); margin: 1.1rem auto 0; padding-top: 1rem; border-top: 1px solid var(--line); color: var(--ink); font-size: 0.98rem; line-height: 1.6; }
.site-footer .footer-legal p { margin: 0.2rem 0; }
.site-footer .footer-legal a { color: var(--ink); text-decoration: underline; text-underline-offset: 3px; }
.site-footer .footer-legal a:hover { color: var(--accent); }
.legal ul { padding-left: 1.2rem; }
.legal li { margin: 0.5rem 0; }
"""

def main():
    pages = sorted(glob.glob(str(ROOT / "*.html")) + glob.glob(str(ROOT / "pieces" / "*.html")))
    for path in pages:
        rel = str(Path(path).relative_to(ROOT))
        if rel in ("terms.html", "privacy.html", "disclaimer.html"):
            continue
        s = Path(path).read_text(encoding="utf-8")
        n = fix_footer(s, "../" if rel.startswith("pieces/") else "./")
        n = fix_blocks(n)
        if rel == "about.html":
            old = "It is operated by Joshua Israel Ventures LLC and shares the series on Instagram as Night Shade Art."
            new = "Moonlit Windows is a brand of Joshua Israel Ventures LLC. The LLC runs the shop and handles every order, and the series is shared on Instagram as Night Shade Art."
            if old in n:
                n = n.replace(old, new)
            elif new not in n:
                print("WARN about.html anchor missing")
        write(rel, n)

    about = (ROOT / "about.html").read_text(encoding="utf-8") if CHECK is False else fix_footer((ROOT / "about.html").read_text(encoding="utf-8"), "./")
    header = about[about.index("    <header"): about.index("</header>") + len("</header>")]
    footer = re.search(r"<footer.*?</footer>", about, re.S).group(0)
    for cfg in (TERMS, PRIVACY, DISCLAIMER):
        write(cfg["slug"], legal_page(cfg, header, footer))

    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    if ".footer-legal" not in css:
        write("styles.css", css.rstrip("\n") + "\n" + CSS)

    js = (ROOT / "site.js").read_text(encoding="utf-8")
    old = 'return sku === "framed" ? stripe.framedUrl || null : stripe.posterUrl || null;'
    new = ('if (sku === "framed") return stripe.framedUrl || null;\n'
           '    if (sku === "mural") return stripe.muralUrl || null;\n'
           '    return stripe.posterUrl || null;')
    if old in js:
        write("site.js", js.replace(old, new))

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    n = llms.replace("The series is also published as Prompt Framed and shared on Instagram as Night Shade Art (@moonnightshadeart). Operated by Joshua Israel Ventures LLC.",
                     "Moonlit Windows is a brand, not a separate company: the shop is owned and operated by Joshua Israel Ventures LLC, which handles every order. Night Windows, Night Shade Art (Instagram @moonnightshadeart) and Prompt Framed are also brands of Joshua Israel Ventures LLC.")
    if "## Legal" not in n:
        n = n.rstrip("\n") + ("\n\n## Legal\n\n"
             f"- [Terms of Use and Sale]({SITE}/terms.html): Orders are contracts with Joshua Israel Ventures LLC; Stripe checkout, made-to-order printing, USD pricing, damaged or misprinted items, Florida law\n"
             f"- [Privacy Policy]({SITE}/privacy.html): What is collected (Stripe checkout, fulfilment, Google Analytics, email) and how to make a privacy request\n"
             f"- [Disclaimer]({SITE}/disclaimer.html): Colour and screen accuracy, watermarked previews, creator promo code commissions\n")
    write("llms.txt", n)

    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    n = sm
    for slug in ("terms.html", "privacy.html", "disclaimer.html"):
        loc = f"{SITE}/{slug}"
        if f"<loc>{loc}</loc>" not in n:
            n = n.replace("</urlset>", f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod></url>\n</urlset>")
    for rel in changed:
        if rel.endswith(".html") or rel == "llms.txt":
            url = f"{SITE}/" if rel == "index.html" else f"{SITE}/{rel}"
            n = re.sub(rf"(<loc>{re.escape(url)}</loc>)(<lastmod>[^<]*</lastmod>)?", rf"\g<1><lastmod>{TODAY}</lastmod>", n)
    write("sitemap.xml", n)

    print(("WOULD CHANGE" if CHECK else "CHANGED"), len(changed), "files")
    print(" ".join(c for c in changed if not c.startswith("pieces/")), f"+ {sum(c.startswith('pieces/') for c in changed)} piece pages")
    if not CHECK:
        Path("/tmp/legal_changed.txt").write_text("\n".join(changed) + "\n")

if __name__ == "__main__":
    main()
