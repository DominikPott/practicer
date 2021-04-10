import sys

from PySide6 import QtWidgets, QtCore, QtGui

import exercises


class PractiseApp(QtWidgets.QMainWindow):

    def __init__(self, exercises, parent=None):
        super(PractiseApp, self).__init__(parent)
        self.setWindowTitle("Practicer")
        self._exercises = exercises
        self.exercise = self._exercises[0]

        self.exercises_overview = QtWidgets.QListWidget()

        self.thumbnail = QtGui.QPixmap(self.exercise.get("thumbnail", "")).scaled(512, 512, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        self.thumbnailWidget = QtWidgets.QLabel()
        self.thumbnailWidget.setPixmap(self.thumbnail)

        self.summary = QtWidgets.QLineEdit(self.exercise.get("summary", "No Summary"))
        self.summary.setEnabled(False)
        self.instruction = QtWidgets.QLineEdit(self.exercise.get("instruction", "No Instruction"))
        self.instruction.setEnabled(False)

        self.previewLayout = QtWidgets.QVBoxLayout()
        self.previewLayout.addWidget(self.summary)
        self.previewLayout.addWidget(self.thumbnailWidget)
        self.previewLayout.addWidget(self.instruction)
        self.previewWidget = QtWidgets.QWidget()
        self.previewWidget.setLayout(self.previewLayout)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addWidget(self.exercises_overview)
        self.mainLayout.addWidget(self.previewWidget)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

        self.populate_exercise_list()

    def populate_exercise_list(self):
        for exercise in self._exercises:
            item = QtWidgets.QListWidgetItem(exercise.get("name", "No Name"))
            item.setData(32, exercise)
            self.exercises_overview.addItem(item)


app = QtWidgets.QApplication(sys.argv)
w = PractiseApp(exercises=exercises.exercises())
w.show()
sys.exit(app.exec_())
