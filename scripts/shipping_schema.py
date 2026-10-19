#!/usr/bin/env python3
"""Shared OfferShippingDetails JSON-LD for every Offer on moonlitwindows.com.

Sources (2026-10-19):
- Countries: Stripe Payment Link shipping_address_collection.allowed_countries (docs/STRIPE_SITE_CHECKOUT.md).
- Handling: Joshua places each order with Printseekers within 1-2 business days (MURAL_FULFILLMENT.md),
  then Printseekers production: posters/framed 2-5 business days, wallpaper 2-4 (printseekers.com/faq).
  Murals are stretched to 3-10 days to match terms.html ("murals usually ship within 1-2 weeks").
- Transit: Printseekers Standard shipping 2-7 business days (printseekers.com/shipping); Standard is
  the method used in unit_costs.md / MURAL_FULFILLMENT.md.
Shipping included in price -> rate 0 USD.
Usage: python3 scripts/shipping_schema.py   (rewrites JSON-LD in every *.html, idempotent)
"""
import json, re, sys
from pathlib import Path

COUNTRIES = ["US", "GB", "CA", "AU", "NZ", "IE", "FR", "DE", "NL", "BE", "LU", "AT",
             "ES", "PT", "IT", "DK", "SE", "FI", "NO", "CH", "PL"]
HANDLING = {"poster": (3, 7), "framed": (3, 7), "mural": (3, 10)}
TRANSIT = (2, 7)

def _qv(lo, hi):
    return {"@type": "QuantitativeValue", "minValue": lo, "maxValue": hi, "unitCode": "DAY"}

def shipping_details(kind: str = "poster") -> dict:
    h = HANDLING.get(kind, HANDLING["poster"])
    return {"@type": "OfferShippingDetails",
            "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "USD"},
            "shippingDestination": [{"@type": "DefinedRegion", "addressCountry": c} for c in COUNTRIES],
            "deliveryTime": {"@type": "ShippingDeliveryTime", "handlingTime": _qv(*h), "transitTime": _qv(*TRANSIT)}}

def _kind(o: dict) -> str:
    s = (o.get("@id", "") + " " + o.get("name", "")).lower()
    return "mural" if "mural" in s else "framed" if "framed" in s else "poster"

def _walk(n) -> bool:
    ch = False
    if isinstance(n, list):
        for x in n: ch |= _walk(x)
    elif isinstance(n, dict):
        t = n.get("@type")
        if t == "Offer" or (isinstance(t, list) and "Offer" in t):
            new = shipping_details(_kind(n))
            if n.get("shippingDetails") != new:
                n["shippingDetails"] = new; ch = True
        for k, v in n.items():
            if k != "shippingDetails": ch |= _walk(v)
    return ch

LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

def apply_file(p: Path) -> bool:
    s = p.read_text()
    changed = False
    def f(m):
        nonlocal changed
        try: d = json.loads(m.group(2))
        except Exception: return m.group(0)
        if not _walk(d): return m.group(0)
        changed = True
        return m.group(1) + "\n" + json.dumps(d, indent=2, ensure_ascii=False) + "\n  " + m.group(3)
    out = LD.sub(f, s)
    if changed: p.write_text(out)
    return changed

def apply_all(root: Path = Path(__file__).resolve().parent.parent) -> list:
    files = sorted(root.glob("*.html")) + sorted((root / "pieces").glob("*.html"))
    return [str(p.relative_to(root)) for p in files if apply_file(p)]

if __name__ == "__main__":
    ch = apply_all(); print(f"shippingDetails updated in {len(ch)} files"); 
