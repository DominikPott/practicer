"""
https://www.youtube.com/watch?v=ynW_vIPVNbc

image = QtGui.QImage()
image.loadFromData()

"""
import requests


def images(exercise):
    for url in exercise.get('reference_urls', []):
        yield requests.get(url).content
