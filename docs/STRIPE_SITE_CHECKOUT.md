# Stripe checkout on moonlitwindows.com

**Plan (28 Sep 2026):** Sell Night Windows posters from the gallery site with **Stripe Payment Links** (no Etsy, no Printful Quick Stores). GitHub Pages stays static — buy buttons open Stripe Checkout.

## Flow
1. Customer on https://moonlitwindows.com (or github.io fallback) clicks **Buy Poster** / **Framed Print**.
2. Button goes to a Stripe Payment Link (per product or per SKU).
3. Stripe collects payment + shipping address.
4. Joshua fulfills via Gelato (already signed in) / Printful after each order email — or later automate with webhook + Gelato API on a server (not static Pages).

## Pricing targets (retail)
- Poster 12×18: £29–£34 (or ~$39)
- Framed 12×18: £69–£79 (or ~$89)

## Instagram
Instagram bio (handle TBD) → https://moonlitwindows.com/buy.html (or site home) once DNS live.

## Status
Awaiting Stripe connector auth, then create Payment Links and write URLs into `products.json`.
