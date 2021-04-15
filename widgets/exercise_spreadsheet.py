from PySide6 import QtWidgets, QtCore, QtGui


class ExerciseSpreadSheet(QtWidgets.QWidget):

    def __init__(self, exercise, parent=None):
        super(ExerciseSpreadSheet, self).__init__(parent)

        self.exercise = exercise
        self.thumbnail = QtWidgets.QLabel()
        self.thumbnail.setMinimumSize(640, 360)

        self.summary = QtWidgets.QLabel()
        self.summary.setAlignment(QtCore.Qt.AlignCenter)
        self.summary.setFixedHeight(50)
        font = QtGui.QFont("Times", 12, QtGui.QFont.DemiBold)
        font.setCapitalization(QtGui.QFont.Capitalize)
        self.summary.setFont(font)

        self.instructionsGroup = QtWidgets.QGroupBox("Instructions:")
        self.instruction = QtWidgets.QLabel()
        self.instruction.setMinimumHeight(100)
        self.instruction.setAlignment(QtCore.Qt.AlignCenter)
        self.instruction.setFont(QtGui.QFont("Times", 10))
        self.instruction.setWordWrap(True)
        self.instructionsLayout = QtWidgets.QVBoxLayout()
        self.instructionsLayout.addWidget(self.instruction)
        self.instructionsGroup.setLayout(self.instructionsLayout)

        self.linksGroup = QtWidgets.QGroupBox("Links:")
        self.linksGroup.setMaximumHeight(60)
        self.links = QtWidgets.QLabel()
        self.links.setAlignment(QtCore.Qt.AlignCenter)
        self.links.setOpenExternalLinks(True)
        self.linksLayout = QtWidgets.QVBoxLayout()
        self.linksLayout.addWidget(self.links)
        self.linksGroup.setLayout(self.linksLayout)

        self.statsGroup = QtWidgets.QGroupBox("Stats:")
        self.stats = QtWidgets.QLabel()

        self.stats.setAlignment(QtCore.Qt.AlignVCenter)
        self.stats.setOpenExternalLinks(True)
        self.statsLayout = QtWidgets.QVBoxLayout()
        self.statsLayout.addWidget(self.stats)
        self.statsGroup.setLayout(self.statsLayout)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.summary)
        self.layout().addWidget(self.thumbnail)
        self.layout().addWidget(self.instructionsGroup)
        self.layout().addWidget(self.linksGroup)
        self.layout().addWidget(self.statsGroup)
        self._refresh()

    def _refresh(self):
        self.summary.setText(self.exercise.get("label", "No Label"))
        self.instruction.setText(self.exercise.get("instruction", "No Instructions"))
        self.links.setText(self._format_hyperlinks())
        self._format_stats()
        self._update_thumbnail()

    def _format_hyperlinks(self):
        links = self.exercise.get("hyperlinks", [""])
        formated_links = ["<a href='{link}' style='color: gray;'>{short_link}</a >".format(link=link, short_link=link[:30]) for link in links]
        return " | ".join(formated_links)

    def _update_thumbnail(self):
        thumbnail_path = self.exercise.get("thumbnail", "")
        thumbnail = QtGui.QPixmap(thumbnail_path).scaled(640, 360, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                         QtCore.Qt.TransformationMode.SmoothTransformation)
        self.thumbnail.setPixmap(thumbnail)
        self.thumbnail.setScaledContents(True)

    def _format_stats(self):
        stats = ""
        stats += "Level: " + str(self.exercise.get("level", -1.0))
        self.stats.setText(stats)

    def refresh(self, exercise):
        self.exercise = exercise
        self._refresh()

