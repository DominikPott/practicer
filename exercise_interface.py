import os
import json


def exercises(root):
    files = _find_exercise_files(root=root)
    return _parse(files)


def _find_exercise_files(root):
    exercise_files = []
    for root_dir, dirs, files in os.walk(root):
        files = [f for f in files if f.endswith(".json")]
        exercise_files.extend([os.path.join(root_dir, exercise) for exercise in files])
    return exercise_files


def _parse(exercise_files):
    exercises_ = []
    for f in exercise_files:
        with open(f, "r") as exercise_file:
            exercises_.append(json.load(exercise_file))
    return exercises_
