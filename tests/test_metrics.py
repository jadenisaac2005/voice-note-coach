import pytest
from voice_coach.metrics import compute_gaps, count_pauses, pause_ratio

def test_borderline_gap_is_not_a_pause():
    words = [
        {"word": "a", "start": 0.0, "end": 1.2},
        {"word": "b", "start": 2.2, "end": 2.7},   # gap of exactly 1.0 s, built so the float error shows up
    ]
    assert count_pauses(compute_gaps(words)) == 0

def test_one_long_gap_is_one_pause():
    words = [
        {"word": "a", "start": 0.0, "end": 0.5},
        {"word": "b", "start": 15.5, "end": 16.0},   # gap of 15.0 s
    ]
    assert count_pauses(compute_gaps(words)) == 1

def test_empty_list():
    assert compute_gaps([]) == []
    assert count_pauses([]) == 0
    assert pause_ratio([], 0.0) == 0.0

def test_pause_ratio_quarter_silence():
    # Last word ends at 60.0 s. Silence before words adds up to 15.0 s.
    words = [
        {"word": "a", "start": 5.0, "end": 15.0},   # leading silence: 5.0 s
        {"word": "b", "start": 25.0, "end": 35.0},   # gap before it: 10.0 s
        {"word": "c", "start": 35.0, "end": 60.0},
    ]
    gaps = compute_gaps(words)
    total_time = words[-1]["end"]
    assert pause_ratio(gaps, total_time) == pytest.approx(0.25)

def test_pause_ratio_no_silence():
    # gaps all 0.0, what should the ratio be?
    words = [
        {"word": "a", "start": 0.0, "end": 5.0},
        {"word": "b", "start": 5.0, "end": 10.0},
        {"word": "c", "start": 10.0, "end": 15.0},
    ]
    gaps = compute_gaps(words)
    total_time = words[-1]["end"]
    assert pause_ratio(gaps, total_time) == pytest.approx(0.0)

def test_pause_ratio_empty_clip():
    # what do you pass in for an empty list, and what should come back?
    gaps = []
    total_time = 1.0
    assert pause_ratio(gaps, total_time) == pytest.approx(0.0)

def test_overlapping_words_give_zero_gap():
    words = [
        {"word": "a", "start": 0.0, "end": 1.0},
        {"word": "b", "start": 0.9, "end": 2.0},   # starts 0.1 s before "a" ends
    ]
    assert compute_gaps(words) == [0.0, 0.0]
