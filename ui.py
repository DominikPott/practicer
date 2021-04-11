import sys

from PySide6 import QtWidgets, QtCore, QtGui

import exercises
import file_setup


class PractiseApp(QtWidgets.QMainWindow):

    def __init__(self, exercises, parent=None):
        super(PractiseApp, self).__init__(parent)
        self.setWindowTitle("Practicer")
        self.setStyleSheet(load_stylesheed())
        self._exercises = exercises
        self.exercise = self._exercises[0]

        self.exercises_overview = ExerciseTree(exercises=self._exercises)
        self.exercises_overview.setFixedWidth(200)

        self.thumbnail = QtWidgets.QLabel()
        self.thumbnail.setFixedSize(640, 400)
        self.summary = QtWidgets.QLabel()
        self.summary.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.summary.setAlignment(QtCore.Qt.AlignCenter)
        self.summary.setFixedHeight(50)
        self.instruction = QtWidgets.QLabel()
        self.instruction.setMinimumHeight(100)
        self.instruction.setAlignment(QtCore.Qt.AlignCenter)
        self.instruction.setFont(QtGui.QFont("Times", 10))
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
        thumbnail = QtGui.QPixmap(thumbnail_path).scaled(640, 400, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
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
        self.exercises_widget = QtWidgets.QTreeWidget()
        self.exercises_widget.setHeaderHidden(True)

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

        sections = {}
        for exercise in filtered:
            categorie = exercise.get('categories', ["uncategoriezed"])[0]
            sections.setdefault(categorie, []).append(exercise)

        for section, exercises in sections.items():
            section_item = QtWidgets.QTreeWidgetItem(self.exercises_widget, [section])
            for exercise in exercises:
                name = exercise.get("name", "no name")
                item = QtWidgets.QTreeWidgetItem(section_item, [name])
                item.setData(0, QtCore.Qt.UserRole, exercise)
        self.exercises_widget.expandAll()
        self.exercises_widget.setItemsExpandable(False)
        self.exercises_widget.setRootIsDecorated(False)

    def _changed_signal(self, index):
        item = self.exercises_widget.itemFromIndex(index)
        exercise = item.data(0, QtCore.Qt.UserRole)
        if exercise:
            self.changed.emit(exercise)

    def _double_clicked(self, index):
        item = self.exercises_widget.itemFromIndex(index)
        exercise = item.data(0, QtCore.Qt.UserRole)
        if exercise:
            self.double_clicked.emit(exercise)


def load_stylesheed():
    path = r".\stylesheets\darkorange.qss"
    with open(path, "r") as s:
        stylesheet = s.read()
    return stylesheet


app = QtWidgets.QApplication(sys.argv)
w = PractiseApp(exercises=exercises.exercises())
w.show()
sys.exit(app.exec_())
