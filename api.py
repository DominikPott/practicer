import logging

import config_loader
import exercise_interface
import file_setup
import reference_images
import exercise_stats.api

log = logging.getLogger("practicer")
log.setLevel(logging.DEBUG)

CONFIG = config_loader.read_config()


def exercises():
    exercise_path = CONFIG["EXERCISES"]["PATH"]
    return exercise_interface.exercises(root=exercise_path)


def create(exercise):
    workpath = CONFIG["WORK"]["PATH"]
    template = CONFIG["TEMPLATE"]["DEFAULT"]
    file_setup.create(exercise=exercise, workpath=workpath, template=template)


def references_images(exercise):
    reference_dirs = exercise.get("references", [CONFIG["REFERENCES"]["PATH"]])
    collection = reference_images.crawl_images(roots=reference_dirs)
    images = []
    for tag in exercise.get("references_tags", []):
        images.extend(collection.get(tag, []))
    return images


def stats(exercise):
    return exercise_stats.api.stats(exercise)


def increment_exercise_stats(exercise):
    stats_ = stats(exercise)
    stats_["progress"] += 1
    if stats_["progress"] >= 10:
        stats_["level"] += 1
        stats_["progress"] = 0
    exercise_stats.api.update(exercise, stats_)