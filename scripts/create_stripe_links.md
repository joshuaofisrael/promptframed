# Create Stripe checkout for a new Night Windows piece

Run for each new `slug`. Uses the **Stripe MCP connector** (`user-Stripe`: `stripe_api_read` /
`stripe_api_write`), `stripe_context=acct_1U7tYaK3OWN3aipg`, `livemode=true`. The same parameters
work with the Stripe CLI or Dashboard. No server needed.

Replace `<slug>`, `<Title>`, `<NN>` below. Do both the poster and framed variants.

## 0. Check first (avoid duplicates)

`GetProductsSearch` with `query: "metadata['slug']:'<slug>'"`. Reuse any product whose
`metadata.variant` already matches (use its `default_price`), and check `GetPaymentLinks` for an existing link.

## 1. Product + default Price (one call per variant): `PostProducts`

```json
{
  "name": "<Title> – Night Windows Poster 12×18",
  "description": "Night Windows by Prompt Framed. 12×18 in poster on enhanced matte paper. Shipping included. Sold by Joshua Israel Ventures LLC.",
  "images": ["https://joshuaofisrael.github.io/promptframed/gallery/social/<NN>-<slug>.jpg"],
  "url": "https://joshuaofisrael.github.io/promptframed/pieces/<slug>.html",
  "shippable": true,
  "metadata": {"slug": "<slug>", "variant": "poster", "series": "night-windows", "size": "12x18"},
  "default_price_data": {"currency": "usd", "unit_amount": 2900, "metadata": {"slug": "<slug>", "variant": "poster"}}
}
```

Framed: name `"<Title> – Night Windows Framed Poster 12×18"`, description
`"... 12×18 in enhanced matte poster in a black frame. ..."`, `variant: "framed"`, `unit_amount: 6900`.

Image rule: only the **watermarked** `gallery/social/*.jpg`. Never `gallery/print-masters/` or `gallery/*.png`.

The response's `default_price` is the Price ID for step 2.

## 2. Payment Link (one per Price): `PostPaymentLinks`

```json
{
  "line_items": [{"price": "<price_id>", "quantity": 1,
                  "adjustable_quantity": {"enabled": true, "minimum": 1, "maximum": 5}}],
  "shipping_address_collection": {"allowed_countries":
    ["US","GB","CA","AU","NZ","IE","FR","DE","NL","BE","LU","AT","ES","PT","IT","DK","SE","FI","NO","CH","PL"]},
  "phone_number_collection": {"enabled": true},
  "after_completion": {"type": "redirect", "redirect":
    {"url": "https://joshuaofisrael.github.io/promptframed/thanks.html?piece=<slug>&variant=poster"}},
  "metadata": {"slug": "<slug>", "variant": "poster", "series": "night-windows"},
  "payment_intent_data": {"metadata": {"slug": "<slug>", "variant": "poster"}}
}
```

Keep the response's `id` (`plink_...`) and `url` (`https://buy.stripe.com/...`).

## 3. Save + publish

In `products.json` for the slug:

```json
"stripe": {
  "posterUrl": "https://buy.stripe.com/...", "framedUrl": "https://buy.stripe.com/...",
  "status": "live", "posterPrice": 2900, "framedPrice": 6900, "currency": "usd", "size": "12x18",
  "posterProductId": "prod_...", "posterPriceId": "price_...", "posterPaymentLinkId": "plink_...",
  "framedProductId": "prod_...", "framedPriceId": "price_...", "framedPaymentLinkId": "plink_..."
}
```

Then:

```bash
python3 scripts/apply_stripe_links.py          # writes buttons into buy.html + pieces/*.html
python3 scripts/apply_stripe_links.py --check  # all pieces live?
git add products.json buy.html pieces/ && git commit -m "Stripe links for <slug>" && git push origin main
```

If a write returns a human-confirmation approval URL, stop and have Joshua approve it before retrying
with the same parameters.
