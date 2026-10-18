#!/usr/bin/env python3
"""Idempotently add the Cloudflare Web Analytics beacon just before </body> on every
HTML page of moonlitwindows.com. Safe to rerun after any publish/build script."""
import pathlib, sys
TOKEN = "899375a6262144aabf5184589abd580c"
BEACON = ("<script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
          "data-cf-beacon='{\"token\": \"" + TOKEN + "\"}'></script>")
ROOT = pathlib.Path(__file__).resolve().parent.parent
def apply(text):
    if "static.cloudflareinsights.com/beacon.min.js" in text or "</body>" not in text:
        return text
    i = text.rfind("</body>")
    return text[:i] + BEACON + "\n" + text[i:]
def main():
    changed = total = 0
    for f in sorted(list(ROOT.glob("*.html")) + list((ROOT / "pieces").glob("*.html"))):
        t = f.read_text(); n = apply(t); total += 1
        if n != t: f.write_text(n); changed += 1
    print(f"cf beacon: {changed} updated, {total} pages checked")
if __name__ == "__main__":
    sys.exit(main())
