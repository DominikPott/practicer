import logging

import practicer.config as config
import practicer.exercise_interface as exercise_interface
import practicer.file_setup as file_setup
import practicer.references.api as references
import practicer.exercise_stats.api as exercise_stats

log = logging.getLogger("practicer")
log.setLevel(logging.DEBUG)

CONFIG = config.load()


def exercises():
    exercise_path = CONFIG["EXERCISES"]["PATH"]
    return exercise_interface.exercises(root=exercise_path)


def start(exercise):
    exercise_stats.increment_exercise_stats(exercise)
    _create(exercise)


def _create(exercise):
    workpath = CONFIG["WORK"]["PATH"]
    template = CONFIG["TEMPLATE"]["DEFAULT"]
    file_setup.create(exercise=exercise, workpath=workpath, template=template)


def references_images(exercise):
    return references.images(exercise)


def stats(exercise):
    return exercise_stats.stats(exercise)
