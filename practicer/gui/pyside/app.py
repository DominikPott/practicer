import sys
from practicer.gui.pyside.widgets import exercise_details, exercise_list

from PySide2 import QtWidgets, QtGui, QtCore
import practicer.gui.pyside.resources  # compiled pyside resources.qrc file which includes the pyside aliases

import practicer.api


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

        self.exercises = exercise_list.ExerciseList(exercises=self._exercises_data)
        self.exercises.setFixedWidth(200)
        self.exercise_details = exercise_details.ExerciseSpreadSheet(exercise=self.exercise,
                                                                     stats=practicer.api.stats(self.exercise))

        self.mainLayout.addWidget(self.exercises)
        self.mainLayout.addWidget(self.exercise_details)

        self.exercises.changed.connect(self.exercise_changed)
        self.exercises.double_clicked.connect(self.start_exercise)
        self.statusBar().showMessage("Starting Practiver", 3000)
        self.adjustSize()

    def exercise_changed(self, new_exercise):
        stats = practicer.api.stats(new_exercise)
        self.exercise_details.refresh(new_exercise, stats)

    def start_exercise(self, new_exercise):
        practicer.api.start(exercise=new_exercise)
        self.statusBar().showMessage("Starting {label} Exercise".format(**new_exercise), 5000)


def load_stylesheet():
    stylesheet = QtCore.QFile(":/stylesheets/darkorange.qss")
    stylesheet.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    return QtCore.QTextStream(stylesheet).readAll()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    exercises = practicer.api.exercises()
    w = PractiseApp(exercises=exercises)
    w.show()
    sys.exit(app.exec_())
