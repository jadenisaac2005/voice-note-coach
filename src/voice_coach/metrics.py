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
