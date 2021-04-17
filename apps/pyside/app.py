import sys
from apps.pyside.widgets import exercise_details, exercise_tree, reference_widget

from PySide6 import QtWidgets, QtGui, QtCore
import apps.pyside.resources  # compiled pyside resources.qrc file which includes the pyside aliases

import api


class PractiseApp(QtWidgets.QMainWindow):

    def __init__(self, exercises, parent=None):
        super(PractiseApp, self).__init__(parent)
        self.setWindowTitle("Practicer")
        self.setWindowIcon(QtGui.QIcon(":/icons/practicer.png"))
        self.setStyleSheet(load_stylesheet())

        self.setCentralWidget(QtWidgets.QWidget())
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.mainLayout)
        self.setStatusBar = QtWidgets.QStatusBar()

        self._exercises_data = exercises
        self.exercise = self._exercises_data[0]

        self.exercises = exercise_tree.ExerciseTree(exercises=self._exercises_data)
        self.exercises.setFixedWidth(200)
        self.exercise_details = exercise_details.ExerciseSpreadSheet(exercise=self.exercise,
                                                                     stats=api.stats(self.exercise))
        self.references = reference_widget.ReferenceWidget(references=api.references_images(exercise=self.exercise))

        self.mainLayout.addWidget(self.exercises)
        self.mainLayout.addWidget(self.exercise_details)
        self.mainLayout.addWidget(self.references)

        self.exercises.changed.connect(self.exercise_changed)
        self.exercises.double_clicked.connect(self.start_exercise)
        self.statusBar().showMessage("Starting Practiver", 3000)

    def exercise_changed(self, new_exercise):
        stats = api.stats(new_exercise)
        self.exercise_details.refresh(new_exercise, stats)
        images = api.references_images(new_exercise)
        self.references.new_images(images)

    def start_exercise(self, new_exercise):
        api.start(exercise=new_exercise)
        self.statusBar().showMessage("Starting {label} Exercise".format(**new_exercise), 5000)


def load_stylesheet():
    stylesheet = QtCore.QFile(":/stylesheets/darkorange.qss")
    stylesheet.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    return QtCore.QTextStream(stylesheet).readAll()


app = QtWidgets.QApplication(sys.argv)
w = PractiseApp(exercises=api.exercises())
w.show()
sys.exit(app.exec_())
