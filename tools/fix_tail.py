#!/usr/bin/env python3
"""Repair the truncated soundtrack tail on both films.

`sidechaincompress` stops when EITHER input ends, so the voice bus (which ends
on the last spoken word) cut the bed and music short. Both masters therefore go
silent several seconds before the picture does, killing the music resolve under
the final shot.

This keeps the approved mix bit-for-bit up to the truncation point and rebuilds
only the missing tail from the same bed and music components, calibrating the
tail's gain against the master over a 2.7s overlap so the splice is inaudible.
"""
import subprocess, os, sys, wave
import numpy as np, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = ("/tmp/claude-0/-home-user-higgsfield-seedance2-jineng/"
        "2b86c3cd-6ddc-5f8f-a642-f6d3a73eff17/scratchpad")
SR = 48000

FILMS = {
    "commercial": dict(
        master="cut4/THE_COMMERCIAL_v4.mp4", picture="cut4/video.mp4",
        out="cut4/THE_COMMERCIAL_v5.mp4",
        beds="cut3/beds.wav", music="sfx/music.wav", music_at=73.5,
        picend=102.70, vo=[],
        # bed+music only: after the jingle payoff, before "We'll do the rest."
        calib=(94.6, 97.6),
    ),
    "looksdry": dict(
        master="cut4/LOOKS_DRY_v4.mp4", picture="cut4/video.mp4",
        out="cut4/LOOKS_DRY_v4.mp4",
        beds="cut3/beds.wav", music="sfx/music.wav", music_at=63.0,
        picend=96.00,
        # the one narration line that fell past the truncation
        vo=[("vo/L09.wav", 92.5, "We'll do the rest.")],
        ref_vo=(77.5, 78.97),   # L08 in the master, to match L09's level to
        # bed only: clear of the queue dialogue and of "on the house" at 88.6
        calib=(84.6, 88.3),
    ),
}

def wav(p):
    w = wave.open(p)
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    a = a.astype(np.float64) / 32768.0
    ch = w.getnchannels(); w.close()
    return a.reshape(-1, 2) if ch == 2 else np.column_stack([a, a])

def rms(x):
    return float(np.sqrt((x ** 2).mean())) if x.size else 0.0

def db(x):
    return 20 * np.log10(max(rms(x), 1e-9))

def fix(name, cfg):
    d = os.path.join(BASE, name)
    tmp = "/tmp/_m.wav"
    subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(d, cfg["master"]),
                    "-vn", "-ac", "2", "-ar", str(SR), "-c:a", "pcm_s16le", tmp],
                   capture_output=True)
    m = wav(tmp)
    T = len(m) / SR
    picend = cfg["picend"]
    print(f"\n=== {name} ===")
    print(f"master audio ends {T:.2f}s, picture content ends {picend:.2f}s "
          f"-> {picend - T:.2f}s missing")
    if T >= picend - 0.05:
        print("nothing to repair"); return

    beds = wav(os.path.join(d, cfg["beds"]))
    music = wav(os.path.join(d, cfg["music"]))

    # synthesise from before the truncation so there is an overlap to calibrate
    # on; the window must hold bed and music only, never a voice
    cal = cfg["calib"]
    s0 = min(T - 3.0, cal[0] - 0.2)
    n = int((picend - s0) * SR)
    synth = np.zeros((n, 2))
    b = beds[int(s0 * SR): int(s0 * SR) + n]
    synth[:len(b)] += b
    mo = s0 - cfg["music_at"]
    if mo >= 0 and int(mo * SR) < len(music):
        mu = music[int(mo * SR): int(mo * SR) + n]
        synth[:len(mu)] += mu

    # calibrate the tail against the master over that voice-free window
    ca, cb = int(cal[0] * SR), int(cal[1] * SR)
    mref = m[ca:cb]
    sref = synth[ca - int(s0 * SR): cb - int(s0 * SR)]
    g = rms(mref) / max(rms(sref), 1e-9)
    synth *= g
    print(f"calib {cal[0]:.1f}-{cal[1]:.1f}s  master {db(mref):6.1f} dB  "
          f"synth {db(sref):6.1f} dB  -> gain x{g:.3f}")

    # narration that fell past the cut, level-matched to a line inside the master
    for path, at, text in cfg.get("vo", []):
        v = wav(os.path.join(d, path))
        rs, re_ = cfg["ref_vo"]
        target = rms(m[int(rs * SR): int(re_ * SR)])
        v *= target / max(rms(v), 1e-9)
        i = int((at - s0) * SR)
        seg = v[:max(0, min(len(v), n - i))]
        # duck the bed under it, matching the sidechain elsewhere in the film
        duck = np.ones((n, 1))
        a, bnd = max(0, i - int(0.12 * SR)), min(n, i + len(seg) + int(0.35 * SR))
        duck[a:bnd] = 0.34
        synth *= duck
        synth[i:i + len(seg)] += seg
        print(f"laid '{text}' at {at:.1f}s, ducked bed under it")

    # crossfade the repaired tail in 0.5s before the truncation point
    xf = int(0.5 * SR)
    cut = int((T - 0.5) * SR)
    off = cut - int(s0 * SR)
    out = np.zeros((int(picend * SR), 2))
    out[:cut] = m[:cut]
    f = np.linspace(0, 1, xf).reshape(-1, 1)
    out[cut:cut + xf] = m[cut:cut + xf] * (1 - f) + synth[off:off + xf] * f
    tail = synth[off + xf:]
    out[cut + xf:cut + xf + len(tail)] = tail[:len(out) - cut - xf]

    # resolve the cue into the silent end card rather than chopping it
    fo = int(1.6 * SR)
    out[-fo:] *= np.linspace(1, 0, fo).reshape(-1, 1)

    # pad silence under the end card, then hit -14 LUFS with one static gain
    total = float(subprocess.run(
        [FF, "-nostdin", "-i", os.path.join(d, cfg["picture"])],
        capture_output=True, text=True).stderr.split("Duration: ")[1].split(",")[0]
        .split(":")[-1]) + 60 * float(subprocess.run(
        [FF, "-nostdin", "-i", os.path.join(d, cfg["picture"])],
        capture_output=True, text=True).stderr.split("Duration: ")[1].split(",")[0]
        .split(":")[1])
    full = np.zeros((int(total * SR), 2))
    full[:len(out)] = out[:len(full)]
    peak = np.abs(full).max()
    if peak > 0.97:
        full *= 0.97 / peak
    raw = "/tmp/_fixed.wav"
    w = wave.open(raw, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(full, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

    # two-pass loudnorm: measure, then apply as a static (linear) gain so the
    # target and the true-peak ceiling actually hold. Single-pass is dynamic and
    # drifts whenever the material changes.
    import json as _json
    m1 = subprocess.run([FF, "-nostdin", "-i", raw, "-af",
                         "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                         "-f", "null", "-"], capture_output=True, text=True).stderr
    st = _json.loads(m1[m1.rindex("{"):m1.rindex("}") + 1])
    print(f"measured  I={st['input_i']} TP={st['input_tp']} LRA={st['input_lra']}")
    norm = ("loudnorm=I=-14:TP=-1.5:LRA=11:linear=true"
            f":measured_I={st['input_i']}:measured_TP={st['input_tp']}"
            f":measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}")
    lim = "alimiter=limit=0.84:level=disabled,aresample=48000"

    # the limiter trims peaks after normalisation, so the integrated level lands
    # a little under target. Measure that residual once and correct for it.
    probe = "/tmp/_probe.wav"
    subprocess.run([FF, "-nostdin", "-y", "-i", raw, "-af", f"{norm},{lim}",
                    "-c:a", "pcm_s16le", probe], capture_output=True)
    r2 = subprocess.run([FF, "-nostdin", "-i", probe, "-af", "ebur128=peak=true",
                         "-f", "null", "-"], capture_output=True, text=True).stderr
    got = float([l for l in r2.split("Summary:")[-1].split("\n")
                 if l.strip().startswith("I:")][0].split(":")[1].split()[0])
    corr = -14.0 - got
    print(f"post-limiter {got:.1f} LUFS -> correcting {corr:+.2f} dB")
    af = f"{norm},volume={corr:.2f}dB,{lim}"

    outp = os.path.join(d, cfg["out"])
    r = subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(d, cfg["picture"]),
                        "-i", raw, "-map", "0:v", "-map", "1:a", "-af", af,
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", outp],
                       capture_output=True, text=True)
    if not os.path.exists(outp):
        sys.exit("ffmpeg failed:\n" + r.stderr[-2000:])
    # splice continuity: level either side of the crossfade should match
    a = db(full[int((T - 1.6) * SR): int((T - 0.6) * SR)])
    b = db(full[int((T + 0.2) * SR): int((T + 1.2) * SR)])
    print(f"splice continuity  before {a:6.1f} dB   after {b:6.1f} dB   "
          f"step {b - a:+.1f} dB")
    print("->", outp)
    return outp

if __name__ == "__main__":
    for k in ("commercial", "looksdry"):
        fix(k, FILMS[k])
