import sys

from PySide6 import QtWidgets, QtCore, QtGui

import exercises
import file_setup


class PractiseApp(QtWidgets.QMainWindow):

    def __init__(self, exercises, parent=None):
        super(PractiseApp, self).__init__(parent)
        self.setWindowTitle("Practicer")
        self._exercises = exercises
        self.exercise = self._exercises[0]

        self.exercises_overview = ExerciseTree(exercises=self._exercises)

        self.thumbnail = QtWidgets.QLabel()
        self.summary = QtWidgets.QLabel()
        self.instruction = QtWidgets.QLabel()
        self.instruction.setWordWrap(True)

        self.previewLayout = QtWidgets.QVBoxLayout()
        self.previewLayout.addWidget(self.summary)
        self.previewLayout.addWidget(self.thumbnail)
        self.previewLayout.addWidget(self.instruction)
        self.previewWidget = QtWidgets.QWidget()
        self.previewWidget.setLayout(self.previewLayout)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addWidget(self.exercises_overview)
        self.mainLayout.addWidget(self.previewWidget)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

        self.exercises_overview.changed.connect(self.exercise_changed)
        self.exercises_overview.double_clicked.connect(self.open_exercise)
        self.refresh()

    def refresh(self):
        self.summary.setText(self.exercise.get("summary", "No Summary"))
        self.instruction.setText(self.exercise.get("instruction", "No Instructions"))
        self._update_thumbnail()

    def _update_thumbnail(self):
        thumbnail_path = self.exercise.get("thumbnail", "")
        thumbnail = QtGui.QPixmap(thumbnail_path).scaled(512, 512, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                         QtCore.Qt.TransformationMode.SmoothTransformation)
        self.thumbnail.setPixmap(thumbnail)

    def exercise_changed(self, exercise):
        self.exercise = exercise
        self.refresh()

    def open_exercise(self, exercise):
        file_setup.run(data=exercise)


class ExerciseTree(QtWidgets.QWidget):

    changed = QtCore.Signal(object)
    double_clicked = QtCore.Signal(object)

    def __init__(self, exercises, parent=None):
        super(ExerciseTree, self).__init__(parent)
        self._exercises = exercises

        self.filter = QtWidgets.QLineEdit()
        self.exercises_widget = QtWidgets.QListWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.filter)
        layout.addWidget(self.exercises_widget)
        self.setLayout(layout)

        self.filter.setPlaceholderText("tag filter")

        self._populate()

        self.filter.textChanged.connect(self._populate)
        self.exercises_widget.clicked.connect(self._changed_signal)
        self.exercises_widget.doubleClicked.connect(self._double_clicked)

    def exercise_tags(self):
        tags = []
        for exercise in self._exercises:
            tags.extend(exercise.get("tags", []))
        return set(tags)

    def _filter_exercises_by_tag(self, exercises):
        filters = self.filter.text().split()
        if not filters:
            return exercises
        filtered = []
        for e in exercises:
            filtered.extend(self.filter_exercise_by_tag(e, filters))
        return filtered

    @staticmethod
    def filter_exercise_by_tag(exercise, tags):
        for filter_tag in tags:
            for tag in exercise.get("tags", []):
                if filter_tag in tag:
                    return [exercise]
        return []

    def _populate(self):
        self.exercises_widget.clear()
        filtered = self._filter_exercises_by_tag(self._exercises)
        for exercise in filtered:
            item = QtWidgets.QListWidgetItem(exercise.get("name", "No Name"))
            item.setData(QtCore.Qt.UserRole, exercise)
            self.exercises_widget.addItem(item)

    def _changed_signal(self, item):
        exercise = item.data(QtCore.Qt.UserRole)
        self.changed.emit(exercise)

    def _double_clicked(self, item):
        exercise = item.data(QtCore.Qt.UserRole)
        self.double_clicked.emit(exercise)


app = QtWidgets.QApplication(sys.argv)
w = PractiseApp(exercises=exercises.exercises())
w.show()
sys.exit(app.exec_())
