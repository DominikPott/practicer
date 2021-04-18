import sys
from gui.pyside.widgets import exercise_details, exercise_list, reference_widget

from PySide6 import QtWidgets, QtGui, QtCore
import gui.pyside.resources  # compiled pyside resources.qrc file which includes the pyside aliases

import practicer.api


class PractiseApp(QtWidgets.QMainWindow):

    def __init__(self, exercises, parent=None):
        super(PractiseApp, self).__init__(parent)
        self.setWindowTitle("Practicer")
        self.setWindowIcon(QtGui.QIcon(":/icons/practicer.png"))
        self.setStyleSheet(load_stylesheet())

        self.setMenuBar(QtWidgets.QMenuBar())
        self.file_menu = QtWidgets.QMenu("Settings")
        self.about_menu = QtWidgets.QMenu("About")
        self.help = QtGui.QAction('Help')
        self.about_menu.addAction(self.help)

        self.menuBar().addMenu(self.file_menu)
        self.menuBar().addMenu(self.about_menu)

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
        self.references = reference_widget.ReferenceWidget(
            images=practicer.api.references_images(exercise=self.exercise))

        self.mainLayout.addWidget(self.exercises)
        self.mainLayout.addWidget(self.exercise_details)
        self.mainLayout.addWidget(self.references)

        self.exercises.changed.connect(self.exercise_changed)
        self.exercises.double_clicked.connect(self.start_exercise)
        self.statusBar().showMessage("Starting Practiver", 3000)

    def exercise_changed(self, new_exercise):
        stats = practicer.api.stats(new_exercise)
        self.exercise_details.refresh(new_exercise, stats)
        images = practicer.api.references_images(new_exercise)
        self.references.new_images(images)

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
