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

## 2026-10-08 London — AI search follow-up (gaps from the morning pass)
- guide-print-sizes.html rewritten to the formats actually sold: 12×18 poster ($29), 12×18 black-framed print ($69), 4×6 ft peel-and-stick wall mural ($149). Removed 20×30 / 24×36 advice, wood/white/gold frame suggestions (frame is black only) and the pixel-size note. Answer-first opener, new title/meta/OG, WebPage + BreadcrumbList JSON-LD.
- how-it-works.html: step 5 for the $149 mural (printed to order, shipped by post in 1–2 weeks); "Five steps"; new title/meta/OG; WebPage + BreadcrumbList JSON-LD.
- contact.html: title "Contact Moonlit Windows | …"; ContactPage + BreadcrumbList JSON-LD. about.html: AboutPage + BreadcrumbList JSON-LD.
- Deleted how-to-turn-chatgpt-art-into-a-framed-poster.html (redirect stub, no inbound links, not in sitemap); removed it from README and from the page list in seo_commercial_pass.py (that script would otherwise crash on the missing file).
- scripts/build_collection_mountain.py now renders the FAQPage JSON-LD; regenerated output is byte-identical to the live page.
- (untracked) scripts/publish_pieces_51_55.py: new piece sale-line includes the $149 mural; keeps the "50" counts in index answer-first, buy sale-line, about.html and llms.txt in step; saves new + changed URLs to promptframed-private/publish_51_55_urls.json; new `--ping` mode (run after commit+push) waits for the new pages to return 200, then IndexNow-pings. Dry-run tested in a throwaway copy with placeholder images only.
- sitemap lastmod 2026-10-08 on the four changed pages.

## 2026-10-08 London — Public-copy cleanup (no tool/generator mentions)
- gallery/catalog.json (public): removed `source` and `stylePrompt` from all 50 rows and dropped 2 tool-name keywords per row. Nothing in site.js or scripts reads those fields (only the publish scripts write them). Originals moved to /workspace/promptframed-private/catalog_private.json (keyed by slug, incl. removedKeywords).
- (untracked) scripts/publish_pieces_51_55.py: tool-name keywords removed; catalog rows no longer get source/stylePrompt (written to the private file instead); keywords are now checked against the banned list; verify flags private fields or banned words in catalog.json. Dry-run tested in a /tmp copy.
- about.html title/og:title now end "| Moonlit Windows".
- Public-file grep (tracked HTML/JSON/txt/xml/md outside scripts/ and docs/): fixed README.md (bio suggestion, two disclosure lines) and instagram-kit/first-posts/CAPTIONS.md. Only remaining hit: `User-agent: ChatGPT-User` in robots.txt (intentional).

## 2026-10-08 London — Brand/legal pass (owner rule: Moonlit Windows is a brand of Joshua Israel Ventures LLC, not a DBA)
- Every page footer: "© 2026 Joshua Israel Ventures LLC. All rights reserved. Moonlit Windows is owned and operated by Joshua Israel Ventures LLC." + Terms · Privacy · Disclaimer · Contact links (readable ink colour, ~1rem). Old "Operated by…" and "© … Prompt Framed" lines removed. Class `operated-by` kept on the new block so existing markers/checks still match.
- New pages: terms.html (Terms of Use and Sale, Michigan law), privacy.html (controller Joshua Israel Ventures LLC, joshuaofisrael@gmail.com; Stripe, print partner, GA4, Google Fonts, GitHub Pages, mailto form), disclaimer.html (colour accuracy, watermarked previews, general info, creator promo code commission). WebPage + BreadcrumbList JSON-LD; added to sitemap (62 URLs) and llms.txt (## Legal).
- Refund wording: the site stated no returns/refund policy, so terms use the default: damaged or misprinted items replaced or refunded if reported within 30 days of delivery with a photo.
- JSON-LD: Organization/publisher/seller = Joshua Israel Ventures LLC (@id #org) with brand Moonlit Windows; Product brand = Moonlit Windows (was Night Shade Art); all poster/framed/mural offers' seller = the LLC.
- about.html: "Moonlit Windows is a brand of Joshua Israel Ventures LLC." llms.txt summary says the same.
- Gap fixed: site.js rewrote mural buttons to the poster Stripe link after products.json loaded (buy.html, mountain page, older piece pages). Mural buttons now keep muralUrl.
- Generators: scripts/legal_pass.py (idempotent, --check); build_collection_mountain.py renders the new footer (output byte-identical to live); untracked publish_pieces_51_55.py renders the new footer + LLC seller/brand (template test: skeleton matches piece 50).
- 2026-10-08 14:30: governing law corrected Michigan to Florida (Joshua Israel Ventures LLC is a Florida LLC) in terms.html, llms.txt, legal_pass.py.

## 2026-10-08 14:32 London — Scheduled run: peel-and-stick wall murals collection page
### Data review
- Stripe: no Night Windows sales. One $29 Lakeside Cabin poster checkout (7 Oct 13:49 London) expired unpaid.
- GSC: blocked. Box Chrome shows joshuaofisrael@gmail.com as "Signed out" at the Google account chooser, so the sitemap was not resubmitted, no indexing was requested and no numbers were read. Last real numbers are from 6 Oct (28d: 0 clicks, 1 impression).

### Opportunity chosen (and why)
**New collection page `/peel-and-stick-wall-murals.html`.** The $149 mural is the highest-ticket product (live on all 50 pieces since 7 Oct), but no page could rank for "peel and stick wall mural", "moon wall mural", "landscape wall mural", "removable wallpaper mural" or "<place> wall mural". This was the planned next step from the 7 Oct entry.

### Shipped (commit 86383fb)
- Title "Peel and Stick Wall Murals: Moonlit Landscape Murals, $149 | Moonlit Windows"; price-led meta/OG/Twitter; H1 "Peel and Stick Wall Murals: Moonlit Landscapes for a Feature Wall"; answer-first opener.
- 19 pieces in tall 2:3 shape (matches the portrait 48×72 in mural) in 5 groups: mountains, lakes and waterfalls, coasts and fjords, forests, castles. Mural button first, plus poster $29 / framed $69, from products.json.
- Buying help: measuring a 48×72 in panel, which walls suit it, general prep/hanging/removal, mural vs framed vs poster; 7-question FAQ mirrored in FAQPage JSON-LD. CollectionPage + ItemList + BreadcrumbList JSON-LD. No invented specs, reviews or vendor names.
- Internal links: all 50 piece pages (under the mural note), buy.html "Browse by theme", night-windows.html, guide-print-sizes.html, how-it-works.html, mountain-wall-art.html. llms.txt Shop line. sitemap.xml now 63 URLs, 53 image entries.
- Generator `scripts/build_collection_murals.py` (idempotent, `--check`); `build_collection_mountain.py` updated to keep its new link.
- Checks: JSON-LD parses, sitemap parses, no broken links, no banned words, `apply_stripe_links.py --check` 50/50, mural check 50/50. Live 200 at 14:48 London; IndexNow 200 for 58 URLs.

### Known issue
- `scripts/apply_stripe_links.py` run WITHOUT `--check` rebuilds the buy.html grid in an old format (drops thumbnails, alt text and the $149 mural from the price line), which then breaks both collection builders (KeyError). Pre-existing. Use `--check` only until fixed.

### Next signed-in run
- Resubmit sitemap (63 URLs); request indexing for /peel-and-stick-wall-murals.html, /mountain-wall-art.html, /buy.html (dolomites piece after that).
- Pull 7/28d GSC numbers into the scorecard. If either collection page earns impressions, build the next theme (castles, Japan, lakes/waterfalls, coasts).
- 2026-10-08 15:05 GSC (Joshua re-signed in): sitemap resubmitted, Success, 59 discovered. Indexing requested: peel-and-stick-wall-murals, mountain-wall-art, buy (all unknown to Google), / (indexed). Performance 28d: 0 clicks, 4 impressions, avg pos 6.8.

## 2026-10-12 London — Pieces 51–55 drop + murals collection
- Published Sintra Pena Palace Moon, Lake Como Bellagio Moon, Grand Canyon Rim Moon, Cliffs of Moher Moon, Big Sur Bixby Bridge Moon (`scripts/publish_pieces_51_55.py`), with live Stripe poster/framed/mural Payment Links (15 products, 15 prices, 15 links).
- SEO action: all 5 added to `peel-and-stick-wall-murals.html` (24 pieces; “Mountain and canyon wall murals”; meta names canyons); new piece pages carry the murals collection link; hub canyons/coasts paragraph keeps the murals link. `publish_pieces_51_55.py` now renders the murals markup itself so re-runs no longer strip it.
- Gotcha: `build_collection_mountain.py` has no `--check` mode; running it rewrites mountain-wall-art.html from its template and reverts the series-count line (re-run the publish script after it).
- Next signed-in run: request indexing for the 5 new piece URLs and the murals page.

## 2026-10-12 05:20 London — Scheduled run: lake and waterfall wall art collection page
### Data review
- Stripe: no Night Windows sales since the last run (only checkout session since 8 Oct was an expired, unpaid $5 tip on another project).
- GSC: not checked this run (the daily drop was publishing pieces 51–55 on the shared desktop/repo at the same time). Last numbers: 8 Oct, 28d 0 clicks, 4 impressions, avg pos 6.8. Too little data to pick winners, so the planned theme-cluster expansion continues.

### Opportunity chosen (and why)
**New collection page `/lake-wall-art.html`** targeting "lake wall art", "lake house wall art", "lake poster", "waterfall wall art", "waterfall poster" and place variants (Lake Como, Lake Bled, Hallstatt, Lake Louise, Plitvice, Iguazu). Lakes and waterfalls are the biggest themed group in the catalogue (14 of 55) with no page that could rank for them; it was the next cluster on the plan after mountains and murals.

### Shipped (commit 5412c44)
- Title "Lake Wall Art & Waterfall Posters, Framed Prints | Moonlit Windows"; price-led meta/OG; H1 "Lake & Waterfall Wall Art: Moonlit Lake Posters and Framed Prints"; answer-first opener.
- 14 pieces in two groups (9 lakes, 5 waterfalls); poster $29 / framed $69 / mural $149 buttons from products.json; place-named alt text.
- Room guide (lake house or cabin, bedroom, living room/feature wall, office/hallway, trip souvenir pairs); 5-question FAQ mirrored in FAQPage JSON-LD, including an honest real-vs-imagined places answer. CollectionPage + ItemList + BreadcrumbList JSON-LD.
- Internal links: the 14 piece pages, buy.html "Browse by theme", night-windows.html lakes/coasts paragraph, murals page ("Looking for something else", via build_collection_murals.py, which also dropped a stale "all fifty"). llms.txt Shop line (and murals count 19 → 24). sitemap.xml + lake page.
- Generator `scripts/build_collection_lakes.py` (idempotent, `--check`). Checks: JSON-LD parses, sitemap parses, no broken relative links, both collection builders `--check` up to date, `apply_stripe_links.py --check` 55/55. Live 200; IndexNow 200 for 20 URLs.

### Notes
- `publish_pieces_51_55.py` re-renders Lake Como Bellagio; if it is ever re-run, re-run `build_collection_lakes.py` afterwards to restore the lakes link.
- Mountain page still says "all fifty" and isn't linked to the lakes page (its builder has no --check; left alone).

### Next
- Signed-in GSC: request indexing for /lake-wall-art.html, the 5 new piece URLs (51–55) and /peel-and-stick-wall-murals.html; pull 7/28d numbers.
- Next clusters if these earn impressions: coasts (Amalfi, Santorini, Cinque Terre, Lofoten, Cliffs of Moher, Big Sur), Asia temples (Kyoto, Fuji, Angkor, Bagan), castles once there are more than 3.

## 2026-10-13 04:55 London — Scheduled run: coastal wall art collection page
### Data review
- Stripe: no Night Windows sales. Only checkout since the last run is an open, unpaid $35 Lakeside Cabin poster session (12 Oct 08:44 London, the $35 price-change check). The `joshua-israel-ventures-llc` Stripe connector needs re-auth; the `stripe` connector (same LLC account) works.
- GSC: not checked. The daily drop was using the shared desktop browser to make pieces 56–60 at the same time. Last numbers: 8 Oct, 28d 0 clicks, 4 impressions, avg pos 6.8. Still too little data to pick winners, so the theme-cluster plan continues.
- Price raise check: no stale $29 left in public HTML/JSON/txt; `apply_stripe_links.py --check` 55/55.

### Opportunity chosen (and why)
**New collection page `/coastal-wall-art.html`** targeting "coastal wall art", "ocean wall art", "seaside poster", "fjord wall art" and place variants (Amalfi Coast, Santorini, Cinque Terre, Cliffs of Moher, Big Sur, Lofoten, Mont Saint-Michel, Ha Long Bay). Coasts were the next cluster on the plan after mountains, murals and lakes; 14 of 55 pieces fit and no page could rank for them.

### Shipped (commit d0ad58a)
- Title "Coastal Wall Art: Moonlit Ocean & Seaside Posters, Framed Prints | Moonlit Windows"; price-led meta/OG; H1 "Coastal Wall Art: Moonlit Ocean, Seaside and Fjord Prints"; answer-first opener.
- 14 pieces in three groups (Mediterranean coast 5, ocean cliffs and wild shores 5, fjords and bays 4); poster $35 / framed $69 / mural $149 buttons from products.json; place-named alt text.
- Room guide (beach house, bedroom, living room/feature wall, office, trip pairs); 6-question FAQ mirrored in FAQPage JSON-LD, including honest real-vs-imagined and "is this beach decor?" answers. CollectionPage + ItemList + BreadcrumbList JSON-LD.
- Internal links: the 14 piece pages (after their last collection link), buy.html "Browse by theme", night-windows.html coasts paragraph, lake page ("Looking for peaks rather than water?") and murals page ("Looking for something else") via their builders. Lake/murals page footers carry the new link. llms.txt Shop line. sitemap.xml 70 URLs (lake + murals lastmod 13 Oct).
- Generator `scripts/build_collection_coastal.py` (idempotent, `--check`). Checks: JSON-LD parses, sitemap parses, no broken relative links, no banned words, coastal/lakes/murals builders `--check` up to date, `apply_stripe_links.py --check` 55/55. Live 200 at 04:59 London; IndexNow 200 for 21 URLs.

### Next
- Signed-in GSC: request indexing for /coastal-wall-art.html, /lake-wall-art.html, pieces 51–55, /peel-and-stick-wall-murals.html, and today's drop (56–60); pull 7/28d numbers.
- Next cluster if these earn impressions: Asia temples (Kyoto, Fuji, Angkor, Bagan, Bali), or a "moon poster for bedroom" buyer guide.

## 2026-10-14 04:55 London — Scheduled run: Asian wall art collection page
### Data review
- Stripe: no Night Windows sales. No new checkout sessions since the 12 Oct $35 Lakeside Cabin price-check session (now expired, unpaid).
- GSC: not checked. The daily drop was using the shared desktop browser to make the next pieces (Bruges) at the same time. Last numbers: 8 Oct, 28d 0 clicks, 4 impressions, avg pos 6.8. Still too little data to pick winners, so the theme-cluster plan continues.
- News post: none (no genuinely relevant news for the niche today).
- Outreach: no emails sent. This routine's saved instruction doesn't name outreach sends, so the 5/day allotment needs the parent/Joshua to authorise it (or the routine prompt updated) before any go out.

### Opportunity chosen (and why)
**New collection page `/asian-wall-art.html`** targeting "asian wall art", "japanese wall art", "japan poster", "temple wall art" and place variants (Mount Fuji, Kyoto, Great Wall, Guilin, Taj Mahal, Angkor Wat, Bagan, Ha Long Bay). Asia was the next cluster on the plan after mountains, murals, lakes and coasts; 12 of 60 pieces fit and no page could rank for them. "Japanese wall art" is a large buyer-intent term.

### Shipped (commit 5d1ee23)
- Title "Asian Wall Art: Japanese & Temple Posters, Framed Prints | Moonlit Windows"; price-led meta/OG; H1 "Asian Wall Art: Moonlit Japanese, Chinese and Temple Prints"; answer-first opener.
- 12 pieces in three groups (Japan 3, China 3, Southeast Asia and India 6); poster $35 / framed $69 / mural $149 buttons from products.json; place-named alt text.
- Room guide (bedroom, living room/feature wall, meditation corner/study, office/hallway, trip pairs); 6-question FAQ mirrored in FAQPage JSON-LD, including honest real-vs-imagined and "Japanese wall art for a bedroom" answers. CollectionPage + ItemList + BreadcrumbList JSON-LD.
- Internal links: the 12 piece pages (after their last collection link), buy.html "Browse by theme", night-windows.html (after the coastal sentence). llms.txt Shop line. sitemap.xml (+ lastmod 14 Oct on changed URLs).
- Generator `scripts/build_collection_asian.py` (idempotent, `--check`). Checks: JSON-LD parses, sitemap parses, no broken relative links, no banned words, asian/coastal/lakes/murals builders `--check` up to date, `apply_stripe_links.py --check` 60/60. Live 200 at 04:59 London; IndexNow 200 for 17 URLs.

### Notes
- Taj Mahal and Great Wall pages are rendered by `publish_pieces_56_60.py`; if it's re-run, re-run `build_collection_asian.py` afterwards to restore the Asian link.
- Lake, coastal and murals pages don't link to the new page yet (their builders own those templates); add it next time one is touched.

### Next
- Signed-in GSC: request indexing for /asian-wall-art.html, /coastal-wall-art.html, /lake-wall-art.html, pieces 51–60 and today's drop; pull 7/28d numbers. GSC has now gone unchecked since 8 Oct because the desktop is busy during this slot — consider checking it from a later run.
- Next: cross-link the Asian page from the other collection builders; then a "moon poster for bedroom" buyer guide or a European cities/castles cluster.

## 2026-10-14 ~05:05 London — Night Windows daily drop 61–65 + collection wiring
### Data review
- Stripe: no sales since last check; created 15 live products + 15 payment links for pieces 61–65 (poster $35 / framed $69 / mural $149).
- GSC: not rechecked this run (desktop busy during drop).
- News post: none (no genuinely relevant news).

### Opportunity chosen (and why)
**Wire pieces 61–65 into lakes, mountain, coastal and murals collection pages** so the new Tekapo / Kirkjufell / Na Pali / Bruges / Bibury windows rank with existing buyer-intent hubs instead of only as orphan piece pages. Highest EV after the Asian collection page shipped earlier this morning.

### Shipped
- Night Windows 61–65 live: Lake Tekapo Church Moon, Bruges Canal Moon, Kirkjufell Waterfall Moon, Bibury Arlington Row Moon, Na Pali Coast Moon (piece pages, buy.html, night-windows hub, sitemap, IndexNow list).
- Collections: lake-wall-art.html (+Tekapo, Kirkjufellsfoss), mountain-wall-art.html (+Tekapo, Kirkjufell), coastal-wall-art.html (+Na Pali), peel-and-stick-wall-murals.html (all five). Piece-page collection-link notes for lakes/coastal/mountain.
- apply_stripe_links.py --check and apply_mural_links.py --check: 65/65 live.
- Instagram candidate queued (not posted): Lake Tekapo Church Moon.

### Next
- Signed-in GSC: request indexing for pieces 61–65 and updated collection hubs.
- Cross-link Asian page from other collection builders when next touched.

## 2026-10-15 04:55 London — Scheduled run: European wall art collection page
### Data review
- Stripe: no Night Windows sales. No checkout sessions or charges since the 14 Oct run (checked via the `stripe` connector, Joshua Israel Ventures LLC live account).
- GSC: not checked. The daily drop (pieces 66–70) was running in this slot again. Last numbers: 8 Oct, 28d 0 clicks, 4 impressions, avg pos 6.8. GSC has now gone a week unchecked; it needs a run outside the 04:45–05:15 drop window.
- News post: none (no genuinely relevant news for the niche today).
- Outreach: no emails sent; this routine's saved instruction doesn't name outreach sends, so the daily allotment (now 3/day) still needs Joshua's go-ahead or a routine update.

### Opportunity chosen (and why)
**New collection page `/european-wall-art.html`** targeting "european wall art", "castle wall art", "castle poster", "European city wall art" and place variants (Neuschwanstein, Venice, Prague, Bruges, Dubrovnik, Hallstatt, Provence, Tuscany, Mont Saint-Michel). European castles and old towns were the next cluster on the plan; 14 of 70 pieces fit, and most of them (Neuschwanstein, Venice, Prague, Bruges, Rothenburg, Sintra, Meteora, Provence, Tuscany, Bibury) had no themed hub at all beyond the murals page.

### Shipped (commit 15633f6)
- Title "European Wall Art: Castle & Old Town Posters, Framed Prints | Moonlit Windows"; price-led meta/OG (Neuschwanstein image); H1 "European Wall Art: Moonlit Castles, Old Towns and Villages"; answer-first opener.
- 14 pieces in three groups (castles 5, old towns and cities 6, countryside and villages 3); poster $35 / framed $69 / mural $149 buttons from products.json; place-named alt text drawn from the existing card blurbs.
- Room guide (bedroom, child's room/nursery, living room/feature wall, kitchen/hallway, trip pairs); 7-question FAQ mirrored in FAQPage JSON-LD, with honest real-vs-imagined and castle-for-kids answers. CollectionPage + ItemList + BreadcrumbList JSON-LD.
- Internal links: the 14 piece pages (after their last collection link), buy.html "Browse by theme", night-windows.html "Castles and old towns" paragraph, Asian page (room-guide sentence + footer, via build_collection_asian.py). llms.txt Shop line. sitemap.xml 87 URLs.
- Generator `scripts/build_collection_european.py` (idempotent, `--check`). Checks: JSON-LD parses, sitemap parses, no broken relative links across hubs and all piece pages, no banned words, european/asian/coastal/lakes/murals builders `--check` up to date, `apply_stripe_links.py --check` 70/70, `apply_mural_links.py --check` 70/70. Live 200 at 05:07 London; IndexNow 200 for 20 URLs.

### Notes
- Dubrovnik, Eilean Donan and Rothenburg pages are rendered by `publish_pieces_66_70.py`; if it's re-run, re-run `build_collection_european.py` (and coastal) afterwards to restore the links.
- Lake, coastal, mountain and murals pages still don't link to the Asian or European pages (their builders own those templates); add both next time one is touched.

### Next
- Signed-in GSC: request indexing for /european-wall-art.html, /asian-wall-art.html, /coastal-wall-art.html, /lake-wall-art.html and pieces 51–70; pull 7/28d numbers.
- Then: cross-link Asian + European from the other collection builders; a "moon poster for bedroom" buyer guide; Friday summary tomorrow.

## 2026-10-16 05:30 London — Daily drop 71–75: collection placement + European/Asian links on every collection hub
### Data review
- Stripe: no Night Windows sales. No charges and no checkout sessions since 15 Oct 05:00 London (read-only check, Joshua Israel Ventures LLC live account). Last checkout session on the account: 12 Oct (Lakeside Cabin poster, expired unpaid).
- GSC: not checked (drop window again).
- News post: none.

### Opportunity chosen (and why)
1. **Collection placement for the five new pieces** (each lands on the hubs searchers reach for: murals, European, Asian, lakes, mountain).
2. **Close the collection-hub link gap** flagged on 15 Oct: the lake, coastal, mountain and murals pages did not link to the European or Asian collections, and mountain linked to none of lake/coastal/European/Asian. Those four builders were being touched for the drop anyway, so the fix rides along with no extra churn.

### Shipped
- Pieces 71–75 (Colmar Petite Venise, Glenfinnan Viaduct, Monument Valley, Sigiriya Rock, Cradle Mountain Dove Lake): piece pages, buy cards, hub, sitemap image entries, related links, next chain; Stripe poster $35 / framed $69 / mural $149 links live (75/75).
- murals: all five (2:3). European: Colmar (old towns), Glenfinnan (countryside), meta + FAQ + room guide. Asian: Sigiriya (South and Southeast Asian group), meta + FAQ. Lakes: Cradle Mountain + FAQ. Mountain: Monument Valley + Cradle Mountain, meta + room guide.
- Lake, coastal, mountain, murals hubs: contextual body links to European + Asian collections (mountain also to lake + coastal), and the full six-collection footer.
- Alt text and collection captions corrected to what is in each image before publishing (see SEO_SCORECARD).
- Checks: all six `build_collection_*.py --check` up to date, `apply_stripe_links.py --check` 75/75, `apply_mural_links.py --check` 75/75, `publish_pieces_71_75.py --check` 0 issues, sitemap parses, JSON-LD parses, 0 broken relative links.
- Instagram candidate queued (not posted): Monument Valley Moon (runner-up Cradle Mountain Dove Lake Moon).

### Next
- Signed-in GSC: request indexing for pieces 51–75, the six collection hubs and /moon-poster-bedroom.html; pull 7/28d numbers. Still needs a run outside 04:45–05:15 London (browser lock / drop collision).

## 2026-10-16 ~05:15 London — Scheduled SEO run: moon poster bedroom guide + Friday weekly summary
### Data review
- Stripe: no Night Windows sales (same read as the drop entry above; 75/75 pieces now live with poster/framed/mural). Parent/drop already confirmed no charges since 15 Oct.
- GSC: still unchecked this week. Last numbers 8 Oct (28d: 0 clicks, 4 impressions, avg pos 6.8). Signed-in browser collided with the daily Night Windows drop again; blocker remains for a run outside 04:45–05:15 London.
- News post: none (no genuinely relevant news for the niche today).
- Outreach: not sent (this routine does not authorise outbound outreach).

### Opportunity chosen (and why)
**A+B (cross-links + pieces 71–75 on theme hubs) already shipped in the concurrent daily-drop commit `7549422`.** Highest remaining EV for this Friday slot: ship the planned **"moon poster for bedroom" buyer guide**, fix stale llms.txt collection counts, and write the Friday weekly summary.

### Shipped
- `/moon-poster-bedroom.html`: title "Moon Poster for Bedroom: Calm Night Windows Wall Art"; answer-first opener; size/viewing-distance notes (links `guide-print-sizes.html` + murals); theme guidance (lakes/mountains, Asian, European); eight calm pieces (Lakeside Cabin, Banff Lake Louise, Japanese Temple Pond, Kyoto Bamboo, Bruges Canal, Scottish Highlands Loch, Cradle Mountain Dove Lake, Provence Lavender); 5-question FAQ mirrored in FAQPage JSON-LD; WebPage + ItemList + BreadcrumbList JSON-LD.
- Internal links: buy.html note, night-windows.html, guide-print-sizes.html, and Bedroom paragraphs on lake/mountain/asian/european hubs (builders updated so re-runs keep the link). llms.txt Buying help + Shop counts corrected (coastal 18, asian 13 + Sigiriya, european 16 + Colmar). asian/european/coastal builders now keep llms counts in step on re-run. sitemap + lastmod 16 Oct.
- Checks: JSON-LD parses; sitemap parses; no banned words; no broken relative links among hubs; all six `build_collection_*.py --check` up to date; `apply_stripe_links.py --check` 75/75; `apply_mural_links.py --check` 75/75.

### Friday weekly summary (10–16 Oct 2026)
- **Impressions/clicks:** Last known GSC is still 8 Oct (28d: 0 clicks, 4 impressions, avg pos 6.8). GSC was not checked Mon–Fri this week because the signed-in desktop browser is held by the daily Night Windows drop in the 04:45–05:15 London slot. Blocker: need a GSC pass outside that window.
- **Top queries:** Unknown (no GSC pull this week).
- **What shipped this week:**
  - Mon 12 Oct: pieces 51–55; lake-wall-art.html; murals expanded.
  - Tue 13 Oct: coastal-wall-art.html; pieces 56–60 wired into murals/mountain/lakes; poster price $35 confirmed site-wide.
  - Wed 14 Oct: asian-wall-art.html; pieces 61–65 wired into lakes/mountain/coastal/murals.
  - Thu 15 Oct: european-wall-art.html; pieces 66–70 wired; Asian link restored on series hub.
  - Fri 16 Oct: pieces 71–75 live (75 series); collection placement on murals/European/Asian/lakes/mountain; European + Asian cross-links on lake/coastal/mountain/murals hubs; moon-poster-bedroom.html buyer guide; Stripe 75/75 live.
- **Next week priorities:** (1) Signed-in GSC outside the drop window — resubmit sitemap, request indexing for new hubs + pieces 51–75 + bedroom guide, pull 7/28d numbers into the scorecard. (2) Watch which collection hubs earn first impressions and double down. (3) Optional: deepen bedroom guide with room photos or a second buyer guide only if GSC shows demand. (4) Keep white-hat outreach only if Joshua authorises sends for this bot.

### Notes
- A+B were completed by the daily-drop publish (commit `7549422`) before this SEO slot finished; this entry covers the bedroom guide, llms count fix and Friday summary only.
- Digital wallpapers are still not live; murals remain the physical wallpaper product. Prices: poster $35, framed $69, mural $149.

### Next
- Signed-in GSC outside 04:45–05:15 London.
- No further collection page planned until impression data exists.

## 2026-10-19 ~05:30 London — Daily drop 76–80 + new waterfall wall art collection page
### Data review
- Stripe: no Night Windows sales. No charges since 16 Oct 00:00 London (live Joshua Israel Ventures LLC account, read-only check). The only checkout sessions since then are Tax Deed Pack ones on 18 Oct: three unpaid/expired and one internal $0 QA test (100% promo code, joshuaofisrael@gmail.com); none are Moonlit Windows.
- GSC: not checked (drop window; no browser runs in this routine).
- News post: none.

### Opportunity chosen (and why)
1. **Collection placement for the five new pieces** (lakes, mountain, European, murals), as on prior drops.
2. **New `waterfall-wall-art.html` collection.** With Skógafoss and Havasu Falls the series has nine waterfall pieces (Skógafoss, Kirkjufellsfoss, Múlafossur/Gásadalur, Plitvice, Staubbach/Lauterbrunnen, Iguazu, Havasu, Victoria Falls, Moonlit Waterfall). Waterfall wall art / waterfall poster is a distinct buyer query that until now only had a sub-section of lake-wall-art.html; waterfalls are also the owner’s favourite theme and the strongest Instagram content, so a dedicated landing page gives that traffic somewhere to convert. Unique copy (regional groups, room guide, moonlight/moonbow FAQ), not a thin duplicate: lake-wall-art.html keeps its waterfalls group and links to the new page.

### Shipped
- Pieces 76–80 (Skógafoss Waterfall Moon, Moraine Lake Moon, Hohenzollern Castle Moon, Havasu Falls Moon, Ponte Vecchio Florence Moon): piece pages with a new “Where it fits” room note, buy cards, home cards, hub (80 pieces), sitemap image entries, related links both ways, next chain Cradle Mountain → 76 → … → 80 → First window. Stripe poster $35 / framed $69 / mural $149 links live (80/80).
- Collections: lakes (Moraine Lake; Skógafoss + Havasu in waterfalls; FAQ), mountain (Moraine Lake + room guide), European (Hohenzollern in castles, Ponte Vecchio in old towns; FAQ), murals (all five are 2:3: Skógafoss, Havasu, Moraine Lake in lakes-waterfalls; Hohenzollern, Ponte Vecchio in castles and landmarks).
- `waterfall-wall-art.html` via new `scripts/build_collection_waterfalls.py`: CollectionPage + ItemList + BreadcrumbList + FAQPage JSON-LD, 9 cards with live poster/framed/mural Stripe buttons, piece-page collection notes on all nine, links from buy.html theme row, series hub, lake-wall-art.html (waterfalls intro + footer), llms.txt, sitemap.
- Checks: all seven `build_collection_*.py --check` up to date, `publish_pieces_76_80.py --check` 0 issues (re-run idempotent); live: 5 piece pages 200 on moonlitwindows.com and github.io with 3 buy.stripe.com links each, all 15 payment links 200; IndexNow 200 (23 URLs + 6 collection/sitemap URLs), `apply_stripe_links.py --check` 80/80, `apply_mural_links.py --check` 80/80, sitemap parses, JSON-LD parses on 100 pages, 0 broken relative links.
- Instagram candidate queued (not posted): Skógafoss Waterfall Moon (runner-up Havasu Falls Moon).

### Next
- Signed-in GSC outside 04:45–05:15 London: submit sitemap, request indexing for /waterfall-wall-art.html, pieces 76–80 and the earlier backlog (51–75, hubs, bedroom guide).
- Watch whether waterfall-wall-art.html or lake-wall-art.html earns the waterfall impressions; if they compete, narrow the lake page title to lakes.

## 2026-10-19 ~05:20 London — Scheduled SEO run: snippet-length meta descriptions on all 80 piece pages
### Data review
- Stripe: no Night Windows sales. No charges since 16 Oct 05:00 London (live Joshua Israel Ventures LLC account, read-only). The only checkout sessions are Tax Deed Pack ones on 18 Oct (unpaid/expired plus an internal $0 QA test); none are Moonlit Windows.
- GSC: not checked. The browser lock was held by the daily drop for the whole slot (since 04:50), the fifth weekday in a row this has blocked the GSC pass. Last numbers still 8 Oct (28d: 0 clicks, 4 impressions, avg pos 6.8).
- Cloudflare Web Analytics: no moonlitwindows.com rows yet for 17–18 Oct (beacon only went live 18 Oct 09:42).
- News post: none (nothing genuinely relevant for the niche). Outreach: none (not authorised for this routine).

### Opportunity chosen (and why)
On-page audit of every page: no duplicate titles or descriptions, one H1 each, canonical/OG/Twitter in place, but every piece page's meta description ran ~235–245 characters and opened with the same 175-character boilerplate ("Moon poster wall art: buy X as a 12×18 art print poster ($35) or framed print ($69), shipping included, or a $149 peel and stick wall mural (removable wallpaper)."). Google cuts snippets at ~155–160 characters, so the part that makes each piece unique (the place and scene) never showed in results, and the repeated opener read as boilerplate across 80 pages. With almost no impressions yet, indexing is the real bottleneck, but this is the highest-value change that does not need the browser, and it improves CTR on every piece page as impressions arrive.

### Shipped
- New `scripts/seo_piece_snippets.py` (idempotent, `--check`): rewrites `<meta name="description">` on every fully-live piece page to `<Title> [moon ]poster $35, framed print $69, wall mural $149, shipping included. <scene clause>`, ≤158 characters, trimmed at a clause boundary (62 of 80 end on a full stop, 18 on an ellipsis). OG/Twitter descriptions unchanged. Example: "Kirkjufell Waterfall Moon poster $35, framed print $69, wall mural $149, shipping included. Kirkjufellsfoss pours silky white over mossy rocks."
- `publish_pieces_76_80.py` `meta_description()` now calls the same builder, so the next publish script (copied from it) emits the short format for new pieces.
- 80 piece pages updated, commit `8260a5c`, live 05:12 London; IndexNow 200 for 80 piece URLs.
- Checks: `seo_piece_snippets.py --check` 0 to change, `publish_pieces_76_80.py --check` 0 issues, `apply_stripe_links.py --check` 80/80, `apply_mural_links.py --check` 80/80 (new text contains "mural", so it is not re-expanded), all seven `build_collection_*.py --check` up to date.

### Next
- GSC still needs a browser pass outside the drop window (submit sitemap, request indexing for waterfall-wall-art.html, pieces 51–80, hubs, bedroom guide; pull 7/28d numbers).
- Collection hub descriptions are also 237–270 characters; shorten them in the builders (keep the place-name tails the publish scripts maintain) on a non-drop day.
- Piece titles run 70–86 characters; consider dropping the "| Moonlit Windows" suffix on piece pages once GSC shows which title words earn impressions.

## 2026-10-20 ~05:00 London — Scheduled SEO run: branded 404 page
### Data review
- Stripe: no Night Windows sales. No checkout sessions and no charges since 19 Oct 05:00 London (live Joshua Israel Ventures LLC account, read-only).
- GSC: not checked. The browser lock is held by the daily drop (since 04:47), so no browser work in this slot. The Sunday 12:47 London Search Console routine is the planned fix for this; it has not run yet. Last numbers still 8 Oct (28d: 0 clicks, 4 impressions, avg pos 6.8).
- News post: none (nothing genuinely relevant). Outreach: none (not authorised for this routine).
- The drop (pieces 81+, Seljalandsfoss first) was mid-edit in the collection builders and `build_categories.py`, so this run stayed out of those files and the piece pages.

### Opportunity chosen (and why)
Technical audit found the site had no `404.html`. Any mistyped, shared-wrong or old URL (for example an Instagram caption link with a typo, or a piece slug guessed from a place name) showed GitHub's plain "Page not found · GitHub Pages" page: off-brand, no navigation and a dead end for a buyer. A branded 404 keeps those visitors on the shop, gives crawlers links back into the collections, and the GA4 tag on it lets us spot broken inbound links by the "Page not found" title. It is a new file, so it could ship without touching anything the drop was editing.

### Shipped
- `404.html` (commit `1fa4950`, live 05:01 London): `noindex, follow`, no canonical, not in the sitemap; absolute paths so it renders at any depth; full Categories nav and footer; search box that submits to `/browse.html?q=` (browse already reads `q`); a small script that turns the bad path into search words and suggests up to six matching pieces from `/products.json` (tested: `/pieces/skogafoss-waterfall.html` suggests Skógafoss Waterfall Moon first, `/lake-bled.htm` suggests Lake Bled Island Moon first); ten popular collection links; GA4 + Cloudflare beacon.
- Checks: live `https://moonlitwindows.com/pieces/skogafoss-waterfall.html` and `/xyz-nope` both return HTTP 404 with the branded page; all internal links on the page resolve; no AI/ChatGPT/Higgsfield/github.io in copy; `apply_stripe_links.py --check` 80/80.

### Next
- GSC still needs a signed-in browser pass outside the drop window (sitemap, request indexing for waterfall-wall-art.html, browse.html + the 15 category pages, pieces 51–85, bedroom guide; pull 7/28d numbers).
- Shorten collection hub meta descriptions (237–270 characters) in the builders once the drop is not editing them.
