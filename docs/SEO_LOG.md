# Moonlit Windows — SEO operator log

**Site:** https://moonlitwindows.com/ (Prompt Framed / Night Windows · Night Shade Art)  
**Operator:** JI Ventures SEO growth operator (quality over volume; one highest-EV action/day)  
**Hosting:** GitHub Pages · joshuaofisrael/promptframed

---

## Rolling scorecard

| Window | Impressions | Clicks | CTR | Avg position | Indexed pages | Notes |
|---|---:|---:|---:|---:|---:|---|
| 7d (as of 2026-10-02 BST) | no data yet | no data yet | no data yet | no data yet | no data yet | GSC/GA4 browser review unavailable this run (executor has no computerUse/Task tool). Do not invent metrics. |
| 28d | no data yet | no data yet | no data yet | no data yet | no data yet | Property verified via HTML tag (meta on homepage); GA4 G-663R8VD62L on all public pages. |
| 90d | no data yet | no data yet | no data yet | no data yet | no data yet | Site custom domain live early Oct 2026 — expect lag before query data. |

**Top queries:** no data yet  
**Top pages (GA4):** no data yet / session not readable this run  
**Page views (GA4 7/28d):** no data yet / session not readable this run  

Fill real numbers on the next run that can open Search Console + GA4 while signed in as joshuaofisrael@gmail.com.

---

## 2026-10-02 (BST) — first scheduled SEO operator fire

### Hygiene
- Ran `python3 scripts/inject_head_tags.py` → updated 0 pages (GA4 `G-663R8VD62L` already on every public HTML page; homepage already has Search Console verification meta).
- Sitemap: added missing public page `how-to-turn-chatgpt-art-into-a-framed-poster.html`. All 35 `pieces/*.html` URLs already listed. No print-master image URLs in sitemap.
- Stripe Payment Links: not created today; existing piece CTAs present. Did not audit every link’s promo-code / thanks redirect settings in Stripe admin (no Stripe write today).

### Data review
- **GSC / GA4:** Could not open box browser via computerUse from this executor (Task tool not available to the subagent). Metrics left as “no data yet” — not guessed.

### Opportunity chosen (and why)
**Add Product + Offer + ImageObject + BreadcrumbList JSON-LD to all 35 piece pages.**

Why highest EV for a brand-new product gallery:
1. Titles, meta descriptions, canonicals, OG tags, and image alt text were already unique per piece — diminishing returns there.
2. Only homepage + one guide had structured data; piece/buy surfaces had none — competitors in “moonlit landscape poster” / place-specific night poster SERPs are Shopify/print shops with Product rich-result markup.
3. Technical/schema on existing product URLs beats speculative new articles for a young site with no impression winners yet.
4. Images in schema point only at already-public `assets/*.jpg` web derivatives (never `gallery/print-masters` or clean `gallery/*.png`).

### Shipped
- Injected `@graph` of Product (two Offers: poster $29 / framed $69 USD, InStock), ImageObject, BreadcrumbList (Home → Night Windows → piece) into every `pieces/*.html`.
- Sitemap hygiene entry for the how-to guide.
- This log file.

### Intentionally not done
- No new collection/article pages (speculative content last).
- No commit of print-masters, reels staging/logs, Instagram kit tarball, music, or `.night-windows-*` JSON.
- No spend; GitHub Pages only.
