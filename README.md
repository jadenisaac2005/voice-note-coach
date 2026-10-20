
# voice-note-coach

> **Status:** **released 20 Oct 2026**.

Record yourself speaking, get specific feedback on how you talk: pace,
pauses, filler words, and the longest stretch without a break. Whisper does
the transcription. Every metric, and the WER evaluation, is hand-written and
tested on top of Whisper's word timestamps, and the accuracy section reports
what the numbers can and can't tell you.

## Example

```text
$ python -m voice_coach.report data/raw/09_casualConvo.m4a
Voice-Note Coach: 09_casualConvo
Duration (to last word): 60.8 s     Words: 142

Pace
  Speaking rate:      140.0 WPM   (silence included)
  Articulation rate:  197.6 WPM   (all gaps removed)

Pauses
  Count: 4        (gap > 1 s)
  Time between words: 29.1 %  (all gaps, short ones included)

Fillers (um/uh only)
  Count: 0

Longest run-on
  27.2 s, 71 words  (no pause > 1 s)

Limits: Whisper often drops um/uh, so the filler count is a lower bound.
```

https://github.com/user-attachments/assets/8b50666f-0208-4ab0-be7b-7256dece6b60

## How it works

1. **Transcribe.** [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
   (CPU, int8) with `word_timestamps=True` gives each word a start and end
   time. The transcript is saved to `data/transcripts/<file>.json`.
2. **Gaps.** The silence before each word: `start - previous end`, rounded
   to 2 dp, clamped at 0 when words overlap. The first gap is the silence
   before the first word.
3. **Metrics** (`src/voice_coach/metrics.py`), all timed from 0 to the end
   of the last word, so trailing silence is excluded:

| Metric | Definition |
|---|---|
| Speaking rate | words ÷ total time × 60. Silence included. |
| Articulation rate | words ÷ (total time − all gaps) × 60. Speed while actually talking. |
| Pause count | gaps longer than 1.0 s (a gap of exactly 1.0 s doesn't count) |
| Time between words | sum of all gaps ÷ total time, short gaps included |
| Fillers | words that are "um" or "uh" after lowercasing and stripping punctuation |
| Longest run-on | the longest stretch with no gap over 1.0 s, in seconds and words |

4. **Report** (`src/voice_coach/report.py`). `format_report` turns the
   numbers into text and never touches audio, so it's tested without
   Whisper. `main()` does the wiring.

## Setup

Requires Python 3.10+. Runs on CPU (no GPU needed).

With uv:

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
```

Or with pip:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

The first run downloads the Whisper model (~150 MB for `base`).
`av` is pinned below 19: with faster-whisper 1.2.1, `av` 19 fails when
opening audio (`unexpected keyword argument 'metadata_errors'`).

## Usage

Put a recording in `data/raw/` (audio there is git-ignored), then:

```bash
python -m voice_coach.report data/raw/my_note.m4a
```

To transcribe only (word count, duration, and the saved JSON):

```bash
python scripts/run_transcribe.py data/raw/my_note.m4a
```

Transcripts are saved as `my_note.m4a.json`, extension kept, so
`note.wav` and `note.m4a` don't overwrite each other.

Run the tests (macOS only; `say` generates the test audio):

```bash
pytest
```

## Accuracy

### Transcription (WER)

I read two passages aloud, word for word (clips 07 and 08), and compared
Whisper's transcript with the script using word error rate. WER =
(substitutions + deletions + insertions) ÷ words in the script, computed
with my own edit-distance code (`src/voice_coach/wer.py`). It has no upper
limit, so it's a rate, not "percent wrong". Both texts are lowercased and
stripped of punctuation first. Numbers and contractions are not normalized.

Then I listened back to the errors and sorted them by cause:

| Clip | Words | WER | Formatting | Whisper | Me |
|---|---|---|---|---|---|
| 07 | 165 | 7.9 % | 3 | 8 | 2 |
| 08 | 162 | 5.6 % | 5 | 4 | 0 |

- **Formatting:** Whisper heard the word right but wrote it differently
  ("nine" → `9`, "grey" → `gray`, "do not" → `don't`).
- **Whisper:** I said the script word and Whisper wrote something else.
- **Me:** I didn't read what was written.

**Whisper's own WER on my voice: 12 / 327 words = 3.7 %.** Full table in
`results/wer_07_08.md`.

Caveats: two clips, one speaker, read speech (spontaneous speech will be
worse), `base` model. I didn't check the contractions on clip 08 by ear.
The reference passages were written for this test set. Decoding is
deterministic, so re-running gives the same transcript.

One case worth noting: on clip 08 I said "actually", corrected myself to
"really", and Whisper kept "actually" and dropped "really". On this clip the
transcript hid the self-correction, so anything counting from the
transcript would miss it (see v2).

### Timestamps

<!-- - **Pauses:** I checked __ pauses against the audio and found __. TODO -->
- **Leading silence:** every clip starts with silence (checked with
  `ffmpeg silencedetect`, −35 dB), but Whisper reports the first word at
  0.00 s whenever the real lead is under about 1 s (8 of my 10 clips).
  This shifts time between words by up to about 1.6 points. Above 1 s it
  roughly tracks the audio, but that's based on only two clips.
- **Threshold sweep:** I worried that counting every gap would mostly count
  tiny gaps where Whisper's timestamps are unreliable. The sweep showed
  gaps ≤ 0.25 s make up only 0.9 of the 18.8 points of pause ratio; most
  silence sits in 0.25–1.0 s gaps (11.1 points). So "subtract every gap"
  holds up. The sweep can't show whether a gap is real silence: a word
  that Whisper stretches across a pause never shows up as a gap.

## Known limitations

- **Filler words.** Only "um" and "uh" are counted. Whisper tends to leave
  them out of its transcript, so the count is a lower bound. Words like "so",
  "like" and "right" are not counted, because they are also ordinary words
  and a word-matching rule can't tell the two uses apart.
- **Timestamps are estimates.** Word times come from the model, so pause
  lengths can be off by a fraction of a second.
- **Articulation rate is speed, not clarity.** It is words per minute with
  silence removed. None of the metrics measure how clear someone is.
- **Leading silence counts as a pause.** It includes the delay between
  pressing record and starting to speak.
- **Thresholds matter.** Run-on length depends heavily on the 1.0 s
  threshold: clip 07's longest run is 60.8 s at 1.0 s but 19.1 s at 0.5 s.
- **Empty script.** `wer()` raises `ValueError` for an empty script, because
  dividing by zero words would give `inf`, which silently ruins any average
  it ends up in. An error stops the run instead.

## Data

Only my own recordings. Raw audio is git-ignored. Transcripts, the two
reference passages and results are committed.

## Roadmap

- **v1:** released 20 Oct 2026.
- **v2 (starts by Mar 2027 at the latest):** my own disfluency detector
  trained on audio spectrograms (e.g. SEP-28k): reproduce a published
  baseline, run ablations, and compare it with Whisper-plus-counting. Parked
  ideas are in `v2_ideas.md`.

## License

MIT
