from PySide6 import QtWidgets, QtCore, QtGui


class ReferenceWidget(QtWidgets.QWidget):
    def __init__(self, references=[], parent=None):
        super(ReferenceWidget, self).__init__(parent=parent)
        self.references = references
        self.thumbnails = []
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setMaximumWidth(320)
        self.setMaximumHeight(180 * 4)
        self._randomize_images()
        self._populate_thumbnails()

    def new_images(self, images):
        self._clear()
        self.references = images
        self._randomize_images()
        self._populate_thumbnails()

    def _randomize_images(self):
        import random
        random.shuffle(self.references)

    def _populate_thumbnails(self):
        self._clear()
        for reference in self.references[:3]:
            image_container = QtWidgets.QLabel()
            image = QtGui.QImage(reference)
            thumbnail = QtGui.QPixmap.fromImage(image).scaled(320, 180, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                              QtCore.Qt.TransformationMode.SmoothTransformation)
            image_container.setPixmap(thumbnail)
            image_container.setScaledContents(True)
            image_container.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.layout().addWidget(image_container)
            self.thumbnails.append(image_container)

    def _clear(self):
        for image_container in self.thumbnails:
            self.layout().removeWidget(image_container)
            image_container.clear()
        self.thumbnails = []
