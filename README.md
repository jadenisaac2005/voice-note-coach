# voice-note-coach

> **Status: week 1, WIP.** Transcription only. No metrics or results yet.

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
timestamps to `data/transcripts/my_note.json`.

Run the tests (macOS only; uses the `say` command to generate test audio):

```bash
pytest
```

## Roadmap

- **Week 1:** transcription with word-level timestamps (this).
- **Week 2:** metrics (pace, fillers, pauses, run-ons) and a feedback report.

## License

MIT
