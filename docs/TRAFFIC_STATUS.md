# Prompt Framed — traffic status

**Checked:** 28 Sep 2026 BST

## Spreadsheet
`/workspace/JI_Ventures_Traffic.xlsx` exists. Sheet **DailyViews** columns:

Date | Site | Brand | Bot | Pageviews total | Pageviews non-bot | Visits total | Visits non-bot | GSC Clicks 28d | GSC Impressions 28d | Source | Monetize? | Notes

Prompt Framed / Night Windows is **not** listed on the Sites sheet and has **no** DailyViews rows.

## Analytics availability
- Live host: `joshuaofisrael.github.io/promptframed/` (GitHub Pages)
- Cloudflare Web Analytics: **unavailable** — no CF beacon on this site; hostname absent from `/workspace/seo/cf-web-analytics-tokens-2026-09-27.json`
- No custom domain / CF zone edge totals
- No GA4 / other RUM found for this gallery

## Action
Do **not** append invented pageview numbers. After a custom domain + CF Web Analytics (or equivalent) is wired, start DailyViews rows with total edge/all next to non-bot when both exist; leave non-bot blank and note why if only edge is available.
