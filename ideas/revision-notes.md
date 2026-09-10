# Revision notes — what's wrong and how to fix it

Honest diagnosis of `THE_COMMERCIAL.mp4` v1. Most of this applies to LOOKS DRY
too.

---

# AUDIO

## 1. Twenty-one independent room tones (worst offender)

Every clip generated its own ambience. So across fifteen shots in the *same
hardware store*, the fluorescent hum changes character fifteen times. The ear
notices instantly even when the eye doesn't — it's why the film feels stitched
rather than shot.

**Fix:** generate **one continuous ambience bed per location** and lay it under
the whole scene, then mute or heavily duck the per-clip native audio. Four beds
cover the film: store-day, store-night, kitchen-night, rain. Native audio stays
only where it carries a specific event — the stamp, the phone ring, the shutter.

## 2. There is no music

The shot list says *"music enters at shot 16, first time."* I never generated
any. The turn — the whole emotional pivot of the film — lands on room tone.
That's not a subtle miss, it's a missing element.

**Fix:** one cue, ~40s, entering at shot 16 and resolving under 21. Sparse and
warm; nothing that announces itself. The point of holding music back for 75
seconds is that its arrival *is* the emotional event.

## 3. Dialogue is dubbed, not synced

I generated the talking shots silent and laid TTS over the top. The mouths move,
the words don't match. On a close two-shot that reads as a badly dubbed film.

**Fix:** Seedance 2.5 accepts `audio_references`. Generate the line **first**,
pass it into the video generation, and the model lip-syncs to the actual take.
I had this capability the whole time and used the worse method.

## 4. The performances aren't directed

Preset voices reading text with no delivery notes. Carol's "Mm." is the entire
joke of shot 4 and it came back as a neutral syllable. The jingle is supposed to
land three different ways — thrilled, drained, earned — and all three readings
are identical because I sent identical prompts.

**Fix:** write delivery direction into each line, generate **3 variants per
line**, and pick. At ~1 credit a take this is nearly free and it's the
difference between actors and text-to-speech.

## 5. No mix discipline

Everything is `amix` at fixed gains. The ambience doesn't duck under dialogue,
so the lines fight the room instead of sitting on top of it. And there's no
loudness normalisation, so shot-to-shot level jumps around.

**Fix:** sidechain-compress the bed against the dialogue track, then normalise
the master to **-14 LUFS** (the social platform target) with a true-peak ceiling
of -1 dBTP.

---

# STORY

## 1. Nothing is actually at stake

"The store is quiet" is a mood, not a stake. Dale never stands to *lose*
anything nameable. Compare LOOKS DRY, which had an unopened envelope on the
bench — one silent shot that told you the business was in trouble. This film has
no equivalent, so the low point plays as mild sadness rather than danger.

**Fix:** name the cost in act one and give it a face. A lease renewal on the
counter. A letter he doesn't open. A number written on a pad. One shot, no
dialogue, and the whole film gains weight.

## 2. Carol's turn is unearned

She is dry and unimpressed for seventy-five straight seconds, and then she is
the one who says *"put the hammer one on."* That's a reversal with no
groundwork. Right now she reads as dismissive and then inexplicably supportive.

**Fix:** plant it. One earlier beat where she nearly laughs and hides it, or
where she defends him to somebody else. Then the turn is a reveal — she was
never dismissive, she was *protecting* him — rather than a switch being flipped.

## 3. The false fix costs him nothing

He makes the boring version, they watch it, she says "it's fine," he moves on.
For a false fix to work the safe choice has to be *tempting* and the wrong
choice has to hurt.

**Fix:** he's already booked and paid for the airtime, and the boring version is
the one queued to run. Now choosing means risking money he doesn't have, and
Carol's line becomes a genuine push rather than a suggestion.

## 4. We never see the commercial — the biggest miss

The film is called THE COMMERCIAL. We watch him make it, agonise over it, and
air it. **We never see a single frame of it.** The funniest asset in the entire
production — a hammer mascot, a homemade jingle, a wonky zoom — and it happens
entirely off-screen.

**Fix:** 4 seconds of the actual finished ad, cut in as broadcast footage at
shot 17 — deliberately cheap, wrong aspect, over-saturated, bad zoom, jingle
peaking. It is the single highest-value shot available and it costs one
generation.

## 5. Two payoffs doing the same job

The kid asking for the jingle and the crowd filming him are the same beat twice.
The second one adds nothing the first didn't.

**Fix:** cut the kid, keep the crowd. Or better — make the kid the *reason* the
crowd forms, so they escalate instead of repeat.

## 6. The ending asserts success without earning it

The phone rings, so it worked. But *why* it worked is never said, and that's the
actual point of the story — it worked **because it was unmistakably him**.

**Fix:** one line from a customer. "My kid won't stop singing it." Now the
ending explains itself, and the theme lands without anyone stating it.

---

# Priority order

| # | Change | Cost | Impact |
|---|---|---|---|
| 1 | Show the commercial (4s insert) | 1 video gen | Highest |
| 2 | Music cue entering at the turn | 1 audio gen | Highest |
| 3 | One ambience bed per location | 4 audio gens | High |
| 4 | Name the stake in act one | 1 image + 1 video | High |
| 5 | Lip-sync dialogue via `audio_references` | 6 video regens | High |
| 6 | Direct + triple the dialogue takes | ~21 audio gens | Medium |
| 7 | Plant Carol's turn | 1 image + 1 video | Medium |
| 8 | Customer line at the end | 1 audio gen | Medium |
| 9 | Proper mix: ducking + -14 LUFS | free, ffmpeg | Medium |
| 10 | Cut the kid or escalate it | free, edit | Low |

Items 1–3 and 9 are cheap and fix most of what's wrong with how the film
*feels*. Items 4, 7 and 8 are what make it a story rather than a sequence.

Rough cost for all ten: **~350 credits** against the 1,472 remaining.

---

# CRITICAL: unlimited does not reach the MCP surface

Tested `use_unlim: true` explicitly against every candidate model. All rejected:

| Model | Catalog `supports_unlim` | Actual result |
|---|---|---|
| `nano_banana_2` | true | substituted to `nano_banana_flash` → *"Unlimited generations aren't supported for nano_banana_flash"* |
| `nano_banana` | true | *"Unlimited generations aren't supported for nano_banana"* |
| `nano_banana_pro` | true | *"Unlimited generations aren't supported for nano_banana_pro"* |
| `seedream_v5_pro` | true | *"Unlimited generations aren't supported for seedream_v5_pro"* |
| `seedance_2_5` | — | *"Unlimited generations aren't supported for seedance_2_5"* |
| `seedance_2_0` | true | *"Unlimited generations aren't supported for seedance_2_0"* |

**The catalog's `supports_unlim` flag describes model capability, not account
entitlement on this connection.** It is true in the listing for models that then
reject the flag outright. Do not treat it as a signal.

Together with `unlim.available: false` returned by the very first
`models_explore` call, the conclusion is unambiguous: **the web unlimited
allowance does not extend to the MCP/API surface. Generation from an MCP session
always costs credits, on every model.**

There is a second, compounding problem. `nano_banana_2` and `nano_banana_pro`
are silently substituted to `nano_banana_flash`, which is *specifically* the
variant excluded from unlimited. So even if the entitlement did reach this
surface, the substitution would route around it.

## What this changes

Two films were produced on credits — ~1,941 spent — that should have been
produced in the browser for free. This should have been settled with a single
test call before any production work started.

**New rule: this session designs, the browser generates.** The deliverable from
here is a paste-ready prompt pack per shot — model, aspect ratio, resolution,
duration, references, and the full prompt text — that gets run at
higgsfield.ai where the unlimited applies. MCP generation only when the user
explicitly authorises spending the remaining balance for something the browser
cannot do.

**Remaining balance: 1,472 credits.** Preserve it.

---

# ROOT CAUSE OF THE AUDIO: Seedance invents its own dialogue

A spectrogram of shot 20's native audio settled it. The first 2.4 seconds show
evenly-spaced harmonic bands from ~200 Hz to 4800 Hz with visible vibrato —
the signature of **a sustained human voice singing**, not room tone and not
laughter. The prompt asked only for "warm layered laughter, no intelligible
speech."

`generate_audio: true` does not mean "give me ambience." It means the model
writes and performs its own audio track, **including invented vocal
performances**, on top of whatever the prompt asked for. Fourteen shots carried
one. Then TTS dialogue went over the top of them.

That is why the audio "doesn't make sense": on several shots **two different
voices are singing two different things simultaneously.** No amount of level
balancing or ducking fixes that, which is why the v2 mix pass — unified room
tone, sidechain ducking, −14 LUFS — improved the polish and left the actual
problem untouched.

## The fix

**Strip every native audio track (`-an`) and build the soundtrack from
nothing.** v3 does this:

| Element | Source | Cost |
|---|---|---|
| Store bed | pink noise + 100/200 Hz ballast hum | free, synthesised |
| Store-night bed | brown noise + 62 Hz compressor | free |
| Kitchen bed | filtered brown noise | free |
| Rain bed | white noise, tremolo-modulated | free |
| Music | four sine-triad chords, slow swell, echo | free |
| Telephone bell | dual sine + 22 Hz tremolo | free |
| Dialogue | existing ElevenLabs takes | already paid |

Entire soundtrack rebuilt for **zero credits**. Synthesised beds also beat
generated ones for this job: they are perfectly consistent, loop cleanly, and
carry no risk of a model hallucinating a voice into them.

## Rule for all future generation

**Always set `generate_audio: false`.** Native audio is unusable in a film with
its own dialogue — it will invent competing performances. Design sound in the
edit, where it can be controlled.

---

# THE TRUNCATED TAIL — both films shipped silent under their final shot

Found while cutting LOOKS DRY's narration, and it was already in **both**
delivered masters.

`sidechaincompress` ends when **either** input ends — not when the main input
ends. The voice bus stops on the last spoken word, so it took the bed and the
music down with it:

| Film | Picture content | Audio ended | Silent for |
|---|---|---|---|
| THE COMMERCIAL v4 | 102.70s | **98.79s** | 3.91s |
| LOOKS DRY v3 | 96.00s | **89.64s** | 6.36s |

Both films therefore went dead quiet across their final shot — the hammer on the
wall, the sign lit at night — and the music cue never resolved. It is the one
place in each film where the score is doing the most work, and there was nothing
there. The endcard silence that follows is deliberate; this was not.

It hid because every check had been run on the *mix*, never on the *duration*.
Level, ducking and loudness all measured fine over the audio that existed.

## Fix

`apad` the sidechain key so the bed governs the length, or verify the audio
stream length against the picture length after every mix. `tools/fix_tail.py`
does the repair on the delivered masters: it keeps the approved mix untouched up
to the truncation point, rebuilds the missing tail from the same bed and music
components, and calibrates the tail's gain against the master over a **voice-free**
window so the splice is inaudible.

Getting that window wrong is the trap — the first calibration pass caught the
last dialogue take inside it and came out 5-10 dB hot.

## Two mastering bugs found in the same pass

1. **Single-pass `loudnorm` is dynamic** and drifted as soon as the tail changed.
   Replaced with a measured two-pass `linear=true` normalisation.
2. **`alimiter` auto-levels by default** (`level` is enabled), which renormalises
   the peak *up* to the limit and undoes the normalisation that just ran. That is
   why targeting -14 LUFS / -1 dBTP kept producing -13.2 LUFS / 0.0 dBFS.
   `alimiter=limit=0.84:level=disabled` is the correct form.

## Delivered

| File | Length | Integrated | True peak |
|---|---|---|---|
| `THE_COMMERCIAL_v5.mp4` | 1:46.80 | -14.0 LUFS | -1.4 dBTP |
| `LOOKS_DRY_v4.mp4` | 1:40.00 | -14.3 LUFS | -1.2 dBTP |

Both now carry sound across the whole picture and resolve the cue into the
silent serviceaihq.com card.

---

# WHY THE AUDIO STILL SOUNDED WRONG — I built it out of nothing

"Rebuilt the soundtrack for zero credits" was the wrong thing to be proud of.
Measured, here is what I had actually made:

| Element | Measurement | What that means |
|---|---|---|
| Music | flatness 0.0000, **99.9%** of energy in 30 bins, nothing above **196 Hz** | Three bare sine waves at 131/165/196 Hz. Not music — a test tone, sitting in the same range as the fluorescent hum, so the cue's arrival read as the buzz getting louder |
| Beds | level std **0.3–1.0 dB** | Steady-state noise with no events. My "rain" varied 1.0 dB across 30s; real rain varies **25.9 dB** |
| Narration | rolloff **2.1 kHz**, 0.13% energy >5 kHz | Below telephone bandwidth (a landline reaches 3.4 kHz) — and it carried the entire sales argument |
| Dialogue | rolloff **1523 Hz to 11273 Hz** | An 8x spread between two characters in the same room. The ear reads that as badly glued-together recordings |

Carol's "Put the hammer one on" — the turn of the whole film — was a 1898 Hz take.

## What fixed it

**OpenArt has no audio model.** Every model in its catalogue is image or video;
audio only ever arrives bundled inside a video generation, which is exactly how
the narration ended up at 2.1 kHz. It cannot produce a cue or a clean voice.

**Adobe Stock can**, and its audio library is free-tier. Licensed and used:

| Asset | Use |
|---|---|
| Inspiration for Piano (romantic documentary background) | the cue, both films — a shared sound is the campaign |
| Kitchen Ambience Professional or Commercial | bakery kitchen, kitchen-night |
| Heavy Rain On Parked Car Int | the rainy car park |
| Coffee Shop Interior Light Restaurant Walla | the queue, the crowd |
| School Hallway Quiet Distant Footsteps | quiet shop interiors |
| Empty Warehouse Interior Night | store-night, car, home, exterior night (separated by EQ) |

The per-shot location map was never written down, so it was **recovered by
spectral fingerprinting** every `b##.wav` against the six source beds — 0.96 to
0.999 confidence. Voice placements were recovered the same way, by correlating
each take against the finished master: 11 of 13 confirmed to 0.01s.

**The voices were repaired, not re-recorded.** Adobe's speech enhancer is the
right tool but its async result is unreachable in a headless session. Instead
the missing top end is synthesised from the harmonics still present, and each
take is driven until its high/low band ratio matches the naturally-bright takes
in the same film (0.14). Narration went 2156 -> 7266 Hz, ratio 0.0021 -> 0.1448;
every voice now lands within 0.138-0.145 instead of spanning 0.0002-0.22.

## Three mixing lessons, all measured

1. **Dynamic `loudnorm` lifts quiet passages.** It reached -14 LUFS by raising
   the room tone ~10 dB, leaving dialogue only 5 dB above ambience. Linear mode
   preserves the balance at the cost of ~2 LU. Balance wins.
2. **`alimiter` auto-levels by default** — `level` enabled renormalises the peak
   back up to the limit, undoing the normalisation that just ran.
3. **-14 LUFS is not free.** With honest dynamic range it costs 4-7 dB of peak
   limiting. Shipped at -15.9/-16.4 LUFS with dialogue **+15.6 to +20.2 dB over
   room tone**, which is the professional range. Platforms normalise anyway.

## Delivered

| File | Length | Integrated | True peak | Dialogue over room |
|---|---|---|---|---|
| `THE_COMMERCIAL_v6.mp4` | 1:46.80 | -15.9 LUFS | -1.5 dBTP | +15.6 to +18.0 dB |
| `LOOKS_DRY_v5.mp4` | 1:40.00 | -16.4 LUFS | -1.5 dBTP | +18.8 to +20.2 dB |

## Still outstanding

- **Both masters are mono.** The stock beds are stereo and the pipeline
  collapsed them; stereo ambience is a real width gain still on the table.
- **Dialogue is still dubbed, not lip-synced.** Seedance accepts
  `audio_references` — generate the line first, pass it in, and the model syncs
  to the actual take.
- **The narration is repaired, not performed.** Band extension cannot invent a
  read. A real TTS pass is the only way to fix delivery, and it also unlocks the
  3-variants-per-line direction both films still want.
