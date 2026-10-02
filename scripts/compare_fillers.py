import json
from pathlib import Path
from voice_coach.metrics import FILLERS, clean_token

CLIPS = ["05_impromptu", "09_casualConvo", "10_casualConvo"]

for path in sorted(Path("data/transcripts").glob("*.json")):
    if not any(path.name.startswith(c) for c in CLIPS):
        continue
    words = json.loads(path.read_text())["words"]
    for i, w in enumerate(words):
        token = clean_token(w["text"])
        if token in FILLERS:
            context = " ".join(x["text"] for x in words[max(0, i - 3): i + 4])
            print(f"{path.name[:2]} {token:6} | {context}")
