# Nike-Style Story Slate — AI Studio

**Model:** Seedance 2.5 · **Duration cap:** 15s · **Status:** awaiting story approval

The Nike 15-second structure, which every concept below follows:

| Beat | Time | Job |
|---|---|---|
| Hook | 0–2s | A body, a sound, or a hard cut. No context. |
| Grind | 2–7s | The work. Texture, sweat, repetition, failure. |
| Doubt | 7–9s | The lowest point. Often near-silence. |
| Turn | 9–13s | It breaks open. Cut on the beat. |
| Line | 13–15s | The words land. Then the mark, in silence. |

Rules: voiceover is second-person and declarative. Never explain the product.
The logo is the last thing, and it arrives after the sound stops.

---

## 01 — CREW OF ONE
**For:** social growth · **Hero candidate**

Match-cut ping-pong. A full film set: forty crew, dolly track, lighting rig,
boom operator, clapper snapping shut. Hard cut to one person on a couch with a
laptop — *identical framing, identical result on screen.* We do it three times,
each pair faster than the last, until the cuts are almost strobing. On the final
cut the forty-person crew dissolves mid-frame and only the one person is left,
lit the same way the set was lit.

**Line:** *"You are the crew."*

**Why it works:** the contrast is legible in under a second with no sound. It is
the single most screenshot-able idea on this list.

---

## 02 — THE 3AM CUT
**For:** showreel

Blue monitor glow on a face. The rest of the room is black. Hands move to the
keyboard and we shoot them the way you shoot a fighter's hands being taped —
close, reverent, slow. Cold coffee. A progress bar. A window going from dark to
the first grey of morning behind them. The doubt beat is the cursor blinking on
nothing.

Then the render completes, and the light of what they made floods the room and
paints their face in color for the first time in the film.

**Line:** *"Nobody was watching. That's when you made it."*

---

## 03 — NO BUDGET
**For:** social growth

A montage of everything they don't have, each cut harder than the last: a bank
balance, an empty studio, a rejection email, a door closing, a "we're going in
another direction." The rhythm is punishing.

Then — without any triumphant transition — the shots simply start becoming
beautiful anyway. Same cutting speed, same aggression, but now every frame is
gorgeous. The film never acknowledges the change. That's the whole trick.

**Line:** *"They gave you nothing. You made everything."*

---

## 04 — THE SOUND BEFORE THE PICTURE
**For:** spec vertical (music) · showcases the audio/song capability

Black screen. A heartbeat. A snare enters. A bassline builds. The only image is
a waveform pulsing light across a face in the dark — we are listening, not
watching. The build gets unbearable.

On the drop, the picture explodes into existence and every cut lands on a beat.

**Line:** *"Make the noise. The world will picture it."*

**Why it matters:** this is the one that proves the studio does sound, not just
pixels. It's the differentiator most competitors can't show.

---

## 05 — RUN IT BACK
**For:** showreel · spec vertical

One shot — a runner cresting a hill — generated six ways in rapid fire:
cinematic, anime, 3D, film noir, hand-drawn, photoreal. Cut like a highlight
reel, each version held for barely a beat. The same motion, six universes.

Then it stops. One version holds on screen. The chosen one.

**Line:** *"Take every shot. Keep the best one."*

**Why it works:** it sells iteration speed, which is the actual product.

---

## 06 — THE PITCH
**For:** spec work you send to agencies

A creator walks into a boardroom. Suits, crossed arms, one person already
looking at their phone. The creator doesn't say a word. They just press play.

We never see the screen. We only watch the faces change — the phone goes down,
someone leans forward, the arms uncross.

**Line:** *"Stop describing it. Show them."*

---

## 07 — FIRST FRAME
**For:** showreel opener

Extreme close on an eye opening. Cut inside the idea: a storm of half-formed
images — a face assembling, a city rising, a wave building — all of it flickering
and unfinished and beautiful in its incompleteness. It's chaos, and it's honest
about being chaos.

Then it resolves. Everything snaps into one perfect, still frame.

**Line:** *"Every film starts as a blur. Finish it."*

---

## 08 — THE KID WITH THE PHONE
**For:** social growth

A young creator in a small bedroom, phone propped up on a stack of books.
Intercut with what's actually in their head: enormous cinematic worlds, oceans,
armies, cities at dusk. We keep cutting between the two, and the gap between the
bedroom and the vision is the entire tension of the film.

The turn is the two spaces merging — the bedroom wall becomes the ocean.

**Line:** *"The only thing between you and the movie was the money."*

---

## Recommended first three

**01 CREW OF ONE** — the hook that travels furthest on social.
**04 THE SOUND BEFORE THE PICTURE** — the one that proves the full stack.
**02 THE 3AM CUT** — the emotional anchor for the showreel.

## Production pipeline (after story approval)

1. **Key frames first.** Generate stills for each concept's hook, turn, and final
   frame. `seedream_v5_pro` or `nano_banana_pro` for environments and graphic
   frames; `soul_2` for anything with a human face, since identity has to hold
   across shots.
2. **Lock identity.** The approved stills become `image_references` so the same
   person and the same room persist across every beat.
3. **Video.** Seedance 2.5 in `omni_reference` mode, 15s, 720p, `bitrate_mode:
   high`. 9:16 for social, 21:9 for the showreel cut.
4. **Sound.** Native `generate_audio` for foley and room tone. Concept 04 needs a
   real track generated first and passed in as an `audio_reference` so the cuts
   land on actual beats.
