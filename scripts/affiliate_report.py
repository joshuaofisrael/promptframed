#!/usr/bin/env python3
"""Affiliate commission report for Night Windows promo codes (default: Sakshi / SAKSHI10).

Lists completed Stripe Checkout Sessions that redeemed the promotion code and prints, per order:
date, piece, variant, qty, gross, discount, net paid, refunded, and commission on net paid
(default 20%), followed by a total owed per calendar month (UTC).

Two ways to feed it:

  1. Live Stripe API (needs a secret or restricted key with read access to Checkout Sessions):
       STRIPE_API_KEY=rk_live_... python3 scripts/affiliate_report.py
       python3 scripts/affiliate_report.py --month 2026-10 --csv out.csv
     Also reads STRIPE_SECRET_KEY if STRIPE_API_KEY is unset. Keys are never stored in the repo.

  2. Offline, from a JSON dump pulled through the Stripe connector / Dashboard / CLI
     (see docs/AFFILIATES.md, "Pulling the commission report"):
       python3 scripts/affiliate_report.py --from-json sessions.json
     The file may be a Stripe list object ({"data": [...]}) or a plain array of sessions,
     ideally fetched with expand[]=data.total_details.breakdown (and optionally
     data.payment_intent.latest_charge for refund amounts).

With no key and no --from-json it prints those instructions and exits 2.
Read-only: never writes to Stripe. Standard library only (no `stripe` package needed).
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.stripe.com/v1"

DEFAULT_CODE = "SAKSHI10"
DEFAULT_PROMO_ID = "promo_1ULhq0K3OWN3aipgp2uUwWtr"
DEFAULT_COUPON_ID = "dOuqUokk"
DEFAULT_RATE = 0.20

CONNECTOR_HELP = f"""\
No Stripe API key found (STRIPE_API_KEY / STRIPE_SECRET_KEY).

Get the same report through the Stripe connector (account acct_1U7tYaK3OWN3aipg, livemode=true):
  1. stripe_api_read  GetCheckoutSessions
       {{"status": "complete", "limit": 100,
        "created": {{"gte": <month start unix>, "lt": <next month start unix>}},
        "expand": ["data.total_details.breakdown"]}}
     Page with "starting_after": <last session id> while has_more is true.
  2. Keep sessions where total_details.breakdown.discounts[].discount.promotion_code
     == {DEFAULT_PROMO_ID} (code {DEFAULT_CODE}), or discounts[].promotion_code == that id.
  3. Save the combined list as sessions.json and run:
       python3 scripts/affiliate_report.py --from-json sessions.json
     (or compute by hand: net = amount_total, gross = amount_subtotal,
      discount = total_details.amount_discount, commission = 20% of net, all in cents).
"""


def api_key() -> str | None:
    return os.environ.get("STRIPE_API_KEY") or os.environ.get("STRIPE_SECRET_KEY")


def stripe_get(path: str, params: list[tuple[str, str]], key: str) -> dict:
    url = f"{API}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{key}:".encode()).decode())
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def month_bounds(month: str) -> tuple[int, int]:
    y, m = map(int, month.split("-"))
    start = datetime(y, m, 1, tzinfo=timezone.utc)
    end = datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=timezone.utc)
    return int(start.timestamp()), int(end.timestamp())


def resolve_promo_id(code: str, key: str) -> str | None:
    res = stripe_get("/promotion_codes", [("code", code), ("limit", "10")], key)
    ids = [p["id"] for p in res.get("data", [])]
    return ids[0] if ids else None


def fetch_sessions(key: str, month: str | None) -> list[dict]:
    params = [
        ("status", "complete"),
        ("limit", "100"),
        ("expand[]", "data.total_details.breakdown"),
        ("expand[]", "data.payment_intent.latest_charge"),
    ]
    if month:
        gte, lt = month_bounds(month)
        params += [("created[gte]", str(gte)), ("created[lt]", str(lt))]
    out, after = [], None
    while True:
        page = stripe_get("/checkout/sessions", params + ([("starting_after", after)] if after else []), key)
        out += page.get("data", [])
        if not page.get("has_more") or not page.get("data"):
            return out
        after = page["data"][-1]["id"]


def _promo_of(d) -> str | None:
    if isinstance(d, dict):
        p = d.get("promotion_code")
        return p.get("id") if isinstance(p, dict) else p
    return None


def uses_promo(s: dict, promo_id: str, code: str) -> bool:
    for d in s.get("discounts") or []:
        if _promo_of(d) == promo_id:
            return True
    breakdown = (s.get("total_details") or {}).get("breakdown") or {}
    for item in breakdown.get("discounts") or []:
        disc = item.get("discount") or {}
        p = disc.get("promotion_code")
        if (p.get("id") if isinstance(p, dict) else p) == promo_id:
            return True
        if isinstance(p, dict) and str(p.get("code", "")).upper() == code.upper():
            return True
    return False


def piece_titles() -> dict[str, str]:
    try:
        return {p["slug"]: p["title"] for p in json.loads((ROOT / "products.json").read_text())}
    except Exception:
        return {}


def refunded_amount(s: dict) -> int:
    pi = s.get("payment_intent")
    if isinstance(pi, dict):
        ch = pi.get("latest_charge")
        if isinstance(ch, dict):
            return int(ch.get("amount_refunded") or 0)
    return 0


def build_rows(sessions: list[dict], promo_id: str, code: str, rate: float, month: str | None) -> list[dict]:
    titles = piece_titles()
    rows = []
    for s in sessions:
        if s.get("status") not in (None, "complete") or not uses_promo(s, promo_id, code):
            continue
        created = datetime.fromtimestamp(s["created"], tz=timezone.utc)
        if month and created.strftime("%Y-%m") != month:
            continue
        md = s.get("metadata") or {}
        slug = md.get("slug", "?")
        net = int(s.get("amount_total") or 0)
        refunded = refunded_amount(s)
        commissionable = max(net - refunded, 0)
        rows.append({
            "date": created.strftime("%Y-%m-%d"),
            "month": created.strftime("%Y-%m"),
            "session": s["id"],
            "piece": titles.get(slug, slug),
            "variant": md.get("variant", "?"),
            "gross": int(s.get("amount_subtotal") or 0),
            "discount": int((s.get("total_details") or {}).get("amount_discount") or 0),
            "net": net,
            "refunded": refunded,
            "commission": round(commissionable * rate),
            "currency": (s.get("currency") or "usd").upper(),
        })
    return sorted(rows, key=lambda r: (r["date"], r["session"]))


def money(c: int) -> str:
    return f"${c / 100:,.2f}"


def print_report(rows: list[dict], code: str, rate: float) -> None:
    print(f"Affiliate report: promo code {code}, commission {rate:.0%} of net paid (after refunds)\n")
    if not rows:
        print("No completed orders used this code in the selected period.")
        return
    hdr = f"{'Date':<10}  {'Piece':<32} {'Variant':<7} {'Gross':>9} {'Discount':>9} {'Net paid':>9} {'Refund':>8} {'Comm.':>8}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['date']:<10}  {r['piece'][:32]:<32} {r['variant']:<7} {money(r['gross']):>9} "
              f"{money(r['discount']):>9} {money(r['net']):>9} {money(r['refunded']):>8} {money(r['commission']):>8}")
    by_month = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        m = by_month[r["month"]]
        m[0] += 1
        m[1] += r["net"] - r["refunded"]
        m[2] += r["commission"]
    print("\nMonthly totals owed (UTC months; pay monthly):")
    for month in sorted(by_month):
        n, net, comm = by_month[month]
        print(f"  {month}: {n} order(s), net {money(net)} -> commission owed {money(comm)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--code", default=DEFAULT_CODE)
    ap.add_argument("--promo-id", default=None, help=f"promotion code id (default {DEFAULT_PROMO_ID} for {DEFAULT_CODE})")
    ap.add_argument("--rate", type=float, default=DEFAULT_RATE)
    ap.add_argument("--month", help="YYYY-MM (UTC) to limit the report")
    ap.add_argument("--from-json", type=Path, help="offline: Stripe list/array of checkout sessions")
    ap.add_argument("--csv", type=Path, help="also write rows to this CSV")
    a = ap.parse_args()

    promo_id = a.promo_id or (DEFAULT_PROMO_ID if a.code.upper() == DEFAULT_CODE else None)
    if a.from_json:
        raw = json.loads(a.from_json.read_text())
        sessions = raw.get("data", []) if isinstance(raw, dict) else raw
    else:
        key = api_key()
        if not key:
            print(CONNECTOR_HELP, file=sys.stderr)
            return 2
        promo_id = promo_id or resolve_promo_id(a.code, key)
        sessions = fetch_sessions(key, a.month)
    if not promo_id:
        print(f"Unknown promotion code id for {a.code}; pass --promo-id.", file=sys.stderr)
        return 2

    rows = build_rows(sessions, promo_id, a.code, a.rate, a.month)
    print_report(rows, a.code, a.rate)
    if a.csv:
        with a.csv.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["date"])
            w.writeheader()
            w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
