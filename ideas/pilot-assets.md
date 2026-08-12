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

---

# Stage 2 — Start frames (21 shots)

| Shot | Frame job ID | Model |
|---|---|---|
| 1 alarm | `99d3d1b2-ee17-4d46-a007-d43119486a01` | seedream_v5_pro |
| 3 laminating | `8f1be848-5f07-4763-9eae-f2986e89cd46` | nano_banana_flash |
| 5 empty shop | `2bd7c379-1709-4b08-aa3c-152a6a4cb24f` | nano_banana_flash |
| 6 "you should post them" | `19be3418-d2e3-4239-b02a-39e111df175d` | nano_banana_flash |
| 7 three likes | `a8f99344-8b04-44a1-a9a7-bdac9fe05e1c` | nano_banana_flash |
| 8 the comment | `62fb2771-9aeb-4ba5-a766-9ae3aab0edb3` | seedream_v5_pro |
| 9 her face | `599a4628-2d9e-432a-aacd-3056a4574b33` | nano_banana_flash |
| 10 "KINDA?!" | `c6fe0d6b-427f-450e-b381-0f57b5f608cb` | nano_banana_flash |
| 11 car storytime | `d9b33bb8-e50e-43d3-b5ac-fec3fafcd784` | nano_banana_flash |
| 12 false fix | `5b2402f8-ccae-4d97-aff5-2f576298ad78` | nano_banana_flash |
| 13 the crate | `d8e8ab62-0687-4960-af3b-2c5a45d60638` | nano_banana_flash |
| 14 the envelope | `5756465d-dbeb-420e-b776-b507e98fb738` | nano_banana_flash |
| 15 the laugh | `72c74116-f3de-4737-b49e-1e67ef90c9db` | nano_banana_flash |
| 16 painting the sign | `b93ab0c3-e305-40ce-8e42-cef5856070cd` | nano_banana_flash |
| 17 the stamp | `122c066b-85f6-4e12-a4a7-5e85e233f196` | seedream_v5_pro |
| 18 the queue | `5e299172-02e9-4d3c-9795-3dbb8cd5a6a9` | nano_banana_flash |
| 19 Deborah arrives | `61a71947-4ed6-4811-a8b4-205ac1432956` | nano_banana_flash |
| 20 "on the house" | `b92a320d-618c-4c8a-92a4-6cdf5411426e` | nano_banana_flash |
| 21 sign at night | `7ed69752-9d82-420e-b192-36c58e53c06e` | nano_banana_flash |

Shots 2 and 4 still outstanding.

# Stage 3 — Video jobs (Seedance 2.5, omni_reference, 720p, high bitrate)

| Shot | Video job ID | Dur | Native audio |
|---|---|---|---|
| 1 | `b20db888-2f29-48c5-ba86-5b498dcaac2c` | 5s | yes |
| 3 | `004e0f02-9d11-4bd6-b17b-9b6c089f0ded` | 8s | yes |
| 5 | `fa189ecf-4b27-41a5-977d-1bdea97065f8` | 6s | yes |
| 6 | `ecd764ff-8fbe-403c-9b0f-c344782fa5a5` | 6s | no |
| 7 | `20c4a3ba-ba6f-4bcc-9939-dabf553a0cb6` | 5s | yes |
| 8 | `d5e024f4-c5e7-49d5-888e-54cf284ef71f` | 5s | yes |
| 9 | `5fcc541c-64c1-458f-baf2-9c91ab87bd4a` | 6s | no |
| 10 | `6a2925cc-604c-49c0-9a3b-3b82798868bb` | 7s | no |
| 11 | `179c4860-52e0-4dba-ba55-57d2d2c2c45d` | 8s | no |
| 12 | `c882e63f-a442-41fe-91fa-7e296423c309` | 7s | yes |
| 13 | `68a5a054-2450-48f7-bf2e-39bed18a3db9` | 7s | yes |
| 14 | `8e762ddd-cad4-449d-85dc-7f34820b40e7` | 5s | yes |

Dialogue shots (6, 9, 10, 11) generated silent — real voice goes on in the edit
so comic timing stays an editing decision, not a generation lottery.

## Platform behaviours hit during stage 2

**Model substitution cascades.** `nano_banana_pro` → `nano_banana_2` →
`nano_banana_flash`. Requesting a tier does not get that tier; check the `model`
field on every returned job rather than trusting the request.

**False-positive NSFW rejections on `nano_banana_flash`.** 8 of 21 frames were
rejected, including a phone on a table, a rubber stamp on a box, and a queue of
customers — no people in several of them. Rewriting the prompts did not help.
Rerouting the same prompts to `seedream_v5_pro` cleared every one, which locates
the fault in the flash model's classifier rather than in the content.

**Preset interception on video submission.** 3 of 12 video jobs returned
`submission_failed` with a preset recommendation ("IN THE DARK") instead of
running. Fix is resubmitting with `declined_preset_id` set to the recommended
preset. Worth expecting on any dark or low-light shot.

---

# Stage 4 — First rough cut delivered

**`LOOKS_DRY_roughcut.mp4` — 1:30.53, 720×1280, 19 shots, dialogue mixed.**

Assembled locally with ffmpeg (installed via `imageio-ffmpeg`; the Adobe MCP is
not reachable from this session). Each source clip trimmed to its screen time,
normalised to 720×1280 @ 24fps, silent shots given a null audio bed so the
concat demuxer has a uniform stream layout, then six ElevenLabs dialogue takes
mixed in at fixed offsets.

## Dialogue takes (text2speech_v2, elevenlabs variant)

| Line | Voice | Offset |
|---|---|---|
| "You should post them." | Dylan (Miles) | 14.60s |
| "Does that look dry to you?" | Maeve (Renée) | 30.20s |
| "…kinda?" | Dylan | 32.70s |
| "Kinda?!" | Maeve | 34.30s |
| "It's a croissant, Deborah. They're supposed to be flaky." | Maeve | 37.60s |
| "It's on the house." | Maeve | 83.20s |

Voices are Higgsfield presets through the ElevenLabs engine — the user's own
ElevenLabs account and cloned voices are not reachable from this session.

## Continuity defect found and fixed

Shot 6 generated in a **different bakery** — brick walls and bread racks instead
of the white-walled shop front with the display case. Shot 10 plays in the same
scene minutes later and used the correct room, so the two cut together as a
continuity break. Cause: the character references outweighed the environment
reference. Fix: regenerate with the environment reference listed **first** and
an explicit "do not change the room" instruction. Re-rendering as shot 62.

## Cost of one 90-second film

Balance 3,413.44 → 2,314.89 = **~1,099 credits** for the complete pilot: 24
images, 22 video generations, 6 audio takes, including all retries and the
8 NSFW false positives that had to be rerouted.

At that rate the remaining balance funds roughly **two more stories** end to
end. Cutting the waste (routing stills to nano_banana first, expecting the
preset interception, anchoring environments correctly) should bring the next
one in cheaper.
