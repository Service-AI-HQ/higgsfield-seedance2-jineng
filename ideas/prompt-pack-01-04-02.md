# Prompt Pack — Concepts 01, 04, 02

**Model:** Seedance 2.5 · **15s** · **720p** · `bitrate_mode: high` · `generate_audio: true`

Workflow per concept: generate the **key frames** first, pick the keepers, then
feed them into the video prompt as `image_references`. Identity and room have to
survive across beats, and that only happens if the stills are locked first.

---

# 01 — CREW OF ONE

**Format:** 9:16 · social

## Key frames (generate first)

**Frame A — the set.** `seedream_v5_pro`, 9:16, 2k
> Wide shot of a professional film set mid-take, forty crew members at work,
> dolly track laid across the floor, a large HMI lighting rig overhead throwing
> hard white light, boom operator with arm extended, camera operator hunched at
> the eyepiece, clapper board raised. Industrial soundstage, black duvetyne
> walls, cable runs taped to concrete. Cinematic, anamorphic, slight haze in the
> light beams. Shot on 35mm, shallow depth of field, cool white key with warm
> practical spill.

**Frame B — the couch.** `soul_2`, 9:16, 2k
> One person sitting cross-legged on a worn couch in a small apartment, laptop
> open on their knees, face lit by the screen. *The framing, lens, and lighting
> direction exactly match a professional film set wide shot* — same hard key
> from above and camera left, same haze, same composition weight. Mundane room,
> laundry on a chair, a mug on the floor. Cinematic, anamorphic, shot on 35mm.

> **Critical:** B must match A's framing and key direction or the match-cut
> fails. Generate B with A passed in as an `image_reference` for lighting.

**Frame C — the dissolve.** `seedream_v5_pro`, 9:16, 2k
> The forty-person film crew mid-dissolve, bodies breaking into drifting
> particles of light, only one seated figure remaining solid at the center of
> the frame, lit by the same overhead rig that lit the crew. Empty soundstage
> becoming visible behind them. Cinematic, volumetric haze, hard key light.

## Video prompt — paste this

```
15-second commercial, 9:16 vertical, cinematic, high contrast, anamorphic.

@image1 @image2 @image3

0:00-0:02 — HOOK. Hard cut in on a full film set at work: forty crew, dolly
track, boom arm swinging into frame, a clapper board SNAPS shut. Loud, chaotic,
alive. Camera pushes in fast.

0:02-0:03 — MATCH CUT to one person on a couch with a laptop. Identical framing,
identical light direction, identical composition. Silence where the set noise
was. Same result glowing on the laptop screen.

0:03-0:07 — Repeat the pairing twice more, each cut faster than the last: set,
couch, set, couch. The intercutting accelerates until it is nearly strobing.
Match the light and lens across every pair so the cuts feel like one continuous
space folding in on itself.

0:07-0:09 — DOUBT. Everything stops. Hold on the person alone on the couch,
small in frame, room dark around them. Near silence, only room tone and a
laptop fan.

0:09-0:13 — TURN. Cut back to the full crew one last time. The forty people
dissolve into drifting particles of light, mid-motion, and blow away. The lone
figure is left standing in the empty soundstage, lit by the same enormous rig
that lit all forty of them. Slow push in. The rig light swells.

0:13-0:15 — Cut to black. Text appears, clean sans-serif, centered, white on
black: "YOU ARE THE CREW." Hold in complete silence.

CAMERA: locked wides for the set, matched locked wides for the couch, one slow
push on the turn. No handheld.
LIGHTING: hard overhead key, volumetric haze, deep black shadows, cool white
with warm practical spill.
SOUND: dense film-set ambience — shouted calls, cable drags, the clapper snap.
Cut to hard silence on every couch shot. Silence is the rhythm. On the turn, a
single low sustained synth swell that cuts dead before the text.
```

---

# 04 — THE SOUND BEFORE THE PICTURE

**Format:** 9:16 social + 21:9 reel cut
**Order matters:** generate the **track first**, then the frames, then the video
with the track passed in as `audio_reference` so cuts land on real beats.

## Track (generate first)

> Instrumental, 15 seconds, cinematic electronic. Starts with a bare heartbeat
> kick at 70 BPM, isolated, four bars. A tight snare enters on bar three. A
> low analog bassline builds underneath, rising in filter cutoff. Tension
> builds continuously for 9 seconds — add hi-hats, a rising white-noise sweep,
> a sub drop. Hard drop at 0:09 into a full wide-stereo synth chord stab with
> heavy sidechain pumping. Aggressive, confident, modern. Ends abruptly at
> 0:15 on a cut, not a fade.

## Key frames

**Frame A — the face in the dark.** `soul_2`, 9:16, 2k
> Extreme close-up of a face in near-total darkness, eyes closed, head tilted
> slightly back, listening. The only light is a thin horizontal band of cyan
> that falls across the eyes like an audio waveform. Ninety percent of the
> frame is pure black. Skin texture visible, slight sheen. Cinematic, shot on
> 35mm, very shallow depth of field.

**Frame B — the explosion.** `seedream_v5_pro`, 9:16, 2k
> A single frame at the peak of a music drop: a figure standing arms out in a
> vast space as color detonates outward from their chest in every direction,
> saturated magenta and cyan and white, light rays, dust, debris suspended
> mid-air. Overwhelming, maximal, beautiful. Cinematic, high contrast, deep
> blacks under the color.

## Video prompt — paste this

```
15-second commercial, 9:16 vertical, cinematic, extreme contrast.

@image1 @image2 @audio1

Cut strictly to the beats of @audio1.

0:00-0:03 — Pure black screen. A heartbeat kick. Nothing visible at all. Let
the audience sit in the dark and wonder if the video is broken.

0:03-0:06 — A thin horizontal band of cyan light appears and pulses across a
face in the darkness, moving exactly like an audio waveform, expanding on the
kick and collapsing between hits. We see only the eyes and the bridge of the
nose. Everything else is black. The band grows brighter with each bar.

0:06-0:09 — The build. The waveform band fractures into several bands, then
into a shivering field of light across the face. The face is still, eyes still
closed. Almost unbearable tension. Frame begins to shake subtly with the
rising sweep.

0:09-0:13 — THE DROP. On the exact frame of the drop, the picture detonates
into existence: full saturated color, a figure with arms out in a vast space,
light blasting outward. Then hard-cut on every single beat through a rapid
montage — a wave breaking, a city at night, a dancer mid-spin, a desert, a
crowd, a face laughing — one beat each, relentless, all in the same saturated
grade.

0:13-0:15 — Everything cuts to black on the final beat. Text, clean sans-serif,
white on black: "MAKE THE NOISE. THE WORLD WILL PICTURE IT." Total silence.

CAMERA: locked and still for the first 9 seconds. After the drop, every shot is
a different lens and a different move. Contrast stillness against chaos.
LIGHTING: first half is a single cyan band in blackness. Second half is
maximal saturated color, magenta and cyan, deep black shadows underneath.
SOUND: follow @audio1 exactly. No added foley in the first 9 seconds — the
track is the only sound. Silence hard on the final frame.
```

---

# 02 — THE 3AM CUT

**Format:** 21:9 showreel + 9:16 cut-down

## Key frames

**Frame A — the face, before.** `soul_2`, 21:9, 2k
> A person alone at a desk at night, face lit only by the cold blue glow of a
> monitor, the rest of the room in near-total darkness. Tired eyes, slight
> stubble or messy hair, hoodie. Cold coffee in a mug beside them. Cinematic,
> shot on 35mm, shallow depth of field, deep blacks, blue-only color palette.

**Frame B — the hands.** `seedream_v5_pro`, 21:9, 2k
> Extreme close-up of hands poised over a mechanical keyboard, shot with the
> reverence of a boxer's hands being taped before a fight. Hard side light,
> visible skin texture and tendon, everything else falling into black.
> Cinematic, macro, shallow depth of field, cold blue key.

**Frame C — the face, after.** `soul_2`, 21:9, 2k
> The same person at the same desk, but now their face is washed in warm
> saturated color — golds, magentas, oranges — spilling off the screen and
> filling the entire dark room. Eyes open wide, reflecting the color.
> Expression of quiet awe. Cinematic, shot on 35mm, warm color for the first
> time against a cold dark room.

> Generate C with A as an `image_reference` so it is unmistakably the same
> person and the same desk.

## Video prompt — paste this

```
15-second cinematic commercial, 21:9 widescreen, film grain, deep blacks.

@image1 @image2 @image3

0:00-0:02 — HOOK. Extreme close-up: cold blue monitor light crawling across a
tired face in a pitch-black room. Slow. No music. Only the hum of a machine.

0:02-0:07 — THE GRIND. Cut between intimate details, unhurried, reverent:
hands moving to a mechanical keyboard shot like a fighter's hands being taped.
A mug of coffee gone cold, surface still. A progress bar creeping. The window
behind them shifting from black to the first grey of dawn. A hand rubbing an
eye. Everything is blue and cold and quiet.

0:07-0:09 — DOUBT. Hold on a cursor blinking on an empty timeline. Nothing
else. Let it blink three times. Complete silence except a distant fan.

0:09-0:13 — THE TURN. The render completes. Warm saturated light — gold,
magenta, orange — floods out of the screen and fills the entire room, washing
over the person's face. It is the first color in the film. They lean back. Slow
push in on their eyes, wide, reflecting what they made. Hold on the awe.

0:13-0:15 — Fade to black. Text, clean sans-serif, white: "NOBODY WAS WATCHING.
THAT'S WHEN YOU MADE IT." Silence.

CAMERA: slow deliberate moves throughout — a creeping push, a slow tilt down
the arm to the hands. Nothing fast. This one breathes.
LIGHTING: single cold blue monitor source for the first 9 seconds, room falling
to black. At the turn, warm saturated screen spill becomes the only source and
fills the room.
SOUND: room tone, a machine fan, distant city at night, the click of keys. One
sparse piano note every few seconds. At the turn, a warm string swell rising.
Cut to complete silence for the text.
```

---

## After the frames come back

Pick the keepers, then run the video prompts with the chosen stills attached as
`image_references`. If a face drifts between beats, regenerate the still rather
than fighting it in the video prompt — identity is won upstream.
