# VO spine — LOOKS DRY

Same argument as THE COMMERCIAL, reached through a different story. Nine lines,
and the **last two are word-for-word identical** across both films:

> "You've already done the hard part."
> "We'll do the rest."

Same voice, same promise, same card. That is what makes these a campaign rather
than two unrelated shorts — a viewer who sees both hears the same person arrive
at the same conclusion twice.

## The angle

THE COMMERCIAL says: *nobody knows how good you are.*
LOOKS DRY says: *the one thing they saw was wrong.*

Both land on the same place. Renée's problem isn't obscurity — it's that a
single bad photo was the entire public record of thirty years of skill.

## Script

| # | Line | Lands on |
|---|---|---|
| 1 | "Renée is up at four. Nobody asked her to be." | shots 1–2, the alarm and the shutter |
| 2 | "Her croissants are the best thing on this street." | shots 3–4, laminating and the tray |
| 3 | "One stranger saw one photo." | shot 7, three likes |
| 4 | "And said it looked dry." | shots 8–9, the comment and her face |
| 5 | "So she tried to take a better photo." | shot 12, the false fix |
| 6 | "That wasn't it either." | shot 13, the crate |
| 7 | "People don't buy the photo. They buy her." | shot 15, the laugh |
| 8 | "You've already done the hard part." | shots 18–19, the queue and Deborah |
| 9 | "We'll do the rest." | shot 21, the sign lit at night |

## Craft notes

**Line 7 is the mirror of "They want him."** Same position in the structure,
same job, deliberately close phrasing. In THE COMMERCIAL it lands on Dale alone
in the dark; here it lands on Renée laughing — the moment she stops trying to
fix the photo and decides to be the thing people buy.

**Line 4 is the only line with an edge in it.** "And said it looked dry" should
be flat and slightly cold — the narrator quoting someone he doesn't think much
of. Everything else is warm.

**Line 6 is short on purpose.** "That wasn't it either" is four words after two
long ones, and it lands on the quietest shot in the film. Resist any impulse to
expand it.

## Placement offsets (against `cut2`, 96.0s)

| Line | At |
|---|---|
| 1 | 1.0s |
| 2 | 8.5s |
| 3 | 24.0s |
| 4 | 27.5s |
| 5 | 49.0s |
| 6 | 54.0s |
| 7 | 64.0s |
| 8 | 77.5s |
| 9 | 92.5s |

No collisions with the existing dialogue (Miles at 20.6, the KINDA exchange at
35.7–39.9, the croissant line at 43.1, "on the house" at 88.6).

## Generation

**Same seed — `20260812` — as THE COMMERCIAL's VO.** That is what holds the
voice across both films. One 30s Seedance 2.5 take, all nine lines in a single
continuous read, 1,810 credits.

---

# Status — submitted, connector removed before collection

- **historyId** `YV4HcH89ND4rvKvdBCer`
- Seedance 2.5, text2video, 30s, 9:16, 480p, `generateAudio: true`, **seed `20260812`**
- ~1,810 credits

Submitted successfully and confirmed RUNNING. When the scheduled pickup fired,
the OpenArt MCP server was reported **removed from the configuration** — a
stronger state than the disconnects seen earlier, and one this session cannot
recover from on its own. The render is in the account history regardless.

## Everything else is finished

The picture is rebuilt and staged at `scratchpad/looksdry/cut3/`:

- **all 22 native audio tracks stripped** — LOOKS DRY carried the same
  invented-dialogue defect as THE COMMERCIAL, in 16 of its clips
- six synthesised location beds: bakery kitchen at 4am (oven hum), shop front,
  a busier variant of that room for the queue, car interior, domestic kitchen,
  exterior night
- the same warm chord pad as THE COMMERCIAL, so the two films share a sound
- alarm and stamp foley
- the identical `serviceaihq.com` end card

Timeline is 96.0s before the card.

## One command finishes it

```
python3 tools/finish_looksdry.py <url-or-local-file>
```

Takes the render as a URL or a path. It verifies before cutting and **refuses to
proceed** on any of three failures: wrong number of spoken lines, a median F0
more than 15 Hz from THE COMMERCIAL's 105.5 (which would break the campaign
voice), or an audible noise floor between lines. Then it splits the nine lines
and reports ready to cut.

The guard matters more than the convenience — a mismatched voice across two
films is worse than one film with no narration.

---

# Both generation routes down — v3 shipped without narration

- **OpenArt** — connector removed from the session configuration.
- **Higgsfield** — account now reports **free plan, 0 credits** (was Ultra with
  1,472 earlier the same night). Workspace correctly selected; the balance
  itself changed.

With no generation route, `LOOKS_DRY_v3.mp4` ships **without the VO**: 1:40, all
22 native tracks stripped, six synthesised location beds, music entering on the
laugh, alarm and stamp foley, dialogue ducked under a voice-driven sidechain,
mastered to -14 LUFS, ending on the silent serviceaihq.com card.

The audio defect is fixed. What is missing is the argument — without narration
this is a well-cut short film rather than a commercial, exactly the gap
identified earlier.

## To finish it

The narration is already rendered and paid for on OpenArt as job
`YV4HcH89ND4rvKvdBCer`. A direct file URL is all that is needed:

```
python3 tools/finish_looksdry.py <url-or-local-file>
```

Nothing else about the film needs to change.

---

# COLLECTED AND CUT — `LOOKS_DRY_v4.mp4`, 1:40

OpenArt reattached and `YV4HcH89ND4rvKvdBCer` came back COMPLETED. Verified
against the campaign before a frame was cut:

| Check | Result | Verdict |
|---|---|---|
| Median F0 | **100.6 Hz** | 4.9 Hz from THE COMMERCIAL's 105.5 — same voice |
| Noise floor between lines | **-61.6 dBFS** | no booth ambience printed in |
| Speech segments | 11 raw | see below |

## The 11-into-9 trap

The splitter found **11** segments for 9 scripted lines and the guard let it
through on count alone. It was right to pass and wrong to number them 1-10:
two lines carry an internal full stop, and the model performed both pauses long
enough to read as line breaks.

| Group | Segments | Dur | Line |
|---|---|---|---|
| 1 | 1+2 | 3.78s | "Renée is up at four. **/** Nobody asked her to be." |
| 7 | 8+9 | 3.25s | "People don't buy the photo. **/** They buy her." |

Every other group is 1:1. The grouping is confirmed by duration against syllable
count on all nine, and the naive numbering would have shipped line 1 truncated
to "Renée is up at four." and **dropped line 9 entirely** — the 11th segment fell
off the end of a 10-name list.

`tools/cut_looksdry_v4.py` encodes the correct grouping and re-asserts that no
narration line overlaps a scene dialogue take before it will cut.

## Placement — all nine land on their intended shot

| Line | At | Shot |
|---|---|---|
| 1 | 1.0 | 1 — the alarm |
| 2 | 8.5 | 3 — laminating |
| 3 | 24.0 | 7 — three likes |
| 4 | 27.5 | 8 — the comment |
| 5 | 49.0 | 12 — the false fix |
| 6 | 54.0 | 13 — the crate |
| 7 | 64.0 | 15 — the laugh, where music enters |
| 8 | 77.5 | 18 — the queue |
| 9 | 92.5 | 21 — the sign lit at night |
