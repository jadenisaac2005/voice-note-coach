import pytest
from voice_coach.report import format_report

CLIP07 = {
    "speaking_rate": 162.72, "articulation_rate": 188.07,
    "pause_count": 0, "pause_ratio": 0.1348, "fillers": 0,
    "longest_run": {"seconds": 60.84, "n_words": 165},
}

def test_report_rounds_and_converts_units():
    out = format_report("07", CLIP07, 60.84, 165)
    assert "162.7 WPM" in out
    assert "13.5 %" in out

def test_report_zero_pauses_says_whole_clip():
    out = format_report("07", CLIP07, 60.84, 165)
    assert "No pause over 1 s: the whole clip was one stretch (60.8 s, 165 words)" in out

def test_report_with_pauses_prints_run_on():
    m = {**CLIP07, "pause_count": 3,
    "longest_run": {"seconds": 12.4, "n_words": 30}}
    out = format_report("x", m, 60.84, 165)
    assert "Count: 3" in out
    assert "12.4 s, 30 words" in out

def test_report_none_raises():
    with pytest.raises(ValueError):
        format_report("x", None, 0, 0)
