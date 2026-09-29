"""Synthetic smoke test for transcribe().

This only checks that the pipeline runs end-to-end and returns the expected
structure. It does NOT validate transcription accuracy or timestamp quality:
the audio is a macOS `say` TTS clip, not real speech.
"""

import json
import shutil
import subprocess

import pytest

from voice_coach.transcribe import transcribe

pytestmark = pytest.mark.skipif(shutil.which("say") is None, reason="needs macOS `say`")


@pytest.fixture
def tts_wav(tmp_path):
    wav = tmp_path / "smoke.wav"
    subprocess.run(
        ["say", "-o", str(wav), "--data-format=LEI16@16000",
         "This is a short test of the voice note coach."],
        check=True,
    )
    yield wav
    wav.unlink(missing_ok=True)  # tmp_path is also auto-cleaned by pytest


def test_transcribe_structure(tts_wav, tmp_path):
    out_dir = tmp_path / "transcripts"
    result = transcribe(str(tts_wav), model_size="base", output_dir=out_dir)

    words = result["words"]
    assert words, "expected a non-empty words list"
    for w in words:
        assert set(w) >= {"text", "start", "end"}
        assert w["start"] < w["end"]
    starts = [w["start"] for w in words]
    assert starts == sorted(starts), "word start times should be non-decreasing"

    assert result["segments"] and all("text" in s for s in result["segments"])

    saved = json.loads((out_dir / "smoke.wav.json").read_text())
    assert saved["words"] == words
