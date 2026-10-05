# Print masters

Clean PNGs for post-order fulfillment live in this folder on the fulfillment machine only. They are gitignored (`gallery/print-masters/*.png`) and are not on moonlitwindows.com.

`scripts/watermark_for_social.py` refreshes each file as a byte copy of `gallery/NN-short-name.png`. It never draws the Night Shade Art mark onto these files.

Upload these PNGs to Printful or Gelato. Do not upload `assets/*.jpg` or `gallery/social/*.jpg`.

See `../README.md` for how to restore the files from commit `a91f807` if a pull removes them from disk.
