# phonkmakr — Agent Tools Reference

Every tool is an async Python function. The DeepSeek agent calls them by name.

---

## Metadata (2)

| # | Tool | Description |
|---|---|---|
| 1 | `set_project` | Declares BPM, key, and song title upfront. Agent must call this first. |
| 2 | `write_lyrics` | Generates Portuguese lyrics with section tags (`[Intro]`, `[Verse]`, `[Chorus]`, `[Drop]`, `[Outro]` etc). |

### `set_project`

```
Args:   bpm (int 80-200), key (str "Cm" "Fm" "Ebm"...), title (str)
Return: {bpm, key, title, session_dir}
```

### `write_lyrics`

```
Args:   theme (str), mood (str), language (str default "pt"), line_count (int)
Return: {sections: [{tag: str, text: str}], language: str}
```

Uses a secondary DeepSeek call with a dedicated lyrics-writing prompt. Output is
structured Portuguese with section markers the vocal tools consume.

---

## Drums (7)

| # | Tool | Description |
|---|---|---|
| 3 | `create_tamborzao` | Core funk carioca beat — kick + snare + hi-hat pattern. Styles: `classic`, `heavy`, `minimal`, `rave`. |
| 4 | `add_cowbells` | TR-808 cowbell rolls/punches. Signature phonk sound. Patterns: `rolling`, `dot8`, `syncopated`, `sparse`, `punches`. |
| 5 | `add_rimshot` | Rim shots / sidestick for accenting in Brazilian funk. |
| 6 | `add_clap` | Layer claps/snaps on beats 2 and 4 or syncopated. |
| 7 | `add_drum_fill` | Drum fill / transition break between sections. Styles: `classic`, `heavy`, `trap`, `minimal`. |
| 8 | `humanize_drums` | Adds swing, velocity variation, and micro-timing offsets so patterns sound like a human played them. |
| 9 | `add_drum_loop` | Insert a pre-made drum loop from the library. Styles: `tamborzao_loop`, `phonk_loop`, `break_loop`, `hat_loop`. |

### `create_tamborzao`

```
Args:   bpm (int), style (enum), bars (int), pattern (str)
Return: {path: str (wav), duration: float (seconds)}
```

Uses pre-curated MIDI templates derived from real funk carioca transcriptions,
varied programmatically with slight timing/velocity randomization.

### `add_cowbells`

```
Args:   bpm (int), intensity (float 0-1), pattern (enum)
Return: {path: str (wav)}
```

Phonk cowbell patterns:
- `rolling` — constant 16th-note roll (aggressive)
- `dot8` — dotted 8th pattern (groovy)
- `syncopated` — off-beat emphasis (technical)
- `sparse` — occasional hits for texture
- `punches` — single hits on strong beats

### `add_rimshot`

```
Args:   bpm (int), pattern (str), bars (int)
Return: {path: str (wav)}
```

### `add_clap`

```
Args:   bpm (int), pattern (str), bars (int)
Return: {path: str (wav)}
```

### `add_drum_fill`

```
Args:   bpm (int), style (enum), bars (int)
Return: {path: str (wav)}
```

### `humanize_drums`

```
Args:   audio_path (str), swing (float 0-1), velocity_variation (float 0-1)
Return: {path: str (wav)}
```

### `add_drum_loop`

```
Args:   bpm (int), style (enum), bars (int)
Return: {path: str (wav)}
```

Inserts a pre-made loop from the downloaded sample library. Loops are full
patterns (e.g. 8-bar tamborzão loop) rather than individual one-shot hits.
The agent can use this as a quick foundation instead of building from scratch.

---

## Bass (2)

| # | Tool | Description |
|---|---|---|
| 10 | `add_sub_bass` | 808 sub bass tuned to key with adjustable distortion. Patterns: `sustained`, `staccato`, `rhythmic`, `rolling`, `sparse`. |
| 11 | `add_bass_variation` | Variation of current bass pattern for different song sections. |

### `add_sub_bass`

```
Args:   key (str), pattern (enum), distortion (float 0-1), bars (int)
Return: {path: str (wav)}
```

Uses 808 sub one-shot samples mapped to root note frequency. Distortion stages:
< 0.3 = clean sub, 0.3–0.6 = warm saturation, 0.6–0.9 = aggressive (phonk standard),
> 0.9 = fully blown-out.

### `add_bass_variation`

```
Args:   key (str), variation_type (str), bars (int)
Return: {path: str (wav)}
```

Variation types: `rhythm_change`, `octave_up`, `octave_down`, `fill`, `drop_edit`.

---

## Melody (5)

| # | Tool | Description |
|---|---|---|
| 12 | `add_synth_stab` | Minor-key synth stabs — short punchy hits. Styles: `dark`, `aggressive`, `minimal`, `rave`. |
| 13 | `add_horn_hit` | Brass/horn hits — the "Rocky theme" style funk carioca horn stab. |
| 14 | `add_melody` | Melodic lead loop — dark minor repetitive hook. Styles: `dark_lead`, `arpeggio`, `simple_hook`, `atmospheric`. |
| 15 | `add_pad` | Atmospheric pad/ambient texture, often dark and ominous. Styles: `dark`, `tense`, `ethereal`, `distorted`. |
| 16 | `define_melody` | Writes a short pitched melody as a MIDI note sequence for vocal or synth use. |

### `add_synth_stab`

```
Args:   key (str), style (enum), rhythm (str), bars (int)
Return: {path: str (wav)}
```

### `add_horn_hit`

```
Args:   key (str), pattern (str), bars (int)
Return: {path: str (wav)}
```

### `add_melody`

```
Args:   key (str), style (enum), bars (int)
Return: {path: str (wav)}
```

### `add_pad`

```
Args:   key (str), style (enum), bars (int)
Return: {path: str (wav)}
```

### `define_melody`

```
Args:   key (str), notes (int 2-16), style (str)
Return: {melody: [{note: str, octave: int, duration: float}]}
```

Agent uses this to define a melody, then passes the result to `sing_vocals` or
uses the note data for synth melodies.

---

## Vocals (11)

| # | Tool | Description |
|---|---|---|
| 17 | `generate_tts_vocals` | Portuguese TTS via edge-tts (free, CPU). Voices: `male`, `female`, `male_deep`, `female_warm`. |
| 18 | `pitch_shift` | Pitch shift audio maintaining duration. Range: -24 to +24 semitones. Phonk standard is +5 to +12. |
| 19 | `time_stretch` | Stretch/compress audio to fit target BPM while preserving pitch. Separate from pitch shifting. |
| 20 | `formant_shift` | Shift vocal formants while keeping pitch — gender-bend effect. |
| 21 | `chop_vocals` | Rhythmic gating synced to BPM. Creates stutter/chop effect. |
| 22 | `sample_chop` | MPC-style slicing — chop a source audio into slices and rearrange them rhythmically. |
| 23 | `sample_from_file` | Extract a segment from a source audio file. Agent can sample anything — reference tracks, movie dialogue, acapellas. |
| 24 | `sing_vocals` | TTS speech → melodic singing via pyworld vocoder. Takes a melody definition and resynthesizes the voice to match. |
| 25 | `layer_vocals` | Layer multiple vocal tracks with volume mix. e.g. dry + pitched + delayed. |
| 26 | `add_adlibs` | Trigger pre-rendered Portuguese ad-lib one-shots — "yeah", "vai", "skrrt", "vem", shouts, grunts. |
| 27 | `add_vocal_fx_chain` | One-shot phonk vocal processing: time-compress → pitch → formant → distortion → chop. |

### `generate_tts_vocals`

```
Args:   lyrics_text (str), voice (enum), language (str default "pt")
Return: {path: str (wav), duration: float}
```

### `pitch_shift`

```
Args:   audio_path (str), semitones (float -24 to 24)
Return: {path: str (wav)}
```

Uses librosa phase vocoder. Does NOT preserve formants — the chipmunk effect
at high values is desirable for phonk.

### `time_stretch`

```
Args:   audio_path (str), target_bpm (int), preserve_pitch (bool default true)
Return: {path: str (wav)}
```

Stretches or compresses audio to match the target BPM without altering pitch.
Use case: a vocal sample recorded at 120 BPM needs to fit a 145 BPM track.
This is separate from `pitch_shift` which changes pitch but preserves duration.

### `formant_shift`

```
Args:   audio_path (str), shift (float -1 to 1)
Return: {path: str (wav)}
```

Negative = deeper / more masculine. Positive = higher / more feminine.
Phonk often uses slight negative shift (-0.3 to -0.1) with pitch up
for a unique vocal character.

### `chop_vocals`

```
Args:   audio_path (str), bpm (int), rhythm (enum)
Return: {path: str (wav)}
```

Rhythm patterns: `eighth`, `sixteenth`, `syncopated`, `random`, `triplet`.
The vocal is gated on/off in time with the beat.

### `sample_chop`

```
Args:   audio_path (str), bpm (int), num_slices (int), rearrange (list[int] optional)
Return: {path: str (wav), slices: [paths]}
```

MPC/Slicex-style slicing. Detects transients, slices the audio into N equal
or transient-detected chunks, then rearranges them in the specified order.
If no `rearrange` order given, returns the slice paths for the agent to
use later (e.g. placing individual hits across a beat).

### `sample_from_file`

```
Args:   source_path (str), start_seconds (float), duration_seconds (float)
Return: {path: str (wav)}
```

Extracts a segment from any audio file. The agent can sample from user-uploaded
reference tracks, downloaded acapellas, movie files, or any source. Classic
phonk technique — sampling Three 6 Mafia vocals, funk carioca acapellas, etc.

### `sing_vocals`

```
Args:   vocal_path (str), melody (list), key (str)
Return: {path: str (wav)}
```

Pipeline: TTS speech → pyworld analysis (F0 + spectral envelope) →
replace F0 with melody notes → pyworld resynthesis → melodic voice.
This is how TTS becomes actual singing with different pitches per note.

### `layer_vocals`

```
Args:   vocal_paths (list[str]), mix_ratios (list[float])
Return: {path: str (wav)}
```

### `add_adlibs`

```
Args:   bpm (int), adlib_type (enum), count (int)
Return: {path: str (wav)}
```

Pre-rendered Portuguese ad-lib one-shots from library:
- `shouts` — "vai!", "vem!", "é!"
- `grunts` — alpha-male grunts, "ugh", "yeah"
- `laughs` — sinister laughter, chuckles
- `calls` — "olha o beat", "tá bom?", "vai descendo"
- `bruxaria` — demonic/monster sounds from funk bruxaria

### `add_vocal_fx_chain`

```
Args:   audio_path (str), bpm (int), preset (enum)
Return: {path: str (wav)}
```

Presets: `phonk_standard`, `chipmunk`, `deep_dark`, `bruxaria`.
Applies a pre-configured chain of: time-compress → pitch shift → formant shift →
distortion → rhythmic chop. The standard "one-button" phonk vocal tool.

---

## Effects (13)

| # | Tool | Description |
|---|---|---|
| 28 | `apply_distortion` | Saturation / distortion. Styles: `soft_clip`, `hard_clip`, `saturation`, `fuzz`, `bitcrush`. |
| 29 | `apply_reverb` | Room / plate / hall reverb. Sizes: `small`, `medium`, `large`, `plate`, `hall`. |
| 30 | `apply_delay` | Echo / delay with feedback. Duration in beats (BPM-synced). |
| 31 | `apply_eq` | EQ shaping per track. Boost/cut lows, mids, highs. High-pass / low-pass filters. |
| 32 | `apply_compression` | Level compression with threshold, ratio, attack, release. |
| 33 | `apply_sidechain` | Sidechain compression — duck one track against another (e.g. bass ducks when kick hits). |
| 34 | `reverse_audio` | Reverse any audio — classic effect for cymbals, vocal swells, riser tails. |
| 35 | `tape_stop` | Pitch-drop deceleration over N beats. The classic slowdown/spin-down effect. |
| 36 | `slowed_reverb` | The YouTube "slowed + reverb" effect — slow audio down + massive hall reverb. Iconic phonk technique. |
| 37 | `apply_filter` | LPF/HPF/BPF filter with optional automation envelope sweep over time. |
| 38 | `add_stutter` | Gross Beat-style glitch/stutter patterns — triplet stutter, turntable scratch, beat-repeat, gate patterns. |
| 39 | `parallel_process` | Blend processed + dry versions at a mix ratio (e.g. 30% distorted + 70% clean). |
| 40 | `stereo_tool` | Per-band stereo widening or mono-ing. Widen synths, narrow bass to mono. |

### `apply_distortion`

```
Args:   audio_path (str), amount (float 0-1), style (enum)
Return: {path: str (wav)}
```

### `apply_reverb`

```
Args:   audio_path (str), room_size (enum), wet (float 0-1)
Return: {path: str (wav)}
```

### `apply_delay`

```
Args:   audio_path (str), delay_beats (float), feedback (float 0-1), wet (float 0-1), bpm (int)
Return: {path: str (wav)}
```

### `apply_eq`

```
Args:   audio_path (str), low_gain (float), mid_gain (float), high_gain (float),
        highpass (float Hz optional), lowpass (float Hz optional)
Return: {path: str (wav)}
```

### `apply_compression`

```
Args:   audio_path (str), threshold (float dB), ratio (float), attack (float ms),
        release (float ms)
Return: {path: str (wav)}
```

### `apply_sidechain`

```
Args:   target_path (str), trigger_path (str), ratio (float), threshold (float dB)
Return: {path: str (wav)}
```

### `reverse_audio`

```
Args:   audio_path (str)
Return: {path: str (wav)}
```

Classic technique: reverse a cymbal crash for a swooping riser. Reverse a vocal
phrase for an eerie pre-drop effect. Reverse a reverb tail for a swelling pad.

### `tape_stop`

```
Args:   audio_path (str), duration_beats (float), bpm (int)
Return: {path: str (wav)}
```

Pitch drops linearly from normal to near-zero over the specified duration.
Like pressing stop on a tape deck or turntable. Used at section endings,
before drops, and at song outro.

### `slowed_reverb`

```
Args:   audio_path (str), slow_factor (float 0.1-0.9), reverb_mix (float 0-1)
Return: {path: str (wav)}
```

The iconic YouTube phonk technique: slow the audio down (0.5x = half speed)
then wash it in a massive hall reverb. Creates a dark, dreamlike, ominous
atmosphere. Often applied to the full mix as an alternate version.

### `apply_filter`

```
Args:   audio_path (str), filter_type (enum "lpf" "hpf" "bpf"), cutoff_start (Hz),
        cutoff_end (Hz optional), sweep_duration_beats (float optional), bpm (int)
Return: {path: str (wav)}
```

If `cutoff_end` and `sweep_duration_beats` provided, the filter cutoff sweeps
from start to end over the duration (LPF opening for buildups, HPF rolling off
for transitions). If only `cutoff_start` given, applies a static filter.

### `add_stutter`

```
Args:   audio_path (str), bpm (int), pattern (enum)
Return: {path: str (wav)}
```

Gross Beat-style time-based effects:
- `triplet` — triplet gate pattern
- `scratch` — turntable scratch/stab effect
- `beat_repeat` — repeats the last 8th/16th note
- `gate_eighth` — gates audio in 8th-note pulses
- `gate_sixteenth` — gates in 16th-note pulses
- `glitch` — randomized slice-repeat chaos

### `parallel_process`

```
Args:   audio_path (str), effect_type (str), effect_params (dict), mix (float 0-1)
Return: {path: str (wav)}
```

Creates two copies of the audio: one dry, one processed through the specified
effect. Blends them at the given mix ratio. Example: `parallel_process(bass_path,
"distortion", {amount: 0.9, style: "hard_clip"}, mix: 0.3)` = 30% heavily
distorted bass + 70% clean bass. Classic technique for punchy yet clean low end.

### `stereo_tool`

```
Args:   audio_path (str), width (float 0-2), bands (str optional "all" "low" "mid" "high"),
        mono_below (float Hz optional)
Return: {path: str (wav)}
```

Width 0 = mono, 1 = normal stereo, 2 = super-wide. When `bands` specified,
only widens/narrows that frequency range. `mono_below` makes everything below
that frequency mono (standard practice: bass below 120 Hz should be mono).

---

## SFX (3)

| # | Tool | Description |
|---|---|---|
| 41 | `add_riser` | Build-up riser for transitions and drops. Styles: `noise`, `synth`, `filtered`, `vocal`. |
| 42 | `add_impact` | Impact/downlifter for the drop moment. Styles: `sub_boom`, `orchestral`, `noise_burst`, `synth_hit`. |
| 43 | `add_tuin` | High-pitched "tuin" ear-drum burst. Signature of funk bruxaria. Aggressive texture element. |

### `add_riser`

```
Args:   duration_bars (int), bpm (int), style (enum)
Return: {path: str (wav)}
```

### `add_impact`

```
Args:   style (enum)
Return: {path: str (wav)}
```

### `add_tuin`

```
Args:   frequency (int Hz), duration (float seconds), rhythm (enum), bpm (int)
Return: {path: str (wav)}
```

---

## Arrangement & Mix (6)

| # | Tool | Description |
|---|---|---|
| 44 | `arrange_sections` | Arranges all stems into a full track structure with section markers and mute/unmute per bar. |
| 45 | `mix_tracks` | Mix multiple WAVs with individual levels and sidechain routing. |
| 46 | `frequency_carve` | Auto-EQ one track to avoid frequency clash with another (sidechain-EQ, spectral ducking). |
| 47 | `apply_master` | Master bus processing. Presets: `phonk_standard`, `aggressive`, `clean`, `club_ready`. Can match reference loudness. |
| 48 | `analyze_mix` | Analyze current mix — returns metrics and issue flags including frequency masking checks. |
| 49 | `export_song` | Export final track to MP3/WAV. |

### `arrange_sections`

```
Args:   structure (list[{tag, tracks, bars, mute}]), track_files (dict[str: str])
Return: {path: str (wav)}
```

Structure format:
```json
[
  {"tag": "[Intro]",     "tracks": ["drums", "pad"],                    "bars": 4},
  {"tag": "[Build Up]",  "tracks": ["drums", "bass", "riser"],          "bars": 8},
  {"tag": "[Drop]",      "tracks": ["drums", "bass", "cowbells",
                                    "synth", "vocals", "impact"],       "bars": 16},
  {"tag": "[Break]",     "tracks": ["pad", "vocals"],                   "bars": 4},
  {"tag": "[Drop 2]",    "tracks": ["drums", "bass", "cowbells",
                                    "synth", "vocals"],                 "bars": 16},
  {"tag": "[Outro]",     "tracks": ["drums", "pad", "vocals"],          "bars": 4}
]
```

Each section specifies exactly which tracks play. Muting a track between sections
is implicit — if a track is not in the list, it's silent. The agent controls
the arrangement by choosing which tracks are active in each section.

### `mix_tracks`

```
Args:   tracks (dict[str: path]), levels (dict[str: float 0-1]),
        sidechain_target (str optional), sidechain_trigger (str optional)
Return: {path: str (wav)}
```

### `frequency_carve`

```
Args:   target_path (str), sidechain_path (str), freq_range (str optional),
        amount (float dB), q (float)
Return: {path: str (wav)}
```

Dynamically ducks conflicting frequencies in `target_path` whenever energy in
`sidechain_path` is present in the same frequency range. Unlike volume sidechain
(which ducks the whole signal), this only ducks the overlapping frequencies.
Classic use: kick and bass fighting at 60-80 Hz — carve the bass when the kick
hits, preserving the bass's higher harmonics. Also useful for vocals vs synths
in the 2-4k range.

### `apply_master`

```
Args:   audio_path (str), preset (enum), loudness_target (float LUFS optional),
        reference_path (str optional)
Return: {path: str (wav)}
```

When `reference_path` is provided, matches the reference track's loudness curve
and spectral balance. This enables the agent to target a specific phonk track's
master sound — essential for the genre where loudness and tonal balance are
consistent across tracks.

Master presets:
- `phonk_standard` — multiband comp → EQ → stereo widen → limiter (LUFS -9)
- `aggressive` — heavier limiting, more saturation (LUFS -7)
- `clean` — transparent mastering, less squashing (LUFS -12)
- `club_ready` — bass-forward, punchy (LUFS -8)

### `analyze_mix`

```
Args:   audio_path (str)
Return: {rms_db, peak_db, low_energy, mid_energy, high_energy,
         dynamic_range_db, duration, frequency_masking: [{freq, culprit, victim}],
         issues: [str]}
```

Issues the agent can detect and act on:

| Flag | Meaning |
|---|---|
| `bass_too_weak` | Low-end energy below phonk norm |
| `bass_too_loud` | Low end dominates |
| `vocals_buried` | Vocals lost in the mix |
| `cowbells_overpowering` | Cowbells too present |
| `kick_lost_in_mix` | Kick drum not cutting through |
| `too_dynamic` | Too much dynamic range for short-form video |
| `muddy_mids` | 200-500 Hz buildup |
| `harsh_highs` | 4k+ too bright / piercing |
| `too_quiet` | Overall loudness too low for platform |
| `clipping` | Digital clipping detected |
| `freq_mask_kick_bass` | Kick and bass clashing in 60-80 Hz range |
| `freq_mask_vocals_synths` | Vocals and synths competing in 2-4k range |
| `stereo_field_narrow` | Mix is too mono / lacks width |
| `phase_issues` | Potential phase cancellation in low end |

### `export_song`

```
Args:   audio_path (str), format (enum "mp3" "wav"), bitrate (str default "320k")
Return: {path: str, duration: float, size_bytes: int}
```

---

## Reference (1)

| # | Tool | Description |
|---|---|---|
| 50 | `reference_analyze` | Analyzes a user-uploaded reference phonk track. Extracts BPM, key, RMS target, spectral profile, and loudness. Agent can use these as mixing/mastering targets. |

### `reference_analyze`

```
Args:   audio_path (str)
Return: {bpm, key, rms_db, peak_db, spectral_profile: [...], loudness_lufs,
         duration, stereo_width, dynamic_range}
```

---

## Agent Workflow Summary

A typical full generation (~28-38 rounds):

```
 1. set_project()
 2. write_lyrics()
 3. create_tamborzao()       -- or add_drum_loop() for quick start
 4. humanize_drums()          -- on tamborzao
 5. add_cowbells()
 6. add_clap()                -- optional
 7. add_sub_bass()
 8. add_synth_stab()
 9. add_horn_hit()            -- optional
10. add_pad()                 -- optional
11. generate_tts_vocals()
12. time_stretch()            -- fit vocals to project BPM
13. define_melody()
14. sing_vocals()             -- TTS → melodic singing
15. pitch_shift()             -- +5 to +12 semitones
16. formant_shift()           -- slight negative shift
17. chop_vocals()             -- or add_stutter()
18. layer_vocals()            -- optional: dry + pitched layers
19. add_adlibs()              -- shouts, grunts
20. add_riser()
21. add_impact()
22. add_tuin()                -- bruxaria style: optional
23. apply_distortion()        -- on bass
24. apply_eq()                -- on drums, vocals
25. apply_sidechain()         -- bass ducks to kick
26. frequency_carve()         -- carve kick/bass conflict
27. add_drum_fill()           -- transition fill
28. reverse_audio()           -- reverse cymbal for transition
29. apply_filter()            -- LPF sweep on build-up
30. tape_stop()               -- slowdown at outro
31. stereo_tool()             -- widen synths, mono bass
32. arrange_sections()
33. mix_tracks()
34. apply_master()
35. analyze_mix()
36. (iterate: fix issues → back to relevant tool)
37. slowed_reverb()           -- optional: generate slowed+reverb alternate version
38. export_song()
```

Agent can skip optional steps, reorder where musically sensible, and iterate up
to 3 analysis-fix cycles before final export.

Total tools: **50** across 9 categories.
