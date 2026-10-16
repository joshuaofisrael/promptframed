# Prompt Framed — SEO scorecard (starter)

**Site:** Prompt Framed / series Night Windows  
**Operator:** JI Ventures SEO growth operator (quality over volume; highest EV action/day; no article quota; no spam)  
**Baseline date:** 28 Sep 2026 (pre-launch / empty metrics)  
**Primary URL:** https://moonlitwindows.com/
**Custom domain:** moonlitwindows.com is live (GitHub Pages custom domain, HTTPS). Sitemap: https://moonlitwindows.com/sitemap.xml


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


### 2026-10-14 — Drop 61–65 + lakes/mountain/coastal/murals wiring
Published five new Night Windows pieces with live Stripe (15 payment links). Added Tekapo + Kirkjufell to lakes & mountain hubs, Na Pali to coastal, all five to murals. Series count 65. See SEO_LOG.md.

### 2026-10-15 — Drop 66–70 + collection placement + Asian link restored on the series hub
Published five new Night Windows pieces (Eilean Donan Castle, Dubrovnik Old Town, Pamukkale Terraces, Rothenburg Old Town, Bora Bora Lagoon) with live Stripe (15 payment links; 70/70 pieces live with poster, framed and mural). Collection placement: all five added to the **peel and stick wall murals** page (Eilean Donan, Dubrovnik, Rothenburg in castles and landmarks; Pamukkale in lakes, salt flats and waterfalls; Bora Bora in coasts); Dubrovnik (Mediterranean), Bora Bora (ocean shores) and Eilean Donan (fjords and bays: Loch Duich is a sea loch) added to **coastal wall art**, with meta, group intros and FAQ naming them; Pamukkale added to **lake and waterfall wall art** (lakes group + FAQ). Mountain collection left alone on purpose: Eilean Donan's mountains are background, not the subject. **Restored the Asian wall art collection link** in the hub's "Find your window" themes (the 61–65 publish run had dropped it; `publish_pieces_66_70.py` now carries it on every re-run). Alt text checked against the real images (heather, bougainvillea, frangipani, pink flowers, town lights added; Rothenburg wording softened to what is visible, no named towers). All five `build_collection_*.py --check`, `apply_stripe_links.py --check`, `apply_mural_links.py --check` and `publish_pieces_66_70.py --check` clean. Series count 70. IndexNow pinged after deploy.

### 2026-10-16 — Drop 71–75 + collection placement + European/Asian links on every collection hub
Published five new Night Windows pieces (Colmar Petite Venise, Glenfinnan Viaduct, Monument Valley, Sigiriya Rock, Cradle Mountain Dove Lake) with live Stripe (15 payment links; 75/75 pieces live with poster, framed and mural). Collection placement: all five on the **peel and stick wall murals** page (all 2:3; Colmar, Glenfinnan, Sigiriya in castles and landmarks; Monument Valley in mountain and canyon; Cradle Mountain in lakes and waterfalls); Colmar (old towns) and Glenfinnan (countryside) on **European wall art**; Sigiriya on **Asian wall art** (group renamed South and Southeast Asian); Cradle Mountain on **lake and waterfall wall art**; Monument Valley and Cradle Mountain on **mountain wall art**; metas, group intros, FAQs and room guides name them. **Internal-link fix (the open item from 15 Oct):** the lake, coastal, mountain and murals hubs now link to the European and Asian collections in body copy and a unified footer, so all six collection hubs link to each other (before: mountain linked to none of lake/coastal/European/Asian; lake, coastal and murals linked to neither European nor Asian). Alt text checked against the real images before publishing (Colmar willow on the right bank, small arched bridge, moon reflected; Glenfinnan heather and mossy rocks, no bracken; Monument Valley winding red dirt road, no wildflowers; Sigiriya terraced water gardens with cascade and lily-pad pools, no visible summit ruins or mist; Cradle Mountain boatshed on the right shore, flowering shrubs, no pencil pines). All six `build_collection_*.py --check`, `apply_stripe_links.py --check` (75/75), `apply_mural_links.py --check` (75/75) and `publish_pieces_71_75.py --check` clean; 0 broken relative links. Series count 75. IndexNow pinged after deploy.

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
3. Unique `<title>` + meta description per page; canonical host is https://moonlitwindows.com/.
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
| 29 Sep 2026 | Strengthened `night-windows.html` series hub: unique intro naming new destinations, full cross-links for all 20 pieces, richer title/meta, sitemap already includes hub; new piece pages ship with unique title/meta/OG/alt | Highest EV at thin-traffic launch: compound the series hub + internal links rather than a new article; new product URLs get discovery paths from the hub | Shipped with pieces 16–20 drop |
| 30 Sep 2026 BST | Strengthened `night-windows.html` hub for pieces 21–25: unique intro, updated meta/OG/Twitter copy to twenty-five windows, full cross-link list including Cappadocia / Santorini / Tuscany / Machu Picchu / Ha Long Bay, and a New this drop paragraph with deep links | Series hub is the strongest internal-link target for new piece pages; keeps crawl paths and snippet unique as catalog grows | Done in publish script; live after push |

| 1 Oct 2026 BST | Strengthened `night-windows.html` hub for pieces 26–30: unique intro, updated meta/OG/Twitter to thirty windows, full cross-link list including Banff Lake Louise / Petra Treasury / Kyoto bamboo / Yosemite Half Dome / Norwegian stave church fjord, and a New this drop paragraph with deep links | Series hub remains the strongest internal-link target for new piece pages; unique snippet + crawl paths as catalog hits 30 | Done in publish script; live after push |

| 2 Oct 2026 BST | Strengthened `night-windows.html` hub for pieces 31–35 (unique intro, meta/OG/Twitter to thirty-five windows, full cross-links + New this drop) AND refreshed `buy.html` hero/meta from stale “Twenty windows” to thirty-five with new-drop destinations named | Series hub is the strongest internal-link target for new piece URLs; buy page was still indexing as 20-piece shop copy — fixing that protects CTR/snippet accuracy as catalog hits 35 | Done with drop publish + second commit; live after push |

| 2 Oct 2026 BST | Added Product+Offer+ImageObject+BreadcrumbList JSON-LD to all 35 piece pages (public assets/*.jpg only); sitemap + how-to guide URL; created docs/SEO_LOG.md with scorecard stub | First SEO-operator fire: piece pages lacked commerce schema while titles/meta/alt already unique — highest EV vs speculative content on a zero-impression young gallery | Pushed; GSC/GA4 numbers pending browser session |

| 2026-10-05 BST | Added thematic **“More windows like this”** internal links between related pieces in both directions (Chefchaouen ↔ Moroccan Kasbah / Amalfi; Plitvice ↔ Banff Lake Louise / Hallstatt; Neuschwanstein ↔ Hallstatt / Matterhorn; Angkor Wat ↔ Bagan / Bali; Faroe Gásadalur ↔ Iceland Black Sand / Norwegian stave church), so 9 already-crawled piece pages now link contextually to the 5 new URLs. Hub `night-windows.html` refreshed to forty windows with a unique intro, a “Find your window” themed section (castles & old towns / temples / waterfalls & coasts), and CollectionPage + ItemList JSON-LD (40 items); `buy.html` hero/meta updated to forty. New pages ship with Product/Offer/Breadcrumb JSON-LD + GA4. | Piece pages previously only linked “next window” in a single chain, so a new URL got one inbound link from a page plus the hub; contextual links from topically related, already-indexed pages are the cheapest real signal for discovery/relevance on a young gallery, and ItemList gives the hub structured parity with piece-page schema | Shipped with pieces 36–40 drop (`scripts/publish_pieces_36_40.py`, idempotent) |

| 6 Oct 2026 BST | Aligned the 10 earliest piece pages (01–10: Moonlit Alpine Meadow … Mediterranean Lantern Walk) with the template used by 11+: `<title>` now “{Title} — Night Windows print | Prompt Framed”, meta description now “{Title} from the Night Windows series. Poster and framed print options. {mood}”, and the Product JSON-LD description matches (`scripts/seo_align_early_piece_titles.py`, idempotent; og/twitter left as the mood line like 11+). Shipped alongside the pieces 41–45 drop, whose hub/buy copy moved to forty-five windows and whose “More windows like this” links reach 10 older pages (Matterhorn, Wildflower Meadow Cabin, Norwegian stave church, Northern Lights Fjord, Amalfi, Coastal Cliffside Town, Hallstatt, Moonlit Mediterranean Village, Ha Long Bay, Zhangjiajie). | The oldest, most-crawled URLs were the only pages whose titles lacked the buyer word “print” and whose snippets never mentioned poster/framed options, so they under-matched “… print / poster” queries and looked inconsistent next to 11–45. Fixing existing indexed pages beats a new URL on a young site with no impression data yet | Pushed with the 41–45 drop; GSC/GA4 numbers still pending a signed-in session |

| 7 Oct 2026 BST | Added Google **image-sitemap** entries to `sitemap.xml`: every piece URL (50) now carries an `<image:image><image:loc>` pointing at its watermarked `assets/NN-*.jpg` preview, plus the contact sheet on `night-windows.html` (51 image entries; `scripts/seo_image_sitemap.py`, idempotent, now called at the end of `scripts/publish_pieces_46_50.py` so future drops get it automatically; refuses to write any `.png` or `print-masters` URL). Shipped with the pieces 46–50 drop (Meteora, Lauterbrunnen, Mount Fuji Chureito Pagoda, Iguazu Falls, Isle of Skye Old Man of Storr), whose hub/buy copy moved to fifty windows, “Find your window” gained a temples/pagodas/monasteries group, and “More windows like this” links reach 10 older pages (Cappadocia, Santorini, Matterhorn, Moonlit Waterfall, Japanese Temple Pond, Kyoto Bamboo, Plitvice, Machu Picchu, Scottish Highlands Loch, Faroe Gásadalur). | Wall-art buyers browse Google Images heavily, and an art-print gallery's product *is* the picture; until now Google could only find our 50 images by rendering each page. Image sitemap entries are Google's documented way to get images discovered and tied to their landing page, apply to every existing URL at once (not just today's), and use only the watermarked previews, so no clean print master is ever exposed. Only `image:loc` is used (title/caption/license tags were deprecated in 2022) | Pushed with the 46–50 drop; check GSC Sitemaps “discovered images” and the Search type: Image report next signed-in run |

| 12 Oct 2026 BST | Added the 5 new pieces (Sintra Pena Palace, Lake Como Bellagio, Grand Canyon South Rim, Cliffs of Moher, Big Sur Bixby Bridge) to the **peel and stick wall murals collection** (`peel-and-stick-wall-murals.html`, now 24 pieces; mountains group renamed “Mountain and canyon wall murals”, meta now names canyons; card alt text carries each place name), gave each new piece page the same “Planning a feature wall?” collection link the other 50 have, and restored the murals link on the hub’s canyons/coasts paragraph. Fixed the root cause: `publish_pieces_51_55.py` now renders that markup itself (it had been stripping it on re-runs), so it and `build_collection_murals.py --check` stay consistent. Shipped with the pieces 51–55 drop (hub/buy copy to fifty-five, “More windows like this” links from 11 older pages, image sitemap 58 entries). | The $149 mural is the highest-ticket SKU and the murals page is the only URL targeting “<place> wall mural” / “peel and stick wall mural” queries; the new pieces were the only 5 of 55 without a path to it, and the publish script would have quietly removed the link on every re-run. Adds 5 place-name entities (Sintra, Lake Como, Grand Canyon, Cliffs of Moher, Big Sur) to an already-submitted collection URL instead of creating a thin new page | Pushed with the 51–55 drop; IndexNow pinged; next signed-in GSC run: request indexing for the 5 new piece URLs + murals page |

| 13 Oct 2026 BST | Added the 5 new pieces (Prague Charles Bridge, Taj Mahal, Salar de Uyuni, Victoria Falls, Great Wall Mutianyu) to the **peel and stick wall murals collection** (`peel-and-stick-wall-murals.html`, now 29 pieces; Great Wall in mountains, Uyuni + Victoria Falls in a renamed “Lake, salt flat and waterfall” group, Prague + Taj Mahal in a renamed “Castle and landmark” group; card alt text carries each place name). Closed the Great Wall gap on **`mountain-wall-art.html`** (now 14 pieces; meta, hero and room guide name the Great Wall; the piece note on all 14 mountain pages no longer carries a count that goes stale). Added Victoria Falls + Salar de Uyuni to **`lake-wall-art.html`** (now 16; meta, FAQ and room guide updated). Victoria Falls copy now names the moonbow in the image (alt, meta, Product JSON-LD, buy/home cards, catalog). llms.txt collection counts updated (posters already read $35, no $29 left); `publish_pieces_56_60.py` now keeps the hub’s coastal link (its first run had dropped it) and any lakes/coastal notes on re-runs. All four `build_collection_*.py --check` and `publish_pieces_56_60.py --check` clean. | Collection pages are the only URLs targeting “mountain wall art”, “lake/waterfall wall art” and “peel and stick wall mural” queries, and the $149 mural is the highest-ticket SKU; the new drop’s pieces had no path to them, and the Great Wall page linked to a mountain collection that did not list it. Adds 5 high-volume place entities (Prague, Taj Mahal, Uyuni, Victoria Falls, Great Wall) to already-submitted collection URLs instead of creating thin new pages, and the moonbow is a distinctive, true image detail for image search | Pushed with the 56–60 drop; IndexNow pinged (piece URLs + murals/mountain/lakes collections + llms.txt); next signed-in GSC run: request indexing for the 5 new piece URLs + 3 collection pages |

Update this log when an SEO action ships. Prefer improving existing piece pages over speculative new URLs.

## 2026-10-02 afternoon update
- GSC processing; sitemap Success / 42 URLs.
- GA4: no data received yet (tag G-663R8VD62L live).
