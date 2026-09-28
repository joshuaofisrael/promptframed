# Prompt Framed

Night Windows, a static gallery for Joshua Israel Ventures LLC.

**Live:** https://joshuaofisrael.github.io/promptframed/

GitHub Pages already serves `main` from the repository root. There is no paid host. This site does not charge a card. Buy Poster opens a Printful link only after a real product URL is saved in `products.json`.

## WAKE UP

Full morning notes: `docs/WAKE_UP.md`. Domain DNS: `docs/DOMAIN_HANDOFF.md`. Printful clicks: `docs/PRINTFUL_SETUP.md`.

When you sit down, these are yours. The gallery, including Photos 1–10, is already on the live URL.

### 1. Buy the domain

Namecheap or Cloudflare Registrar. Not Porkbun. Do not buy a name you have not checked.

1. promptframed.com
2. framedprompt.com
3. aicanvasprints.com

Then follow `docs/DOMAIN_HANDOFF.md`:

- CNAME `www` → `joshuaofisrael.github.io`
- Apex: ALIAS/ANAME to `joshuaofisrael.github.io`, or all four A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- Optional AAAA: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
- On Cloudflare, leave the proxy grey (DNS only) until GitHub issues the certificate
- Repo **Settings → Pages → Custom domain** → save → **Enforce HTTPS**
- Pages is already set to deploy from branch `main` / root. A root `CNAME` file is how that mode remembers the domain. Put only the domain in the file, for example `promptframed.com`, after you own it.

After the domain answers, replace `https://joshuaofisrael.github.io/promptframed` in canonical tags, Open Graph tags, `sitemap.xml`, `robots.txt`, and the Instagram captions.

### 2. Instagram, if the captcha is still open

The footer says `@promptframed (pending)` and does not link out, so we never send people to someone else’s account.

1. Finish signup at Instagram. The overnight note is in `docs/WAKE_UP.md` section 5. Do not commit a password file.
2. Bio link, until the custom domain works: `https://joshuaofisrael.github.io/promptframed/`
3. For a post, open the piece page and press **Copy caption**. Every caption ends with:

```
Want a poster? Buy at the link:
https://joshuaofisrael.github.io/promptframed/pieces/moonlit-alpine-meadow.html
```

Use the URL of the picture you posted. Photo 2 is `pieces/moonlit-mediterranean-village.html`.

### 3. Printful Quick Store, when you want money to move

Do this when you are ready. Nothing is charged today. `posterUrl` and `framedUrl` in `products.json` are `null`, so Buy Poster stays on this site.

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
4. Add a card on `index.html` and `buy.html`, a page at `pieces/short-name.html` (copy a neighbor), and a line in `sitemap.xml`.
5. Push to `main`. Pages republishes from that branch.

Keep piece titles in the Night Windows voice. The AI disclosure stays in the footer and on About.

## Pages

Live source: **Settings → Pages → Deploy from a branch → `main` → `/ (root)`**. That is already on. `.nojekyll` is in the root so Jekyll does not rewrite the HTML.

If the URL 404s, open https://github.com/joshuaofisrael/promptframed/settings/pages and confirm that source. Do not switch to GitHub Actions unless you also remove the branch source. One source only.

## Map

| Path | Page |
| --- | --- |
| `/` | Night Windows gallery, Photos 1–10 |
| `/pieces/moonlit-alpine-meadow.html` | Photo 1, Buy Poster, caption |
| `/pieces/moonlit-mediterranean-village.html` | Photo 2 |
| `/buy.html` | All ten, poster and framed buttons |
| `/about.html` | Studio and AI disclosure |
| `/how-it-works.html` | Gallery → Instagram → poster shipped |
| `/contact.html` | Email the studio |
| `/how-to-turn-chatgpt-art-into-a-framed-poster.html` | Evergreen poster guide |
| `products.json` | Printful URLs per slug |
| `docs/WAKE_UP.md` | Morning checklist |
