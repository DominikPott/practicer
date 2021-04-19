import logging

from PySide6 import QtWidgets, QtCore, QtGui

log = logging.getLogger('practicer')
log.setLevel(logging.DEBUG)


class ReferenceWidget(QtWidgets.QWidget):
    def __init__(self, images=[], parent=None):
        super(ReferenceWidget, self).__init__(parent=parent)
        self.images = images
        self.containers = []
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setFixedSize(320, 540)
        self._randomize_images()
        self._populate_containers()

    def new_images(self, images):
        self._clear()
        self.images = images
        self._randomize_images()
        self._populate_containers()

    def _randomize_images(self):
        import random
        random.shuffle(self.images)

    def _populate_containers(self):
        self._clear()
        for reference in self.images[:3]:
            container = QtWidgets.QLabel()
            self.layout().addWidget(container)
            self.containers.append(container)
            container.setScaledContents(True)
            container.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

            image = image_factory(image=reference)
            thumbnail = QtGui.QPixmap.fromImage(image).scaled(320, 180, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                              QtCore.Qt.TransformationMode.SmoothTransformation)
            container.setPixmap(thumbnail)

    def _clear(self):
        for image_container in self.containers:
            self.layout().removeWidget(image_container)
            image_container.clear()
        self.containers = []


def image_factory(image):
    if image.type == 'path':
        return image_from_path(image)
    elif image.type == 'url':
        return image_from_url(image)


def image_from_url(image):
    img = QtGui.QImage()
    img.loadFromData(image.path)
    return img


def image_from_path(image):
    return QtGui.QImage(image.path)
