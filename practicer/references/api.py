from collections import namedtuple

import practicer.references.fs as filesystem
import practicer.references.url as url

Image = namedtuple("Image", ["path", "type"])


def images(exercise):
    imgs = [Image(i, 'path') for i in filesystem.images(exercise)]
    imgs += [Image(i, 'url') for i in url.images(exercise)]
    return imgs
