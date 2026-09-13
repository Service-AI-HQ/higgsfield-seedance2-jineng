# Narration pack — ElevenLabs, both films

Seventeen takes in `assets/vo/`. Committed to the repo deliberately: the
scratchpad was wiped once by a container recycle and took 42 generated clips
with it. These are small and irreplaceable-by-memory, so they live in git.

## Why this replaces the Seedance narration

| | Seedance 2.5 (old) | ElevenLabs v3 |
|---|---|---|
| Route | video model, audio as a by-product | purpose-built TTS |
| Bandwidth | rolloff **2.1 kHz**, below telephone | full-band 44.1 kHz, content to ~10 kHz |
| Cost | **1,810 credits per take** | **~5c per line**, 4 takes |
| Audition before paying | no | yes |
| Voice held across lines | only within one continuous take | guaranteed by `voice_id` |
| Delivery direction | prose hints in a video prompt | inline `[tags]` per line |

Whole pack: **~1,800 ElevenLabs credits, about 40 cents.** One earlier Seedance
attempt cost 1,810 OpenArt credits for a single unauditionable take.

## Voice

**David — Deep, Warm, Narration** · `cCYjmrGZaI86GUJ7F2Nn` · model `eleven_v3`
(chosen for inline audio-direction tags). Median F0 across all 17 takes is
**110.1 Hz**, against the retired narration's 105.5 — same register, so the
campaign voice carries over.

The 81–154 Hz spread across lines is prosody, not drift: "We'll do the rest"
lands at 81 Hz because it is directed to fall, and "So he tried telling them
himself" sits at 154 Hz because it lifts. Identity is fixed by the voice id.

## The takes

| File | Film | Line |
|---|---|---|
| `tc_L01` | COMMERCIAL | "Dale has run this store for thirty-one years." |
| `tc_L02` | COMMERCIAL | "He can find anything in here with his eyes shut." |
| `tc_L03a` | COMMERCIAL | "Nobody knows that." |
| `tc_L03b` | COMMERCIAL | "Because nobody's told them." |
| `tc_L04` | COMMERCIAL | "So he tried telling them himself." |
| `tc_L05` | COMMERCIAL | "Then he tried telling them… properly." |
| `tc_L06` | COMMERCIAL | "Turns out nobody wants properly." |
| `tc_L07` | COMMERCIAL | "They want him." |
| `ld_L01` | LOOKS DRY | "Renée is up at four. Nobody asked her to be." |
| `ld_L02` | LOOKS DRY | "Her croissants are the best thing on this street." |
| `ld_L03` | LOOKS DRY | "One stranger saw one photo." |
| `ld_L04` | LOOKS DRY | "And said it looked dry." |
| `ld_L05` | LOOKS DRY | "So she tried to take a better photo." |
| `ld_L06` | LOOKS DRY | "That wasn't it either." |
| `ld_L07` | LOOKS DRY | "People don't buy the photo. They buy her." |
| `shared_L08` | **BOTH** | "You've already done the hard part." |
| `shared_L09` | **BOTH** | "We'll do the rest." |

**Seventeen files, nineteen placements.** The two closing lines are rendered
once and used in both films — that is the campaign device, and rendering them
once makes the match exact rather than approximate.

THE COMMERCIAL: 18.4s of speech over 10 placements.
LOOKS DRY: 19.2s over 9.

## Platform note

The account allows **3 concurrent requests**, and generations that fail on that
limit are **still charged**. A first batch of 4 calls x 4 takes lost 5
generations that way. Serialise to 3 in flight.

## Correction to an earlier claim

`tools/voice_restore.py` drives every voice to a high/low band ratio of 0.14,
calibrated against Renée's brightest dialogue take. That reference was a
**female** voice. A deep male narrator naturally measures 0.001-0.013 there, so
0.14 was far too bright a target for narration — the DSP repair shipped in
`THE_COMMERCIAL_v6` / `LOOKS_DRY_v5` was almost certainly over-brightened.
These ElevenLabs takes need no band extension at all; use them raw.
