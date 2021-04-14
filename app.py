import sys

from PySide6 import QtWidgets

import api
from widgets import exercise_spreadsheet, exerciseTree, reference_widget


class PractiseApp(QtWidgets.QMainWindow):

    def __init__(self, exercises, parent=None):
        super(PractiseApp, self).__init__(parent)
        self.setWindowTitle("Practicer")
        self.setStyleSheet(self.load_stylesheet())

        self.setCentralWidget(QtWidgets.QWidget())
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.mainLayout)

        self._exercises_data = exercises
        self.exercise = self._exercises_data[0]

        self.exercises = exerciseTree.ExerciseTree(exercises=self._exercises_data)
        self.exercises.setFixedWidth(200)
        self.exercise_details = exercise_spreadsheet.ExerciseSpreadSheet(exercise=self.exercise)
        self.references = reference_widget.ReferenceWidget(references=api.references_images(exercise=self.exercise))

        self.mainLayout.addWidget(self.exercises)
        self.mainLayout.addWidget(self.exercise_details)
        self.mainLayout.addWidget(self.references)

        self.exercises.changed.connect(self.exercise_changed)
        self.exercises.double_clicked.connect(api.create)

    @staticmethod
    def load_stylesheet():
        path = r".\stylesheets\darkorange.qss"
        with open(path, "r") as s:
            stylesheet = s.read()
        return stylesheet

    def exercise_changed(self, new_exercise):
        self.exercise_details.refresh(new_exercise)
        self.references.new_images()


app = QtWidgets.QApplication(sys.argv)
w = PractiseApp(exercises=api.exercises())
w.show()
sys.exit(app.exec_())
