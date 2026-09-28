# Stripe checkout on GitHub Pages

**Plan (28 Sep 2026):** Sell Night Windows posters from the gallery site with **Stripe Payment Links** (no Etsy, no Printful Quick Stores). GitHub Pages stays static — buy buttons open Stripe Checkout.

## Flow
1. Customer on https://joshuaofisrael.github.io/promptframed/ clicks **Buy Poster** / **Framed Print**.
2. Button goes to a Stripe Payment Link (per product or per SKU).
3. Stripe collects payment + shipping address.
4. Joshua fulfills via Gelato (already signed in) / Printful after each order email — or later automate with webhook + Gelato API on a server (not static Pages).

## Pricing targets (retail)
- Poster 12×18: £29–£34 (or ~$39)
- Framed 12×18: £69–£79 (or ~$89)

## Instagram
Instagram bio (@moonnightshadeart) → https://joshuaofisrael.github.io/promptframed/buy.html.

## Status
Awaiting Stripe connector auth, then create Payment Links and write URLs into `products.json`.
