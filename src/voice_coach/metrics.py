def compute_gaps(words):
    """Return the silence before each word, in seconds."""
    gaps = []
    for i in range(len(words)):
        if i == 0:
            gaps.append(round(words[i]["start"], 2))
        else:
            gaps.append(round(words[i]["start"] - words[i - 1]["end"], 2))
    return gaps

PAUSE_THRESHOLD = 1
def count_pauses(gaps, threshold=PAUSE_THRESHOLD):
    """Number of gaps strictly longer than threshold."""
    count = 0
    for gap in gaps:
        if gap > threshold:
            count += 1
    return count

def pause_ratio(gaps, total_time):
    """Fraction of the clip spent in silence between/before words."""
    if total_time == 0:
        return 0.0
    return sum(gaps) / total_time
