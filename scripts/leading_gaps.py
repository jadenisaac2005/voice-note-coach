import json
from pathlib import Path
from voice_coach.metrics import compute_gaps, count_pauses, pause_ratio

rows = []
for path in sorted(Path("data/transcripts").glob("*.json")):
    words = json.loads(path.read_text())["words"]
    if not words:
        continue
    gaps = compute_gaps(words)
    total_time = words[-1]["end"]

    leading = gaps[0] if gaps else 0                      # the leading gap
    ratio_with = pause_ratio(gaps, total_time)
    ratio_without = pause_ratio(gaps[1:], total_time)   # same clip, leading gap removed
    # blank 3: pause count with vs without the leading gap (same threshold as the repo)
    pause_count_with = count_pauses(gaps, total_time)
    pause_count_without = count_pauses(gaps)
    rows.append((path.name[:2], leading, ratio_with, ratio_without))
    print(f"{path.name[:2]}  lead={leading:5.2f}s  ratio {ratio_with:.1%} -> {ratio_without:.1%}")

# blank 4: print min / median / max of the leading gaps
if rows:
    leading_gaps = [row[1] for row in rows]
    print(f"Leading gaps: min={min(leading_gaps):.2f}s  median={sorted(leading_gaps)[len(leading_gaps)//2]:.2f}s  max={max(leading_gaps):.2f}s")
