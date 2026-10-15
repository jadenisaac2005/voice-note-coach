import json
from pathlib import Path
from voice_coach.wer import wer, normalize
import difflib

for clip in ["07", "08"]:
    ref = Path(f"data/references/{clip}.txt").read_text()
    path = next(Path("data/transcripts").glob(f"{clip}*.json"))
    data = json.loads(path.read_text())
    hyp = " ".join(w["text"] for w in data["words"])
    print(clip, len(normalize(ref)), len(normalize(hyp)), round(wer(ref, hyp), 4))
    r, h = normalize(ref), normalize(hyp)
    for op in difflib.SequenceMatcher(None, r, h).get_opcodes():
        if op[0] != "equal":
            print("  ", op[0], r[op[1]:op[2]], "->", h[op[3]:op[4]])
