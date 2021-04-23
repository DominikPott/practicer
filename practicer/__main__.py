import sys

from PySide6 import QtWidgets

import practicer.api
from practicer.gui.pyside.app import PractiseApp

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    exercises = practicer.api.exercises()
    w = PractiseApp(exercises=exercises)
    w.show()
    sys.exit(app.exec_())
