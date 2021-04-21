import practicer.api as api


def test_exercises():
    assert api.exercises() == []


def test_exercise_stats():
    assert api.exercise_stats(exercise=[]) == dict()
