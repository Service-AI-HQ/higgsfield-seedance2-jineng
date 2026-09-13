#!/usr/bin/env python3
"""Assemble THE COMMERCIAL. Skips any shot whose clip is missing, so it can be
run partway through production and again when the rest land."""
import subprocess, imageio_ffmpeg, os, sys, json

BASE = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
CLIPS = os.path.join(BASE, "clips")
AUDIO = os.path.join(BASE, "audio")
CUT = os.path.join(BASE, "cut")
VF = "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:-1:-1,fps=24"

# shot, file, trim_in, screen_duration
EDL = [
    ("01", "c01.mp4", 0.5, 4.5),
    ("02", "c02.mp4", 0.0, 4.0),
    ("03", "c03.mp4", 0.0, 4.5),
    ("04", "c04.mp4", 0.0, 5.5),
    ("05", "c05.mp4", 0.5, 4.5),
    ("06", "c06.mp4", 0.0, 5.5),
    ("07", "c07.mp4", 0.5, 5.0),
    ("08", "c08.mp4", 0.0, 4.0),
    ("09", "c09.mp4", 0.5, 4.0),
    ("10", "c10.mp4", 0.0, 6.5),
    ("11", "c11.mp4", 0.0, 5.5),
    ("12", "c12.mp4", 0.0, 5.5),
    ("13", "c13.mp4", 0.0, 4.5),
    ("14", "c14.mp4", 0.0, 6.0),
    ("15", "c15.mp4", 0.0, 4.0),
    ("16", "c16.mp4", 0.0, 5.5),
    ("17", "c17.mp4", 0.0, 5.0),
    ("18", "c18.mp4", 0.0, 4.5),
    ("19", "c19.mp4", 0.0, 5.5),
    ("20", "c20.mp4", 0.0, 5.5),
    ("21", "c21.mp4", 0.0, 5.5),
]

# dialogue: file, shot it belongs to, offset within that shot, gain
DIA = [
    ("a04_dale_making.mp3",   "04", 0.8, 1.6),
    ("a04b_carol_mm.mp3",     "04", 3.3, 1.6),
    ("a06_dale_jingle.mp3",   "06", 0.9, 1.6),
    ("a11_dale_flat.mp3",     "11", 0.8, 1.5),
    ("a12_carol_fine.mp3",    "12", 3.6, 1.6),
    ("a16_carol_hammer.mp3",  "16", 2.6, 1.7),
    ("a19_dale_jingle2.mp3",  "19", 1.6, 1.6),
]

def has_audio(p):
    return "Audio:" in subprocess.run([FF, "-nostdin", "-i", p],
                                      capture_output=True, text=True).stderr

def main():
    os.makedirs(CUT, exist_ok=True)
    for f in os.listdir(CUT):
        if f.endswith((".mp4", ".txt")):
            os.remove(os.path.join(CUT, f))

    lines, t, offsets, missing = [], 0.0, {}, []
    for shot, fname, tin, dur in EDL:
        src = os.path.join(CLIPS, fname)
        if not os.path.exists(src):
            missing.append(shot)
            continue
        out = os.path.join(CUT, f"s{shot}.mp4")
        cmd = [FF, "-nostdin", "-y", "-ss", str(tin), "-t", str(dur), "-i", src]
        if not has_audio(src):
            cmd += ["-f", "lavfi", "-t", str(dur),
                    "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                    "-map", "0:v:0", "-map", "1:a:0"]
        cmd += ["-vf", VF, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-ac", "2",
                "-t", str(dur), out]
        subprocess.run(cmd, capture_output=True)
        offsets[shot] = t
        t += dur
        lines.append(f"file 's{shot}.mp4'")

    listfile = os.path.join(CUT, "list.txt")
    open(listfile, "w").write("\n".join(lines) + "\n")
    base = os.path.join(CUT, "base.mp4")
    subprocess.run([FF, "-nostdin", "-y", "-f", "concat", "-safe", "0",
                    "-i", listfile, "-c", "copy", base], capture_output=True)

    # mix dialogue only for shots that made it into the cut
    live = [(f, offsets[s] + o, g) for f, s, o, g in DIA
            if s in offsets and os.path.exists(os.path.join(AUDIO, f))]

    final = os.path.join(CUT, "THE_COMMERCIAL.mp4")
    if live:
        cmd = [FF, "-nostdin", "-y", "-i", base]
        for f, _, _ in live:
            cmd += ["-i", os.path.join(AUDIO, f)]
        parts = ["[0:a]volume=0.85[bed]"]
        labels = ["[bed]"]
        for i, (f, off, g) in enumerate(live, start=1):
            ms = int(off * 1000)
            parts.append(f"[{i}:a]adelay={ms}|{ms},volume={g}[d{i}]")
            labels.append(f"[d{i}]")
        parts.append("".join(labels) +
                     f"amix=inputs={len(labels)}:duration=first:"
                     f"dropout_transition=0:normalize=0,alimiter=limit=0.95[out]")
        cmd += ["-filter_complex", ";".join(parts), "-map", "0:v", "-map", "[out]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", final]
        subprocess.run(cmd, capture_output=True)
    else:
        subprocess.run([FF, "-nostdin", "-y", "-i", base, "-c", "copy", final],
                       capture_output=True)

    info = subprocess.run([FF, "-nostdin", "-i", final],
                          capture_output=True, text=True).stderr
    dur = [l.strip() for l in info.split("\n") if "Duration" in l]
    print(f"shots in cut : {len(lines)}/21")
    print(f"missing      : {', '.join(missing) if missing else 'none'}")
    print(f"dialogue laid: {len(live)}/{len(DIA)}")
    print(f"{dur[0] if dur else 'no output'}")
    print(f"-> {final}")
    json.dump(offsets, open(os.path.join(CUT, "offsets.json"), "w"))

if __name__ == "__main__":
    main()
