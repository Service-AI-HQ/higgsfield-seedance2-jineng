# VO spine — THE COMMERCIAL

The missing element. Both films were shorts with no client, no promise and no
ask. This is what turns THE COMMERCIAL into an actual commercial.

## The constraint

Service AI HQ sells services, software, automations, agents, internal operating
systems, and full marketing campaigns. The brief also says: **nothing techy,
never say "agents."**

So the VO sells all of it without naming any of it. It does that by talking
about the *outcome* — "the rest" — instead of the machinery. Ten lines, and not
one technical word appears.

## The argument

> Your business is already good. The problem is nobody knows.

That is the whole pitch, and it is true of every small business owner watching.
It flatters the viewer's competence and locates the failure somewhere they don't
feel ashamed of — which is why it can sell a full systems-and-marketing offer
without ever listing what's in it.

## Script

| Time | Line | Lands on |
|---|---|---|
| 0:03 | "Dale has run this store for thirty-one years." | Shot 1 — alone behind the counter |
| 0:11 | "He can find anything in here with his eyes shut." | Shot 2 — the shopper walking past |
| 0:19 | "Nobody knows that. Because nobody's told them." | Shot 3 — watching the rival's ad |
| 0:29 | "So he tried telling them himself." | Shot 5 — 11pm, two-finger typing |
| 0:45 | "Then he tried telling them *properly*." | Shot 11 — the false fix, clean shirt |
| 0:57 | "Turns out nobody wants properly." | Shot 12 — "It's fine." |
| 1:09 | "They want him." | Shot 14 — alone in the dark aisle |
| 1:20 | "You've already done the hard part." | Shot 16 — Carol sits beside him |
| 1:31 | "We'll do the rest." | Shot 20 — the crowd |
| 1:38 | `serviceaihq.com` — end card, silent | Shot 21 — the hammer on the wall |

## Craft notes

**The pronoun turn at 1:20 is the whole mechanism.** Eight lines about Dale in
the third person, then one switch to *you*. The viewer has spent seventy seconds
agreeing about a stranger before realising the film was about them. Move that
switch earlier and it becomes a sales pitch; leave it later and there's no time
to land.

**"We'll do the rest" is the only company line in the film**, and it never says
what "the rest" is. That is deliberate: naming automations or systems shrinks
the offer to whatever the viewer pictures. "The rest" is bigger than any list.

**"Properly" is the pivot word.** Said with a slight edge at 0:45, it sets up
"turns out nobody wants properly" — which is the film's actual thesis and the
reason the hammer suit beats the clean shirt.

**The end card is silent.** Music resolves under shot 21, then the URL sits in
quiet. No voice reading out a web address.

## Delivery direction

Warm, dry, unhurried. A man about Dale's age talking about a neighbour he likes.
Never salesy, never announcer-ish, no upward inflection on the last line. The
line "They want him" should land almost under the breath.

## Production route

Ten lines, ~1 credit each on Higgsfield TTS. OpenArt's catalogue carries no
standalone text-to-speech — its audio arrives bundled inside video generation
(Seedance 2.x audio elements, Gemini Omni Flash native dialogue), which suits
in-scene voice rather than narration laid over a finished cut.

Whichever engine renders it, generate **3 takes per line** with the delivery
direction written into the prompt, and pick. The difference between a read and a
performance is entirely in that step, and it was skipped on the dialogue.

---

# Status — VO blocked on connector, not on craft

The narration was submitted to OpenArt and paid for:

- **historyId** `Bgu28Fy4K6O61I94BiWC`
- Seedance 2.5, text2video, 30s, 9:16, 480p, `generateAudio: true`, seed `20260812`
- **1,810 credits** (21,194 → ~19,384)

It could not be collected. `mcp__Openart__*` was absent across **four** scheduled
retrieval attempts over ~90 minutes, while ten other MCP servers dropped and
reconnected repeatedly in the same window. The job itself is fine — it is in the
account's OpenArt history and the credits are spent either way. This is purely a
retrieval problem.

## Two ways past it

1. **A direct file URL.** Open the job in OpenArt's history, copy the download
   link, paste it. `curl` does not need the connector, so this bypasses the
   problem entirely and the rebuild takes minutes.
2. **A real TTS connector.** ElevenLabs on the user's own account would render
   all ten lines, with voice selection and consistent delivery, for a fraction of
   one 1,810-credit video generation — and would also cover LOOKS DRY's spine and
   the directed dialogue re-takes both films still want.

## Why narration-from-a-video-model was always the weak link

It is off-label use. A video model asked for narration may return the wrong age,
an announcer read, booth ambience printed into the take, or simply fail to speak
all ten lines in the time available — and each attempt costs 1,810 credits with
no way to audition before paying. Standalone TTS costs cents per take and lets
you pick the voice first. The video-model route was a workaround for not having
a TTS route, and it is the single weakest link in the pipeline.

## Ready and waiting

- `assets/endcard/serviceaihq-endcard.png` — the end card frame
- `scratchpad/commercial/insert/endcard.mp4` — 4s, silent, fades up and out
- `scratchpad/commercial/cut3/` — film with native audio stripped, synthesised
  location beds, music at the turn, phone foley, existing dialogue

The moment the VO audio exists in any form, it drops into that cut and the film
is finished.
