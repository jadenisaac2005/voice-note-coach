"""CLI: python scripts/run_transcribe.py path/to/audio.m4a [--model base]"""

import argparse

from voice_coach.config import WHISPER_MODEL_SIZE
from voice_coach.transcribe import transcribe


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe a voice note with word timestamps.")
    parser.add_argument("audio_path", help="Path to an audio file (.m4a, .wav, .mp3, ...)")
    parser.add_argument("--model", default=WHISPER_MODEL_SIZE, help="faster-whisper model size")
    args = parser.parse_args()

    result = transcribe(args.audio_path, model_size=args.model)
    print(f"Words:    {len(result['words'])}")
    print(f"Duration: {result['duration']:.1f}s")
    print(f"Saved:    {result['output_path']}")


if __name__ == "__main__":
    main()
