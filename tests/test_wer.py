import pytest
from voice_coach.wer import edit_distance, normalize, wer

def test_edit_distance_cat_example():
    assert edit_distance("the cat sat".split(), "cat sat down".split()) == 2

def test_wer_cat_example():
    assert wer("the cat sat", "cat sat down") == pytest.approx(2 / 3)

def test_wer_perfect():
    assert wer("the cat sat", "the cat sat") == 0.0

def test_wer_can_exceed_one():
    hyp = "the cat sat" + " down" * 97
    assert wer("the cat sat", hyp) == pytest.approx(97 / 3)

def test_wer_both_empty():
    assert wer("", "") == 0.0

def test_wer_empty_reference_nonempty_hyp():
    with pytest.raises(ValueError):
        wer("", "hello")

def test_wer_empty_hypothesis():
    assert wer("the cat sat", "") == 1.0

def test_wer_whitespace_reference():
    with pytest.raises(ValueError):
        wer("   ", "hello")

