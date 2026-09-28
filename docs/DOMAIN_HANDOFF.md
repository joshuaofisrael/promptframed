# Domain handoff — moonlitwindows.com

**Chosen domain:** `moonlitwindows.com`  
**Registrar:** Namecheap (Joshua)  
**Entity:** Joshua Israel Ventures LLC  
**Pages host:** `joshuaofisrael.github.io` / repo `joshuaofisrael/promptframed`  
**Instagram:** Night Shade Art on Instagram: [@moonnightshadeart](https://www.instagram.com/moonnightshadeart/)

## Temporary live URL (DNS incomplete)

Custom domain was **temporarily removed** from GitHub Pages (and the root `CNAME` file deleted) because Namecheap has **no A records** yet. With the custom domain set, `https://joshuaofisrael.github.io/promptframed/` 301-redirected to a dead `moonlitwindows.com`.

**Live gallery now:** https://joshuaofisrael.github.io/promptframed/  
(Verified HTTP 200 HTML for the homepage.)

Site copy, Open Graph, and Instagram captions temporarily use the github.io base so visitors and shares do not hit a dead host. When DNS works, restore the custom domain and switch public URLs back to `https://moonlitwindows.com/`.

Hosting stays **free GitHub Pages only**. No Porkbun. No paid Vercel unless Joshua asks.

---

## Exact Namecheap DNS steps (still required)

In Namecheap → Domain List → **moonlitwindows.com** → **Advanced DNS**:

| Type | Host | Value | TTL |
|---|---|---|---|
| **A Record** | `@` | `185.199.108.153` | Automatic |
| **A Record** | `@` | `185.199.109.153` | Automatic |
| **A Record** | `@` | `185.199.110.153` | Automatic |
| **A Record** | `@` | `185.199.111.153` | Automatic |
| **CNAME Record** | `www` | `joshuaofisrael.github.io` | Automatic |

Optional IPv6 **AAAA** on `@` (all four):

```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

Remove any conflicting `@` A/CNAME or parking records that do not point at GitHub.

Confirm with:

```bash
dig +short A moonlitwindows.com
# expect the four 185.199.* addresses
dig +short CNAME www.moonlitwindows.com
# expect joshuaofisrael.github.io.
```

---

## Reconnect custom domain on GitHub Pages (after DNS answers)

1. Add a root file named `CNAME` (no extension) with one line:

```
moonlitwindows.com
```

2. Repo → **Settings → Pages** → Custom domain → `moonlitwindows.com` → Save  
   (or let the `CNAME` file reattach the domain on the next Pages build.)
3. Wait for DNS check to pass. Leave **Enforce HTTPS** off until the certificate is ready, then enable it.
4. Confirm:
   - https://moonlitwindows.com serves the gallery
   - https://www.moonlitwindows.com reaches the same site
   - https://joshuaofisrael.github.io/promptframed/ may redirect to the custom domain again
5. Switch site canonicals / OG / Instagram captions / `sitemap.xml` / `robots.txt` back to `https://moonlitwindows.com/` (project path `/promptframed/` is not used on the custom domain root).
6. Instagram bio, once DNS works: `https://moonlitwindows.com/`

### Troubleshooting

- **Not resolving:** wait for TTL; confirm all four apex A records and `www` CNAME
- **404 on custom domain:** Pages source must stay branch `main`, folder `/ (root)`
- **HTTPS pending:** leave Enforce HTTPS off until cert is ready
- **Broken images:** keep HTML asset links relative (`./`, `../`); do not hard-prefix `/promptframed/` for custom-domain serving

---

## Reminder

Do not buy a second domain. Do not invent Stripe or Printful product URLs. Buy buttons stay on-site (`buy.html` anchors) until real Payment Link / shop URLs are pasted into `products.json`.
