import logging
import os

import practicer.config as config

log = logging.getLogger(name=__name__)
log.setLevel(logging.DEBUG)


def images(exercise):
    roots = exercise.get("reference_paths", [])
    return crawl_images(roots=roots)


def crawl_images(roots):
    for directory in roots:
        for root, dirs, files in os.walk(directory):
            for f in files:
                yield os.path.join(root, f)

