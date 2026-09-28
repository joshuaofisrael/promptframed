# Prompt Framed — SEO scorecard (starter)

**Site:** Prompt Framed / series Night Windows  
**Operator:** JI Ventures SEO growth operator (quality over volume; highest EV action/day; no article quota; no spam)  
**Baseline date:** 28 Sep 2026 (pre-launch / empty metrics)  
**Primary URL (until custom domain):** https://joshuaofisrael.github.io/promptframed/

Follow `/home/box/agent-data/workflows/seo-growth-operator/` — additive to BUSINESS_PLAN. Hard no: spammy links, fake expertise, mass near-duplicates, manufactured freshness.

---

## Baseline metrics (empty until Search Console + analytics exist)

| Metric | 7d | 28d | 90d | Notes |
|---|---:|---:|---:|---|
| Organic impressions | — | — | — | GSC when property verified |
| Organic clicks | — | — | — | |
| Average CTR | — | — | — | |
| Average position | — | — | — | |
| Indexed pages | 0 | — | — | Confirm after Pages live |
| Queries Top 100 / 20 / 10 / 3 | 0 / 0 / 0 / 0 | — | — | |
| Growing pages | — | — | — | |
| Declining pages | — | — | — | |
| Conversions (print orders) | 0 | — | — | Printful / store attribution |
| Non-bot pageviews (CF Web Analytics) | — | — | — | After custom domain |

Fill the first real row the day after GSC + Cloudflare Web Analytics are connected.
**Traffic note (28 Sep 2026 BST):** `JI_Ventures_Traffic.xlsx` DailyViews columns are Date / Site / Brand / Bot / Pageviews total / Pageviews non-bot / Visits total / Visits non-bot / GSC Clicks 28d / GSC Impressions 28d / Source / Monetize? / Notes. Prompt Framed is **not** on the Sites sheet and has **no** Cloudflare Web Analytics beacon (github.io host; no custom domain / CF token yet). Do not invent pageview rows until a beacon or other RUM is live.
 Append daily CF views to `JI_Ventures_Traffic.xlsx` per owner rules. Ads only after trailing 7-day non-bot pageviews ≥ 10,000 OR yesterday ≥ 2,000.

---

## Topic cluster (seed — do not mass-publish)

- AI art prints / ChatGPT wall art / framed AI posters (category intent)
- Night Windows series + individual piece pages (product intent)
- One practical guide (informational intent) — see week-1 plan
- Avoid thin “what is AI art” clones; prefer unique piece context + buying utility

---

## First-week plan (technical + piece pages + one guide)

### A. Technical (do first — highest EV at launch)

1. Confirm GitHub Pages serves `index.html`, clean 200s, no soft-404.
2. Add `robots.txt` + `sitemap.xml` (home, gallery index, each piece, buy/about if present).
3. Unique `<title>` + meta description per page; canonical to final host (swap when custom domain is live).
4. Open Graph / Twitter cards using gallery images; sensible `alt` text (see `gallery/catalog.json`).
5. Image performance: compressed derivatives for web; keep print masters separate; lazy-load below fold.
6. Internal links: home ↔ gallery ↔ each piece ↔ buy CTA.
7. After custom domain: Search Console property + sitemap submit; Cloudflare Web Analytics.

### B. Piece pages (product/SEO hybrid)

For each Night Windows work (start with the two ready assets):

- Dedicated URL (e.g. `/pieces/moonlit-alpine-meadow/`)
- Title pattern: `{Piece title} — Night Windows print | Prompt Framed`
- Short mood description + medium details + buy CTAs (poster / framed) linking to Printful
- Keywords from catalog only where natural; no keyword stuffing
- Cross-link to series hub and the other piece

### C. One guide (single new informational page — only if unique value)

**Candidate:** “How to choose a size for a framed AI art print (12×18 vs 20×30 vs 24×36)”  
Why it can exist: decision utility tied to our real SKUs/prices/mockups — not a generic AI-art explainer.  
Include: room-distance heuristic, frame colour notes, DPI/print-quality honesty about source resolution, links to live products.  
Skip if you cannot add original practical value beyond what already ranks.

### D. Explicitly not in week 1

- No blog quota / no daily article
- No doorway pages or near-duplicate “AI poster” spam
- No link outreach schemes
- No ads until traffic thresholds in BUSINESS_PLAN

---

## Log

| Date (BST) | Action | Why (EV) | Result |
|---|---|---|---|
| 28 Sep 2026 | Scorecard created; baseline empty | Pre-launch measurement stub | — |
| 28 Sep 2026 | Shipped `guide-print-sizes.html` (12×18 / 20×30 / 24×36 + room-distance + frame notes + print-res honesty); linked from home/buy/about/sitemap; added WebSite + CollectionPage JSON-LD on `index.html` | Week-1 highest-EV: one unique informational page tied to real SKUs + technical schema for a brand-new gallery; compounds product pages without article spam | Ready locally; publish with next drop commit |

Update this log when an SEO action ships. Prefer improving existing piece pages over speculative new URLs.
