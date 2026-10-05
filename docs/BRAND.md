# Night Shade Art — brand

**Entity:** Joshua Israel Ventures LLC  
**Instagram:** [@moonnightshadeart](https://www.instagram.com/moonnightshadeart/)  
**Series:** Night Windows (sold via Prompt Framed gallery)

## Mark

- Crescent moon + **NIGHT SHADE** / **ART** on midnight navy
- Files: `assets/brand/night-shade-art-logo-mark.png`, `assets/brand/night-shade-art-avatar-1080.png`
- Instagram profile avatar: `instagram-kit/profile-avatar-brand-1080.jpg`

## Watermark policy (owner rule)

- **Advertised** (website, og/twitter, Instagram, ads, public previews): always watermarked with the Night Shade Art corner mark (`assets/brand/watermark-corner.png`, 72% opacity, 42% of the image width, 3.5% padding). `scripts/watermark_for_social.py` writes `assets/NN-*.jpg`, `assets/night-windows-contact-sheet.jpg` (every panel), and `gallery/social/*.jpg`. Publish scripts call the same exporter and must not save a clean JPEG into `assets/`.
- **Paid deliverables** (print fulfillment, POD uploads, customer files): clean masters only. The script byte-copies `gallery/NN-*.png` to `gallery/print-masters/` and never composites the logo onto a PNG. Those PNGs are gitignored so GitHub Pages does not serve them. Fulfillment uses the local files, not the website.


## Voice

Public captions stay cinematic. No AI/ChatGPT jargon on Instagram. CTA: want a poster / buy at the link.
