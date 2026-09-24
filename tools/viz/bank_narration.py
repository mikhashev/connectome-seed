"""Voice-over and timeline for the video "real bank vs shuffled bank".

Reads the captions from tools/viz/bank_video_script.py, speaks each one with an offline
text-to-speech engine, measures every clip, and writes
    <build>/narration/NN_<id>.wav   one clip per caption (cached by text + engine)
    <build>/narration_track.wav     the full soundtrack, 48 kHz mono: voice + optional soft pad
    <build>/timing.json             start / end of every caption, total length, engine used
bank_animation.py (Blender) reads timing.json, so pictures follow the voice.

Engines, in order of preference:
  * pocket-tts (Kyutai, runs on CPU; a local checkout of kyutai-labs/pocket-tts). The
    Python running this script must have `pocket_tts` installed; it fetches its public weights
    from Hugging Face on first use and caches them.
  * Windows SAPI through PowerShell (System.Speech), first installed English voice.

Run (normally via make_bank_video.py):
    <python with pocket_tts> tools/viz/bank_narration.py <build_dir> [--engine pocket|sapi]
        [--voice alba] [--no-pad]
"""

import hashlib
import json
import math
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bank_video_script as S  # noqa: E402

SR = 48000
PAD_GAIN = 0.018          # ambient pad peak amplitude (voice peaks are normalised to 0.8)


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    assert sw == 2, f"{path}: expected 16-bit PCM"
    x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(1)
    return x, sr


def write_wav(path, x, sr):
    y = np.clip(x, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((y * 32767).astype("<i2").tobytes())


def resample(x, sr_in, sr_out):
    if sr_in == sr_out:
        return x
    n_out = int(round(len(x) * sr_out / sr_in))
    t_out = np.arange(n_out) * (sr_in / sr_out)
    return np.interp(t_out, np.arange(len(x)), x).astype(np.float32)


def trim_silence(x, sr, thr=0.01, keep=0.06):
    """Cut leading / trailing near-silence, keeping `keep` seconds of margin."""
    idx = np.flatnonzero(np.abs(x) > thr)
    if len(idx) == 0:
        return x
    k = int(keep * sr)
    return x[max(0, idx[0] - k): min(len(x), idx[-1] + k)]


def compress_pauses(x, sr, thr=0.012, longest=0.40, keep=0.28, win=0.02):
    """Shorten silent gaps inside a clip that are longer than `longest` seconds to `keep`
    seconds (the engine sometimes pauses long at commas); speech itself is untouched."""
    w = int(win * sr)
    nwin = len(x) // w
    quiet = np.abs(x[: nwin * w]).reshape(nwin, w).max(1) < thr
    out, i = [], 0
    while i < nwin:
        j = i
        while j < nwin and quiet[j] == quiet[i]:
            j += 1
        seg = x[i * w: j * w]
        if quiet[i] and (j - i) * win > longest:
            k = int(keep * sr) // 2
            seg = np.concatenate([seg[:k], seg[-k:]])
        out.append(seg)
        i = j
    out.append(x[nwin * w:])
    return np.concatenate(out)


# ------------------------------------------------------------------ engines
class Pocket:
    name = "pocket-tts"

    def __init__(self, voice):
        from pocket_tts import TTSModel
        self.voice = voice
        self.model = TTSModel.load_model()
        self.state = self.model.get_state_for_audio_prompt(voice)

    def tag(self):
        return f"{self.name}:{self.voice}"

    def speak(self, text, out):
        audio = self.model.generate_audio(self.state, text)
        write_wav(out, audio.numpy().astype(np.float32), self.model.sample_rate)


class Sapi:
    name = "windows-sapi"

    def __init__(self, voice=None):
        ps = ("Add-Type -AssemblyName System.Speech; "
              "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
              "$s.GetInstalledVoices() | % { $_.VoiceInfo.Name + '|' + $_.VoiceInfo.Culture }")
        out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                             capture_output=True, text=True, check=True).stdout.split("\n")
        voices = [v.strip().split("|") for v in out if "|" in v]
        en = [v[0] for v in voices if v[1].startswith("en")]
        if not en:
            raise RuntimeError(f"no English SAPI voice among {voices}")
        self.voice = voice if voice in en else en[0]

    def tag(self):
        return f"{self.name}:{self.voice}"

    def speak(self, text, out):
        t = text.replace("'", "''")
        ps = ("Add-Type -AssemblyName System.Speech; "
              "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
              f"$s.SelectVoice('{self.voice}'); $s.Rate = 0; "
              f"$s.SetOutputToWaveFile('{out}'); $s.Speak('{t}'); $s.Dispose()")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)


def make_engine(kind, voice):
    if kind in ("pocket", "auto"):
        try:
            return Pocket(voice or "alba")
        except Exception as e:  # noqa: BLE001 - any failure means: fall back
            if kind == "pocket":
                raise
            print(f"pocket-tts unavailable ({e!r}); falling back to Windows SAPI")
    return Sapi(voice)


# ------------------------------------------------------------------ pad
def ambient_pad(n, sr):
    """A very quiet, slowly breathing A-minor-ish drone (sines only), faded in and out."""
    t = np.arange(n) / sr
    x = np.zeros(n, dtype=np.float64)
    for f, a, lfo in [(110.0, 1.0, 0.05), (164.81, 0.6, 0.037), (220.0, 0.45, 0.043),
                      (261.63, 0.3, 0.029), (329.63, 0.2, 0.061)]:
        x += a * np.sin(2 * math.pi * f * t) * (0.6 + 0.4 * np.sin(2 * math.pi * lfo * t))
    x /= np.abs(x).max()
    fade = np.minimum(1.0, np.minimum(t / 4.0, (t[-1] - t) / 4.0))
    return (PAD_GAIN * x * fade).astype(np.float32)


# ------------------------------------------------------------------ main
def main():
    a = sys.argv[1:]
    build = Path(a[0])
    kind = a[a.index("--engine") + 1] if "--engine" in a else "auto"
    voice = a[a.index("--voice") + 1] if "--voice" in a else None
    pad = "--no-pad" not in a
    ndir = build / "narration"
    ndir.mkdir(parents=True, exist_ok=True)

    eng = make_engine(kind, voice)
    print("engine:", eng.tag())
    clips = []
    for i, c in enumerate(S.CHUNKS):
        say = c.get("say", c["text"])
        h = hashlib.sha256(f"{eng.tag()}|{say}".encode()).hexdigest()[:12]
        wav = ndir / f"{i:02d}_{c['id']}_{h}.wav"
        if not wav.exists():
            for old in ndir.glob(f"{i:02d}_*.wav"):
                old.unlink()
            eng.speak(say, wav.resolve())
            print(f"spoke {wav.name}")
        x, sr = read_wav(wav)
        x = compress_pauses(trim_silence(resample(x, sr, SR), SR), SR)
        x = 0.8 * x / max(1e-6, np.abs(x).max())
        clips.append(x)

    t, rows = 0.0, []
    for c, x in zip(S.CHUNKS, clips):
        t += c["lead"]
        dur = len(x) / SR
        rows.append({"id": c["id"], "text": c["text"], "say": c.get("say", c["text"]),
                     "start": round(t, 4), "end": round(t + dur, 4)})
        t += dur + c["hold"]
    total = t
    n = int(math.ceil(total * SR))
    track = np.zeros(n, dtype=np.float32)
    for r, x in zip(rows, clips):
        i0 = int(round(r["start"] * SR))
        track[i0:i0 + len(x)] += x[: n - i0]
    if pad:
        track += ambient_pad(n, SR)
    write_wav(build / "narration_track.wav", track, SR)
    timing = {"engine": eng.tag(), "sample_rate": SR, "total": round(total, 4),
              "pad": pad, "chunks": rows}
    (build / "timing.json").write_text(json.dumps(timing, indent=1), encoding="utf-8")
    print(f"timeline {total:.2f}s, {len(rows)} captions -> {build / 'timing.json'}")


if __name__ == "__main__":
    main()
