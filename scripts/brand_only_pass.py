#!/usr/bin/env python3
"""LLC rule (23 Oct 2026): owner/LLC names only on legal pages. Idempotent."""
import re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
LEGAL = {"terms.html", "privacy.html", "disclaimer.html", "contact.html"}
# Copyright rule (24 Oct 2026): copyright line only on true legal pages, never in sitewide footer.
COPY_PAGES = {"terms.html", "privacy.html", "disclaimer.html"}
COPY = "© 2026 Joshua Israel Ventures LLC. All rights reserved. Moonlit Windows is a trade name of Joshua Israel Ventures LLC, a Florida limited liability company."
LLC = "Joshua Israel Ventures LLC"
FOOT_RE = re.compile(r'<div class="operated-by footer-legal">.*?</div>', re.S)
def footer(prefix, legal=False):
    note = f'<p class="footer-legal-note">{COPY}</p>' if legal else ''
    return (f'<div class="operated-by footer-legal"><p><a href="{prefix}terms.html">Terms</a> · '
            f'<a href="{prefix}privacy.html">Privacy</a> · <a href="{prefix}disclaimer.html">Disclaimer</a> · '
            f'<a href="{prefix}contact.html">Contact</a></p>{note}</div>')
SENT = [
 ("is the Night Windows wall art shop of Joshua Israel Ventures LLC:", "is the Night Windows wall art shop:"),
 ("Night Windows is the gallery. Joshua Israel Ventures LLC is the studio.", "Night Windows is the gallery. Moonlit Windows is the shop."),
 (" Moonlit Windows is a brand of Joshua Israel Ventures LLC. The LLC runs the shop and handles every order, and the series", " Moonlit Windows runs the shop and handles every order, and the series"),
 ("<strong>Joshua Israel Ventures LLC</strong> is the studio behind Prompt Framed.", "<strong>Moonlit Windows</strong> is the studio behind Prompt Framed."),
]
def fix_jsonld_meta(t):
    def j(m):
        s = m.group(0)
        s = re.sub(r'\s*"legalName":\s*"(?:Joshua Israel Ventures LLC|Moonlit Windows)",?', '', s)
        return s.replace(LLC, "Moonlit Windows").replace('"Joshua Israel"', '"Moonlit Windows"')
    t = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>', j, t, flags=re.S)
    t = re.sub(r'<meta [^>]*>', lambda m: m.group(0).replace(LLC, "Moonlit Windows"), t)
    t = re.sub(r'<title>.*?</title>', lambda m: m.group(0).replace(LLC, "Moonlit Windows"), t)
    t = re.sub(r',(\s*})', r'\1', t) if False else t
    return t
def process(p):
    t = p.read_text(); o = t
    prefix = "../" if p.parent != ROOT else "./"
    legal = p.name in LEGAL and p.parent == ROOT
    t = FOOT_RE.sub(lambda m: footer(prefix, p.name in COPY_PAGES and p.parent == ROOT), t)
    t = fix_jsonld_meta(t)
    if not legal:
        for a, b in SENT: t = t.replace(a, b)
        t = t.replace(LLC, "Moonlit Windows")
    if t != o: p.write_text(t); return True
    return False
if __name__ == "__main__":
    files = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "gallery/reels" not in str(p)]
    ch = [str(p.relative_to(ROOT)) for p in files if process(p)]
    l = ROOT / "llms.txt"; t = l.read_text(); n = t.replace(LLC, "Moonlit Windows")
    if n != t: l.write_text(n); ch.append("llms.txt")
    print(len(ch)); print("\n".join(ch), file=sys.stderr)
