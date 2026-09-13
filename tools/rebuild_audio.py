#!/usr/bin/env python3
"""Rebuild both soundtracks from real recordings.

What was wrong: the music was three bare sine waves (99.9% of energy in 30 bins,
nothing above 196 Hz) and the beds were steady noise with no events in them
(1 dB of level variation across 30s, where real rain varies by 26 dB). The
voices were below telephone bandwidth and inconsistent by 8x between characters.

What this does: real Adobe Stock recordings for every location, the licensed
piano cue for the turn, and the bandwidth-restored voices. Ducking is computed
here rather than with ffmpeg's sidechaincompress, which ends when either input
ends and silently truncated both films before.
"""
import numpy as np, wave, subprocess, imageio_ffmpeg, os, json, sys

FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 48000
BASE = ("/tmp/claude-0/-home-user-higgsfield-seedance2-jineng/"
        "2b86c3cd-6ddc-5f8f-a642-f6d3a73eff17/scratchpad")
STOCK = os.path.join(BASE, "stock")

def read(p, tmp="/tmp/_rb.wav"):
    subprocess.run([FF, "-nostdin", "-y", "-i", p, "-ac", "1", "-ar", str(SR),
                    "-c:a", "pcm_s16le", tmp], capture_output=True)
    w = wave.open(tmp)
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    w.close(); return a

def band(a, lo, hi):
    n = 1 << (len(a) - 1).bit_length()
    X = np.fft.rfft(a, n); f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if lo: g *= 1 / (1 + (lo / np.maximum(f, 1e-9)) ** 6)
    if hi: g *= 1 / (1 + (np.maximum(f, 1e-9) / hi) ** 6)
    return np.fft.irfft(X * g, n)[:len(a)]

def loop_to(a, n, xf=int(0.75 * SR)):
    """Seamless loop of a short recording out to n samples."""
    if len(a) >= n: return a[:n]
    body = a[:-xf] if len(a) > 2 * xf else a
    out = [body]
    total = len(body)
    while total < n + xf:
        nxt = a.copy()
        f = np.linspace(0, 1, xf)
        joint = out[-1][-xf:] * (1 - f) + nxt[:xf] * f
        out[-1] = out[-1][:-xf]
        out.append(joint); out.append(nxt[xf:-xf] if len(nxt) > 2 * xf else nxt[xf:])
        total = sum(len(x) for x in out)
    return np.concatenate(out)[:n]

def compress(x, thr=0.06, ratio=3.0, atk=0.005, rel=0.20):
    n = max(1, int(0.01 * SR))
    env = np.sqrt(np.convolve(x ** 2, np.ones(n) / n, mode="same")) + 1e-12
    g = np.where(env > thr, (thr / env) ** (1 - 1 / ratio), 1.0)
    ka, kr = max(1, int(atk * SR)), max(1, int(rel * SR))
    g = np.minimum(g, np.convolve(g, np.ones(kr) / kr, mode="same"))
    g = np.convolve(g, np.ones(ka) / ka, mode="same")
    return x * g

def rms(x): return float(np.sqrt((x ** 2).mean())) if len(x) else 0.0
def db(x): return 20 * np.log10(max(rms(x), 1e-9))

# location -> (stock file, band, gain). Several locations share a recording and
# are separated by EQ, which is how a real mix reuses a room tone.
PROFILE = {
    "quiet":     ("quiet.wav",   (40, 9000),  1.00),
    "kitchen":   ("kitchen.wav", (40, 8000),  1.00),
    "rain":      ("rain.wav",    (60, 12000), 1.00),
    "walla":     ("walla.wav",   (60, 8000),  1.00),
    "night":     ("night.wav",   (30, 3500),  0.80),
    "car":       ("night.wav",   (30, 1200),  0.90),
    "home":      ("night.wav",   (30, 4000),  0.85),
    "night_ext": ("night.wav",   (40, 6000),  0.80),
    "broadcast": ("quiet.wav",   (300, 3400), 1.00),
}

FILMS = {
    "commercial": dict(
        video="cut4/video.mp4", out="cut4/THE_COMMERCIAL_v6.mp4", picend=102.70,
        shots=[("b01",4.5,"quiet"),("b02",4.0,"quiet"),("b03",4.5,"quiet"),
               ("b04",5.5,"kitchen"),("b05",4.5,"kitchen"),("b06",5.5,"kitchen"),
               ("b07",5.0,"quiet"),("b08",4.0,"quiet"),("b09",4.0,"quiet"),
               ("b10",6.5,"rain"),("b11",5.5,"quiet"),("b12",5.5,"kitchen"),
               ("b13",4.5,"kitchen"),("b14",6.0,"night"),("b15",4.0,"night"),
               ("b16",5.5,"night"),("bAD",3.2,"broadcast"),("b17",4.5,"quiet"),
               ("b18",4.5,"quiet"),("b20",6.0,"walla"),("b21",5.5,"quiet")],
        music_at=73.5,
        vo=[(1.0,"L01"),(5.2,"L02"),(9.0,"L03a"),(10.2,"L03b"),(19.0,"L04"),
            (46.9,"L05"),(54.3,"L06"),(64.8,"L07"),(74.4,"L08"),(97.8,"L09")],
        dia=[(13.81,"a04_dale_making"),(16.31,"a04b_carol_mm"),(23.91,"a06_dale_jingle"),
             (49.21,"a11_dale_flat"),(57.11,"a12_carol_fine"),(76.11,"a16_carol_hammer"),
             (91.81,"a19_dale_jingle2")],
        foley=[(83.0,"ring",0.5),(85.2,"ring",0.5)],
    ),
    "looksdry": dict(
        video="cut4/video.mp4", out="cut4/LOOKS_DRY_v5.mp4", picend=96.00,
        shots=[("b01",3.5,"night_ext"),("b02",4.0,"night_ext"),("b03",4.5,"kitchen"),
               ("b04",3.5,"kitchen"),("b05",4.0,"quiet"),("b06",4.0,"quiet"),
               ("b07",3.0,"quiet"),("b08",3.5,"kitchen"),("b09",5.0,"kitchen"),
               ("b10",6.5,"quiet"),("b11",7.0,"car"),("b12",4.5,"home"),
               ("b13",6.0,"kitchen"),("b14",4.0,"kitchen"),("b15",5.5,"kitchen"),
               ("b16",4.5,"home"),("b17",3.5,"quiet"),("b18",4.5,"walla"),
               ("b19",6.0,"quiet"),("b20",5.0,"quiet"),("b21",4.0,"night_ext")],
        music_at=63.0,
        vo=[(1.0,"L01"),(8.5,"L02"),(24.0,"L03"),(27.5,"L04"),(49.0,"L05"),
            (54.0,"L06"),(64.0,"L07"),(77.5,"L08"),(92.5,"L09")],
        dia=[(20.61,"a06_miles_post"),(35.71,"a10a_renee_dry"),(38.20,"a10b_miles_kinda"),
             (39.91,"a10c_renee_kinda"),(43.11,"a11_renee_croissant"),(88.61,"a20_renee_house")],
        foley=[(0.3,"alarm",0.6),(4.0,"stamp",0.6)],
    ),
}

def pick_music(pi, need):
    """Choose a passage that starts sparse and rises, so the cue's arrival is
    the emotional event rather than a wall of piano."""
    n = int(need * SR); step = int(2.0 * SR)
    best, bs = 0, -1e9
    for s in range(0, len(pi) - n, step):
        seg = pi[s:s + n]
        head = rms(seg[:int(6 * SR)]); tail = rms(seg[int(n * 0.45):int(n * 0.8)])
        if head < 1e-5: continue
        score = (tail / head) + 0.4 * (rms(seg) / (np.abs(pi).max() + 1e-9))
        if score > bs: bs, best = score, s
    return best

def build(film, cfg):
    d = os.path.join(BASE, film); vf = os.path.join(d, "voice_fixed")
    picend = cfg["picend"]; N = int(picend * SR)
    print(f"\n=== {film} ===")

    # ---- beds: one continuous stream per location, sliced per shot ----
    src = {k: read(os.path.join(STOCK, v[0])) for k, v in
           {k: PROFILE[k] for k in {s[2] for s in cfg["shots"]}}.items()}
    need = {}
    for _, dur, loc in cfg["shots"]: need[loc] = need.get(loc, 0.0) + dur
    streams, head = {}, {}
    for loc, secs in need.items():
        f, bd, g = PROFILE[loc]
        s = loop_to(src[loc], int((secs + 4) * SR))
        s = band(s, *bd) * g
        s /= (rms(s) + 1e-12)          # normalise, level set below
        streams[loc], head[loc] = s, 0

    bed = np.zeros(N); t = 0.0
    for name, dur, loc in cfg["shots"]:
        n = int(dur * SR); i = int(t * SR)
        seg = streams[loc][head[loc]:head[loc] + n]
        head[loc] += n
        if len(seg) < n: seg = np.pad(seg, (0, n - len(seg)))
        xf = int(0.12 * SR)            # short blend at each shot boundary
        if i > 0 and xf < n:
            f = np.linspace(0, 1, xf)
            bed[i:i + xf] = bed[i:i + xf] * (1 - f) + seg[:xf] * f
            bed[i + xf:i + n] = seg[xf:]
        else:
            bed[i:i + n] = seg
        t += dur
    bed *= 0.0085 / (rms(bed) + 1e-12)  # dialogue lands ~18 dB above the room,
    # which is where speech belongs. Costs master loudness; clarity wins.

    # ---- music: the licensed piano, entering at the turn ----
    pi = read(os.path.join(STOCK, "piano.wav"))
    m_at = cfg["music_at"]; m_need = picend - m_at
    s0 = pick_music(pi, m_need)
    mus = pi[s0:s0 + int(m_need * SR)].copy()
    fi = int(2.5 * SR); mus[:fi] *= np.linspace(0, 1, fi)
    fo = int(4.0 * SR); mus[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    music = np.zeros(N); music[int(m_at * SR):int(m_at * SR) + len(mus)] = mus
    music *= 0.045 / (rms(music[int(m_at * SR):]) + 1e-12)
    print(f"  music from {s0/SR:.1f}s of the cue, entering at {m_at:.1f}s")

    # ---- foley ----
    fol = np.zeros(N)
    for at, name, g in cfg.get("foley", []):
        p = os.path.join(d, "sfx", name + ".wav")
        if not os.path.exists(p): continue
        x = read(p) * g; i = int(at * SR)
        fol[i:i + len(x)] += x[:max(0, N - i)]

    # ---- voices ----
    voice = np.zeros(N); laid = 0
    for at, name in cfg["vo"] + cfg["dia"]:
        p = os.path.join(vf, name + ".wav")
        if not os.path.exists(p):
            print(f"  MISSING {name}"); continue
        x = read(p); i = int(at * SR)
        x = x[:max(0, N - i)]
        voice[i:i + len(x)] += x * 1.0
        laid += 1
    voice *= 0.12 / (rms(voice[np.abs(voice) > 1e-4]) + 1e-12)

    # Level the dialogue. Takes arrived at wildly different levels and the
    # master was previously being pushed 7 dB into a limiter to reach -14 LUFS,
    # which flattens the voice peaks. Compressing the voice bus instead raises
    # the integrated level honestly and evens the performances out.
    pre = rms(voice[np.abs(voice) > 1e-4])
    voice = compress(voice)
    voice *= pre / (rms(voice[np.abs(voice) > 1e-4]) + 1e-12) * 1.35
    print(f"  voices laid: {laid}/{len(cfg['vo']) + len(cfg['dia'])}, bus levelled")

    # ---- duck the bed and music under any voice (computed, not sidechained) ----
    env = np.sqrt(np.convolve(voice ** 2, np.ones(int(0.03 * SR)) / int(0.03 * SR), mode="same"))
    thr = 0.02
    gr = np.ones(N)
    gr[env > thr] = 0.55
    k = int(0.25 * SR)
    gr = np.convolve(gr, np.ones(k) / k, mode="same")       # smooth attack/release
    ducked = (bed + music + fol) * gr

    mix = ducked + voice

    # Gentle master-bus compression. -14 LUFS at -1.5 dBTP is only reachable
    # with a peak-to-loudness ratio under ~12.5 dB; without this the limiter was
    # being asked for 5-7 dB, which flattens every voice peak in the film.
    mix = compress(mix, thr=0.10, ratio=2.0, atk=0.010, rel=0.30)
    mix[-int(1.6 * SR):] *= np.linspace(1, 0, int(1.6 * SR))   # resolve into the card

    # ---- pad under the silent end card and master ----
    vdur = float(subprocess.run([FF, "-nostdin", "-i", os.path.join(d, cfg["video"])],
                                capture_output=True, text=True).stderr
                 .split("Duration: ")[1].split(",")[0].split(":")[-1]) + 60 * float(
          subprocess.run([FF, "-nostdin", "-i", os.path.join(d, cfg["video"])],
                         capture_output=True, text=True).stderr
          .split("Duration: ")[1].split(",")[0].split(":")[1])
    full = np.zeros(int(vdur * SR)); full[:len(mix)] = mix[:len(full)]
    pk = np.abs(full).max()
    if pk > 0.97: full *= 0.97 / pk
    raw = f"/tmp/_rb_{film}.wav"
    w = wave.open(raw, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(full, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

    m1 = subprocess.run([FF, "-nostdin", "-i", raw, "-af",
                         "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                         "-f", "null", "-"], capture_output=True, text=True).stderr
    st = json.loads(m1[m1.rindex("{"):m1.rindex("}") + 1])
    # Linear normalisation, deliberately. Dynamic mode reaches -14 but does it
    # by lifting quiet passages: it raised the room tone ~10 dB and left the
    # dialogue only 5 dB above ambience, where it belongs 15-25 dB above.
    # One static gain preserves the balance; the master lands ~2 LU quieter,
    # which every platform normalises anyway.
    norm = ("loudnorm=I=-14:TP=-1.5:LRA=11:linear=true"
            f":measured_I={st['input_i']}:measured_TP={st['input_tp']}"
            f":measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}")
    af = f"{norm},alimiter=limit=0.9:level=disabled,aresample=48000"
    subprocess.run([FF, "-nostdin", "-y", "-i", raw, "-af", af,
                    "-c:a", "pcm_s16le", "/tmp/_probe2.wav"], capture_output=True)
    sm = subprocess.run([FF, "-nostdin", "-i", "/tmp/_probe2.wav", "-af",
                         "ebur128=peak=true", "-f", "null", "-"],
                        capture_output=True, text=True).stderr.split("Summary:")[-1]
    gg = lambda k: [l for l in sm.split("\n") if l.strip().startswith(k)][0].split(":")[1].strip()
    print(f"  master: {gg('I:')}, LRA {gg('LRA:')}, TP {gg('Peak:')}")

    outp = os.path.join(d, cfg["out"])
    subprocess.run([FF, "-nostdin", "-y", "-i", os.path.join(d, cfg["video"]),
                    "-i", raw, "-map", "0:v", "-map", "1:a", "-af", af,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", outp],
                   capture_output=True)
    print(f"  -> {outp}")
    return outp

if __name__ == "__main__":
    for k, v in FILMS.items():
        build(k, v)
