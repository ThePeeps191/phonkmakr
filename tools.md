# Agent Tools Reference

Every tool is an async Python function. The DeepSeek agent calls them by name.

## Metadata

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

## Drums

| # | Tool | Description |
|---|---|---|
| 3 | `create_tamborzao` | Core funk carioca beat — kick + snare + hi-hat pattern. Available styles: `classic`, `heavy`, `minimal`, `rave`. |
| 4 | `add_cowbells` | TR-808 cowbell rolls/punches. Signature phonk sound. Patterns: `rolling`, `dot8`, `syncopated`, `sparse`, `punches`. |
| 5 | `add_rimshot` | Rim shots / sidestick for accenting in Brazilian funk. |
| 6 | `add_clap` | Layer claps/snaps on beats 2 and 4 or syncopated. |
| 7 | `add_drum_fill` | Drum fill / transition break between song sections. Styles: `classic`, `heavy`, `trap`, `minimal`. |
| 8 | `humanize_drums` | Adds swing, velocity variation, and micro-timing offsets to any drum pattern so it sounds like a human played it. |

### `create_tamborzao`

```
Args:   bpm (int), style (enum), bars (int), pattern (str)
Return: {path: str (wav), duration: float (seconds)}
```

Uses pre-curated MIDI templates derived from real funk carioca transcriptions,
varied programmatically with slight timing/velocity randomization. This is the
foundational beat — agent should call this first in the drum section.

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

---

## Bass

| # | Tool | Description |
|---|---|---|
| 9 | `add_sub_bass` | 808 sub bass tuned to key with adjustable distortion. Patterns: `sustained`, `staccato`, `rhythmic`, `rolling`, `sparse`. |
| 10 | `add_bass_variation` | Variation of current bass pattern for different song sections. |

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

---

## Melody

| # | Tool | Description |
|---|---|---|
| 11 | `add_synth_stab` | Minor-key synth stabs — short punchy hits. Styles: `dark`, `aggressive`, `minimal`, `rave`. |
| 12 | `add_horn_hit` | Brass/horn hits — the "Rocky theme" style funk carioca horn stab. |
| 13 | `add_melody` | Melodic lead loop — dark minor repetitive hook. Styles: `dark_lead`, `arpeggio`, `simple_hook`, `atmospheric`. |
| 14 | `add_pad` | Atmospheric pad/ambient texture, often dark and ominous. Styles: `dark`, `tense`, `ethereal`, `distorted`. |
| 15 | `define_melody` | Writes a short pitched melody as a MIDI note sequence for vocal or synth use. |

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

## Vocals

| # | Tool | Description |
|---|---|---|
| 16 | `generate_tts_vocals` | Portuguese TTS via edge-tts (free, CPU). Voices: `male`, `female`, `male_deep`, `female_warm`. |
| 17 | `pitch_shift` | Pitch shift audio maintaining duration. Range: -24 to +24 semitones. Phonk standard is +5 to +12. |
| 18 | `formant_shift` | Shift vocal formants while keeping pitch — gender-bend effect. |
| 19 | `chop_vocals` | Rhythmic gating synced to BPM. Creates stutter/chop effect. |
| 20 | `sing_vocals` | TTS speech → melodic singing via pyworld vocoder. Takes a melody definition and resynthesizes the voice to match. |
| 21 | `layer_vocals` | Layer multiple vocal tracks with volume mix. e.g. dry + pitched + delayed. |
| 22 | `add_vocal_fx_chain` | One-shot phonk vocal processing: time-compress → pitch → formant → distortion → chop. |

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

### `add_vocal_fx_chain`

```
Args:   audio_path (str), bpm (int), preset (enum)
Return: {path: str (wav)}
```

Presets: `phonk_standard`, `chipmunk`, `deep_dark`, `bruxaria`.
Applies a pre-configured chain of: time-compress → pitch shift → formant shift →
distortion → rhythmic chop. The standard "one-button" phonk vocal tool.

---

## Effects

| # | Tool | Description |
|---|---|---|
| 23 | `apply_distortion` | Saturation / distortion. Styles: `soft_clip`, `hard_clip`, `saturation`, `fuzz`, `bitcrush`. |
| 24 | `apply_reverb` | Room / plate / hall reverb. Sizes: `small`, `medium`, `large`, `plate`, `hall`. |
| 25 | `apply_delay` | Echo / delay with feedback. Synced to BPM. |
| 26 | `apply_eq` | EQ shaping per track. Boost/cut lows, mids, highs. High-pass / low-pass. |
| 27 | `apply_compression` | Level compression with threshold, ratio, attack, release. |
| 28 | `apply_sidechain` | Sidechain compression — duck one track against another (e.g. bass ducks when kick hits). |

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
Args:   audio_path (str), delay_time (float seconds), feedback (float 0-1), wet (float 0-1)
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

---

## SFX

| # | Tool | Description |
|---|---|---|
| 29 | `add_riser` | Build-up riser for transitions and drops. Styles: `noise`, `synth`, `filtered`, `vocal`. |
| 30 | `add_impact` | Impact/downlifter for the drop moment. Styles: `sub_boom`, `orchestral`, `noise_burst`, `synth_hit`. |
| 31 | `add_tuin` | High-pitched "tuin" ear-drum burst. Signature of funk bruxaria. Aggressive texture element. |

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

## Arrangement & Mix

| # | Tool | Description |
|---|---|---|
| 32 | `arrange_sections` | Arranges all stems into a full track structure with section markers. |
| 33 | `mix_tracks` | Mix multiple WAVs with individual levels and sidechain routing. |
| 34 | `apply_master` | Master bus processing. Presets: `phonk_standard`, `aggressive`, `clean`, `club_ready`. |
| 35 | `analyze_mix` | Analyze current mix — returns metrics and issue flags. |
| 36 | `export_song` | Export final track to MP3/WAV. |

### `arrange_sections`

```
Args:   structure (list[{tag, tracks, bars}]), track_files (dict[str: str])
Return: {path: str (wav)}
```

Structure format:
```json
[
  {"tag": "[Intro]",     "tracks": ["drums", "pad"],           "bars": 4},
  {"tag": "[Build Up]",  "tracks": ["drums", "bass", "riser"], "bars": 8},
  {"tag": "[Drop]",      "tracks": ["drums", "bass", "cowbells", "synth", "vocals", "impact"], "bars": 16},
  {"tag": "[Outro]",     "tracks": ["drums", "pad"],           "bars": 4}
]
```

### `mix_tracks`

```
Args:   tracks (dict[str: path]), levels (dict[str: float 0-1]),
        sidechain_target (str optional), sidechain_trigger (str optional)
Return: {path: str (wav)}
```

### `apply_master`

```
Args:   audio_path (str), preset (enum), loudness_target (float LUFS optional)
Return: {path: str (wav)}
```

### `analyze_mix`

```
Args:   audio_path (str)
Return: {rms_db, peak_db, low_energy, mid_energy, high_energy,
         dynamic_range_db, duration, issues: [str]}
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

### `export_song`

```
Args:   audio_path (str), format (enum "mp3" "wav"), bitrate (str default "320k")
Return: {path: str, duration: float, size_bytes: int}
```

---

## Reference

| # | Tool | Description |
|---|---|---|
| 37 | `reference_analyze` | Analyzes a user-uploaded reference phonk track. Extracts BPM, key, RMS target, spectral profile, and loudness. Agent uses this as a mixing/mastering target. |

### `reference_analyze`

```
Args:   audio_path (str)
Return: {bpm, key, rms_db, peak_db, spectral_profile: [...], loudness_lufs, duration}
```

---

## Agent Workflow Summary

A typical full generation (~22-28 rounds):

```
 1. set_project()
 2. write_lyrics()
 3. create_tamborzao()
 4. humanize_drums()          # on tamborzao
 5. add_cowbells()
 6. add_clap()                # optional
 7. add_sub_bass()
 8. add_synth_stab()
 9. add_horn_hit()            # optional
10. add_pad()                 # optional
11. generate_tts_vocals()
12. define_melody()
13. sing_vocals()             # TTS → melodic singing
14. pitch_shift()             # on vocals
15. formant_shift()           # on vocals
16. chop_vocals()
17. add_riser()
18. add_impact()
19. apply_distortion()        # on bass
20. apply_eq()                # on drums
21. apply_sidechain()         # bass ducks to kick
22. arrange_sections()
23. mix_tracks()
24. apply_master()
25. analyze_mix()
26. (iterate if issues found, back to relevant tool)
27. export_song()
```

Total tools: **37** across 8 categories.
