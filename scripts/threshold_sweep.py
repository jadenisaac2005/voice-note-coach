import json
from pathlib import Path
from voice_coach.metrics import compute_gaps, longest_run_on

def silence_above(gaps, t):
    """Total seconds of gaps strictly longer than t."""
    return sum(g for g in gaps if g > t)

THRESHOLDS = [0, 0.25, 0.5, 1.0]
for path in sorted(Path("data/transcripts").glob("*.json")):
    clips = json.loads(path.read_text())["words"]
    words = json.loads(path.read_text())["words"]
    gaps = compute_gaps(words)
    total_time = words[-1]["end"]
    for t in THRESHOLDS:
        silence = silence_above(gaps, t)
        ar = len(words) / (total_time - silence) * 60
        ratio = silence / total_time                     # silence / total_time
        run = longest_run_on(words, threshold=t)
        print(f"{path.name[:2]}", t, round(ar, 1), round(ratio, 2), run["seconds"], run["n_words"])
