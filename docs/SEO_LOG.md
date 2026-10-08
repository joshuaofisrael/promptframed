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
| 7d/28d/90d (as of 2026-10-05 ~14:35 BST) | not checked | not checked | not checked | not checked | not checked | Box Chrome Google session signed out; data step skipped (no guessing). |

**GSC property:** `https://moonlitwindows.com/` (URL-prefix, joshuaofisrael@gmail.com)  
**Sitemap:** `https://moonlitwindows.com/sitemap.xml` — Success (read/submitted 2 Oct 2026); **42 discovered pages** then; local file now lists 47 URLs (40 pieces + public pages) after 5 Oct cleanup. Resubmit next signed-in run, 0 videos. Not resubmitted (already current).  
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


---

## 2026-10-05 (BST) — scheduled SEO operator fire

### Hygiene
- `python3 scripts/inject_head_tags.py` → updated 0 pages (GA4 tag + homepage GSC meta already present).
- All 40 `pieces/*.html` in sitemap; all have Product/Offer/ImageObject/BreadcrumbList JSON-LD (incl. pieces 36–40). No print-master or clean `gallery/*.png` URLs in sitemap or public markup.
- No new Stripe Payment Links created.

### Data review
- **Blocked:** box Chrome is signed out of Google (Search Console redirected to the account chooser). GSC and GA4 not checked; no URL Inspection / indexing requests sent. No numbers recorded rather than guessed.
- Stripe commerce check: Stripe connector needs re-authentication, so no charge check this run.

### Opportunity chosen (and why)
**Retire `how-to-turn-chatgpt-art-into-a-framed-poster.html` into `guide-print-sizes.html`.**
1. It broke the public-copy rule (named ChatGPT in URL, title, H1 and body), flagged on 2 Oct.
2. Wrong intent for a print shop: it was a seller how-to (Printful, products.json, captions), not a buyer page, so it diluted topical focus.
3. Outdated/false: said the buy button "does not pretend to charge anyone" until a shop link exists; live Stripe checkout has existed since 28 Sep.
4. Overlapped the buyer-facing print-size guide. Consolidating is the guide's own advice (consolidate weak overlaps, avoid misleading content).

### Shipped (commit c2614fb)
- Old URL now a thin stub with canonical → `guide-print-sizes.html` and an instant meta refresh (GitHub Pages has no server 301; Google treats an instant meta refresh as a permanent redirect).
- Removed the retired URL from `sitemap.xml` (47 URLs).
- `how-it-works.html`: guide link now points to the print-size guide; checkout steps rewritten to match reality ($29 poster / $69 framed, 12×18, shipping included, Stripe checkout).
- Live check: `/`, `how-it-works.html`, `guide-print-sizes.html`, the stub and `sitemap.xml` all return 200; live sitemap no longer lists the retired URL.

### Next signed-in run
- Resubmit sitemap (changed today). Check Page indexing report and request indexing for homepage, `night-windows.html`, `buy.html` (max 3).
- Pull first GSC/GA4 numbers into the scorecard.
- Candidate next action if data stays thin: titles on the 7 early pieces lack "print" (e.g. "Lakeside Cabin — Night Windows"); align them with the "— Night Windows print" pattern.

---

## 2026-10-06 (BST) — SEO action with the pieces 41–45 drop

### Hygiene
- Pieces 41–45 (Dolomites Tre Cime, Lofoten Reine, Cinque Terre Manarola, Lake Bled Island, Guilin Li River) shipped via `scripts/publish_pieces_41_45.py` with unique title/meta/OG/alt, Product/Offer/ImageObject/BreadcrumbList JSON-LD and GA4. Sitemap now 52 URLs (45 piece pages included).
- Public images are the watermarked `assets/NN-*.jpg` / `gallery/social/NN-*.jpg` only; clean PNG masters and `gallery/print-masters/` stay local and gitignored.
- Hub `night-windows.html` refreshed to forty-five windows (intro, themed “Find your window” links, CollectionPage + ItemList with 45 items); `buy.html` hero/meta updated to forty-five.
- Internal links: each new piece has 2 thematic “More windows like this” links, and 10 older, already-crawled pages link back to the new URLs. Piece 40 “Next window” now points to piece 41; piece 45 loops to the first window.

### Data review
- GSC / GA4 not opened this run (no signed-in session used); no numbers recorded rather than guessed.

### Opportunity chosen (and why)
**Align titles/meta on the 10 earliest piece pages (01–10) with the 11+ template.** (Flagged as the next candidate on 5 Oct.)
1. Pieces 01–10 were built before the template settled: titles read “{Title} — Night Windows | Prompt Framed” with no “print”, and the meta description was only the mood line, with no mention of poster/framed options.
2. These are the oldest, most-crawled URLs, so improving their snippet relevance for “… print / poster” intent is cheap and low-risk, unlike a speculative new page.
3. Consistency: all 45 piece pages now share one title/meta pattern, and the Product JSON-LD description matches the meta description.

### Shipped
- `python3 scripts/seo_align_early_piece_titles.py` → updated 10/10 early piece pages (`<title>`, `<meta name="description">`, Product JSON-LD `description`). og:/twitter: tags left as the mood line, matching 11+.

### Intentionally not done
- No new articles or collection pages.
- No commit of print masters, PNGs, reels staging/logs, music, Instagram kit, or `.night-windows-*` JSON.

### Next signed-in run
- Resubmit sitemap (52 URLs). Request indexing for `night-windows.html` and two new piece pages (max 3).
- Pull first GSC/GA4 numbers into the scorecard.

---

## 2026-10-06 (BST) — scheduled SEO operator fire (14:35)

### Hygiene
- `python3 scripts/inject_head_tags.py` → updated 0 pages (GA4 + homepage GSC meta present).
- Sitemap: 52 URLs, all 45 `pieces/*.html` listed; only `thanks.html` and the retired ChatGPT-guide stub are excluded (intentional). No print-master, clean PNG or github.io URLs.
- No new Stripe Payment Links. Stripe check: no Night Windows checkouts (the only completed live session on the account is a $0 NamedScan promo-code order, not this site).

### Data review
- **Blocked again (2nd run in a row):** box Chrome's Google account joshuaofisrael@gmail.com shows "Signed out" at the account chooser. GSC and GA4 not checked; no sitemap resubmit or indexing requests. No numbers recorded rather than guessed. Joshua asked to sign back in.

### Opportunity chosen (and why)
**Page speed on the two heaviest pages: responsive grid thumbnails for `index.html` and `buy.html`.**
1. Both grids loaded the full 1024–1536px watermarked JPGs (~380 KB each, ~17 MB for all 45 cards) into cards that render ~250–400px wide. The first card is eager-loaded, so it is the homepage's LCP image.
2. Technical/page-experience fixes rank above new content in the operator priority list, and with no Search Console data there's no page-level signal to act on yet; this helps every visitor and crawler regardless.
3. Thumbnails are downscaled from the same watermarked `assets/NN-*.jpg` (watermark verified visible); print masters untouched.

### Shipped
- New `scripts/build_grid_thumbs.py` (idempotent): builds `assets/thumbs/NN-*.jpg` at 600px wide (~118 KB avg, ~5.3 MB total vs ~17 MB) and adds `srcset`/`sizes`/`decoding="async"` to grid images, keeping the full image as the 2x candidate. Run it in future hygiene so new daily pieces get thumbs.
- Piece pages, OG/Twitter images and JSON-LD ImageObject still point at the full watermarked image (image SEO unchanged).

### Next signed-in run
- Resubmit sitemap (52 URLs); request indexing for `night-windows.html`, `pieces/dolomites-tre-cime-moon.html`, `pieces/lofoten-reine-moon.html`.
- Pull first GSC/GA4 numbers into the scorecard.

### Scorecard
| Metric | Value |
|---|---|
| Impressions / clicks / CTR / position (7/28/90d) | not available (Google signed out) |
| Indexed pages | not available |
| GA4 page views | not available |
| Public URLs in sitemap | 52 |

## 6 Oct 2026 15:00 London (manual follow-up after Google re-sign-in)
- Sitemap resubmitted: Success, 52 discovered pages.
- night-windows.html: already indexed.
- pieces/lofoten-reine-moon.html: indexing requested (priority crawl queue).
- pieces/dolomites-tre-cime-moon.html: unknown to Google; request failed (Oops), retry next run.
- Performance 28d: 0 clicks, 1 impression, avg position 5 (retired how-to page). Page indexing report still processing.

---

## 2026-10-07 (BST) — SEO action with the pieces 46–50 drop

### Hygiene
- Pieces 46–50 (Meteora Monasteries, Lauterbrunnen Valley, Mount Fuji Pagoda, Iguazu Falls, Isle of Skye Storr) shipped via `scripts/publish_pieces_46_50.py` with unique title/meta/OG/alt, Product/Offer/ImageObject/BreadcrumbList JSON-LD and GA4. Sitemap now 57 URLs (50 piece pages).
- Public images are the watermarked `assets/NN-*.jpg`, `assets/thumbs/NN-*.jpg` and `gallery/social/NN-*.jpg` only; clean PNG masters and `gallery/print-masters/` stay local and gitignored.
- Hub `night-windows.html` refreshed to fifty windows (intro, themed “Find your window” links incl. a new “Temples, pagodas and monasteries” group, CollectionPage + ItemList with 50 items); `buy.html` hero/meta updated to fifty. Grid thumbnails built for 46–50 (`scripts/build_grid_thumbs.py`).
- Internal links: each new piece has 2 thematic “More windows like this” links, and 10 older pages link back. Piece 45 “Next window” now points to piece 46; piece 50 loops to the first window.

### Data review
- GSC / GA4 not opened this run (no browser session used); no numbers recorded rather than guessed.

### Opportunity chosen (and why)
**Image sitemap for all piece pages.**
1. Google Images is a primary discovery surface for wall art, and nothing in the sitemap told Google about our 50 images; they could only be found by rendering pages.
2. One change improves every existing URL, not just today's five, and costs nothing at runtime.
3. Uses only the watermarked `assets/NN-*.jpg` previews; the script refuses to write `.png` or `print-masters` URLs.

### Shipped
- New `scripts/seo_image_sitemap.py` (idempotent): adds `xmlns:image` and one `<image:image><image:loc>` per piece URL (plus the contact sheet on the hub) → 51 image entries. Called automatically at the end of `scripts/publish_pieces_46_50.py`.

### Next signed-in run
- Resubmit sitemap (57 URLs, 51 images) and confirm GSC reads the image entries.
- Request indexing for `pieces/dolomites-tre-cime-moon.html` (failed 6 Oct) and two of 46–50 (max 3).
- Pull first GSC/GA4 numbers into the scorecard.


## 2026-10-07 — Commercial-intent pass (make it obvious the site sells prints)
- Why: GSC shows ~1 impression/28d; pages read as a gallery, not a shop. Titles/meta/schema now state product + price so results match "poster"/"framed print" queries.
- Audited offers: only 2 products per piece, 50 pieces, all Stripe Payment Links live — 12×18 poster $29, 12×18 black framed print $69, shipping included (products.json + `apply_stripe_links.py --check` 50/50).
- 50 piece pages: title "<Piece> Poster & Framed Print | Moonlit Windows", price-led meta description, OG/Twitter (watermarked assets/), sale line under H1 with #buy link, Product JSON-LD now has url, free-shipping OfferShippingDetails, seller Moonlit Windows (BreadcrumbList kept).
- Homepage: commercial title/meta, sale line, CTA "Shop Posters & Framed Prints"; Organization + WebSite + ItemList JSON-LD.
- buy.html: H1 "Shop Posters & Framed Prints", CollectionPage/ItemList + BreadcrumbList JSON-LD, Twitter tags.
- night-windows.html: commercial title/meta, sale line, BreadcrumbList.
- Nav label "Buy" → "Shop Posters & Framed Prints" and footer shop link on all pages.
- sitemap.xml: lastmod on the 57 changed URLs.
- Validation: 55 JSON-LD blocks parse; sitemap XML parses; no AI/ChatGPT/Higgsfield/github.io in new copy.
- TODO (needs Joshua/Search Console UI): resubmit sitemap.xml in GSC and request indexing of /, /buy.html.
- Script: scripts/seo_commercial_pass.py (idempotent).
- Keyword pass (same day, scripts/seo_keywords_pass.py): buyer terms only for real products (poster $29, framed print $69; no canvas/wallpaper): wall art poster, art print, framed print, framed wall art, moon poster, night/moonlit landscape wall art, home decor print, <place> poster. Applied to titles, meta, sale lines, piece + buy-grid alt text, og:image:alt, Product/Offer JSON-LD names/descriptions.

## 2026-10-07 — Peel & stick wall murals ($149) + owner footer
- New product on all 50 pieces: Peel & Stick Wall Mural 4×6 ft (48×72 in), peel-and-stick polyester, $149, shipping included, printed to order (1–2 weeks). 50 Stripe products/prices/Payment Links (redirect thanks.html?piece=<slug>&variant=mural; shipping+phone; promo codes on). products.json stripe.muralUrl.
- Site via scripts/apply_mural_links.py (idempotent; re-run after apply_stripe_links.py): mural button + info note on piece pages and buy.html, $149 #offer-mural in Product JSON-LD, mural price line.
- Keywords: wall mural, peel and stick wall mural, peel and stick wallpaper / removable wallpaper in titles (pieces "<Piece> Poster, Framed Print & Wall Mural", buy.html, homepage), meta/OG/Twitter descriptions and Product descriptions.
- Nav/footer: "Shop Posters, Prints & Wall Murals". Every HTML page footer: "Operated by Joshua Israel Ventures LLC".
- thanks.html handles variant=mural. sitemap lastmod → 2026-10-07. Poster/framed links still pass apply_stripe_links.py --check (50/50).
- Next: track queries "peel and stick wall mural <place>", "moon wall mural", "removable wallpaper mural"; consider a /wall-murals.html collection page.

## 2026-10-07 14:30 London — Scheduled run: mountain wall art collection page
### Data review
- Stripe: no Night Windows sales (only checkout in the list is a NamedScan $0 promo session).
- GSC: last read 6 Oct (28d: 0 clicks, 1 impression). Too little query data to double down on any term yet, so today's action builds a new buyer-intent entry point instead.

### Opportunity chosen (and why)
**New collection page `/mountain-wall-art.html`.** "Mountain wall art" / "mountain poster" are high-volume buyer searches that no single piece page can rank for, and buy.html (all 50, every theme) is too broad to match them. A themed collection with real buying help is the format that ranks for these queries (Etsy/Desenio-style category pages), and it doesn't cannibalise buy.html or the piece pages.

### Shipped
- `mountain-wall-art.html`: title "Mountain Wall Art Posters, Framed Prints & Wall Murals", price-led meta/OG/Twitter, H1 "Mountain Wall Art: Moonlit Mountain Posters & Framed Prints", 13 mountain pieces (Matterhorn, Dolomites, Mount Fuji, Lauterbrunnen, Isle of Skye, Yosemite, Banff Lake Louise, Patagonia, Zhangjiajie, Machu Picchu, Scottish Highlands, Snowy Peaks, Alpine Meadow) with live poster/framed/mural Stripe buttons, a "how to choose mountain wall art for your room" guide (bedroom, living room/feature wall, office, trip keepsake, pairs), and an FAQ (formats, mural lead time, real places, checkout). CollectionPage + ItemList + BreadcrumbList JSON-LD. Watermarked `assets/` + `assets/thumbs/` only.
- Internal links: all 13 mountain piece pages link to the collection; night-windows.html "Mountains and river valleys" paragraph links to it; buy.html hero "Browse by theme" link.
- sitemap.xml: new URL with image entry (58 URLs). styles.css: `.card h3` matches `.card h2`.
- Script: `scripts/build_collection_mountain.py` (idempotent).
- Checks: JSON-LD parses, sitemap parses, no banned words (AI/ChatGPT/Higgsfield/github.io/canvas), no broken relative links, `apply_stripe_links.py --check` 50/50, mural check 50/50.

### Next
- Signed-in GSC: resubmit sitemap; request indexing for /mountain-wall-art.html, /buy.html, pieces/dolomites-tre-cime-moon.html.
- If the template earns impressions, repeat for the next theme clusters: castles, Japan, lakes/waterfalls, Mediterranean coast, Scotland.
- GSC follow-up (14:38): not done. `sc-domain:moonlitwindows.com` says joshuaofisrael@gmail.com has no access (the 6 Oct resubmit must have used the URL-prefix property). The URL-prefix property couldn't be checked because Chrome tabs kept crashing: the box had ~170 MB free while a realesrgan upscale of gallery/04 was running. Next run: retry https://search.google.com/search-console/sitemaps?resource_id=https%3A%2F%2Fmoonlitwindows.com%2F once memory is free, then resubmit the sitemap and request indexing for mountain-wall-art.html, buy.html and dolomites-tre-cime-moon.html.

## 2026-10-08 London — AI search readiness (owner rule, 8 Oct)
- robots.txt: kept `User-agent: *` / `Allow: /` + Sitemap line; added explicit Allow groups for OAI-SearchBot, ChatGPT-User, GPTBot, PerplexityBot, Perplexity-User, ClaudeBot, Claude-SearchBot, Claude-User, Google-Extended, Applebot, Applebot-Extended, Bingbot, DuckAssistBot, Amazonbot.
- New /llms.txt (llmstxt.org format: H1, blockquote summary incl. "Operated by Joshua Israel Ventures LLC", Shop / Representative pieces / Buying help / About sections). Added to sitemap.xml (59 URLs).
- scripts/ai_search_pass.py (idempotent, `--check`): answer-first opener on homepage + about.html; buy.html, night-windows.html and all 50 piece sale-lines now include the $149 4×6 ft wall mural; about.html title/meta rewritten; homepage first JSON-LD WebSite node unified with #website/#org (was a second "Prompt Framed" WebSite); FAQPage JSON-LD on mountain-wall-art.html mirroring its visible FAQ.
- JSON-LD parses on every page. Hosting: GitHub Pages (no Cloudflare). Changed URLs + /llms.txt + /robots.txt re-pinged via IndexNow.
- Gaps: guide-print-sizes.html discusses 20×30 / 24×36 framed sizes that aren't sold (only 12×18 + 4×6 ft mural); how-it-works.html doesn't mention murals; rerunning build_collection_mountain.py may drop the FAQPage block.
