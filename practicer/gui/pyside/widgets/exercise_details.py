from PySide2 import QtWidgets, QtCore, QtGui
import practicer.gui.pyside.resources  # pyside compiles resources. Holds the icons for qresources


class ExerciseSpreadSheet(QtWidgets.QWidget):

    def __init__(self, exercise, stats, parent=None):
        super(ExerciseSpreadSheet, self).__init__(parent)

        self.exercise = exercise
        self._stats = stats
        self.thumbnail = QtWidgets.QLabel()
        self.thumbnail.setMinimumSize(640, 360)

        self.exercise_name = QtWidgets.QLabel()
        self.exercise_name.setAlignment(QtCore.Qt.AlignCenter)
        self.exercise_name.setFixedHeight(50)
        font = QtGui.QFont("Times", 12, QtGui.QFont.DemiBold)
        font.setCapitalization(QtGui.QFont.Capitalize)
        self.exercise_name.setFont(font)

        self.instructionsGroup = QtWidgets.QGroupBox("Instructions:")
        self.instruction = QtWidgets.QLabel()
        self.instruction.setMinimumHeight(100)
        self.instruction.setAlignment(QtCore.Qt.AlignLeading)
        self.instruction.setFont(QtGui.QFont("Times", 10))
        self.instruction.setWordWrap(True)
        self.instructionsLayout = QtWidgets.QVBoxLayout()
        self.instructionsLayout.addWidget(self.instruction)
        self.instructionsGroup.setLayout(self.instructionsLayout)

        self.linksGroup = QtWidgets.QGroupBox("Tutorials:")
        self.links = QtWidgets.QLabel()
        self.links.setAlignment(QtCore.Qt.AlignLeading)
        self.links.setOpenExternalLinks(True)
        self.linksLayout = QtWidgets.QVBoxLayout()
        self.linksLayout.addWidget(self.links)
        self.linksGroup.setLayout(self.linksLayout)

        self.statsGroup = QtWidgets.QGroupBox("Level:")
        self.statsGroup.setFixedWidth(250)

        self.stats = StatsWidget(stats=self._stats)
        self.statsLayout = QtWidgets.QVBoxLayout()
        self.statsLayout.addWidget(self.stats)
        self.statsGroup.setLayout(self.statsLayout)

        self.additional = QtWidgets.QWidget()
        self.additional.setFixedHeight(160)
        self.additional_layout = QtWidgets.QHBoxLayout()
        self.additional_layout.addWidget(self.statsGroup)
        self.additional_layout.addWidget(self.linksGroup)
        self.additional_layout.setMargin(0)
        self.additional.setLayout(self.additional_layout)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.exercise_name)
        self.layout().addWidget(self.thumbnail)
        self.layout().addWidget(self.instructionsGroup)
        self.layout().addWidget(self.additional)
        self._refresh()

    def _refresh(self):
        self.exercise_name.setText(self.exercise.get("label", "No Label"))
        self._update_thumbnail()
        self.instruction.setText(self.exercise.get("instruction", "No Instructions"))
        self.links.setText(self._format_hyperlinks())
        self.stats.refresh(self._stats)

    def _format_hyperlinks(self):
        links = self.exercise.get("hyperlinks", [""])
        formated_links = [
            "<a href='{link}' style='color: gray;'>{short_link}</a >".format(link=link, short_link=link[:30]) for link
            in links]
        return "<br>".join(formated_links)

    def _update_thumbnail(self):
        thumbnail_path = self.exercise.get("thumbnail", "")
        thumbnail = QtGui.QPixmap(thumbnail_path).scaled(640, 360, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                         QtCore.Qt.TransformationMode.SmoothTransformation)
        self.thumbnail.setPixmap(thumbnail)
        self.thumbnail.setScaledContents(True)

    def refresh(self, exercise, stats):
        self.exercise = exercise
        self._stats = stats
        self._refresh()


class StatsWidget(QtWidgets.QWidget):
    def __init__(self, stats, parent=None):
        super(StatsWidget, self).__init__(parent=parent)
        self._stats = stats
        self.level_progress = QtWidgets.QProgressBar()
        self.level = LevelWidget()

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.level)
        self.layout().addWidget(self.level_progress)

        self.refresh(stats=self._stats)

    def refresh(self, stats):
        self._stats = stats
        self.level.refresh(self._stats.get("level", 0))
        self.level_progress.setRange(0, self._stats.get("level_max_progress", 100))
        self.level_progress.setValue(self._stats.get("progress", 0.0))


class LevelWidget(QtWidgets.QWidget):
    MAX_LEVELS = 5  # TODO: This is buisness logic move into api
    ENABLED = QtGui.QImage(":/icons/enabled.png")
    DISABLED = QtGui.QImage(":/icons/disabled.png")

    def __init__(self, level=0, parent=None):
        super(LevelWidget, self).__init__(parent=parent)
        self.level = level
        self.setLayout(QtWidgets.QHBoxLayout())
        self.level_icons = []

    def populate(self):
        self._clear()
        for index, _ in enumerate(range(self.MAX_LEVELS), 1):
            image = self.ENABLED if index <= self.level else self.DISABLED
            icon = self._build_icon(pixmap=QtGui.QPixmap.fromImage(image))
            self.level_icons.append(icon)
            self.layout().addWidget(icon)

    def _build_icon(self, pixmap):
        container = QtWidgets.QLabel()
        container.setPixmap(pixmap)
        container.setFixedSize(32, 32)
        container.setScaledContents(True)
        return container

    def refresh(self, level):
        self.level = level
        self.populate()

    def _clear(self):
        for widget in self.level_icons:
            self.layout().removeWidget(widget)
            widget.clear()
        self.level_icons = []
