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

        self.exercises_overview = QtWidgets.QListWidget()

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

        self.populate_exercise_list()

        self.exercises_overview.clicked.connect(self.exercise_changed)
        self.exercises_overview.doubleClicked.connect(self.open_exercise)
        self.refresh()

    def refresh(self):
        self.summary.setText(self.exercise.get("summary", "No Summary"))
        self.instruction.setText(self.exercise.get("instruction", "No Instructions"))
        self._updateThumbnail()

    def _updateThumbnail(self):
        thumbnail_path = self.exercise.get("thumbnail", "")
        thumbnail = QtGui.QPixmap(thumbnail_path).scaled(512, 512, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                         QtCore.Qt.TransformationMode.SmoothTransformation)
        self.thumbnail.setPixmap(thumbnail)

    def populate_exercise_list(self):
        for exercise in self._exercises:
            item = QtWidgets.QListWidgetItem(exercise.get("name", "No Name"))
            item.setData(QtCore.Qt.UserRole, exercise)
            self.exercises_overview.addItem(item)

    def exercise_changed(self):
        item = self.exercises_overview.currentItem()
        self.exercise = item.data(QtCore.Qt.UserRole)
        self.refresh()


    def open_exercise(self):
        data = self.exercises_overview.currentItem().data(QtCore.Qt.UserRole)
        print("New Exercise {0}".format(data))
        file_setup.run(data=data)


app = QtWidgets.QApplication(sys.argv)
w = PractiseApp(exercises=exercises.exercises())
w.show()
sys.exit(app.exec_())
