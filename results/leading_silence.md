# Leading silence: audio vs Whisper

Every clip starts with some silence between pressing record and the first
word. This compares how long that silence really is with what Whisper's
timestamps say.

- **Audio lead:** start of the first speech in the audio, from
  `ffmpeg -af silencedetect=noise=-35dB:d=0.1`. This is also an estimate,
  because it depends on the -35 dB threshold.
- **Whisper lead:** the first word's `start` in the transcript
  (`compute_gaps(words)[0]`), which is what the metrics use.

| Clip | Audio lead (s) | Whisper lead (s) | Difference (s) |
|---|---|---|---|
| 01 | 0.73 | 0.00 | 0.73 |
| 02 | 0.41 | 0.00 | 0.41 |
| 03 | 0.35 | 0.00 | 0.35 |
| 04 | 0.12 | 0.00 | 0.12 |
| 05 | 0.48 | 0.00 | 0.48 |
| 06 | 0.99 | 0.00 | 0.99 |
| 07 | 0.91 | 0.00 | 0.91 |
| 08 | 0.41 | 0.00 | 0.41 |
| 09 | 1.09 | 0.82 | 0.27 |
| 10 | 1.75 | 1.82 | -0.07 |

Audio lead: median 0.61 s, mean 0.72 s.

## What it shows

- Whisper puts the first word at 0.00 s on every clip whose audio lead is
  under about 1 s (8 of 10).
- On the two clips with a longer lead (09, 10), Whisper's value is close to
  the audio. Two clips is too few to call that a rule.

## Effect on the metrics

- **Time between words:** the missing leading silence understates it by up
  to about 1.6 points (clip 06).
- **Pause count:** changes on one clip only. Clip 09's real lead (1.09 s) is
  a pause over 1 s, but Whisper's (0.82 s) isn't. Clips 06 and 07 sit just
  under 1 s either way.

v1 keeps Whisper's first-word start. An audio-based onset is parked in
`v2_ideas.md`.
