import logging
import os

import practicer.config as config

log = logging.getLogger(name=__name__)
log.setLevel(logging.DEBUG)

CONFIG = config.load()


def images(exercise):
    roots = exercise.get("references", [CONFIG["REFERENCES"]["PATH"]])  # TODO: Think of a better way. Config should
    # not be imported here.
    return crawl_images(roots=roots)


def crawl_images(roots):
    for directory in roots:
        for root, dirs, files in os.walk(directory):
            for f in files:
                yield os.path.join(root, f)

