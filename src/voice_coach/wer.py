from voice_coach.metrics import clean_token


def edit_distance(ref, hyp):
    rows, cols = len(ref) + 1, len(hyp) + 1
    d = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        d[i][0] = i
    for j in range(cols):
        d[0][j] = j
    for i in range(1, rows):
        for j in range(1, cols):
            cost = 0
            if ref[i - 1] != hyp[j - 1]:
                cost = 1
            d[i][j] = min(
                d[i][j - 1] + 1,      # left: insertion
                d[i - 1][j] + 1,      # up: deletion
                d[i - 1][j - 1] + cost,  # diagonal: match / substitution
            )
    return d[-1][-1]

def wer(ref, hyp):
    ref_words = normalize(ref)
    hyp_words = normalize(hyp)
    if not ref_words and not hyp_words:
        return 0.0
    if not ref_words:
        raise ValueError("Reference is empty while hypothesis is not.")
    return edit_distance(ref_words, hyp_words) / len(ref_words)

def normalize(text):
    words = []
    for w in text.split():
        w = clean_token(w.lower())
        if w:
            words.append(w)
    return words
