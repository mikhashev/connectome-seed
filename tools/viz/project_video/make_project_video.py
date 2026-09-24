"""Build the connectome-seed project video (storyboard revision 3.1) end to end.

Steps (each rerunnable):
  1. timeline + soundtrack: the six measured voice clips (vo_measure/rev3, pocket-tts voice
     alba, already processed like tools/viz/bank_narration.py does), placed with the
     storyboard's leads and holds (0.8 s lead on the first clip, 0.3 s otherwise; 0.3 s holds;
     3.0 s end hold), plus bank_narration.py's quiet ambient pad -> <build>/narration_track.wav
     and <build>/timeline.json. Only clips whose names match measured.json's hashes are used,
     and each clip's length must match measured.json.
  2. frames: build_project_video.py inside Blender (EEVEE, 1920 x 1080, 24 fps), one folder per
     scene, with 6 frames of overlap on each side of every cut.
  3. overlays: captions (<= 8 words), the legend and the end card, drawn with Pillow as
     transparent PNGs; nothing on them is data.
  4. mux: ffmpeg joins the scenes with 12-frame cross-dissolves, lays the overlays on with fades,
     adds a light vignette and grain, and muxes the soundtrack -> connectome_seed_project.mp4.

Explanatory illustration, not evidence.

Run from the repository root with a Python that has numpy and Pillow:
    python tools/viz/project_video/make_project_video.py [--blender <blender.exe>]
        [--skip-frames] [--scenes 1,2,...] [--samples 64] [--stills "1:3.5,4:12"]
Data it needs first (both write outside the repository):
    tools/.venv/Scripts/python.exe tools/viz/export_bank_scene_data.py
    tools/.venv/Scripts/python.exe tools/viz/project_video/export_project_video_data.py
"""

import argparse
import json
import math
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
import bank_narration as N  # noqa: E402  (read_wav, write_wav, ambient_pad; no side effects)

OUT_DIR = ROOT.parent / "connectome-seed-data" / "renderings" / "project_video"
VO_DIR = OUT_DIR / "vo_measure" / "rev3"
BLENDER = "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe"
COMMIT = "b8db9f1"            # the commit that contains tools/viz/project_video/storyboard.md
REPO_URL = "github.com/mikhashev/connectome-seed"   # end card, on Mike's word 2026-09-24
FPS = 24
W, H = 1920, 1080
LEADS = [0.8, 0.3, 0.3, 0.3, 0.3, 0.3]
HOLDS = [0.3, 0.3, 0.3, 0.3, 0.3, 3.0]
PAD = 6
FONT_LIGHT = "C:/Windows/Fonts/segoeuisl.ttf"
FONT_REG = "C:/Windows/Fonts/segoeui.ttf"
TEXT = (232, 236, 244)
TEXT2 = (160, 170, 186)

# Captions, as in the storyboard; times in seconds from the start of the scene's voice clip
# (the same phrase boundaries as build_project_video.py's CUE table).
CAPTIONS = [
    # scene, text, sub-line, t_in, t_out (None = scene end)
    (1, "Goal: an elephant from a fly", None, 1.2, 6.9),
    (2, "Seed: a rule that writes wiring", None, 0.6, 7.6),
    (2, "The bank: a column-averaged template", None, 11.6, None),
    (3, "Cheap \u2248 expensive? Not met, not refuted.", None, 9.36, None),
    (3, None, "underspecified", 11.48, None),
    (4, "Three rules. None passed.", None, 2.2, 12.6),
    (4, "Exam fixed first. Family chosen after.", "rules #2 and #2.1", 13.0, None),
    (5, "Rank 1: sealed before the run.", None, 7.0, 14.6),
    (5, "FlyWire separates. flyvis near-ties \u2014 flag.", None, 15.1, None),
    (6, "Nothing grown yet. Next: one structure?", None, 8.17, 16.3),
]
LEGEND = [(1, 17.3, None), (6, 0.2, 16.3)]          # last ~4 s of scene 1; scene 6


def ffmpeg(name="ffmpeg"):
    exe = shutil.which(name)
    if not exe:
        sys.exit(f"{name} not found on PATH")
    return exe


def run(cmd):
    print(">>", " ".join(str(c) for c in cmd)[:400], flush=True)
    subprocess.run([str(c) for c in cmd], check=True)


# ------------------------------------------------------------------ 1. timeline + audio
def timeline(build):
    M = json.loads((HERE / "measured.json").read_text(encoding="utf-8"))
    keys = sorted(M)
    assert keys == [f"S0{i}" for i in range(1, 7)], keys
    t, scenes, clips = 0.0, [], []
    for i, k in enumerate(keys):
        wav = VO_DIR / f"{k}_{M[k]['sha']}.wav"
        if not wav.exists():
            sys.exit(f"missing clip {wav}")
        x, sr = N.read_wav(wav)
        assert sr == N.SR, (wav, sr)
        sec = len(x) / sr
        if abs(sec - M[k]["seconds"]) > 0.011:
            sys.exit(f"{wav.name}: {sec:.3f}s, measured.json says {M[k]['seconds']}")
        start = t
        v0 = t + LEADS[i]
        v1 = v0 + sec
        t = v1 + HOLDS[i]
        scenes.append({"id": k, "start": round(start, 4), "end": round(t, 4), "voice_start": round(v0, 4),
                       "voice_end": round(v1, 4), "clip": wav.name, "text": M[k]["text"]})
        clips.append(x)
    total = t
    n = int(math.ceil(total * N.SR))
    track = np.zeros(n, dtype=np.float32)
    for s, x in zip(scenes, clips):
        i0 = int(round(s["voice_start"] * N.SR))
        track[i0:i0 + len(x)] += x[: n - i0]
    track += N.ambient_pad(n, N.SR)
    N.write_wav(build / "narration_track.wav", track, N.SR)
    TL = {"total": round(total, 4), "fps": FPS, "scenes": scenes}
    (build / "timeline.json").write_text(json.dumps(TL, indent=1), encoding="utf-8")
    print(f"timeline {total:.2f}s ({int(total // 60)}:{total % 60:05.2f})")
    return TL


# ------------------------------------------------------------------ 3. overlays
def font(path, size):
    return ImageFont.truetype(path, size)


def shadowed(img, draw_fn, blur=6, alpha=190):
    """Draw text twice: a soft dark halo underneath (legibility on glow), then the text."""
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(sh), (3, 6, 12, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(sh)
    draw_fn(ImageDraw.Draw(img), None)


def caption_png(path, main, sub):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f1, f2 = font(FONT_LIGHT, 58), font(FONT_LIGHT, 38)

    def draw(d, col):
        if main:
            d.text((W / 2, 968), main, font=f1, fill=col or TEXT + (255,), anchor="mm")
        if sub:
            y = 1036 if main else 1036
            d.text((W / 2, y), sub, font=f2, fill=col or TEXT2 + (255,), anchor="mm")
    shadowed(img, draw)
    img.save(path)


def legend_png(path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f = font(FONT_LIGHT, 30)
    x, y = 56, 1040
    items = [("solid", "solid: run"), ("dim", "dim: paused"), ("wire", "wire: planned")]
    d = ImageDraw.Draw(img)
    halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.rounded_rectangle((x - 22, y - 30, x + 700, y + 28), 16, fill=(3, 6, 12, 150))
    img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(img)
    for i, (kind, label) in enumerate(items):
        s = 26
        box = (x, y - s / 2, x + s * 0.62, y + s / 2)
        if kind == "solid":
            glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(glow).rectangle(box, fill=(200, 222, 250, 200))
            img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(5)))
            d = ImageDraw.Draw(img)
            d.rectangle(box, fill=(226, 236, 250, 255))
        elif kind == "dim":
            d.rectangle(box, fill=(80, 88, 102, 255))
            bx = box[2] + 7
            d.rectangle((bx, y - 8, bx + 3, y + 8), fill=TEXT + (255,))
            d.rectangle((bx + 7, y - 8, bx + 10, y + 8), fill=TEXT + (255,))
            box = (box[0], box[1], bx + 10, box[3])
        else:
            d.rectangle(box, outline=(255, 255, 255, 170), width=2)
        tx = box[2] + 12
        d.text((tx, y), label, font=f, fill=TEXT + (255,), anchor="lm")
        x = tx + d.textlength(label, font=f) + 34
        if i < 2:
            d.text((x - 20, y), "\u00b7", font=f, fill=TEXT2 + (255,), anchor="mm")
    img.save(path)


END_LINES = [
    (REPO_URL, 54, FONT_REG, TEXT),
    ("", 30, FONT_LIGHT, TEXT),
    ("Made by the DPC Research team:", 36, FONT_LIGHT, TEXT),
    ("Mike Shevchenko, with AI agents Ark, Johnny, Warren and Zcode, and Claude Code", 36, FONT_LIGHT, TEXT),
    ("", 30, FONT_LIGHT, TEXT),
    ("Explanatory illustration, not evidence. Rendered in Blender; synthetic voice (Kyutai pocket-tts).",
     28, FONT_LIGHT, TEXT2),
]


def endcard_png(path):
    img = Image.new("RGBA", (W, H), (4, 6, 12, 205))
    d = ImageDraw.Draw(img)
    y = 430
    for s, size, fp, col in END_LINES:
        if s:
            d.text((W / 2, y), s, font=font(fp, size), fill=col + (255,), anchor="mm")
        y += int(size * 1.55)
    img.save(path)


def overlays(build, TL):
    od = build / "overlays"
    od.mkdir(exist_ok=True)
    ov = []
    sc = TL["scenes"]
    total = TL["total"]
    for i, (k, main, sub, a, b) in enumerate(CAPTIONS):
        s = sc[k - 1]
        t0 = s["voice_start"] + a
        t1 = (s["voice_start"] + b) if b is not None else s["end"] - 0.15
        p = od / f"cap{i:02d}.png"
        caption_png(p, main, sub)
        ov.append((p, t0, min(t1, total), 0.35))
    for k, a, b in LEGEND:
        s = sc[k - 1]
        p = od / "legend.png"
        legend_png(p)
        t1 = (s["voice_start"] + b) if b is not None else s["end"] - 0.15
        ov.append((p, s["voice_start"] + a, t1, 0.5))
    p = od / "endcard.png"
    endcard_png(p)
    s6 = sc[5]
    ov.append((p, s6["voice_end"] - 0.4, total, 0.7))
    return ov


# ------------------------------------------------------------------ 4. mux
def mux(build, TL, ov, out):
    sc = TL["scenes"]
    total = TL["total"]
    args = [ffmpeg(), "-y", "-loglevel", "error"]
    durs = []
    for k in range(1, 7):
        d = build / "frames" / f"s{k}"
        nfr = len(list(d.glob("f_*.png")))
        durs.append(nfr / FPS)
        args += ["-framerate", FPS, "-i", d / "f_%05d.png"]
    for p, t0, t1, fd in ov:
        args += ["-loop", "1", "-framerate", FPS, "-t", f"{t1 - t0:.4f}", "-i", p]
    args += ["-i", build / "narration_track.wav"]
    fx, xd = [], 2 * PAD / FPS
    prev, acc = "[0:v]", durs[0]
    for k in range(1, 6):
        off = acc - xd
        lab = f"[x{k}]"
        fx.append(f"{prev}[{k}:v]xfade=transition=fade:duration={xd:.4f}:offset={off:.4f}{lab}")
        prev, acc = lab, acc + durs[k] - xd
    print(f"joined length {acc:.3f}s vs timeline {total:.3f}s")
    if abs(acc - total) > 1.5 / FPS:
        sys.exit("joined scene length does not match the timeline; re-render the frames")
    for j, (p, t0, t1, fd) in enumerate(ov):
        i = 6 + j
        d = t1 - t0
        fx.append(f"[{i}:v]format=rgba,fade=t=in:st=0:d={fd}:alpha=1,"
                  f"fade=t=out:st={max(0, d - fd):.4f}:d={fd}:alpha=1,setpts=PTS+{t0:.4f}/TB[o{j}]")
        fx.append(f"{prev}[o{j}]overlay=eof_action=pass:format=auto[v{j}]")
        prev = f"[v{j}]"
    fx.append(f"{prev}vignette=angle=0.42,noise=alls=3:allf=t,format=yuv420p,trim=duration={total:.4f}[vout]")
    script = build / "filter.txt"
    script.write_text(";\n".join(fx), encoding="utf-8")
    ai = 6 + len(ov)
    args += ["-/filter_complex", script, "-map", "[vout]", "-map", f"{ai}:a",
             "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-r", FPS,
             "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-t", f"{total:.4f}",
             "-movflags", "+faststart", out]
    run(args)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blender", default=BLENDER)
    ap.add_argument("--out", default=str(OUT_DIR / "connectome_seed_project.mp4"))
    ap.add_argument("--build", default=str(OUT_DIR / "build"))
    ap.add_argument("--skip-frames", action="store_true")
    ap.add_argument("--scenes", default="1,2,3,4,5,6")
    ap.add_argument("--samples", default="64")
    ap.add_argument("--stills")
    ap.add_argument("--percent", default="100")
    a = ap.parse_args()
    build = Path(a.build)
    build.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    TL = timeline(build)
    bl = [a.blender, "--background", "--factory-startup", "--python", HERE / "build_project_video.py", "--",
          "--build", build, "--samples", a.samples, "--percent", a.percent]
    if a.stills:
        run(bl + ["--stills", a.stills])
        return
    if not a.skip_frames:
        run(bl + ["--scenes", a.scenes])
    t1 = time.time()
    ov = overlays(build, TL)
    mux(build, TL, ov, a.out)
    t2 = time.time()
    print(f"wrote {a.out}")
    print(f"timings: frames {t1 - t0:.0f}s, overlays + mux {t2 - t1:.0f}s")


if __name__ == "__main__":
    main()
