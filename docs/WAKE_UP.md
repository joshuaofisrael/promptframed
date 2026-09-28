**Instagram:** Night Shade Art on Instagram (handle TBD)

# Wake-up checklist — Prompt Framed
**Prepared:** 28 Sep 2026 ~02:50 BST (while Joshua slept)  
**Domain update:** 28 Sep 2026 — GitHub Pages is live; the custom domain remains disabled.

Owner email for all accounts: **joshofisrael@yahoo.com** (retain access).

## Domain status

Joshua registered **moonlitwindows.com** on Namecheap on 28 Sep 2026. Current gallery URL: **https://joshuaofisrael.github.io/promptframed/**

- Root `CNAME` file: absent (custom domain intentionally disabled)
- Canonicals, Open Graph, sitemap, robots.txt, and Instagram captions use `https://joshuaofisrael.github.io/promptframed/`
- Instagram: **Night Shade Art (handle TBD)**. Bio link: `https://joshuaofisrael.github.io/promptframed/buy.html`
- GitHub Pages live URL: https://joshuaofisrael.github.io/promptframed/
- Namecheap DNS (apex A records and `www` CNAME) is the coordinator’s step. Values are in `docs/DOMAIN_HANDOFF.md`. Do not buy another domain.

---

## 1. What’s done overnight

| Item | Status |
|---|---|
| Repo seeded | Done — https://github.com/joshuaofisrael/promptframed |
| Gallery assets (local) | Photo 1 + 2 + Night Windows contact sheet in `/workspace/promptframed/gallery/` |
| Docs | BUSINESS_PLAN, MARKETING_NIGHT_WINDOWS, PRINTFUL_SETUP, INSTAGRAM_ACCOUNT, DOMAIN_HANDOFF, SEO_SCORECARD, this file |
| Cloud site-build agent | `bc-0b12b08c-1714-5e8e-be1f-d86cc4e8f3c4` — **no PR appeared**; overnight executor shipped gallery site instead |
| GitHub Pages | **Live** — https://joshuaofisrael.github.io/promptframed/ (HTTP 200) |
| Printful | **Not spent** — click-path ready in §4 (no account created overnight) |
| Instagram | **Incomplete** — captcha blocker; details in §5 |
| Custom domain | **Registered** — moonlitwindows.com on Namecheap, 28 Sep 2026. Preferred URL https://moonlitwindows.com. DNS at Namecheap is the coordinator’s step (`docs/DOMAIN_HANDOFF.md`) |

---

## 2. Live URL / site / PR status

**Live URL:** https://joshuaofisrael.github.io/promptframed/
**Custom domain:** disabled until DNS is ready.

**Cloud agent PR:** none as of wake checklist (agent id `bc-0b12b08c-1714-5e8e-be1f-d86cc4e8f3c4` never opened a PR). Gallery site was shipped directly to `main` overnight.

**GitHub Pages:** already enabled (legacy, `main` `/`). Live URL above is serving. Re-check Settings → Pages only if the URL 404s.

Full DNS/CNAME steps for a custom domain: `docs/DOMAIN_HANDOFF.md`.

---

## 3. Domain (done in the repo)

**Registrar:** Namecheap. **Domain:** moonlitwindows.com, registered by Joshua on 28 Sep 2026. **No second purchase.** No Porkbun.

Repo work is in place:

1. Root `CNAME` is absent; do not re-enable the custom domain yet
2. Public canonicals, Open Graph, sitemap, and Instagram captions use https://joshuaofisrael.github.io/promptframed/
3. DNS at Namecheap is still the coordinator’s step — `docs/DOMAIN_HANDOFF.md` (four apex A records, `www` CNAME → `joshuaofisrael.github.io`)
4. After DNS answers, Settings → Pages → **Enforce HTTPS**
5. Instagram bio once a handle is chosen: `https://joshuaofisrael.github.io/promptframed/buy.html`

---

## 4. Printful Quick Store (you click — $0 until you publish; no overnight spend)

Source of truth: `docs/PRINTFUL_SETUP.md`. Condensed click path:

1. Sign in / create Printful with **joshofisrael@yahoo.com**; business **Joshua Israel Ventures LLC** (US tax/bank as owner).
2. **Stores → Add store → Quick Stores** → name **Prompt Framed** → pick slug → upload logo → expect URL like `https://promptframed.printful.me/`.
3. **My products → Add product**: poster + framed poster; upload Night Windows art (keep 2:3); set frame colours, copy, retail prices, mockups → **Publish**.
4. **Billing → Quick Stores**: Stripe onboarding + W-9 as owner.
5. Preview mobile + shipping; optional sample order before ads.
6. Paste store + product URLs into the site buy buttons / `buy.html` and Instagram bio.

Suggested retail test ranges (your call): 12×18 unframed $34–44; 12×18 framed $79–99; 20×30 framed $129–159; 24×36 framed $179–229 (+ shipping). Upscale art before large framed sizes (current files are 1024×1536).

**Skip Quick Stores** if you need UK/EU shipping → use Gelato + Etsy instead (see PRINTFUL_SETUP.md §1).

---

## 5. Instagram (if still incomplete)

**Status at sleep:** signup form submitted for username **`promptframed`** with **joshofisrael@yahoo.com**. Instagram showed username valid, then blocked on **reCAPTCHA Enterprise** (“Help us confirm it’s you”) — Next disabled until a human completes the captcha. Account is **not** created yet.

**Your clicks:**
1. Open https://www.instagram.com/accounts/emailsignup/ (or continue the open signup session).
2. Complete the captcha → Next → finish signup.
3. Password is recorded in `docs/INSTAGRAM_ACCOUNT.md` (local only; do **not** commit that file to GitHub).
4. Bio: `Night Windows · AI landscapes as posters · Link buys the print`
5. The Instagram handle for this series is TBD. Bio link: `https://joshuaofisrael.github.io/promptframed/buy.html`
6. First posts: Night Windows series. Caption ends with “Want a poster? Buy at the link” plus the piece URL on moonlitwindows.com (see MARKETING_NIGHT_WINDOWS.md). Keep “AI/ChatGPT” out of captions and out of the site hero. Disclosure stays in the footer and on About.

---

## 6. Morning order of operations

1. Check live URL / merge green site PR if not already merged  
2. Confirm GitHub Pages serves the gallery  
3. Coordinator applies Namecheap DNS for moonlitwindows.com (`docs/DOMAIN_HANDOFF.md`)  
4. Choose an Instagram handle, then set the bio link to https://joshuaofisrael.github.io/promptframed/buy.html
5. Create Printful Quick Store + publish first Night Windows products + paste buy URLs into site  

Then you’re live for Instagram → site → Printful checkout.

---

## Overnight run result
_(executor fills this section before sleep ends)_

- Checked at: 28 Sep 2026 ~02:50 BST
- Repo `main`: seed only (`07b0787` — gallery photo 1 + business plan); **no open PR yet** when checklist first written
- Pages: not enabled at first check (`has_pages: false`)
- Follow-up poll / enable / PR merge notes appended below by the overnight executor

### Executor update — 28 Sep 2026 ~02:53 BST

- Cloud agent `bc-0b12b08c-1714-5e8e-be1f-d86cc4e8f3c4`: **no PR / no new commits** after multiple `gh` polls (~10 min). No open or closed PRs on the repo.
- **GitHub Pages enabled** via API: legacy build from `main` `/` → https://joshuaofisrael.github.io/promptframed/
- **Minimal complete gallery site shipped to `main`** by overnight executor so the live URL is not a 404 while waiting on the cloud agent: `index.html`, piece pages, `buy.html`, `about.html`, `styles.css`, web JPEGs in `assets/`, `robots.txt`, `sitemap.xml`.
- If the cloud agent later opens a PR with a fuller design, review & merge when checks are green (prefer improving, not blocking morning domain buy).
- Docs added: `WAKE_UP.md`, `DOMAIN_HANDOFF.md`, `SEO_SCORECARD.md` (Instagram password file stays local-only; not committed).
- **Still for morning (as of ~02:53 BST):** (1) domain buy + DNS, (2) Instagram captcha, (3) Printful Quick Store publish + paste buy URLs.

### Live confirmation — 28 Sep 2026 ~02:54 BST

- https://joshuaofisrael.github.io/promptframed/ → **HTTP 200** (Pages `built`, commit `057a3ae`)
- Piece pages, buy.html, assets, sitemap also serving
- Cloud agent PR: **none** as of this confirmation

### Domain — 28 Sep 2026

- Joshua registered **moonlitwindows.com** on Namecheap.
- Preferred URL is https://moonlitwindows.com (repo `CNAME` plus site canonicals, sitemap, and Instagram captions).
- https://joshuaofisrael.github.io/promptframed/ remains the fallback until Namecheap DNS is verified.
- DNS records at Namecheap are the coordinator’s step (`docs/DOMAIN_HANDOFF.md`). No Printful spend.
