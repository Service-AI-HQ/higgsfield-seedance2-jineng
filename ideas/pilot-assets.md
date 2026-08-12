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
| 4 | Kitchen, 4am (v1) | `18437599-00d4-4aa9-9fc9-51193eb36ca3` | Superseded — read too derelict |
| 7 | **Kitchen, 4am (v2)** | `fd0b857f-a9ac-4362-ad05-e6e1661e8ea2` | Approved candidate — 4K, clean-worn |
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

## Model substitution — confirmed, not overridable

`nano_banana_pro` was requested twice, explicitly, on separate calls. Both times
the backend ran **`nano_banana_2`**. This is a server-side substitution that
cannot be forced from the MCP surface. Results are strong, and the `resolution:
"4k"` parameter *does* take effect regardless (kitchen v2 returned
3072×5504), so the practical loss is small — but Pro is not what runs.

## Per-model cost, derived from balance deltas

| Model | Approx credits | Note |
|---|---|---|
| `nano_banana_2` @ 4k | **~4** | Kitchen v2: 3252.44 → 3248.44 |
| `seedream_v5_pro` @ 2k | **~50** | Back-solved from the 161-credit first batch |

Seedream was consuming almost the entire first batch. **Use nano_banana for
everything** — roughly 12× cheaper at equal or better resolution. The 21 start
frames land near 85 credits rather than ~1,000, which removes stills from the
budget risk entirely. Video remains the expensive stage and the open question.

## Model choice still open: 2.5 vs 2.0

There is no "Seedance 2.5 Pro" — the catalog search returns nothing. The real
tradeoff:

| | `seedance_2_5` | `seedance_2_0` |
|---|---|---|
| Resolution | 480p / **720p max** | 480p / 720p / 1080p / **4K** (mode `std`) |
| Duration | 4–30s | 4–15s |
| Modes | t2v, omni_reference, video_edit, video_extension | reference-driven only |
| `supports_unlim` | **no** | **yes** |

For a showreel that has to look expensive, 2.0 at 1080p likely beats 2.5 at
720p, and 2.0 is the one flagged for unlimited. 2.5 wins only if the 30-second
continuous take or extension chaining is needed — and at 4–8s per shot, this
project does not need either.
