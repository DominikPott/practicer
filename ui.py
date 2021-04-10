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
        self.exercises = QtWidgets.QListWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.filter)
        layout.addWidget(self.exercises)
        self.setLayout(layout)

        self._populate()

        self.exercises.clicked.connect(self._changed_signal)
        self.exercises.doubleClicked.connect(self._changed_signal)

    def _populate(self):
        for exercise in self._exercises:
            item = QtWidgets.QListWidgetItem(exercise.get("name", "No Name"))
            item.setData(QtCore.Qt.UserRole, exercise)
            self.exercises.addItem(item)

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
