# Domain → GitHub Pages handoff (Prompt Framed)

**Pages host:** `joshuaofisrael.github.io`  
**Project site path:** `/promptframed/`  
**Default URL until custom domain:** https://joshuaofisrael.github.io/promptframed/  
**Repo:** https://github.com/joshuaofisrael/promptframed  
**Registrars allowed:** Namecheap or Cloudflare Registrar (**not** Porkbun)

---

## After you buy the domain

Pick one: `promptframed.com` | `framedprompt.com` | `aicanvasprints.com`

### A. DNS records (at the registrar or Cloudflare DNS)

Point the apex and `www` at GitHub Pages:

| Type | Name / Host | Value / Target | TTL |
|---|---|---|---|
| **CNAME** | `www` | `joshuaofisrael.github.io` | Auto / 300 |
| **ALIAS / ANAME** (preferred for apex) **or** A records | `@` (apex) | See A-record IPs below if no ALIAS | Auto / 300 |

GitHub Pages apex **A** records (use all four if your registrar has no ALIAS/ANAME):

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Optional IPv6 **AAAA** (all four):

```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

**Cloudflare Registrar tip:** if the domain is on Cloudflare DNS, you can use a CNAME flattening / ALIAS-style apex to `joshuaofisrael.github.io`, or the A/AAAA set above. Proxy status can be DNS-only (grey cloud) until HTTPS is confirmed; orange-cloud proxy is fine later with Cloudflare Full SSL once GitHub has issued the cert.

Do **not** create a conflicting A/CNAME that points elsewhere.

### B. GitHub Pages custom domain

1. Repo → **Settings → Pages**
2. Under **Custom domain**, enter the bare domain (e.g. `promptframed.com`) → **Save**
3. GitHub will usually commit a `CNAME` file at the repo root containing that hostname. If not, add a root file named `CNAME` (no extension) with a single line:

```
promptframed.com
```

(replace with the domain you bought)

4. Check **Enforce HTTPS** after the certificate provisions (can take a few minutes to an hour).
5. Confirm:
   - http://www.YOURDOMAIN.com → redirects / serves the site
   - https://YOURDOMAIN.com serves the gallery
   - Project path `/promptframed/` may still work on github.io; custom domain typically serves from the Pages root for that site — verify both and fix internal links if needed

### C. After DNS is live

1. Update Instagram bio link from github.io → `https://YOURDOMAIN.com`
2. Update canonical URLs / Open Graph on the site
3. Add Cloudflare Web Analytics (owner rule) and append daily views to `JI_Ventures_Traffic.xlsx`
4. Submit sitemap to Google Search Console when ready (see `docs/SEO_SCORECARD.md`)

### D. Troubleshooting

- **Not resolving:** wait for DNS TTL; check dig/nslookup for `www` CNAME → `joshuaofisrael.github.io`
- **404 on custom domain:** Pages source branch/folder wrong, or site files not on `main`
- **HTTPS pending:** leave Enforce HTTPS off until cert is ready, then enable
- **Wrong site:** confirm the custom domain is set on **this** repo’s Pages settings, not another

---

## Reminder

Hosting stays **free GitHub Pages only**. No paid Vercel unless Joshua asks. Domain purchase is the only paid infra step for launch (plus Printful product costs when you publish).
