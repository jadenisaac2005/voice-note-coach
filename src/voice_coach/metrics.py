import string


def compute_gaps(words):
    """Return the silence before each word, in seconds."""
    gaps = []
    for i in range(len(words)):
        if i == 0:
            gaps.append(round(words[i]["start"], 2))
        else:
            gaps.append(max(0.0, round(words[i]["start"] - words[i - 1]["end"], 2)))
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

def speaking_rate(n_words, total_time):
    """Words per minute over the whole clip, silence included."""
    if total_time == 0:
        return 0.0
    return n_words / total_time * 60.0

def articulation_rate(n_words, total_time, gaps):
    """Words per minute over speaking time only (all gaps removed)."""
    speaking_time = total_time - sum(gaps)
    if speaking_time <= 0:
        return 0.0
    return n_words / speaking_time * 60.0

FILLERS = {"uh", "um" }   # your list

def clean_token(text):
    """Lowercase and strip spaces/punctuation so 'Um,' matches 'um'."""
    return text.lower().strip(string.punctuation + string.whitespace)

def count_fillers(words, fillers=FILLERS):
    """Number of words whose cleaned text is in the filler set."""
    count = 0
    for w in words:
        if clean_token(w["text"]) in fillers:
            count += 1
    return count

def split_runs(words, gaps, threshold=PAUSE_THRESHOLD):
    """Group words into stretches. A new stretch starts when the
    silence before a word is longer than threshold."""
    runs = []
    current = []
    for i, w in enumerate(words):
        if i > 0 and gaps[i] > threshold:   # blank 1: which comparison? why "i > 0"?
            runs.append(current)
            current = []
        current.append(w)
    if current:                                         # blank 2: what's lost if this is missing?
        runs.append(current)
    return runs

def longest_run_on(words, threshold=PAUSE_THRESHOLD):
    """Longest stretch of speech with no pause, as {"seconds": seconds, "n_words": n_words}."""
    if not words:
        return                       # same shape as the normal return
    gaps = compute_gaps(words)          # which existing function?
    runs = split_runs(words, gaps, threshold)
    best = dict()                          # what do you compare runs by? (your decision in #3)
    for run in runs:
        if not run:
            continue
        n_words = len(run)
        seconds = run[-1]["end"] - run[0]["start"]  # first word's start to last word's end
        if seconds > best.get("seconds", 0):
            best = {"seconds": seconds, "n_words": n_words}
    return best

def compute_metrics(words):
    """All v1 metrics for one clip, or None if there are no words."""
    if not words:
        return None
    gaps = compute_gaps(words)
    total_time = words[-1]["end"]              # last words end time
    return {
        "speaking_rate": speaking_rate(len(words), total_time),
        "articulation_rate": articulation_rate(len(words), total_time, gaps),
        "pause_count": count_pauses(gaps),
        "pause_ratio": pause_ratio(gaps, total_time),
        "fillers": count_fillers(words),
        "longest_run": longest_run_on(words),
    }
