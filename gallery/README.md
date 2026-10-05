# Gallery files

`catalog.json` and `social/*.jpg` are public. `social/*.jpg` is watermarked and is the image Stripe should fetch.

These stay on the fulfillment machine and are gitignored, so GitHub Pages does not serve them:

- `NN-short-name.png` — clean canonical master
- `print-masters/NN-short-name.png` — clean byte copy for Printful / Gelato upload
- `night-windows-contact-sheet.png` — clean contact-sheet source

`scripts/watermark_for_social.py` reads the canonical PNG, writes watermarked JPEGs to `assets/` and `gallery/social/`, and copies the PNG into `print-masters/` without changing its pixels. It will not write a watermark onto a PNG.

Ship prints from `print-masters/`. Do not download `assets/*.jpg` or `gallery/social/*.jpg` for a customer order.

Keep a second copy of the PNGs somewhere private (a disk or a private repo). This public repo is not that copy.

If a merge deletes the tracked masters from a working tree, restore them from the last commit that still has every piece, including 36–40 (`a91f807`), without republishing:

```
git ls-tree -r --name-only a91f807 gallery \
  | grep -E '(^gallery/[0-9]{2}-.+\.png$|^gallery/print-masters/.+\.png$|^gallery/night-windows-contact-sheet\.png$)' \
  | xargs -r git checkout a91f807 --
```

After that checkout the files match `.gitignore`. Do not `git add -f` them.
