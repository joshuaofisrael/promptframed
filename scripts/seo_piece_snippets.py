#!/usr/bin/env python3
"""Piece-page meta descriptions that fit Google's snippet (~155 chars).

Old pattern (from the commercial/keyword/mural passes) ran ~240 chars and opened
with the same boilerplate on every page, so the unique scene text never showed
in search results. New pattern, per piece with live poster + framed + mural links:

  "<Title> [moon ]poster $35, framed print $69, wall mural $149, shipping included. <scene>"

Only <meta name="description"> changes; og/twitter descriptions are untouched.
Idempotent. Usage:
  python3 scripts/seo_piece_snippets.py --check   # list pages that would change (exit 1 if any)
  python3 scripts/seo_piece_snippets.py           # rewrite
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIMIT = 158
META = re.compile(r'(<meta name="description" content=")([^"]*)(" />)')
OG = re.compile(r'<meta property="og:description" content="([^"]*)"')


def scene_of(page: str):
    m = OG.search(page)
    if not m:
        return None
    txt = html.unescape(m.group(1))
    # "Title: Night Windows poster $35 · framed print $69 (12×18, shipping included). Scene."
    parts = txt.split("shipping included). ", 1)
    return parts[1].strip() if len(parts) == 2 else None


def build(title: str, scene: str) -> str:
    noun = "poster" if "moon" in title.lower() else "moon poster"
    head = f"{title} {noun} $35, framed print $69, wall mural $149, shipping included. "
    room = LIMIT - len(head)
    if len(scene) <= room:
        return head + scene
    cut = scene[:room + 1]
    for seps in ((" while ", " as ", ": ", " beneath ", " under ", " — "), (", ",)):
        best = max(cut.rfind(sep) for sep in seps)
        if best > room * 0.4:
            return head + cut[:best].rstrip(",;:—- ") + "."
    return head + scene[:room].rsplit(" ", 1)[0].rstrip(",;:—- ") + "…"


def main() -> int:
    check = "--check" in sys.argv
    products = json.loads((ROOT / "products.json").read_text(encoding="utf-8"))
    changed, skipped = [], []
    for p in products:
        st = p.get("stripe") or {}
        live = all(str(st.get(k) or "").startswith("https://buy.stripe.com/") for k in ("posterUrl", "framedUrl", "muralUrl"))
        f = ROOT / "pieces" / f"{p['slug']}.html"
        if not live or not f.exists():
            skipped.append(p["slug"]); continue
        s = f.read_text(encoding="utf-8")
        scene = scene_of(s)
        if not scene:
            skipped.append(p["slug"]); continue
        new = html.escape(build(p["title"], scene), quote=True)
        m = META.search(s)
        if not m or m.group(2) == new:
            continue
        changed.append((p["slug"], len(html.unescape(new)), html.unescape(new)))
        if not check:
            f.write_text(s[:m.start(2)] + new + s[m.end(2):], encoding="utf-8")
    for slug, n, d in changed:
        print(f"{'WOULD CHANGE' if check else 'updated'} {slug} ({n}): {d}")
    if skipped:
        print("skipped (not fully live or no scene):", ", ".join(skipped))
    print(f"{len(changed)} {'to change' if check else 'updated'}")
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
