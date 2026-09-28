# Prompt Framed

Night Windows, a static art gallery for Joshua Israel Ventures LLC.

Live site: https://joshuaofisrael.github.io/promptframed/

The gallery is HTML, CSS, and a little JavaScript. GitHub Pages serves it. There is no paid host and no card checkout on this site. Buy Poster opens a Printful link only after you paste a real product URL.

## WAKE UP

When you sit down, only two things are yours. Everything else is already on the site.

### 1. Buy the domain

Do this at **Namecheap** or **Cloudflare Registrar**. Do not use Porkbun.

Try these names in order:

1. promptframed.com
2. framedprompt.com
3. aicanvasprints.com

Leave the site on `joshuaofisrael.github.io/promptframed` until the name is actually yours. Do not add a domain you do not own.

#### Point DNS at GitHub Pages

GitHub’s Pages addresses:

| Type | Host | Value |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |
| CNAME | `www` | `joshuaofisrael.github.io` |

**Namecheap:** Domain List → Manage → Advanced DNS. Add the records above. Delete any parking or URL-redirect record that fights them.

**Cloudflare:** Add the same records. Leave the proxy **off** (grey cloud, DNS only) until GitHub has issued the certificate. An orange cloud in front of Pages often blocks that step.

Then, in this repo:

1. Open **Settings → Pages → Custom domain**.
2. Enter the apex domain you bought, for example `promptframed.com`. Save.
3. Wait until DNS checks out. GitHub will offer **Enforce HTTPS**. Turn it on.
4. This site publishes with GitHub Actions. For an Actions site, the custom domain is stored in Pages settings. A `CNAME` file in the repo is not required and is ignored by the Actions publish. If you ever switch Pages to “Deploy from a branch”, add a `CNAME` file containing only the domain so the next deploy does not drop it.

After the domain answers, search the repo for `https://joshuaofisrael.github.io/promptframed` and replace it in page canonical tags, Open Graph tags, `robots.txt`, `sitemap.xml`, and the Instagram caption on the piece page. The github.io address can stay as a second door; the caption should use the domain you want people to buy from.

### 2. Instagram, if it is not finished

The footer handle is `@placeholder` until you change it. It is not a link, on purpose, so we never send people to someone else’s account.

1. Finish the Instagram account.
2. In `data/products.json`, set `instagram.handle` to the real handle and `instagram.url` to `https://instagram.com/yourhandle`.
3. Push to `main`. The footer links itself.

Caption to paste under a post (also on the piece page, with a copy button):

```
Moonlit Alpine Meadow

Wildflowers in the dark, a village still awake, the moon on the peaks.

Want a poster? Buy at the link:
https://joshuaofisrael.github.io/promptframed/art/moonlit-alpine-meadow/
```

The link opens the piece page. The gold **Buy Poster** button on that page is the shop.

### Printful Quick Store, when you want money to move

Do this when you are ready. The site is already shaped for it. **Buy Poster does not charge anyone today.** The URL in `data/products.json` is empty, so the button stays on the page and explains that.

Printful Quick Stores are a free storefront. As of this writing they are available to US merchants, and products ship to US addresses only. Confirm that in your Printful dashboard before you promise shipping farther out.

1. Create a Printful account at https://www.printful.com.
2. Dashboard → **Stores → Quick Stores → Create store now**.
3. Name it Prompt Framed. The store web address cannot be renamed later.
4. Add a **poster**. Upload the print master `gallery/01-moonlit-alpine-meadow.png` (1024×1536). That size is honest for a smaller poster, about 7×10 inches at 150 dpi. For a large poster, export a higher-resolution file first so the print is not soft.
5. Set your price. Publish.
6. Add a **framed print** of the same picture as the second product. Publish that too.
7. Copy the public store link from the Stores section. If Printful gives you a direct product link, use that instead.
8. Paste it into `data/products.json`:
   - `pieces["moonlit-alpine-meadow"].poster.url` → poster or store link
   - `pieces["moonlit-alpine-meadow"].framed_print.url` → framed product link
9. Commit and push to `main`.

Use a real `https://` link. Leave the string empty until the product is public. Values that look like placeholders are ignored. This website never asks for a card number.

### Photo 2

Photo 1, Moonlit Alpine Meadow, is hanging. **Photo 2 was not in this repo and no file was attached**, so it was not invented. Drop the real file in and follow “Add a picture” below.

## Add a picture

1. Save the print master as `gallery/NN-short-name.png`.
2. Make a display copy in `gallery/web/NN-short-name.jpg` and `.webp` (the page should not ship the multi-megabyte PNG to phones).
3. Add an entry to `gallery/catalog.json`.
4. Add a slug under `pieces` in `data/products.json` with empty `poster.url` and `framed_print.url`.
5. Copy `art/moonlit-alpine-meadow/index.html` to `art/your-slug/index.html`. Change the title, description, image paths, canonical URL, caption, and `data-buy` slug. Keep the caption ending `Want a poster? Buy at the link:` plus the page URL.
6. Add a card on `index.html`.
7. Add the new URL to `sitemap.xml`.
8. Push to `main`.

Marketing pages stay in the Night Windows voice. The AI disclosure stays in the footer and on About. Do not put “ChatGPT” in a piece title or a buy button.

## GitHub Pages

The site is the root of `main`: `index.html`, page folders, `css/`, `js/`, `gallery/`, `robots.txt`, and `sitemap.xml`. `.nojekyll` stops Jekyll from touching the files.

Publish path: `.github/workflows/pages.yml` runs on every push to `main` and deploys with GitHub Actions.

One-time setting, if the site is not already on github.io:

1. Open https://github.com/joshuaofisrael/promptframed/settings/pages
2. **Build and deployment → Source → GitHub Actions**
3. Save. The workflow **Deploy GitHub Pages** publishes https://joshuaofisrael.github.io/promptframed/

If Actions is unavailable, use the branch fallback instead: Source → **Deploy from a branch** → Branch `main` → Folder `/ (root)` → Save. Use one source, not both.

## Contact address

The public studio address on the contact page is `joshuaofisrael@gmail.com`. Change it in `contact/index.html` if you want a different inbox.

## Map

| Path | Page |
| --- | --- |
| `/` | Gallery |
| `/art/moonlit-alpine-meadow/` | Photo 1, buy buttons, Instagram caption |
| `/about/` | Studio and AI disclosure |
| `/how-it-works/` | Gallery → Instagram → poster shipped |
| `/contact/` | Email the studio |
| `/guides/how-to-turn-chatgpt-art-into-a-framed-poster/` | Evergreen poster guide |
| `data/products.json` | Printful URLs and Instagram handle |
| `gallery/catalog.json` | Piece metadata |
