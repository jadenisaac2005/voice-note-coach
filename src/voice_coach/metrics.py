def compute_gaps(words):
    """Return the silence before each word, in seconds."""
    gaps = []
    for i in range(len(words)):
        if i == 0:
            gaps.append(words[i]["start"])
        else:
            gaps.append(words[i]["start"] - words[i - 1]["end"])
    return gaps

words = [
    {"word": "hello", "start": 0.0, "end": 0.5},
    {"word": "there", "start": 0.6, "end": 1.0},
    {"word": "friend", "start": 3.0, "end": 3.4},
]
print(compute_gaps(words))
