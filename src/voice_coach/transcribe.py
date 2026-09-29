"""Transcribe audio with faster-whisper, keeping word-level timestamps.

What is a word-level timestamp? Whisper natively predicts text in segments
(roughly sentence-sized chunks), not per-word times. faster-whisper estimates
when each word starts and ends by looking at the decoder's cross-attention
weights (which audio frames each output token "attended to") and aligning
tokens to frames with dynamic time warping (DTW). These times are therefore
model-derived estimates, not ground truth: expect errors of tens to a few
hundred milliseconds, especially around silences and fast speech.
"""

from __future__ import annotations

import json
from pathlib import Path

from faster_whisper import WhisperModel

from voice_coach.config import WHISPER_MODEL_SIZE

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "transcripts"


def transcribe(
    audio_path: str,
    model_size: str = WHISPER_MODEL_SIZE,
    output_dir: str | Path | None = None,
) -> dict:
    """Transcribe `audio_path` and write the result to `<output_dir>/<stem>.json`.

    Returns a JSON-serializable dict with top-level `words` (text/start/end)
    and `segments` (text/start/end), plus metadata. `output_dir` defaults to
    data/transcripts/.
    """
    audio = Path(audio_path)
    # CPU + int8 quantization: the fastest option on Intel Macs without a GPU.
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments_iter, info = model.transcribe(str(audio), word_timestamps=True)

    segments = []
    words = []
    # `segments_iter` is a lazy generator; transcription happens as we iterate.
    for seg in segments_iter:
        segments.append({"text": seg.text.strip(), "start": seg.start, "end": seg.end})
        for w in seg.words or []:
            words.append({"text": w.word.strip(), "start": w.start, "end": w.end})

    result = {
        "audio_path": str(audio),
        "model_size": model_size,
        "language": info.language,
        "duration": info.duration,
        "segments": segments,
        "words": words,
    }

    out_dir = Path(output_dir) if output_dir is not None else DEFAULT_OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{audio.name}.json"
    out_path.write_text(json.dumps(result, indent=2))
    result["output_path"] = str(out_path)
    return result
