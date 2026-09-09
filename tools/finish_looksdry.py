#!/usr/bin/env python3
"""Finish LOOKS DRY once the VO audio is in hand.

    python3 tools/finish_looksdry.py <url-or-local-file>

Takes the OpenArt render (job YV4HcH89ND4rvKvdBCer) as a URL or a local path,
verifies the voice, splits the lines, and cuts the finished film. Everything
else is already staged in the scratchpad.
"""
import subprocess, sys, os, wave, json
import numpy as np, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = os.environ.get("LD_BASE", os.path.expanduser(
    "~/../tmp/claude-0/-home-user-higgsfield-seedance2-jineng/"
    "2b86c3cd-6ddc-5f8f-a642-f6d3a73eff17/scratchpad/looksdry"))
COMMERCIAL_F0 = 105.5          # THE COMMERCIAL's median, for campaign match
def run(a): return subprocess.run([FF, "-nostdin", "-y"] + a, capture_output=True, text=True)

def fetch(src, dst):
    if src.startswith(("http://", "https://")):
        subprocess.run(["curl", "-sSL", "-o", dst, src], check=True)
    else:
        subprocess.run(["cp", src, dst], check=True)
    return dst

def segments(wav):
    r = subprocess.run([FF, "-nostdin", "-i", wav, "-af",
                        "silencedetect=noise=-34dB:d=0.35", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    starts, ends = [], []
    for line in r.split("\n"):
        if "silence_start:" in line: starts.append(float(line.split("silence_start:")[1].strip()))
        if "silence_end:"   in line: ends.append(float(line.split("silence_end:")[1].split("|")[0].strip()))
    dur = float(subprocess.run(
        ["python3","-c","import sys;print(0)"],capture_output=True,text=True).stdout or 0)
    w = wave.open(wav); dur = w.getnframes()/w.getframerate(); w.close()
    segs, cur = [], 0.0
    if starts and starts[0] == 0: cur = ends[0] if ends else 0.0; ends = ends[1:]; starts = starts[1:]
    for i, s in enumerate(starts):
        segs.append((cur, s))
        cur = ends[i] if i < len(ends) else dur
    if cur < dur - 0.2: segs.append((cur, dur))
    return [(a, b) for a, b in segs if b - a > 0.25]

def f0(x, sr, fmin=60, fmax=320):
    est, fl, hop = [], int(0.04*sr), int(0.02*sr)
    for i in range(0, max(1, len(x)-fl), hop):
        fr = x[i:i+fl]
        if np.sqrt((fr**2).mean()) < 0.02: continue
        fr = fr - fr.mean()
        ac = np.correlate(fr, fr, mode="full")[len(fr)-1:]
        lo, hi = int(sr/fmax), int(sr/fmin)
        if hi >= len(ac) or ac[0] <= 0: continue
        p = np.argmax(ac[lo:hi]) + lo
        if ac[p]/ac[0] > 0.3: est.append(sr/p)
    return float(np.median(est)) if est else None

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    vo = os.path.join(BASE, "vo"); os.makedirs(vo, exist_ok=True)
    raw = fetch(sys.argv[1], os.path.join(vo, "vo_raw.mp4"))
    full = os.path.join(vo, "vo_full.wav")
    run(["-i", raw, "-vn", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", full])

    segs = segments(full)
    w = wave.open(full); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768.0
    w.close()
    pitches = [p for p in (f0(a[int(s*sr):int(e*sr)], sr) for s, e in segs) if p]
    med = float(np.median(pitches)) if pitches else 0.0
    gap = a[int(segs[0][1]*sr):int(segs[1][0]*sr)] if len(segs) > 1 else a[:sr]
    floor = 20*np.log10(max(np.sqrt((gap**2).mean()), 1e-9))

    print(f"segments: {len(segs)}  (expect 9-10)")
    print(f"median F0: {med:.1f} Hz  (THE COMMERCIAL: {COMMERCIAL_F0})  delta {abs(med-COMMERCIAL_F0):.1f}")
    print(f"noise floor: {floor:.1f} dBFS")
    if not (7 <= len(segs) <= 11): sys.exit("STOP: wrong number of spoken lines — inspect before cutting.")
    if abs(med - COMMERCIAL_F0) > 15: sys.exit("STOP: voice does not match the campaign. Report, do not ship.")
    if floor > -55: sys.exit("STOP: audible noise floor between lines.")

    names = ["01","02","03","04","05","06","07","08","09","10"][:len(segs)]
    for (s, e), n in zip(segs, names):
        d = round(e - s + 0.16, 3); st = round(max(s - 0.08, 0), 3)
        run(["-ss", str(st), "-i", full, "-t", str(d), "-af",
             f"afade=t=in:st=0:d=0.05,afade=t=out:st={round(d-0.08,3)}:d=0.08,"
             "loudnorm=I=-18:TP=-2:LRA=7", "-ar", "48000", "-ac", "1",
             "-c:a", "pcm_s16le", os.path.join(vo, f"L{n}.wav")])
    print("lines split ->", vo)
    print("now run the cut4 build (offsets in ideas/vo-spine-looksdry.md)")

if __name__ == "__main__":
    main()
