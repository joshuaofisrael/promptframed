# Prompt Framed — traffic status

**Checked:** 28 Sep 2026 BST

## Spreadsheet
`/workspace/JI_Ventures_Traffic.xlsx` exists. Sheet **DailyViews** columns:

Date | Site | Brand | Bot | Pageviews total | Pageviews non-bot | Visits total | Visits non-bot | GSC Clicks 28d | GSC Impressions 28d | Source | Monetize? | Notes

Prompt Framed / Night Windows is **not** listed on the Sites sheet and has **no** DailyViews rows.

## Analytics availability
- Current host: https://moonlitwindows.com/ (GitHub Pages). Custom domain `moonlitwindows.com` is live (HTTPS) since 1 Oct 2026; github.io redirects to it.
- Cloudflare Web Analytics: **unavailable** — no CF beacon on this site; hostname absent from `/workspace/seo/cf-web-analytics-tokens-2026-09-27.json`
- Namecheap DNS is not in this repo, so there are no CF zone edge totals yet
- No GA4 / other RUM found for this gallery

## Action
Do **not** append invented pageview numbers. After a custom domain + CF Web Analytics (or equivalent) is wired, start DailyViews rows with total edge/all next to non-bot when both exist; leave non-bot blank and note why if only edge is available.
