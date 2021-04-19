import logging
import json
import os
import pathlib

import practicer.config

CONFIG = practicer.config.load()
DEFAULT_STATS = {'level': 0, 'progress': 0.0, 'level_max_progress': 1}

log = logging.getLogger('practicer')
log.setLevel(logging.DEBUG)


def update_exercise_stats(exercise, stats):
    filepath = _exercise_path(exercise)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as fp:
        json.dump(stats, fp)


def load_stats(exercise):
    try:
        return _load_stats_file(exercise)
    except FileNotFoundError:
        return DEFAULT_STATS


def _load_stats_file(exercise):
    filepath = _exercise_path(exercise)
    with open(filepath) as fp:
        return json.load(fp)


def _exercise_path(exercise):
    stats_dir = CONFIG['STATS']['PATH']
    filepath = pathlib.Path(stats_dir)
    name = exercise.get('name', 'default')
    return filepath / (name + '.json')
