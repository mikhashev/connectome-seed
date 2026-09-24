"""Build the narrated video "real bank vs shuffled bank" end to end.

Steps (each rerunnable; narration clips are cached by text):
  1. voice-over + timeline: bank_narration.py, run with a Python that has pocket-tts installed
     (falls back to Windows SAPI inside that script if pocket-tts cannot load);
  2. frames: bank_animation.py inside Blender (EEVEE, 1920x1080, 30 fps);
  3. mux: ffmpeg, H.264 video + AAC audio -> bank_real_vs_shuffled.mp4.

Explanatory video, not evidence; it reads scene_data.json written by export_bank_scene_data.py.

Run from the repository root with any Python 3.10+ (no third-party packages needed here):
    python tools/viz/make_bank_video.py --tts-python <python with pocket_tts> \
        [--blender <blender.exe>] [--engine auto|pocket|sapi] [--voice alba] [--skip-tts]
        [--skip-frames]
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parents[2] / "connectome-seed-data" / "renderings" / "bank_scene"
BLENDER = "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe"


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg not found (PATH or imageio-ffmpeg)")


def run(cmd):
    print(">>", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tts-python", default=sys.executable)
    ap.add_argument("--blender", default=BLENDER)
    ap.add_argument("--engine", default="auto")
    ap.add_argument("--voice", default="alba")
    ap.add_argument("--data", default=str(OUT_DIR / "scene_data.json"))
    ap.add_argument("--out", default=str(OUT_DIR / "bank_real_vs_shuffled.mp4"))
    ap.add_argument("--skip-tts", action="store_true")
    ap.add_argument("--skip-frames", action="store_true")
    a = ap.parse_args()
    build = OUT_DIR / "video_build"
    build.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    if not a.skip_tts:
        run([a.tts_python, HERE / "bank_narration.py", build, "--engine", a.engine,
             "--voice", a.voice])
    t1 = time.time()
    if not a.skip_frames:
        run([a.blender, "--background", "--python", HERE / "bank_animation.py", "--",
             "--build", build, "--data", a.data])
    t2 = time.time()
    fps = json.loads((build / "frames_info.json").read_text())["fps"]
    run([ffmpeg_exe(), "-y", "-loglevel", "error",
         "-framerate", fps, "-i", build / "frames" / "f_%05d.png",
         "-i", build / "narration_track.wav",
         "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
         "-r", fps, "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
         "-movflags", "+faststart", a.out])
    t3 = time.time()
    print(f"wrote {a.out}")
    print(f"timings: tts {t1 - t0:.0f}s, frames {t2 - t1:.0f}s, mux {t3 - t2:.0f}s, "
          f"total {t3 - t0:.0f}s")


if __name__ == "__main__":
    main()
