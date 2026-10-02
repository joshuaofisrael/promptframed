#!/usr/bin/env python3
"""
Turn a raw Higgsfield image-to-video clip into a postable Instagram Reel.

  - 1080x1920, H.264 (yuv420p, high profile), 30 fps, AAC 48 kHz stereo, +faststart
  - Night Shade Art watermark burned in for the full duration, bottom-right,
    same geometry/opacity as scripts/watermark_for_social.py
    (42% of frame width, 72% opacity, 3.5% padding from right/bottom edges)
  - Background music bed from assets/music/ with fade in/out, native clip audio
    (wind/water) kept ~12 dB under the music, final mix normalised to about -14 LUFS,
    true peak limited to -1.5 dBTP
  - Mid-point still JPG saved next to the MP4 for a watermark check

Usage:
  python3 scripts/make_reel.py RAW.mp4 OUT.mp4 --music assets/music/04-calm-night.mp3 [--music-start 1.4]
  (omit --music-start to use the start offset listed in assets/music/tracks.json)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "scripts"))
import watermark_for_social as wm  # reuse exact constants + asset

W, H, FPS = 1080, 1920, 30
TARGET_LUFS = -16.0       # gentle, calming level
NATIVE_DUCK_DB = -12.0     # native ambient audio relative to music
FADE_IN, FADE_OUT = 1.5, 2.0


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr[-3000:])
    return p.stderr


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format",
                          "-show_streams", str(path)], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def build_watermark(tmp: Path) -> tuple[Path, int, int]:
    mark = wm.load_watermark()
    target_w = max(120, int(W * wm.WIDTH_FRAC))
    target_h = max(40, int(mark.height * (target_w / mark.width)))
    mark_r = wm.apply_opacity(mark.resize((target_w, target_h), Image.Resampling.LANCZOS), wm.OPACITY)
    p = tmp / "wm.png"
    mark_r.save(p)
    x = W - target_w - int(W * wm.PAD_FRAC)
    y = H - target_h - int(H * wm.PAD_FRAC)
    return p, x, y


def default_start(music: Path) -> float:
    meta = ROOT / "assets" / "music" / "tracks.json"
    if meta.exists():
        for t in json.loads(meta.read_text()):
            if t["file"] == music.name:
                return float(t.get("reel_start_sec", 0))
    return 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("out")
    ap.add_argument("--music", required=True)
    ap.add_argument("--music-start", type=float, default=None)
    ap.add_argument("--no-native-audio", action="store_true", help="(default now) music only")
    ap.add_argument("--keep-native-audio", action="store_true", help="mix in the clip's generated sound under the music")
    a = ap.parse_args()

    raw, out, music = Path(a.raw), Path(a.out), Path(a.music)
    start = a.music_start if a.music_start is not None else default_start(music)
    info = probe(raw)
    dur = float(info["format"]["duration"])
    has_audio = any(s["codec_type"] == "audio" for s in info["streams"]) and a.keep_native_audio and not a.no_native_audio
    fo_start = max(0.0, dur - FADE_OUT)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        wm_png, x, y = build_watermark(tmp)

        vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"fps={FPS},format=yuv420p[base];"
              f"[base][2:v]overlay={x}:{y}:format=auto,format=yuv420p[v]")
        mus = (f"[1:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
               f"aformat=channel_layouts=stereo,loudnorm=I={TARGET_LUFS}:TP=-2:LRA=11,aresample=48000,"
               f"afade=t=in:st=0:d={FADE_IN},afade=t=out:st={fo_start:.3f}:d={FADE_OUT}[m]")
        if has_audio:
            nat = (f"[0:a]aresample=48000,aformat=channel_layouts=stereo,"
                   f"loudnorm=I={TARGET_LUFS + NATIVE_DUCK_DB}:TP=-6:LRA=11,aresample=48000,"
                   f"afade=t=in:st=0:d=0.3,afade=t=out:st={fo_start:.3f}:d={FADE_OUT}[n]")
            # duration=first truncates after loudnorm's look-ahead; mix longest, then pad/trim exactly
            mix = f"[m][n]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:{dur:.3f}[mx]"
            af = f"{mus};{nat};{mix}"
        else:
            af = f"{mus};[m]apad,atrim=0:{dur:.3f}[mx]"

        def mix_audio(dst: Path, gain_db: float) -> None:
            # audio is rendered on its own (loudnorm/alimiter look-ahead buffers get
            # truncated if they share a graph with the video encode)
            fc = f"{af};[mx]volume={gain_db:.2f}dB,alimiter=limit=0.84:level=false,aresample=48000[a]"
            run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-ss", f"{start}", "-i", str(music),
                 "-filter_complex", fc, "-map", "[a]", "-t", f"{dur:.3f}", "-c:a", "pcm_s16le", str(dst)])

        def encode(dst: Path, audio: Path) -> None:
            run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-i", str(audio), "-i", str(wm_png),
                 "-filter_complex", vf, "-map", "[v]", "-map", "1:a", "-af", "apad",
                 "-t", f"{dur:.3f}", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow",
                 "-crf", "18", "-r", str(FPS), "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                 "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(dst)])

        def lufs(p: Path) -> float:
            e = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-map", "0:a",
                     "-af", "ebur128", "-f", "null", "-"])
            return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", e)[-1])

        # pass 1 measure, pass 2 apply linear gain so the whole mix lands at ~-14 LUFS
        a1, a2 = tmp / "mix1.wav", tmp / "mix2.wav"
        mix_audio(a1, 0.0)
        gain = TARGET_LUFS - lufs(a1)
        mix_audio(a2, gain)
        out.parent.mkdir(parents=True, exist_ok=True)
        encode(out, a2)
        final = lufs(out)

    still = out.with_name(out.stem + "-still.jpg")
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{dur / 2:.3f}", "-i", str(out),
         "-frames:v", "1", "-q:v", "2", str(still)])
    print(json.dumps({"out": str(out), "still": str(still), "music": music.name,
                      "music_start": start, "duration": dur, "loudness_lufs": final,
                      "watermark_xywh": [x, y]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
