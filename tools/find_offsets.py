#!/usr/bin/env python3
"""Recover where every voice take actually sits in the finished master.

Rebuilding the soundtrack means re-laying every line, and remembered offsets
are not good enough. Each take is cross-correlated against the master's audio,
so the placements come from the film itself.
"""
import numpy as np, wave, subprocess, imageio_ffmpeg, os, json, sys

FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 48000

def read(p, tmp="/tmp/_fo.wav"):
    subprocess.run([FF, "-nostdin", "-y", "-i", p, "-ac", "1", "-ar", str(SR),
                    "-c:a", "pcm_s16le", tmp], capture_output=True)
    w = wave.open(tmp)
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    w.close(); return a

def locate(hay, needle):
    """Normalised cross-correlation; returns (offset_seconds, confidence)."""
    n = len(hay) + len(needle)
    N = 1 << (n - 1).bit_length()
    # correlate on the envelope: immune to the ducking and EQ applied in the mix
    def env(x, d=256):
        e = np.sqrt(np.convolve(x ** 2, np.ones(d) / d, mode="same"))[::d]
        return (e - e.mean()) / (e.std() + 1e-12)
    H, Nd = env(hay), env(needle)
    M = 1 << (len(H) + len(Nd) - 1).bit_length()
    c = np.fft.irfft(np.fft.rfft(H, M) * np.conj(np.fft.rfft(Nd, M)), M)
    c = c[:len(H)]
    i = int(np.argmax(c))
    peak = c[i]
    med = np.median(np.abs(c))
    return i * 256 / SR, float(peak / (med + 1e-12))

if __name__ == "__main__":
    BASE = ("/tmp/claude-0/-home-user-higgsfield-seedance2-jineng/"
            "2b86c3cd-6ddc-5f8f-a642-f6d3a73eff17/scratchpad")
    FILMS = {
        "commercial": dict(master="cut4/THE_COMMERCIAL_v5.mp4", volines=10),
        "looksdry":   dict(master="cut4/LOOKS_DRY_v4.mp4",      volines=9),
    }
    GROUPS = {"looksdry": [[1,2],[3],[4],[5],[6],[7],[8,9],[10],[11]]}
    for film, cfg in FILMS.items():
        d = os.path.join(BASE, film)
        hay = read(os.path.join(d, cfg["master"]))
        print(f"=== {film} ({len(hay)/SR:.2f}s) ===")
        res = {}
        # dialogue takes, from the originals that were actually mixed in
        for f in sorted(os.listdir(os.path.join(d, "audio"))):
            if not f.endswith((".mp3", ".wav")): continue
            nd = read(os.path.join(d, "audio", f), "/tmp/_fo2.wav")
            off, conf = locate(hay, nd)
            res[f] = round(off, 2)
            print(f"  {f:26s} {off:7.2f}s   conf {conf:6.1f}")
        json.dump(res, open(os.path.join(d, "recovered_offsets.json"), "w"), indent=1)
