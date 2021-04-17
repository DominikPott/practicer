import logging
import os

from PIL import Image, ExifTags, UnidentifiedImageError

log = logging.getLogger(name=__name__)
log.setLevel(logging.DEBUG)


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
        print("No Tags found in reference images.")
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
