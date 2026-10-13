from voice_coach.wer import edit_distance

def test_edit_distance_cat_example():
    assert edit_distance("the cat sat".split(), "cat sat down".split()) == 2
