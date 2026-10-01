# Affiliates

Night Windows affiliate codes run on **Stripe promotion codes** (account: Joshua Israel Ventures LLC,
`acct_1U7tYaK3OWN3aipg`, live mode). Customers type the code on the Stripe checkout page; nothing
about any affiliate code is shown on the site's own pages.

## Sakshi (first affiliate, set up 1 Oct 2026)

### Offer terms (as sent in the affiliate offer email)

| Term | Detail |
| --- | --- |
| Follower discount | **10% off** with her own code **`SAKSHI10`** |
| Commission | **20% of the net amount paid** on every order that uses the code (after the 10% discount, less any refund) |
| Payout | Monthly, for the previous calendar month's orders |
| Gift | **One free framed print** (12×18) of the piece she picks |
| Prices the code applies to | $29 poster / $69 framed, 12×18, shipping included |

Example: one framed print: gross $69.00, discount $6.90, net paid $62.10, commission **$12.42**.
One poster: gross $29.00, discount $2.90, net paid $26.10, commission **$5.22**.

Her contact email is stored in the Stripe coupon/promo metadata (`affiliate_email`) and in the
offer email thread, and is deliberately not repeated here because this repo is public.

### Stripe objects

| Object | ID | Notes |
| --- | --- | --- |
| Coupon | `dOuqUokk` | "Sakshi 10% off", `percent_off: 10`, `duration: once`, no expiry or redemption cap |
| Promotion code | `promo_1ULhq0K3OWN3aipgp2uUwWtr` | code `SAKSHI10`, active, any customer, no minimum |

Metadata on both: `affiliate=sakshi`, `affiliate_email=<her email>`, `commission_rate=0.20`.

All 60 Night Windows Payment Links listed in `products.json` (30 pieces × poster/framed) now have
**`allow_promotion_codes: true`**, so the "Add promotion code" field appears at checkout. No other
link settings were changed (line items, shipping, phone collection, metadata and the
`after_completion` redirect stayed as they were). **Any new Payment Link must also be created with
`allow_promotion_codes: true`**, or affiliate codes won't work on that piece.

To pause the code: set the promotion code `active: false` (the coupon can stay). To end the deal:
deactivate the promo code, then pay out the final month.

## Pulling the commission report

Each Checkout Session created by a Payment Link carries the link's metadata (`slug`, `variant`), and
a redeemed code shows up in `total_details.breakdown.discounts[].discount.promotion_code` (and in
`discounts[].promotion_code`). Amounts are in cents: `amount_subtotal` = gross,
`total_details.amount_discount` = discount, `amount_total` = net paid.

### Option A: script with a Stripe key

```bash
STRIPE_API_KEY=rk_live_... python3 scripts/affiliate_report.py --month 2026-10
python3 scripts/affiliate_report.py --month 2026-10 --csv sakshi-2026-10.csv
```

Use a **restricted key** with read-only access to Checkout Sessions, Promotion Codes, Payment
Intents and Charges. Never commit the key. The script prints one row per order (date, piece,
variant, gross, discount, net paid, refunded, 20% commission) and a total owed per month (UTC).

### Option B: no key on hand (Stripe connector / Dashboard)

1. List completed Checkout Sessions for the month with the discount breakdown expanded. Through
   the connector that's `stripe_api_read` → `GetCheckoutSessions` with
   `{"status": "complete", "limit": 100, "created": {"gte": <month start>, "lt": <next month start>},
   "expand": ["data.total_details.breakdown"]}`, paging with `starting_after` while `has_more`.
2. Keep sessions whose `total_details.breakdown.discounts[].discount.promotion_code` (or
   `discounts[].promotion_code`) is `promo_1ULhq0K3OWN3aipgp2uUwWtr`.
3. Save the list as JSON and run `python3 scripts/affiliate_report.py --from-json sessions.json`,
   or compute by hand: commission = 20% × `amount_total` for each session.
4. Check refunds in the Dashboard (Payments → filter refunded) and reduce commission for any
   refunded order. (Option A does this automatically through `payment_intent.latest_charge`.)

Dashboard shortcut: Products → Coupons → "Sakshi 10% off" → the `SAKSHI10` code shows its
redemption count, a quick check that the report caught every order.

### Monthly payout routine

1. In the first days of the month, run the report for the previous month.
2. Pay the "commission owed" total (PayPal/Wise/bank, whichever she prefers) and keep the CSV as
   the payout record.
3. Send her the per-order lines (date, piece, net paid, commission) with the payment.

## Free framed print (manual fulfilment)

This print is **not** run through Stripe and needs no Payment Link or 100% coupon.

1. Once Sakshi picks a piece, collect her shipping address directly.
2. Order a **12×18 framed poster** at Gelato/Printful by hand, uploading the **clean print master**
   from `gallery/print-masters/NN-slug.png`, never the watermarked social image.
3. Log the order (piece, date, cost, tracking) here under a "Fulfilled" note. The product cost is a
   marketing expense, not a commission deduction.
