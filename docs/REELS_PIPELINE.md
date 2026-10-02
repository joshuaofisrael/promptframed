# Instagram Reels pipeline (Night Shade Art / Night Windows)

Turns one gallery piece into a 6 s vertical Reel: gentle motion via Higgsfield image-to-video,
background music from our licensed library, Night Shade Art watermark burned in, ready for review.
First test Reel: `gallery/reels/26-banff-lake-louise-moon-reel.mp4` (2026-10-01). Nothing is posted by this pipeline.

## Rules (unchanged)
- Anything public carries the Night Shade Art watermark for the **full** duration. `make_reel.py` burns it into every frame.
- Never publish clean masters or `*-raw.mp4` clips (un-watermarked; gitignored). A private Higgsfield upload as a generation input is OK.
- Public copy and captions never mention AI.

## Model and cost (Higgsfield, checked 2026-10-01)
| Option | Settings | Credits per 6 s Reel |
|---|---|---|
| **Default: Kling v3.0 (`kling3_0`)** | mode `pro`, `sound: on`, 9:16, duration 6, `start_image` | **15** |
| Kling v3.0, no native audio | mode `pro`, `sound: off` (music only) | 10.5 |
| Seedance 2.5 (`seedance_2_5`) | 1080p, audio on | 72 |
| Seedance 2.5 | 720p, audio on | 42 |

- Plan: Higgsfield **Plus**. Balance 1210 before the first test, 1195 after (one 15-credit job).
- At 15 credits per Reel, 1195 credits cover **79 Reels**. At 2 Reels per weekday (about 10 a week, about 43 a month) that is
  about 8 weeks, or about 650 credits a month. Switching to `sound: off` (10.5) covers 113 Reels.
- Kling pro outputs native 1080x1920, 24 fps, with AAC audio. `start_image` keeps the composition faithful.
- Free-trial "unlim" generations were **not** available on this account (`models_explore` reported `unlim.available: false`). Pay with credits.
  Do not pass `use_unlim` unless the server returns `unlim_choice`. Never buy credits or start trials from the routine.

## Steps
1. **Balance and preflight:** call Higgsfield `balance`, then `generate_video` with the params below plus `get_cost: true` (should be 15).
2. **Make the 9:16 input** (private, written to /tmp only):
   `python3 scripts/prep_reel_source.py 26-banff-lake-louise-moon --x-offset 60`
   This centre-crops 2:3 masters to 9:16 by default. Use `--x-offset` to keep key subjects (moon, dock) inside the frame.
3. **Upload:** `media_upload` (filename `<piece>-9x16.png`), run the returned `curl -X PUT ...` and expect HTTP 200, then `media_confirm` with type `image`.
4. **Generate:**
   ```json
   {"model":"kling3_0","mode":"pro","sound":"on","aspect_ratio":"9:16","duration":6,
    "medias":[{"value":"<media_id>","role":"start_image"}],"prompt":"<prompt template below>"}
   ```
5. **Wait:** call `job_status` with `sync: true`, repeating until it shows `completed`. This took about 3 minutes. Then download the result:
   `curl -sL -o gallery/reels/<piece>-raw.mp4 "<cloudfront mp4 url>"`
6. **Finish (watermark, music, encode):**
   ```bash
   python3 scripts/make_reel.py gallery/reels/<piece>-raw.mp4 gallery/reels/<piece>-reel.mp4 \
       --music assets/music/<track>.mp3          # optional: --music-start SEC, --no-native-audio
   ```
   This writes `<piece>-reel.mp4` and `<piece>-reel-still.jpg` (the middle frame, for checking the watermark).
7. **Verify:**
   `ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,sample_rate -of compact gallery/reels/<piece>-reel.mp4`
   Expect 1080x1920, h264, 30/1, aac 48000, about 6.0 s. Also look at the still: the watermark must be visible, with no warping or new objects.
8. Send to Joshua for review. Post only after approval, using the watermarked `-reel.mp4`.

## Prompt template
> Slow, smooth cinematic push-in toward the {SUBJECT}. Soft clouds drift gently across the sky past the full moon, thin mist
> drifts low over the {WATER/VALLEY}, moonlight shimmers and sparkles on {REFLECTIVE SURFACE}, stars twinkle subtly. {ONE SMALL
> NATURAL MOTION, e.g. wildflowers sway slightly in a light breeze}. Keep the original composition exactly: same {LIST KEY
> ELEMENTS}; no new objects, no people, no animals. Dreamy photorealistic fantasy, blue-green night tones, volumetric haze,
> stable camera, no warping. Ambient audio: soft night wind and {gentle lapping water | rustling leaves | distant waterfall}.

The Banff example used: SUBJECT = "moonlit lake"; elements = "mountains, moon, dock, canoes, trees, rocks and flowers".
Higgsfield job `e77326f1-6b83-44c6-9626-0a75a1a21055`.

## What make_reel.py does
- **Video:** scales/crops to 1080x1920, converts to 30 fps (`fps=30`, which duplicates frames from 24 fps), H.264 High profile, yuv420p, CRF 18, `-movflags +faststart`.
- **Watermark:** uses the same asset and constants as `scripts/watermark_for_social.py` (`watermark-corner.png`, **42 % of frame
  width, 72 % opacity, 3.5 % padding**, bottom-right). At 1080x1920 the mark is 453x254 px, placed at x=590, y=1599, on every frame.
  The equivalent manual command, where wm.png is the pre-scaled 453x254 mark at 72 % alpha:
  ```bash
  ffmpeg -i raw.mp4 -i music.mp3 -i wm.png -filter_complex \
   "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p[b];[b][2:v]overlay=590:1599[v]" \
   -map "[v]" -map 1:a -c:v libx264 -profile:v high -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart out.mp4
  ```
- **End banner (default, 2 Oct 2026):** every Reel ends with "Like this? Follow for more" (Montserrat Medium 60 px, white) over a smaller "@moonnightshadeart" (silver) on a rounded midnight-navy pill (#0b1530 at 70 % opacity), 860x166 px centred at x=110, y=1203 (about 63–71 % of the height, above the 320 px caption/UI band and clear of the watermark). It shows for the last 2.0 s with a 0.4 s fade-in (Pillow PNG + ffmpeg `overlay` with `enable='gte(t,START)'` and an alpha `fade`). Audio is unchanged. Pass `--no-end-banner` to turn it off.
- **Audio:** music is trimmed to the clip length from `reel_start_sec` (in `assets/music/tracks.json`), loudness-normalised,
  with a 0.8 s fade-in and a 1.2 s fade-out. Native Kling audio (wind/water) sits **12 dB under** the music. Two passes bring the final mix to
  **-14 LUFS integrated**, with a limiter at about -1.5 dBFS. Audio is rendered separately from the video encode: an `amix=duration=first` chained after
  `loudnorm` cut the audio to 3.1 s, so the script mixes with `duration=longest` plus pad/trim.

## Music library
`assets/music/`: 8 Pixabay Music tracks (calm and cinematic ambient, piano). `LICENSES.md` lists each track's title, artist and URL,
and `tracks.json` holds the metadata and start offsets. License: **Pixabay Content License** (https://pixabay.com/service/license-summary/), which allows free
commercial use with no attribution. The files must not be redistributed standalone, so the mp3s are gitignored and never pushed to the public repo.
Rotate the tracks so that consecutive Reels don't repeat one. Some Pixabay tracks are Content-ID registered; if a platform flags a Reel, the license page and track URL are the proof.

| File | Title, artist | Source |
|---|---|---|
| 01-calm-ambient-dreamscape.mp3 | Calm Ambient Dreamscape, morgan-ambient | https://pixabay.com/music/ambient-calm-ambient-dreamscape-529861/ |
| 02-ambient-cinematic.mp3 | Ambient Cinematic, AtlasAudio | https://pixabay.com/music/ambient-ambient-cinematic-510518/ |
| 03-peace-of-mind.mp3 | peace of mind (Calm Ambient Music), Clavier-Music | https://pixabay.com/music/ambient-peace-of-mind-calm-ambient-music-341056/ |
| **04-calm-night.mp3** (used on the Banff test) | calm night, Clavier-Music | https://pixabay.com/music/ambient-calm-night-312296/ |
| 05-mystical-piano-atmosphere.mp3 | Mystical Piano Atmosphere, Universfield | https://pixabay.com/music/modern-classical-mystical-piano-atmosphere-231511/ |
| 06-ethereal-discovery.mp3 | Ethereal Discovery (Background Piano Music), SigmaMusicArt | https://pixabay.com/music/modern-classical-ethereal-discovery-background-piano-music-288355/ |
| 07-cinematic-ambient.mp3 | Cinematic Ambient, Tunetank | https://pixabay.com/music/small-drama-cinematic-ambient-348342/ |
| 08-ambient-astronomy.mp3 | Ambient Astronomy, AtlasAudio | https://pixabay.com/music/ambient-ambient-astronomy-511860/ |

## Known caveats
- Instagram's Reels UI (caption, username, and the right-hand like/comment/share column) covers roughly the bottom 20 % and the right
  edge. The bottom-right watermark (y 1599–1853, x 590–1043) sits partly under that UI in the feed. It still appears on the video, in the grid
  and in downloads. If Joshua wants it clearly visible in-feed, consider moving it up and left (for example y ≈ 1350) as a Reels-only variant.
- The 24 to 30 fps conversion duplicates frames. Motion is slow, so judder is minimal. Kling only outputs 24 fps.
- Kling adds mist and cloud movement. Always check the still and scrub the clip for invented objects before approval.


## Audio rule (2 Oct 2026)
Every Reel plays calming music only: soft ambient/piano tracks from assets/music, gentle 1.5s fade in / 2s fade out, about -16 LUFS. The clip's generated sound is dropped by default (`--keep-native-audio` to override). No dramatic, percussive or loud tracks.
