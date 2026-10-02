# Moonlit Windows — SEO operator log

**Site:** https://moonlitwindows.com/ (Prompt Framed / Night Windows · Night Shade Art)  
**Operator:** JI Ventures SEO growth operator (quality over volume; one highest-EV action/day)  
**Hosting:** GitHub Pages · joshuaofisrael/promptframed

---

## Rolling scorecard

| Window | Impressions | Clicks | CTR | Avg position | Indexed pages | Notes |
|---|---:|---:|---:|---:|---:|---|
| 7d (as of 2026-10-02 ~14:35 BST) | processing | processing | processing | processing | n/a yet | GSC: “Processing data, please check again in a day or so.” |
| 28d / ~3mo GSC default | processing | processing | processing | processing | n/a yet | Same processing banner; no queries/pages table yet. |
| 90d | processing | processing | processing | processing | n/a yet | Custom domain + property verified early Oct 2026. |

**GSC property:** `https://moonlitwindows.com/` (URL-prefix, joshuaofisrael@gmail.com)  
**Sitemap:** `https://moonlitwindows.com/sitemap.xml` — Success (read/submitted 2 Oct 2026); **42 discovered pages**, 0 videos. Not resubmitted (already current).  
**Indexing requests:** none this run (inspection UI unavailable while performance data processing).  
**Top queries / pages (GSC):** not available yet (processing).  
**GA4 property:** Moonlit Windows · measurement ID `G-663R8VD62L` (confirmed in live HTML; UI label may truncate).  
**GA4 status:** “No data received from your website yet.” Users / sessions / views / sources for 7d and 28d: unavailable (not zero — not reporting).  
**Page views (GA4 7/28d):** no data received yet  

Next run: re-check GSC performance once processing clears; confirm GA4 Realtime/DebugView after a few page hits; request indexing for a few piece URLs when URL Inspection works.

---

## 2026-10-02 (BST) — first scheduled SEO operator fire

### Hygiene
- Ran `python3 scripts/inject_head_tags.py` → updated 0 pages (GA4 `G-663R8VD62L` already on every public HTML page; homepage already has Search Console verification meta).
- Sitemap: added missing public page `how-to-turn-chatgpt-art-into-a-framed-poster.html`. All 35 `pieces/*.html` URLs already listed. No print-master image URLs in sitemap.
- Stripe Payment Links: not created today; existing piece CTAs present. Did not audit every link’s promo-code / thanks redirect settings in Stripe admin (no Stripe write today).

### Data review
- Follow-up computerUse pass (same day, signed in as joshuaofisrael@gmail.com) opened GSC + GA4.
- **GSC:** property `https://moonlitwindows.com/` — performance still “Processing data…” (no clicks/impressions/CTR/position/queries/pages yet). Sitemap Success, 42 discovered URLs. No indexing requests (inspection unavailable while processing).
- **GA4:** Moonlit Windows / `G-663R8VD62L` — “No data received from your website yet.” Live site tag verified correct; treat as new-property lag or hit lag, not invented zeros.

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

### Follow-up same day (~14:35 BST)
- Updated scorecard from live GSC/GA4 browser session.
- Stripe live charges: still none.
- Flag for later (not changed today): public page `how-to-turn-chatgpt-art-into-a-framed-poster.html` still names ChatGPT in the URL/title path — conflicts with public-copy rule; rewrite/redirect on a future high-EV day.

