import logging

import config_loader
import exercise_interface
import file_setup
import references.api
import exercise_stats.api

log = logging.getLogger("practicer")
log.setLevel(logging.DEBUG)

CONFIG = config_loader.read_config()


def exercises():
    exercise_path = CONFIG["EXERCISES"]["PATH"]
    return exercise_interface.exercises(root=exercise_path)


def start(exercise):
    _create(exercise)
    _increment_exercise_stats(exercise)


def _create(exercise):
    workpath = CONFIG["WORK"]["PATH"]
    template = CONFIG["TEMPLATE"]["DEFAULT"]
    file_setup.create(exercise=exercise, workpath=workpath, template=template)


def _increment_exercise_stats(exercise):
    stats_ = stats(exercise)
    stats_["progress"] += 1
    if stats_["progress"] >= 10:
        stats_["level"] += 1
        stats_["progress"] = 0
    exercise_stats.api.update(exercise, stats_)


def references_images(exercise):
    return references.api.images(exercise)


def stats(exercise):
    return exercise_stats.api.stats(exercise)
