#!/usr/bin/env python3
"""SEO (6 Oct 2026): align pieces 01–10 with the title/meta pattern used by 11+.

Pieces 01–10 were built before the piece-page template settled, so their
<title> reads "<Title> — Night Windows | Prompt Framed" (no "print") and their
meta description is only the mood line (no "poster and framed print"). Pieces
11–40 use:
  <title>{Title} — Night Windows print | Prompt Framed</title>
  description: "{Title} from the Night Windows series. Poster and framed print options. {mood}"
and the Product JSON-LD description matches the meta description.

This rewrites only <title>, <meta name="description"> and the Product
"description" in JSON-LD. og:/twitter: tags stay as they are (11+ keep the
mood line there too). Idempotent; no git, no images, no Stripe.

  python3 scripts/seo_align_early_piece_titles.py           # apply
  python3 scripts/seo_align_early_piece_titles.py --dry-run # show what would change
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIECES = ROOT / "pieces"
CATALOG = ROOT / "gallery" / "catalog.json"
PREFIX = "Poster and framed print options."


def main() -> int:
    dry = "--dry-run" in sys.argv
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    early = [e for e in catalog if int(e["photoNumber"]) <= 10]
    changed = 0
    for e in early:
        path = PIECES / f"{e['slug']}.html"
        src = path.read_text(encoding="utf-8")
        title = e["title"]
        m = re.search(r'<meta name="description" content="([^"]*)"', src)
        if not m:
            print(f"  ! no meta description in {path.name}")
            continue
        mood = html.unescape(m.group(1))
        if PREFIX in mood:
            print(f"  skip {path.name} (already aligned)")
            continue
        new_desc = f"{title} from the Night Windows series. {PREFIX} {mood}"
        out = re.sub(
            r"<title>[^<]*</title>",
            f"<title>{title} — Night Windows print | Prompt Framed</title>",
            src,
            count=1,
        )
        out = out.replace(m.group(0), f'<meta name="description" content="{html.escape(new_desc, quote=True)}"', 1)
        # Product JSON-LD description (first "description" inside the Product node).
        jm = re.search(r'("@type": "Product",.*?"description": )("(?:[^"\\]|\\.)*")', out, re.S)
        if jm:
            out = out[: jm.start(2)] + json.dumps(new_desc, ensure_ascii=False) + out[jm.end(2) :]
        else:
            print(f"  ! no Product JSON-LD description in {path.name}")
        print(f"  {path.name}: {title} — Night Windows print")
        if not dry:
            path.write_text(out, encoding="utf-8")
        changed += 1
    print(f"{'would update' if dry else 'updated'} {changed}/{len(early)} early piece pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
