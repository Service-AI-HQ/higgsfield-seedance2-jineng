#!/usr/bin/env python3
"""Restore bandwidth to the voice takes.

The narration came out of a video model at ~2.1 kHz rolloff with 0.13% of its
energy above 5 kHz — below telephone bandwidth. The scene dialogue is worse:
inconsistent, from 1.5 kHz to 11.3 kHz between characters in the same room.

Adobe's speech enhancer would be the right tool but its async result is
unreachable in a headless session, so this synthesises the missing top end from
the harmonics already present: drive a band just under the rolloff into a
nonlinearity, which generates its own 2nd/3rd harmonics an octave and a fifth
above, then band-limit that and mix it back under the original envelope so
nothing is added between words.

This is a repair, not a substitute for rendering the lines on a real TTS.
"""
import numpy as np, wave, subprocess, imageio_ffmpeg, os

FF = imageio_ffmpeg.get_ffmpeg_exe()
SR = 48000

def read(path):
    subprocess.run([FF, "-nostdin", "-y", "-i", path, "-ac", "1", "-ar", str(SR),
                    "-c:a", "pcm_s16le", "/tmp/_vr.wav"], capture_output=True)
    w = wave.open("/tmp/_vr.wav")
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    w.close()
    return a

def write(path, a):
    a = np.clip(a, -1, 1)
    w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((a * 32767).astype(np.int16).tobytes()); w.close()

def band(a, lo, hi):
    """Zero-phase brick-wall band filter in the frequency domain."""
    n = 1 << (len(a) - 1).bit_length()
    X = np.fft.rfft(a, n); f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if lo: g *= 1 / (1 + (lo / np.maximum(f, 1e-9)) ** 8)      # high-pass
    if hi: g *= 1 / (1 + (np.maximum(f, 1e-9) / hi) ** 8)      # low-pass
    return np.fft.irfft(X * g, n)[:len(a)]

def envelope(a, ms=25):
    n = max(1, int(SR * ms / 1000))
    e = np.sqrt(np.convolve(a ** 2, np.ones(n) / n, mode="same"))
    return e / (e.max() + 1e-12)

def rolloff(a, pct=0.99):
    fl = 2048; acc = None; peak = np.abs(a).max()
    for i in range(0, max(1, len(a) - fl), 1024):
        fr = a[i:i + fl]
        if np.sqrt((fr ** 2).mean()) < 0.08 * peak: continue
        X = np.abs(np.fft.rfft(fr * np.hanning(fl))) ** 2
        acc = X if acc is None else acc + X
    if acc is None: return 0.0, 0.0
    f = np.fft.rfftfreq(fl, 1 / SR); m = (f > 80) & (f < 20000); P = acc[m]
    c = np.cumsum(P)
    return float(f[m][np.searchsorted(c, pct * c[-1])]), float(P[f[m] > 5000].sum() / P.sum())

def hi_lo(a):
    """Ratio of 5-10 kHz to 300-3000 Hz energy over voiced frames. Natural
    speech in these films measures ~0.16; the narration arrived at 0.002."""
    fl = 2048; acc = None; pk = np.abs(a).max()
    if pk < 1e-9: return 0.0
    for i in range(0, max(1, len(a) - fl), 1024):
        fr = a[i:i + fl]
        if np.sqrt((fr ** 2).mean()) < 0.08 * pk: continue
        X = np.abs(np.fft.rfft(fr * np.hanning(fl))) ** 2
        acc = X if acc is None else acc + X
    if acc is None: return 0.0
    f = np.fft.rfftfreq(fl, 1 / SR); m = (f > 80) & (f < 20000)
    P = acc[m]; ff = f[m]
    lo = P[(ff >= 300) & (ff < 3000)].sum()
    return float(P[(ff >= 5000) & (ff < 10000)].sum() / max(lo, 1e-20))

TARGET = 0.14      # just under natural, so the lift never reads as fizzy

def _excite(a, drive, amount, src, out):
    if np.abs(a).max() < 1e-6: return a
    seed = band(a, *src)
    s = seed / (np.abs(seed).max() + 1e-12)
    harm = np.tanh(drive * s) + 0.35 * (np.tanh(drive * s) ** 2 - 0.5)
    harm = band(harm, *out)
    harm = harm / (np.abs(harm).max() + 1e-12)
    harm *= envelope(a)          # only while someone is speaking
    pre = np.abs(a).max()
    y = a + amount * harm * pre
    return y * (pre / (np.abs(y).max() + 1e-12))

def restore(a, src=(800, 2000), out=(2200, 10000), drive=11.0, target=TARGET):
    """Lift a take until its spectral balance matches natural speech.

    Bisect on the mix amount rather than using a fixed gain, so every voice in
    the film lands at the same brightness regardless of how muffled it began.
    """
    if hi_lo(a) >= target: return a
    lo_a, hi_a = 0.0, 6.0
    best = a
    for _ in range(12):
        mid = (lo_a + hi_a) / 2
        y = _excite(a, drive, mid, src, out)
        r = hi_lo(y)
        best = y
        if abs(r - target) < 0.005: break
        if r < target: lo_a = mid
        else: hi_a = mid
    return best

def process(src, dst, **kw):
    a = read(src)
    r0, h0 = rolloff(a); b0 = hi_lo(a)
    b = restore(a, **kw)
    r1, h1 = rolloff(b); b1 = hi_lo(b)
    write(dst, b)
    tag = "" if b1 > b0 + 1e-4 else "   (already bright, left alone)"
    print(f"  {os.path.basename(src):26s} {r0:6.0f}->{r1:6.0f}Hz   "
          f"hi/lo {b0:.4f}->{b1:.4f}{tag}")

if __name__ == "__main__":
    BASE = ("/tmp/claude-0/-home-user-higgsfield-seedance2-jineng/"
            "2b86c3cd-6ddc-5f8f-a642-f6d3a73eff17/scratchpad")
    for film in ("looksdry", "commercial"):
        d = os.path.join(BASE, film)
        out = os.path.join(d, "voice_fixed"); os.makedirs(out, exist_ok=True)
        print(f"=== {film} ===")
        process(os.path.join(d, "vo/vo_full.wav"), os.path.join(out, "vo_full.wav"))
        ad = os.path.join(d, "audio")
        for f in sorted(os.listdir(ad)):
            if f.endswith((".mp3", ".wav")):
                process(os.path.join(ad, f), os.path.join(out, f[:-4] + ".wav"))
