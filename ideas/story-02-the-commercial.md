# THE COMMERCIAL — shot list

**Target:** ~1:35 · **Format:** 9:16 · **Shots:** 21
**Cast:** Dale, Carol (two speaking parts only — the nephew from the slate is
cut and Carol films instead, which saves a character sheet and makes the
marriage the spine of the film)

## Structure, following what worked on LOOKS DRY

| Act | Shots | Job |
|---|---|---|
| Stakes established first | 1–4 | The store is quiet. He is not a fool, he is losing. |
| The attempt escalates | 5–10 | Jingle, costume, rain. Commitment played straight. |
| **The false fix** | 11–13 | He makes the "professional" version instead. It's dead. |
| Quiet low point | 14–15 | No music, no joke. |
| The turn | 16–18 | Carol decides it. |
| Payoff | 19–21 | |

The false fix is the load-bearing beat again: Dale's instinct after being
embarrassed is to do it *properly* — stiff, straight to camera, off a cue card.
It is competent and completely lifeless, and that failure is what earns the
ending. Without it the film is just "silly ad works," which is a bit, not a
story.

## Shot list

### ACT ONE — the store is quiet (0:00–0:22)

| # | Gen | Shot | Audio |
|---|---|---|---|
| 1 | 6s | Hardware store interior. Dale alone behind the counter, straightening a display of screwdrivers that does not need straightening. Aisles empty. | Fluorescent hum, a clock. |
| 2 | 5s | A shopper passes the front window, slows, glances in — and keeps walking. Dale watches them go. | Muffled street. |
| 3 | 5s | Dale on his phone at the counter, watching a competitor's slick polished ad. His face, lit by it. | Tinny ad audio, then silence. |
| 4 | 6s | Kitchen table, night. Dale announces: *"I'm making a commercial."* Carol, crossword, doesn't look up. *"Mm."* | **Dialogue.** |

### ACT TWO-A — the attempt (0:22–0:50)

| # | Gen | Shot | Audio |
|---|---|---|---|
| 5 | 6s | 11pm. Dale two-finger typing at the kitchen table, one lamp on, absolutely thrilled with himself. | Slow key taps. |
| 6 | 6s | He reads the jingle aloud with full theatrical commitment. Carol does not look up. | **Dialogue.** |
| 7 | 6s | The costume arrives. He lifts the hammer head out of the box and holds it up. The eyes are wrong. He is delighted. | Cardboard, packing tape. |
| 8 | 5s | Dale inside the hammer costume, standing in his own aisle, giving a thumbs up to camera. | Muffled voice inside foam. |
| 9 | 6s | Carol holding the phone vertically, filming him, entirely deadpan. | Room tone. |
| 10 | 7s | Rainy car park. Dale in the costume, rain streaming off it. Carol holds the umbrella over the phone, not over Dale. | Heavy rain, no music. |

### ACT TWO-B — the false fix (0:50–1:05)

| # | Gen | Shot | Audio |
|---|---|---|---|
| 11 | 6s | Dale straight to camera in a clean shirt, no costume, reading off a cue card Carol holds. Stiff, corporate, lifeless. | **Dialogue**, flat delivery. |
| 12 | 6s | The two of them watching the serious version on a laptop. Long silence. Carol, carefully: *"It's fine."* | **Dialogue.** |
| 13 | 5s | Dale alone looking at the two files side by side on the screen. He knows. | Room tone. |

### ACT THREE — the low point (1:05–1:16)

| # | Gen | Shot | Audio |
|---|---|---|---|
| 14 | 7s | Store closed, lights half off. Dale sitting on a stool among the shelves, still, hands on his knees. | Fridge hum. Nothing else. |
| 15 | 4s | The hammer head on the counter beside him, discarded, staring at nothing. | **Silence. Do not score.** |

### THE TURN (1:16–1:30)

| # | Gen | Shot | Audio |
|---|---|---|---|
| 16 | 6s | Carol comes and sits beside him. A beat. *"Put the hammer one on."* | **Dialogue.** Music enters here, first time. |
| 17 | 6s | It airs. Dale watching a small TV from behind his hands, peeking through his fingers. | TV audio, muffled. |
| 18 | 5s | The store phone rings. Then again. Dale looks at it like it's a bomb. | Ringing, sharp. |

### PAYOFF (1:30–1:42)

| # | Gen | Shot | Audio |
|---|---|---|---|
| 19 | 6s | A kid at the counter asks him to do the jingle. Dale, after a beat, does the jingle. | **Dialogue.** |
| 20 | 6s | A small delighted crowd filming him on their phones. Dale mid-jingle, arms out. | Laughter, phones, warmth. |
| 21 | 6s | The hammer costume framed and mounted on the wall behind the register. Dale rings up a customer beneath it, entirely unbothered. | Store ambience, music resolves. |

**Generated ≈ 121s → trimmed to ≈ 95s.**

## Dialogue

| Shot | Line | Voice |
|---|---|---|
| 4 | "I'm making a commercial." / "Mm." | Dale / Carol |
| 6 | "Quality service, at a price that is also quality." | Dale |
| 11 | "Come on down to Dale's Hardware for all your hardware needs." | Dale, flat |
| 12 | "It's fine." | Carol |
| 16 | "Put the hammer one on." | Carol |
| 19 | "…Quality service, at a price that is also quality." | Dale |

The jingle line is deliberately terrible and gets said three times — thrilled at
shot 6, drained out of him at 11, and earned at 19. Same words, three different
meanings. That repetition is the spine.

## Production rule carried over from the pilot

**Environment reference listed FIRST in every media array**, character
references after, plus an explicit "do not change the room" instruction. Getting
this backwards is what put shot 6 of LOOKS DRY in a different bakery.

---

## Platform finding: "Out of credits" is really a concurrency cap

Submitting 12 video jobs at once returned, for 6 of them:

```
Out of credits on ultra (monthly) plan in Private workspace.
```

**The balance was 2,064 credits at the time and never moved.** Evidence it is a
concurrency limit, not a billing state:

- `balance` reported 2,064.89 before and after the rejections.
- `list_workspaces` showed a single private ultra workspace holding those
  2,064.89 credits.
- With 5 jobs in flight, a batch of 7 failed entirely; a batch of **1**
  submitted successfully moments later against the identical balance.

So the ceiling is on **simultaneous video jobs (~6)**, and the error message
misattributes it to credits. Anyone reading that message at face value would
stop work and go top up an account that has plenty of headroom.

`list_workspaces` also showed `is_selected: false` — no active workspace.
Calling `select_workspace` fixed that, and it is worth doing regardless since
the selection governs what all subsequent operations bill against, but it was
**not** the cause of these rejections.

### Working rule

Submit video in waves of ~5 and drain before the next wave. Image batches of 12
were never throttled — the cap applies to video only.

---

# DELIVERED — `THE_COMMERCIAL.mp4`, 1:45.03, 21/21 shots, 7/7 dialogue takes

## Cost

Balance 2,301.89 → **1,472.19 = ~830 credits**, against ~1,099 for LOOKS DRY.
A 25% saving on a film with the same shot count, entirely from not repeating
the pilot's mistakes:

- **Zero NSFW rejections** (8 of 21 last time). Listing the environment
  reference first appears to settle the classifier as well as the room.
- **Zero continuity redos** (one last time).
- **Zero wasted seedream calls** on shots nano_banana could carry.

## What the environment-first rule bought

Every one of the 15 hardware-store shots shares the same shelving, the same
service counter, the same fluorescent tubes with the one dimmer tube, and the
same front window. Across 15 separate generations the room never drifted once.
On the pilot, one shot out of 21 relocated to a different building — and that
was with fewer location-heavy setups.

## Reusable assembler

`tools/assemble.py` — skips any shot whose clip is missing, so it can be run
partway through production and again when the remaining renders land. It
recomputes dialogue offsets from the shots actually present, which means the
lines stay glued to their scenes no matter how much of the film exists yet.
Used mid-production here to cut a 15-shot / 1:14 assembly while six shots were
still rendering.

## Remaining budget

**1,472 credits** — roughly one more film at the improved ~830 rate.
