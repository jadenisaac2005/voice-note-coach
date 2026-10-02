# voice-note-coach

> **Status: work in progress.** Transcription and the core timing metrics
> (pauses, speaking and articulation rate, filler words) are implemented.
> The report and accuracy evaluation are still to come. v1 target: 25 Oct 2026.
## Problem

Voice notes are an easy way to practise speaking, but they give you no
feedback. voice-note-coach aims to analyse a recorded voice note and report
on delivery: speaking pace, filler words, long pauses, and run-on sentences.

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

## Usage

Put a recording in `data/raw/` (audio files there are git-ignored), then:

```bash
python scripts/run_transcribe.py data/raw/my_note.m4a
```

This prints the word count and duration, and saves segment- and word-level
timestamps to `data/transcripts/my_note.m4a.json` (the extension is kept so `note.wav` and
`note.m4a` don't overwrite each other).

Run the tests (macOS only; uses the `say` command to generate test audio):

```bash
pytest
```

## Roadmap

- **Done:** transcription with word-level timestamps; pause, rate and filler metrics.
- **Next:** longest run-on, a feedback report, accuracy evaluation on my own recordings.
- **v1 (25 Oct 2026):** public release with real accuracy numbers and limitations.
- **v2:** disfluency detection, pause tiers, and more metrics.

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

## License

MIT
