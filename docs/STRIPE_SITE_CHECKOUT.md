# Stripe checkout on GitHub Pages

**Live since 29 Sep 2026.** Every Night Windows piece sells through **Stripe Payment Links**
(account: Joshua Israel Ventures LLC, `acct_1U7tYaK3OWN3aipg`, live mode). GitHub Pages stays
static: no server, no API keys in the repo. Each Buy button is a plain `<a href>` to
`https://buy.stripe.com/...`.

## Offer (USD, shipping included for now)

| Variant | Spec | Price |
| --- | --- | --- |
| `poster` | 12×18 in, enhanced matte | $29.00 (`2900`) |
| `framed` | 12×18 in poster, black frame | $69.00 (`6900`) |

Visible copy on the site: **$29 poster · $69 framed (12×18)**.

## Flow

1. Customer clicks **Buy this print · Poster $29** or **Buy framed · $69** on `buy.html` or a piece page.
2. The link opens that piece's Stripe Payment Link (quantity 1–5, shipping address + phone collected).
3. After payment Stripe redirects to `thanks.html?piece=<slug>&variant=<poster|framed>` and emails a receipt.
4. Joshua fulfils manually (Gelato / Printful) from the Stripe order email or dashboard, uploading the
   **clean print master** from `gallery/print-masters/` (never the watermarked social image).
   Metadata `slug` + `variant` is on the Payment Link, the Checkout Session, and the PaymentIntent,
   so every order says which piece and size to print.

## What exists in Stripe (per piece × 2 variants)

- **Product** `"<Title> – Night Windows Poster 12×18"` / `"<Title> – Night Windows Framed Poster 12×18"`
  - metadata: `slug`, `variant` (`poster|framed`), `series=night-windows`, `size=12x18`
  - image: the **watermarked** preview `gallery/social/NN-slug.jpg` on github.io (never a print master)
  - `url`: the piece page; `shippable: true`
- **Price**: one-time USD default price (`2900` or `6900`), metadata `slug`, `variant`
- **Payment Link**:
  - `line_items[0]`: that price, quantity 1, `adjustable_quantity` enabled, min 1, max 5
  - `shipping_address_collection.allowed_countries`: US, GB, CA, AU, NZ, IE, FR, DE, NL, BE, LU, AT,
    ES, PT, IT, DK, SE, FI, NO, CH, PL
  - `phone_number_collection.enabled: true`
  - `after_completion`: redirect to `https://joshuaofisrael.github.io/promptframed/thanks.html?piece=<slug>&variant=<variant>`
  - metadata `slug`, `variant`, `series`; `payment_intent_data.metadata` `slug`, `variant`

All IDs are recorded in `products.json` under `stripe` (`posterProductId`, `posterPriceId`,
`posterPaymentLinkId`, same for `framed`), alongside `posterUrl`, `framedUrl`, `status: "live"`.

## Adding new pieces (daily drop checklist)

A new piece is **not sellable** until it has its own two Products, Prices and Payment Links.

1. Publish the piece as usual (print master in `gallery/print-masters/`, display JPEG in `assets/`,
   watermarked `gallery/social/NN-slug.jpg` via `scripts/watermark_for_social.py`, piece page,
   `products.json` row with `stripe.posterUrl/framedUrl: null`, `status: "placeholder"`).
2. Push once so the watermarked social JPEG is public (Stripe fetches the product image by URL).
3. Create the Stripe objects exactly as in `scripts/create_stripe_links.md` (Stripe MCP connector or
   Dashboard). **Search first** (`metadata['slug']:'<slug>'`) so nothing is duplicated.
4. Paste the two `https://buy.stripe.com/...` URLs + IDs into `products.json`, set `status: "live"`.
5. Run `python3 scripts/apply_stripe_links.py`. It rewrites the buy block on every piece page and the
   whole `buy.html` grid from `products.json` (idempotent; pieces without links show "opens for orders soon").
   `python3 scripts/apply_stripe_links.py --check` exits 1 if any piece is missing live links.
6. Commit + push to `main`, then check the live page: `curl -s <piece url> | grep buy.stripe.com`.

## Changing prices later

Stripe prices are immutable. Create a new Price on the same Product, then either update each Payment
Link's line item or create new links, update `products.json`, rerun `apply_stripe_links.py`, and update
the `PRICE_LINE` constant in that script plus this doc. Deactivate (don't delete) old links.

## Instagram

Instagram bio (@moonnightshadeart) → https://joshuaofisrael.github.io/promptframed/buy.html.
Deep links such as `buy.html#moonlit-alpine-meadow` land on (and highlight) that piece's buttons.
