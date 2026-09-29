#!/usr/bin/env python3
"""Write Stripe Payment Link buy buttons into buy.html and every piece page.

Source of truth: products.json -> stripe.posterUrl / stripe.framedUrl.

  python3 scripts/apply_stripe_links.py          # rewrite buy.html + pieces/*.html
  python3 scripts/apply_stripe_links.py --check  # exit 1 if any piece lacks live links

Idempotent. Content between <!-- buy:start --> and <!-- buy:end --> markers is
regenerated on every run; the first run converts the older placeholder blocks.
Pieces whose links are still null get a quiet "coming soon" block instead of
dead buttons. Does NOT touch images, print masters, git, or Stripe.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products.json"
BUY = ROOT / "buy.html"
PIECES = ROOT / "pieces"

PRICE_LINE = "$29 poster · $69 framed (12×18)"
START, END = "<!-- buy:start -->", "<!-- buy:end -->"


def is_live(url) -> bool:
    return isinstance(url, str) and url.startswith("https://buy.stripe.com/")


def load():
    return json.loads(PRODUCTS.read_text(encoding="utf-8"))


def piece_desc(slug: str) -> str:
    page = PIECES / f"{slug}.html"
    if not page.exists():
        return ""
    m = re.search(r'<p class="desc">(.*?)</p>', page.read_text(encoding="utf-8"), re.S)
    return m.group(1).strip() if m else ""


def buttons(item, indent: str) -> str:
    s = item.get("stripe") or {}
    slug = item["slug"]
    if is_live(s.get("posterUrl")) and is_live(s.get("framedUrl")):
        return (
            f'{indent}<p class="price-line">{PRICE_LINE}</p>\n'
            f'{indent}<div class="actions buy-actions">\n'
            f'{indent}  <a class="btn" data-buy="{slug}" data-sku="poster" href="{s["posterUrl"]}">Buy this print · Poster $29</a>\n'
            f'{indent}  <a class="btn secondary" data-buy="{slug}" data-sku="framed" href="{s["framedUrl"]}">Buy framed · $69</a>\n'
            f'{indent}</div>\n'
        )
    return f'{indent}<p class="price-line">{PRICE_LINE}</p>\n{indent}<p class="note">This window opens for orders soon.</p>\n'


# ---------- piece pages ----------
PIECE_NOTE = "Enhanced matte poster or black-framed print, 12×18 in. Shipping included. Secure checkout by Stripe; your receipt arrives by email."


def piece_block(item) -> str:
    ind = "        "
    return (
        f"{START}\n"
        f'{ind}<section class="buy-box" id="buy">\n'
        + buttons(item, ind + "  ")
        + f'{ind}  <p class="note">{PIECE_NOTE}</p>\n'
        f"{ind}</section>\n"
        f"{ind}{END}"
    )


def update_piece(item) -> bool:
    page = PIECES / f"{item['slug']}.html"
    if not page.exists():
        print(f"  ! missing page {page.name}")
        return False
    src = page.read_text(encoding="utf-8")
    block = piece_block(item)
    if START in src:
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, src, flags=re.S)
    else:
        # Template A (pieces 01-10): soft-cta + actions + buy-status note
        pat_a = re.compile(
            r'<p class="soft-cta">.*?</p>\s*<div class="actions">.*?</div>\s*<p class="note" id="buy-status">.*?</p>',
            re.S,
        )
        # Template B (pieces 11+): actions with "Buy this print" + nav link, then a note
        pat_b = re.compile(
            r'<div class="actions">\s*<a class="btn" href="\.\./buy\.html#[^"]*">Buy this print</a>\s*'
            r'(<a class="btn secondary" href="[^"]*">[^<]*</a>)\s*</div>\s*<p class="note">Want a poster\?.*?</p>',
            re.S,
        )
        if pat_a.search(src):
            new = pat_a.sub(lambda _: block, src, count=1)
        elif pat_b.search(src):
            new = pat_b.sub(lambda m: block + f'\n        <p class="window-nav">{m.group(1)}</p>', src, count=1)
        else:
            print(f"  ! no buy block found in {page.name}; add {START}{END} markers by hand")
            return False
    if new != src:
        page.write_text(new, encoding="utf-8")
    return True


# ---------- buy.html ----------
def buy_card(item) -> str:
    from PIL import Image  # optional, only for orientation

    slug, title = item["slug"], html.escape(item["title"])
    cls = "card"
    try:
        w, h = Image.open(ROOT / "assets" / item["asset"]).size
        if w > h:
            cls += " landscape"
    except Exception:
        pass
    desc = piece_desc(slug)
    ind = "          "
    return (
        f'      <article class="{cls}" id="{slug}">\n'
        f'        <a href="./pieces/{slug}.html"><img src="./assets/{item["asset"]}" alt="{title}" loading="lazy"></a>\n'
        f'        <div class="meta">\n'
        f"{ind}<h2>{title}</h2>\n"
        + (f"{ind}<p>{desc}</p>\n" if desc else "")
        + buttons(item, ind)
        + f"        </div>\n"
        f"      </article>"
    )


def update_buy(items) -> None:
    src = BUY.read_text(encoding="utf-8")
    grid = f"{START}\n" + "\n".join(buy_card(i) for i in items) + f"\n      {END}"
    if START in src:
        src = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: grid, src, flags=re.S)
    else:
        src = re.sub(
            r'(<section class="grid">)\s*.*?\s*(</section>)',
            lambda m: f"{m.group(1)}\n      {grid}\n    {m.group(2)}",
            src,
            count=1,
            flags=re.S,
        )
    # Older publish scripts append cards just before </section>; those are now
    # generated from products.json above, so drop any strays after the marker.
    src = re.sub(re.escape(END) + r"\s*<article.*?(?=\s*</section>)", END, src, count=1, flags=re.S)
    BUY.write_text(src, encoding="utf-8")


def main() -> int:
    items = load()
    missing = [i["slug"] for i in items if not (is_live((i.get("stripe") or {}).get("posterUrl")) and is_live((i.get("stripe") or {}).get("framedUrl")))]
    if "--check" in sys.argv:
        for s in missing:
            print(f"missing live Stripe links: {s}")
        print(f"{len(items) - len(missing)}/{len(items)} pieces live")
        return 1 if missing else 0
    ok = sum(update_piece(i) for i in items)
    update_buy(items)
    print(f"piece pages updated: {ok}/{len(items)}; buy.html regenerated ({len(items)} cards)")
    if missing:
        print("pieces without live links (showing 'soon'):", ", ".join(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
