import os
import json

from config import EXERCISES_DIRECTORY


def exercises():
    files = _find_exercise_files()
    return _parse(files)


def _find_exercise_files():
    exercise_files = []
    for root, dirs, files in os.walk(EXERCISES_DIRECTORY):
        exercises = [f for f in files if f.endswith(".json")]
        exercise_files.extend([os.path.join(root, exercise) for exercise in exercises])
    return exercise_files


def _parse(exercise_files):
    exercises = []
    for f in exercise_files:
        with open(f, "r") as exercise_file:
            exercises.append(json.load(exercise_file))
    return exercises
