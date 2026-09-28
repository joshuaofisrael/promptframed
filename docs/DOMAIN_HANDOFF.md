# Domain → GitHub Pages handoff (Prompt Framed)

**Live custom domain:** https://moonlitwindows.com  
**Registered:** Namecheap, 28 Sep 2026 (Joshua)  
**Pages host:** `joshuaofisrael.github.io`  
**Project site path on github.io:** `/promptframed/`  
**Fallback URL:** https://joshuaofisrael.github.io/promptframed/  
**Repo:** https://github.com/joshuaofisrael/promptframed  
**Repo `CNAME`:** root file, one line, `moonlitwindows.com`

The preferred public URL is **https://moonlitwindows.com**. Canonicals, Open Graph, `sitemap.xml`, `robots.txt`, and Instagram captions already use that host. Relative asset and page paths are unchanged.

A custom domain on a GitHub Pages project site serves this repo from the domain root. Piece URLs are `https://moonlitwindows.com/pieces/SLUG.html` (no `/promptframed/` prefix). Once GitHub verifies DNS, https://joshuaofisrael.github.io/promptframed/ redirects to https://moonlitwindows.com/.

DNS A/CNAME records at Namecheap are a separate coordinator step. This file does not change the registrar.

---

## DNS records (Namecheap)

Point the apex and `www` at GitHub Pages. Do not create a conflicting A or CNAME that points elsewhere.

| Type | Name / Host | Value / Target | TTL |
|---|---|---|---|
| **A** | `@` | `185.199.108.153` | Automatic |
| **A** | `@` | `185.199.109.153` | Automatic |
| **A** | `@` | `185.199.110.153` | Automatic |
| **A** | `@` | `185.199.111.153` | Automatic |
| **CNAME** | `www` | `joshuaofisrael.github.io` | Automatic |

Namecheap has no ALIAS/ANAME on a typical domain, so the apex uses all four A records. The `www` host is a DNS CNAME. The Pages custom-domain hostname stays the apex (`moonlitwindows.com`), which is what the repo `CNAME` file contains.

Optional IPv6 **AAAA** on `@` (all four):

```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

### GitHub Pages custom domain

1. The root `CNAME` file is already `moonlitwindows.com`. That is how branch publishing (`main` / `/`) remembers the domain.
2. Repo → **Settings → Pages** should show custom domain `moonlitwindows.com`.
3. Check **Enforce HTTPS** after the certificate provisions (minutes to about an hour after DNS answers). Leave it off while the certificate is pending.
4. Confirm:
   - https://moonlitwindows.com serves the gallery
   - https://www.moonlitwindows.com reaches the same site
   - https://joshuaofisrael.github.io/promptframed/ redirects to https://moonlitwindows.com/

### After DNS is live

1. Instagram bio for **@nightshadeart** (Night Shade Art): `https://moonlitwindows.com/`
2. Submit `https://moonlitwindows.com/sitemap.xml` in Google Search Console (see `docs/SEO_SCORECARD.md`)
3. Add Cloudflare Web Analytics (owner rule) and append daily views to `JI_Ventures_Traffic.xlsx`
4. Do not invent Printful product URLs. Buy buttons stay on-site until a real product URL is pasted into `products.json`.

### Troubleshooting

- **Not resolving:** wait for DNS TTL; check that `@` answers with the four GitHub A records and `www` is a CNAME to `joshuaofisrael.github.io`
- **404 on the custom domain:** Pages source must stay branch `main`, folder `/ (root)`, on this repo
- **HTTPS pending:** leave Enforce HTTPS off until the cert is ready, then enable it
- **Wrong site:** the custom domain must be set on **this** repo’s Pages settings
- **Broken images after the domain works:** page and asset links in HTML are relative (`./`, `../`). Do not prefix them with `/promptframed/`

---

## Reminder

Hosting stays **free GitHub Pages only**. No paid Vercel unless Joshua asks. The domain is already registered. Do not buy a second name. Printful product costs happen only when Joshua publishes products.
