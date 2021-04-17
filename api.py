import logging

import exercise_interface
import file_setup
import reference_images

from config import REFERENCES_DIRECTORY

log = logging.getLogger("practicer")
log.setLevel(logging.DEBUG)


def exercises():
    return exercise_interface.exercises()


def create(exercise):
    file_setup.create(exercise)


def references_images(exercise):
    reference_dirs = exercise.get("references", [REFERENCES_DIRECTORY])
    return []
    collection = reference_images.crawl_images(roots=reference_dirs)
    images = []
    for tag in exercise.get("references_tags", []):
        images.extend(collection.get(tag, []))
    return images


def exercise_stats(exercise):
    stats = {"level": 1,
             "progress": 20}
    return stats
