import pytest
from voice_coach.metrics import compute_gaps, compute_metrics, count_pauses, pause_ratio, speaking_rate, articulation_rate, count_fillers, longest_run_on

def test_borderline_gap_is_not_a_pause():
    words = [
        {"word": "a", "start": 0.0, "end": 1.2},
        {"word": "b", "start": 2.2, "end": 2.7},   
    ]
    assert count_pauses(compute_gaps(words)) == 0

def test_one_long_gap_is_one_pause():
    words = [
        {"word": "a", "start": 0.0, "end": 0.5},
        {"word": "b", "start": 15.5, "end": 16.0},
    ]
    assert count_pauses(compute_gaps(words)) == 1

def test_empty_list():
    assert compute_gaps([]) == []
    assert count_pauses([]) == 0
    assert pause_ratio([], 0.0) == 0.0

def test_pause_ratio_quarter_silence():

    words = [
        {"word": "a", "start": 5.0, "end": 15.0},
        {"word": "b", "start": 25.0, "end": 35.0},
        {"word": "c", "start": 35.0, "end": 60.0},
    ]
    gaps = compute_gaps(words)
    total_time = words[-1]["end"]
    assert pause_ratio(gaps, total_time) == pytest.approx(0.25)

def test_pause_ratio_no_silence():

    words = [
        {"word": "a", "start": 0.0, "end": 5.0},
        {"word": "b", "start": 5.0, "end": 10.0},
        {"word": "c", "start": 10.0, "end": 15.0},
    ]
    gaps = compute_gaps(words)
    total_time = words[-1]["end"]
    assert pause_ratio(gaps, total_time) == pytest.approx(0.0)

def test_pause_ratio_empty_clip():

    gaps = []
    total_time = 1.0
    assert pause_ratio(gaps, total_time) == pytest.approx(0.0)

def test_overlapping_words_give_zero_gap():
    words = [
        {"word": "a", "start": 0.0, "end": 1.0},
        {"word": "b", "start": 0.9, "end": 2.0},
    ]
    assert compute_gaps(words) == [0.0, 0.0]

def test_rates_sixty_second_example():
    gaps = [0.5] * 30
    assert speaking_rate(150, 60.0) == pytest.approx(150.0)
    assert articulation_rate(150, 60.0, gaps) == pytest.approx(200.0)

def test_rates_equal_when_no_silence():
    gaps = [0.0, 0.0, 0.0]
    assert speaking_rate(30, 15.0) == pytest.approx(articulation_rate(30, 15.0, gaps))

def test_rates_zero_time():
    assert speaking_rate(10, 0.0) == pytest.approx(0.0)
    assert articulation_rate(10, 0.0, []) == pytest.approx(0.0)

def test_count_fillers_normalises_whisper_tokens():
    words = [
        {"text": " Um,", "start": 0.0, "end": 0.3},
        {"text": "uh", "start": 0.4, "end": 0.6},
        {"text": " umbrella", "start": 0.7, "end": 1.1},
        {"text": " table", "start": 1.2, "end": 1.5},
        {"text": " so", "start": 1.7, "end": 2.0},
    ]
    assert count_fillers(words) == 2

def test_count_fillers_empty():
    assert count_fillers([]) == 0

def test_longest_run_on():
    words = [
        {"text": "a", "start": 0.0, "end": 0.4},
        {"text": "b", "start": 0.5, "end": 0.9},
        {"text": "c", "start": 1.0, "end": 1.4},
        {"text": "d", "start": 2.1, "end": 2.5},
        {"text": "e", "start": 2.6, "end": 3.0},
        {"text": "f", "start": 3.1, "end": 3.5},
        {"text": "g", "start": 3.6, "end": 4.0},
        {"text": "h", "start": 5.5, "end": 5.9},
        {"text": "i", "start": 6.0, "end": 6.4},
    ]
    assert longest_run_on(words) == {'seconds': 4.0, 'n_words': 7}

def test_longest_run_on_leading_silence():
    words = [
        {"text": "a", "start": 3.0, "end": 3.4},
        {"text": "b", "start": 3.5, "end": 3.9},
        {"text": "c", "start": 4.0, "end": 4.4},
        {"text": "d", "start": 5.1, "end": 5.5},
        {"text": "e", "start": 5.6, "end": 6.0},
        {"text": "f", "start": 6.1, "end": 6.5},
        {"text": "g", "start": 6.6, "end": 7.0},
        {"text": "h", "start": 8.5, "end": 8.9},
        {"text": "i", "start": 9.0, "end": 9.4},
    ]
    assert longest_run_on(words) == {'seconds': 4.0, 'n_words': 7}

def test_longest_run_on_empty():
    assert longest_run_on([]) == None

def make_words(start, n, word_len, gap):
    """n words from `start`, each word_len long, with `gap` of silence between them."""
    words = []
    t = start
    for i in range(n):
        words.append({"text": f"w{i}", "start": round(t, 2), "end": round(t + word_len, 2)})
        t += word_len + gap
    return words

def test_longest_is_by_seconds_not_words():
    slow = make_words(0.0, 10, 0.6, 0.2)
    fast = make_words(slow[-1]["end"] + 1.5, 20, 0.3, 0.0)
    result = longest_run_on(slow + fast)
    assert result == pytest.approx({"seconds": 7.8, "n_words": 10})

def test_compute_metrics_nine_word_example():
    words = [
        {"text": "a", "start": 0.0, "end": 0.4},
        {"text": "b", "start": 0.5, "end": 0.9},
        {"text": "c", "start": 1.0, "end": 1.4},
        {"text": "d", "start": 2.1, "end": 2.5},
        {"text": "e", "start": 2.6, "end": 3.0},
        {"text": "f", "start": 3.1, "end": 3.5},
        {"text": "g", "start": 3.6, "end": 4.0},
        {"text": "h", "start": 5.5, "end": 5.9},
        {"text": "i", "start": 6.0, "end": 6.4},
        ]
    m = compute_metrics(words)
    assert m["speaking_rate"] == pytest.approx(84.375)
    assert m["articulation_rate"] == pytest.approx(150.0)
    assert m["pause_count"] == 1
    assert m["pause_ratio"] == pytest.approx(0.4375)
    assert m["fillers"] == 0
    assert m["longest_run"] == {"seconds": 4.0, "n_words": 7}

def test_compute_metrics_empty():
    assert compute_metrics([]) is None

def test_compute_metrics_leading_silence():
    words = [
        {"text": "a", "start": 3.0, "end": 3.4},
        {"text": "b", "start": 3.5, "end": 3.9},
        {"text": "c", "start": 4.0, "end": 4.4},
        {"text": "d", "start": 5.1, "end": 5.5},
        {"text": "e", "start": 5.6, "end": 6.0},
        {"text": "f", "start": 6.1, "end": 6.5},
        {"text": "g", "start": 6.6, "end": 7.0},
        {"text": "h", "start": 8.5, "end": 8.9},
        {"text": "i", "start": 9.0, "end": 9.4},
    ]
    m = compute_metrics(words)
    assert m["speaking_rate"] == pytest.approx(57.4468085106)
    assert m["articulation_rate"] == pytest.approx(150.0)
    assert m["pause_count"] == 2
    assert m["pause_ratio"] == pytest.approx(0.6170212766)
    assert m["fillers"] == 0
    assert m["longest_run"] == {"seconds": 4.0, "n_words": 7}
