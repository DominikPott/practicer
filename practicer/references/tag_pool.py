import logging
import os

import practicer.config

log = logging.getLogger(name=__name__)
log.setLevel(logging.DEBUG)

CONFIG = practicer.config.load()


def images(exercise):
    roots = exercise.get("references", [CONFIG["REFERENCES"]["PATH"]])  # TODO: Think of a better way. Config should
    # not be imported here.
    collection = crawl_images(roots=roots)
    images = []
    for tag in exercise.get("references_tags", []):
        images.extend(collection.get(tag, []))
    return images


def crawl_images(roots):
    data = {}
    for directory in roots:
        for root, dirs, files in os.walk(directory):
            for f in files:
                tags = image_tags(image=os.path.join(root, f))
                for tag in tags:
                    data.setdefault(tag, []).append(os.path.join(root, f))
    try:
        data.pop("")
    except KeyError:
        pass
    if not list(data.keys()):
        return {}
    log.debug(data)
    return data


def image_tags(image):
    try:
        return parse_image_for_tags(image)
    except UnidentifiedImageError:
        return []


def parse_image_for_tags(image):
    img = Image.open(image)
    img_exif = img.getexif()
    data = {}
    if img_exif:
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                data[ExifTags.TAGS[key]] = val
    tags = data.get("XPKeywords", b"")
    tags = tags.decode('utf-16')
    tags = tags.replace("\x00", "")
    tags = tags.split(";")
    return tags
