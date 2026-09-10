#!/usr/bin/env python3
"""Cut LOOKS DRY v4 — the v3 mix with the VO spine laid over it.

The nine narration lines come from OpenArt job YV4HcH89ND4rvKvdBCer, split on
the grouping in ideas/vo-spine-looksdry.md. The approved v3 mix (beds, music,
foley, dialogue, already mastered) becomes the base bus and is sidechained
under the narration. VO and dialogue never overlap, so nothing in the film is
stepped on.
"""
import subprocess, os, wave, sys
import numpy as np, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = ("/tmp/claude-0/-home-user-higgsfield-seedance2-jineng/"
        "2b86c3cd-6ddc-5f8f-a642-f6d3a73eff17/scratchpad/looksdry")
VO, CUT4 = os.path.join(BASE, "vo"), os.path.join(BASE, "cut4")

# 11 detected segments -> 9 scripted lines. Groups 1 and 7 each span an
# internal full stop, which is why the naive 1:1 numbering was wrong.
GROUPS = [[1, 2], [3], [4], [5], [6], [7], [8, 9], [10], [11]]
OFFSETS = [1.0, 8.5, 24.0, 27.5, 49.0, 54.0, 64.0, 77.5, 92.5]
LINES = [
    "Renee is up at four. Nobody asked her to be.",
    "Her croissants are the best thing on this street.",
    "One stranger saw one photo.",
    "And said it looked dry.",
    "So she tried to take a better photo.",
    "That wasn't it either.",
    "People don't buy the photo. They buy her.",
    "You've already done the hard part.",
    "We'll do the rest.",
]

def run(a):
    return subprocess.run([FF, "-nostdin", "-y"] + a, capture_output=True, text=True)

def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import finish_looksdry as F
    full = os.path.join(VO, "vo_full.wav")
    segs = F.segments(full)
    if len(segs) != 11:
        sys.exit(f"STOP: expected 11 raw segments, found {len(segs)}.")

    # split on the grouped boundaries, keeping any internal pause intact
    for i, g in enumerate(GROUPS, 1):
        s = segs[g[0] - 1][0]
        e = segs[g[-1] - 1][1]
        st, d = round(max(s - 0.08, 0), 3), round(e - s + 0.16, 3)
        run(["-ss", str(st), "-i", full, "-t", str(d), "-af",
             f"afade=t=in:st=0:d=0.05,afade=t=out:st={round(d - 0.08, 3)}:d=0.08,"
             "loudnorm=I=-18:TP=-2:LRA=7", "-ar", "48000", "-ac", "1",
             "-c:a", "pcm_s16le", os.path.join(VO, f"L{i:02d}.wav")])

    ends = []
    for i, off in enumerate(OFFSETS, 1):
        w = wave.open(os.path.join(VO, f"L{i:02d}.wav"))
        d = w.getnframes() / w.getframerate(); w.close()
        ends.append(off + d)
        print(f"L{i:02d}  {off:6.2f} -> {off + d:6.2f}  {LINES[i-1]}")

    # narration must clear the scene dialogue entirely
    DIA = [(20.6, 1.15), (35.7, 1.80), (38.2, 0.99), (39.9, 1.23),
           (43.1, 3.24), (88.6, 1.07)]
    for (ds, dd) in DIA:
        for off, end in zip(OFFSETS, ends):
            if off < ds + dd and ds < end:
                sys.exit(f"STOP: VO at {off} collides with dialogue at {ds}.")
    print("no VO/dialogue collisions")

    v3 = os.path.join(CUT4, "LOOKS_DRY_v3.mp4")
    cmd = [FF, "-nostdin", "-y", "-i", v3]
    for i in range(1, 10):
        cmd += ["-i", os.path.join(VO, f"L{i:02d}.wav")]

    parts, labels = [], []
    for i, off in enumerate(OFFSETS, 1):
        ms = int(off * 1000)
        parts.append(f"[{i}:a]adelay={ms}|{ms},volume=1.5[n{i}]")
        labels.append(f"[n{i}]")
    parts.append("".join(labels) +
                 f"amix=inputs={len(labels)}:duration=longest:normalize=0[vo]")
    parts.append("[vo]asplit=2[vsc][vmx]")
    parts.append("[0:a]volume=1.0[base]")
    parts.append("[base][vsc]sidechaincompress=threshold=0.045:ratio=8:"
                 "attack=12:release=350[ducked]")
    parts.append("[ducked][vmx]amix=inputs=2:duration=first:normalize=0,"
                 "loudnorm=I=-14:TP=-1:LRA=11,alimiter=limit=0.97,"
                 "aresample=48000[out]")

    out = os.path.join(CUT4, "LOOKS_DRY_v4.mp4")
    cmd += ["-filter_complex", ";".join(parts), "-map", "0:v", "-map", "[out]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(out):
        sys.exit("ffmpeg failed:\n" + r.stderr[-2500:])

    e = subprocess.run([FF, "-nostdin", "-i", out],
                       capture_output=True, text=True).stderr
    for l in e.split("\n"):
        if "Duration" in l or "Stream #" in l:
            print("   ", l.strip()[:110])
    print("->", out)

if __name__ == "__main__":
    main()
