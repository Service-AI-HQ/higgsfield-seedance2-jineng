# PILOT ASSETS — LOOKS DRY

Stage 1 complete. Job IDs are reusable as `image_references` in later
generations — pass the job_id as the media value, not the URL.

## Characters (nano_banana_2, 16:9, 2k)

| # | Asset | Job ID | Status |
|---|---|---|---|
| 1 | **Renée** | `b27ef275-4dab-4347-8b48-554033b41352` | Approved candidate |
| 2 | **Miles** | `86bdadba-0f41-4e97-957a-25883e298a6e` | Approved candidate |
| 3 | **Deborah** | `89f4dce5-a097-455c-88c5-3895b0dd3376` | Approved candidate |

## Environments (seedream_v5_pro, 9:16, 2k)

| # | Asset | Job ID | Status |
|---|---|---|---|
| 4 | Kitchen, 4am | `18437599-00d4-4aa9-9fc9-51193eb36ca3` | **Flagged — reads too derelict** |
| 5 | Shop front | `897946c5-41d3-4402-af82-623ca585693a` | Approved candidate |
| 6 | Car interior | `858a67b2-3f19-4590-820b-23291483e3df` | Approved candidate |

## Notes on what came back

**Renée** landed on the first pass. Visible pores, fine lines at the eyes, the
tiredness reading as real rather than styled, adult bone structure with no trace
of the airbrushed AI face. The anti-retouch module in the character-sheet
workflow is doing exactly what it claims.

**Deborah** is the important one. She reads warm and faintly apologetic, not
mean — which is the whole hinge of the ending. If she looked like a villain,
"it's on the house" becomes a power move instead of grace.

**Shop front** came back better than specified: the wilting plant, the
half-rubbed chalkboard, two lonely croissants in a case built for twenty, and a
blank rectangle of wall to the right of the window that is precisely where the
LOOKS DRY sign goes.

**Kitchen is the one to redo.** It's beautiful, but the sooty walls and the
depth of the shadows read as a condemned basement rather than a working bakery.
Act one has to say *she is good at this* — if her workplace looks like a
hellhole, the audience reads defeat before the story has earned it. Wanted:
same 4am darkness and single work light, but clean-worn instead of grimy.

## Cost finding

Balance before: **3,413.44** · after: **3,252.44** · **161 credits for 6 images**
(~27 each).

The unlim flag was deliberately omitted so the server could raise the balance
question. It did not — it submitted and charged credits. So **the web unlimited
does not automatically reach this session's image generations.**

Implication: the remaining 21 start frames plus retries run roughly 800–1,000
credits, and video is materially more expensive than stills. The balance will
not fund six stories end to end through MCP. The likely split is stills here for
control, video on web where 2.5 is unlimited — pending an explicit `use_unlim`
test on one video generation, which fails as a typed rejection rather than a
silent charge.

## Model substitution

`nano_banana_pro` was requested for the character sheets; the backend ran
`nano_banana_2`. Results are strong so it isn't worth fighting, but worth
knowing the requested model isn't always the one that runs.
