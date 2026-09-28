# Prompt Framed: low-cost print-on-demand setup

**Prepared:** 28 September 2026 (UK time)  
**Business:** Prompt Framed, Joshua Israel Ventures LLC

## 1. Recommendation

**Use Printful Quick Stores first**, provided Joshua's LLC has a **US tax residence and the buyers will ship to US addresses**. It is the lowest-friction fit for a GitHub Pages site: $0 monthly/store fee, hosted checkout, no inventory, and Printful prints, packs, ships, and handles Quick Store sales tax as seller of record. A static page only needs ordinary links to the hosted store/product pages.

Important limitation: Quick Stores is currently US-seller/US-shipping only, uses a `*.printful.me` URL, cannot use a custom domain, and does not offer free shipping. If Prompt Framed must sell to UK/EU/international buyers, use **Gelato + Etsy** instead (Gelato's free plan and global local production, with Etsy providing the hosted checkout); budget Etsy's $0.20 listing fee, 6.5% transaction fee, payment-processing fee, and any location-specific fees. Gelato itself has no static hosted checkout. Prodigi is a good API/fulfillment option but requires a secure server plus a payment checkout, so it is not the cheap first launch for GitHub Pages.

## 2. Exact setup for Joshua

1. Create/sign in to Printful with **`joshofisrael@yahoo.com`** as the owner email. Use the legal business name **Joshua Israel Ventures LLC** and the correct US tax/bank details; do not use a developer's personal account.
2. Confirm Quick Store eligibility (US tax residence and US delivery addresses). In Printful Dashboard, open **Stores → Add store → Quick Stores**, name it Prompt Framed, choose an available slug, and upload the Prompt Framed logo. The resulting URL will be similar to `https://promptframed.printful.me/`.
3. Open **My products → Add product/Product Push Generator**. Add the poster and framed-poster products below, upload each artwork, keep the artwork's 2:3 portrait crop, select frame colours, write the listing copy, set retail prices, choose mockups, and **Publish**.
4. In **Billing → Quick Stores**, complete Stripe onboarding as the owner (identity, bank, business and tax information). Submit the requested W-9 promptly; Printful says payouts are monthly once the balance reaches $25 and warns that missing tax information can trigger backup withholding.
5. Check product previews, shipping at checkout, mobile layout, confirmation email, and one sample order before advertising. Quick Stores applies Printful's standard shipping rate at checkout; free shipping is not available.
6. Copy the store URL and each published product URL into the static gallery's buy page. Instagram can link to that buy page (or directly to a product page) from the bio/post link.

## 3. Static-page buy links

There is no need for JavaScript, a Vercel plan, or an API key. GitHub Pages cannot safely hold a private fulfillment/payment secret, so use normal links to the hosted checkout:

```html
<a class="buy-button"
   href="https://promptframed.printful.me/PRODUCT-PATH"
   target="_blank" rel="noopener">
  Buy this framed print
</a>
```

Replace `PRODUCT-PATH` with the URL Printful gives after Publish. A single **Shop all prints** button can link to the store home. Instagram's call-to-action should point to the GitHub Pages `/buy.html` page or the relevant `printful.me` product URL. The actual cart, address collection, payment, order email, and fulfillment stay on Printful.

## 4. Products/variant SKUs for a 1024×1536 (2:3) portrait

The current public Printful catalog uses product IDs **1** (unframed) and **2** (framed). The IDs in the table are the individual catalog variant IDs, not the final Quick Store product URLs; verify they remain available for the destination region before publishing.

| Offering | Printful product / variant ID | Size | Public catalog price* |
|---|---|---:|---:|
| Poster, enhanced matte | `3876` | 12×18 in | $11.62 |
| Poster, enhanced matte | `16365` | 20×30 in | $13.15 |
| Poster, enhanced matte | `2` | 24×36 in | $18.25 |
| Framed, enhanced matte, black | `4398` | 12×18 in | $32.77 |
| Framed, enhanced matte, black | `19520` | 20×30 in | $56.18 |
| Framed, enhanced matte, black | `4` | 24×36 in | $75.90 |

Useful colour variants: red oak `15026` (12×18), `19521` (20×30), `15032` (24×36); white `10752`, `19522`, and `10750` respectively. Availability differs by country. Printful's framed catalog currently lists 12×18, 20×30 and 24×36; **16×24 is not a current framed variant**, so do not promise it without checking the dashboard.

The supplied 1024×1536 file is the correct aspect ratio but is low resolution for large physical prints (about 85 DPI at 12×18 and 43 DPI at 24×36). Use the highest-resolution source or regenerate/upscale before publishing; Printful's preferred paper-poster target is 300 DPI (3,600×5,400 px for 12×18; 7,200×10,800 px for 24×36). Order a sample before selling large framed sizes.

## 5. Information needed from Joshua later

For the static integration, request only:

- The live Quick Store home URL and the published product URLs (poster and framed versions).
- The GitHub repository/page URL and the desired button labels, if someone is updating the gallery.
- Confirmation of the shipping countries and retail prices.

**No API key is needed** for Quick Stores. Never put a Printful private token, Stripe secret, or bank/tax information in GitHub Pages or send it in chat. If Joshua later wants a custom checkout/API integration, he would create a scoped Printful Developers private token, Printful store ID, and a payment provider account; those must be held by a server-side function/secret manager, not static HTML. Gelato/Prodigi API keys are similarly unnecessary for the recommended launch and must never be exposed client-side.

## 6. Pricing note

The starred figures above are the current public Printful API catalog prices checked on 28 September 2026; they are **production cost only**, before shipping, tax, and payment processing, and can vary with destination/catalog changes. Quick Store shipping is added at checkout.

Reasonable test retail (Joshua's decision, not Printful's quoted recommendation) is approximately:

- 12×18 unframed: **$34–$44 + shipping**
- 12×18 framed: **$79–$99 + shipping**
- 20×30 framed: **$129–$159 + shipping**
- 24×36 framed: **$179–$229 + shipping**

These leave room for the listed production cost and Stripe/payment fees while positioning the work as art rather than commodity posters. Recheck the live dashboard cost, shipping, taxes, and sample quality before fixing retail prices.

## Sources checked

- [Printful Quick Stores](https://www.printful.com/quick-stores) and [Quick Store setup help](https://help.printful.com/hc/en-us/articles/50265713128593-How-do-I-set-up-a-shop-with-Printful-Quick-Stores)
- [Quick Store availability](https://help.printful.com/hc/en-us/articles/15045280299548-Is-Quick-Stores-available-in-my-area), [payments](https://help.printful.com/hc/en-us/articles/15045592337180-How-do-I-get-paid-with-Quick-Stores), and [shipping](https://help.printful.com/hc/en-us/articles/50265737106193-How-does-shipping-for-Quick-Stores-work)
- [Printful public poster catalog API](https://api.printful.com/products/1) and [framed-poster catalog API](https://api.printful.com/products/2)
- [Printful wall-art file guidance](https://www.printful.com/create-digital-print-file)
- [Gelato posters and frames](https://www.gelato.com/products/posters-frames), [Gelato pricing](https://www.gelato.com/pricing), and [Etsy fees](https://www.etsy.com/legal/fees/)
- [Prodigi Print API](https://www.prodigi.com/print-api/)
