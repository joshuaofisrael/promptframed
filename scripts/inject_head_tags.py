#!/usr/bin/env python3
"""Idempotently add Google Analytics 4 (all public pages) and the Search Console
verification meta (homepage) to the site's HTML. Run after publishing new pages."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
GA_ID = "G-663R8VD62L"
GSC = '<meta name="google-site-verification" content="B9Kg6mHXUkaRdKQCfbYAPrAzRt2JqRSxC2UIlc0Iepo" />'
GA = f'''<!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>'''
SKIP = {"instagram-kit", "docs", "node_modules", ".git", "assets"}
changed = 0
for p in ROOT.rglob("*.html"):
    if SKIP & set(p.relative_to(ROOT).parts):
        continue
    s = p.read_text(encoding="utf-8"); o = s
    if GA_ID not in s:
        s = re.sub(r"<head([^>]*)>", lambda m: f"<head{m.group(1)}>\n  {GA}", s, count=1)
    if p == ROOT / "index.html" and "google-site-verification" not in s:
        s = re.sub(r"<head([^>]*)>", lambda m: f"<head{m.group(1)}>\n  {GSC}", s, count=1)
    if s != o:
        p.write_text(s, encoding="utf-8"); changed += 1
print(f"updated {changed} pages")
