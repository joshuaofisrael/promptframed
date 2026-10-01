# Prompt Framed

Night Windows, a static gallery for Joshua Israel Ventures LLC.

**Live:** https://moonlitwindows.com/
**Custom domain:** moonlitwindows.com is live on GitHub Pages (custom domain + HTTPS, enabled 1 Oct 2026). https://joshuaofisrael.github.io/promptframed/ redirects there.

## Night Windows marketing

Source: `docs/MARKETING_NIGHT_WINDOWS.md`.

Prompt Framed presents **Night Windows**, a series of dreamy moonlit landscape posters. The hook: each piece is a window into somewhere you wish you were. The public site says “Windows into places you wish you were.”

Every Instagram post uses the same close:

```
Want a poster? Buy at the link:
https://moonlitwindows.com/pieces/SLUG.html
```

Or, in a bio: poster link in bio. Suggested bio: `Night Windows · AI landscapes as posters · Link buys the print`. Keep “AI” and “ChatGPT” out of captions and out of the site hero. The disclosure stays in the footer and on About. The style prompt stays internal.

Drop formats: one window (art, short mood, CTA); which window tonight (two or three pieces, then the buy link); detail crop into a full reveal; room mockup; day/night twins when they exist. Cadence: 3–5 posts a week inside this series before a new style line.

The contact sheet (`gallery/night-windows-contact-sheet.png`, shown on `/night-windows.html`) is the series reference. Photos 1 and 2 were specified first. The other eight windows are already individual pages because the files were in the gallery. Buy links still come from `products.json` and do not charge anyone until a real Printful URL is pasted in.

GitHub Pages already serves `main` from the repository root. There is no paid host. This site does not charge a card. Buy Poster opens a Printful link only after a real product URL is saved in `products.json`.

## WAKE UP

Full morning notes: `docs/WAKE_UP.md`. Domain DNS: `docs/DOMAIN_HANDOFF.md`. Printful clicks: `docs/PRINTFUL_SETUP.md`.

When you sit down, these are yours. The gallery, including Photos 1–10, is already on the live URL.

### 1. Hosting

GitHub Pages serves `main` from the repository root at https://moonlitwindows.com/. The custom domain `moonlitwindows.com` is set in Pages settings and in the root `CNAME` file; HTTPS is enforced. The site uses relative asset paths, so it works at the domain root.

### 2. Instagram

The Instagram account is **[@moonnightshadeart](https://www.instagram.com/moonnightshadeart/)** for **Night Shade Art**.

1. Bio link: `https://moonlitwindows.com/buy.html`
2. For a post, open the piece page and press **Copy caption**. Every caption ends with:

```
Want a poster? Buy at the link:
https://moonlitwindows.com/pieces/moonlit-alpine-meadow.html
```

Use the URL of the picture you posted. Photo 2 is `pieces/moonlit-mediterranean-village.html`.

### 3. Printful Quick Store, when you want money to move

**Superseded:** checkout now runs on Stripe Payment Links (see `docs/STRIPE_SITE_CHECKOUT.md`). The Printful notes below are kept for fulfilment reference only.

Quick Stores, as documented in `docs/PRINTFUL_SETUP.md`, are for US merchants shipping to US addresses. Confirm that in the dashboard before promising other countries.

1. Sign in at https://www.printful.com with the studio account.
2. **Stores → Add store → Quick Stores.** Name it Prompt Framed. The store address cannot be casually renamed, so choose the slug on purpose.
3. Add a poster for each picture you want to sell. Upload the print master in `gallery/` (the PNG, not the smaller JPEG in `assets/`). Photos 1 and 2 are 1024×1536, about a 7×10 inch print at 150 dpi. Use a higher-resolution file before you sell a large poster.
4. Add a framed print of the same picture as the second product. Publish.
5. Copy the public product URL.
6. Paste it into `products.json` for that slug: `printful.posterUrl` and `printful.framedUrl`.
7. Push to `main`.

Use a real `https://` link. Leave the value `null` until the product is public. This website never asks for a card number.

## Add a picture

1. Save the print master as `gallery/NN-short-name.png`.
2. Save a display JPEG as `assets/NN-short-name.jpg`.
3. Add the piece to `gallery/catalog.json` and `products.json` (`posterUrl` and `framedUrl` null).
4. Add a card on `index.html`, a page at `pieces/short-name.html` (copy a neighbor), and a line in `sitemap.xml`.
5. Create its Stripe Products, Prices and Payment Links (poster $29 + framed $69) following `scripts/create_stripe_links.md`, paste the URLs into `products.json`, then run `python3 scripts/apply_stripe_links.py` (writes the buy buttons into `buy.html` and the piece page). See `docs/STRIPE_SITE_CHECKOUT.md`.
6. Push to `main`. Pages republishes from that branch.

Keep piece titles in the Night Windows voice. The AI disclosure stays in the footer and on About.

## Pages

Live source: **Settings → Pages → Deploy from a branch → `main` → `/ (root)`**. That is already on. `.nojekyll` is in the root so Jekyll does not rewrite the HTML.

If the URL 404s, open https://github.com/joshuaofisrael/promptframed/settings/pages and confirm that source. Do not switch to GitHub Actions unless you also remove the branch source. One source only.

## Map

| Path | Page |
| --- | --- |
| `/` | Night Windows gallery |
| `/night-windows.html` | Series page and contact sheet |
| `/pieces/moonlit-alpine-meadow.html` | Photo 1, Buy Poster, caption |
| `/pieces/moonlit-mediterranean-village.html` | Photo 2 |
| `/buy.html` | All ten, poster and framed buttons |
| `/about.html` | Studio and AI disclosure |
| `/how-it-works.html` | Gallery → Instagram → poster shipped |
| `/contact.html` | Email the studio |
| `/how-to-turn-chatgpt-art-into-a-framed-poster.html` | Evergreen poster guide |
| `products.json` | Printful URLs per slug |
| `docs/WAKE_UP.md` | Morning checklist |
