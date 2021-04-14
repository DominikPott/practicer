import sys

from PySide6 import QtWidgets, QtCore, QtGui

import api


class PractiseApp(QtWidgets.QMainWindow):

    def __init__(self, exercises, parent=None):
        super(PractiseApp, self).__init__(parent)
        self.setWindowTitle("Practicer")
        self.setStyleSheet(load_stylesheed())

        self.setCentralWidget(QtWidgets.QWidget())
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.mainLayout)

        self._exercises = exercises
        self.exercise = self._exercises[0]

        self.exercises_overview = ExerciseTree(exercises=self._exercises)
        self.exercises_overview.setFixedWidth(200)
        self.exercise_details = ExerciseDetails(exercise=self.exercise)
        self.referenceWidget = ReferenceWidget(references=api.references_images(exercise=self.exercise))

        self.mainLayout.addWidget(self.exercises_overview)
        self.mainLayout.addWidget(self.exercise_details)
        self.mainLayout.addWidget(self.referenceWidget)

        self.exercises_overview.changed.connect(self.exercise_details.refresh)
        self.exercises_overview.double_clicked.connect(api.create)



class ExerciseTree(QtWidgets.QWidget):

    changed = QtCore.Signal(object)
    double_clicked = QtCore.Signal(object)

    def __init__(self, exercises, parent=None):
        super(ExerciseTree, self).__init__(parent)
        self._exercises = exercises

        self.filter = QtWidgets.QLineEdit()
        self.filter.setPlaceholderText("tag filter")
        self.exercises_widget = QtWidgets.QTreeWidget()
        self.exercises_widget.setHeaderHidden(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.filter)
        layout.addWidget(self.exercises_widget)
        self.setLayout(layout)

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
            categorie = exercise.get('categories', ["uncategoriezed"])[0].title()
            sections.setdefault(categorie, []).append(exercise)

        for section, exercises in sections.items():
            section_item = QtWidgets.QTreeWidgetItem(self.exercises_widget, [section])
            for exercise in exercises:
                name = exercise.get("label", "No Label").title()
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


class ExerciseDetails(QtWidgets.QWidget):

    def __init__(self, exercise, parent=None):
        super(ExerciseDetails, self).__init__(parent)

        self.exercise = exercise
        self.thumbnail = QtWidgets.QLabel()
        self.thumbnail.setMinimumSize(640, 360)

        self.summary = QtWidgets.QLabel()
        self.summary.setAlignment(QtCore.Qt.AlignCenter)
        self.summary.setFixedHeight(50)
        font = QtGui.QFont("Times", 12, QtGui.QFont.DemiBold)
        font.setCapitalization(QtGui.QFont.Capitalize)
        self.summary.setFont(font)

        self.instructionsGroup = QtWidgets.QGroupBox("Instructions:")
        self.instruction = QtWidgets.QLabel()
        self.instruction.setMinimumHeight(100)
        self.instruction.setAlignment(QtCore.Qt.AlignCenter)
        self.instruction.setFont(QtGui.QFont("Times", 10))
        self.instruction.setWordWrap(True)
        self.instructionsLayout = QtWidgets.QVBoxLayout()
        self.instructionsLayout.addWidget(self.instruction)
        self.instructionsGroup.setLayout(self.instructionsLayout)

        self.linksGroup = QtWidgets.QGroupBox("Links:")
        self.links = QtWidgets.QLabel()
        self.links.setAlignment(QtCore.Qt.AlignCenter)
        self.links.setOpenExternalLinks(True)
        self.links.setMaximumHeight(80)
        self.linksLayout = QtWidgets.QVBoxLayout()
        self.linksLayout.addWidget(self.links)
        self.linksGroup.setLayout(self.linksLayout)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.summary)
        self.layout().addWidget(self.thumbnail)
        self.layout().addWidget(self.instructionsGroup)
        self.layout().addWidget(self.linksGroup)
        self._refresh()

    def _refresh(self):
        self.summary.setText(self.exercise.get("label", "No Label"))
        self.instruction.setText(self.exercise.get("instruction", "No Instructions"))
        self.links.setText(self._format_hyperlinks())
        self._update_thumbnail()

    def _format_hyperlinks(self):
        links = self.exercise.get("hyperlinks", [""])
        formated_links = ["<a href='{link}' style='color: gray;'>{short_link}</a >".format(link=link, short_link=link[:30]) for link in links]
        return " | ".join(formated_links)

    def _update_thumbnail(self):
        thumbnail_path = self.exercise.get("thumbnail", "")
        thumbnail = QtGui.QPixmap(thumbnail_path).scaled(640, 360, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                         QtCore.Qt.TransformationMode.SmoothTransformation)
        self.thumbnail.setPixmap(thumbnail)
        self.thumbnail.setScaledContents(True)

    def refresh(self, exercise):
        self.exercise = exercise
        self._refresh()


class ReferenceWidget(QtWidgets.QWidget):
    def __init__(self, references=[], parent=None):
        super(ReferenceWidget, self).__init__(parent=parent)
        self.references = references
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setMaximumWidth(320)
        self.setMaximumHeight(180*4)
        self.refresh_button = QtWidgets.QPushButton("Random")
        self.layout().addWidget(self.refresh_button)
        self.thumbnails = []
        self.randomize_images()
        self.populate_thumbnails()
        self.refresh_button.clicked.connect(self.new_images)

    def randomize_images(self):
        import random
        random.shuffle(self.references)

    def populate_thumbnails(self):
        self._clear()
        for reference in self.references[:3]:
            image_container = QtWidgets.QLabel()
            image = QtGui.QImage(reference)
            thumbnail = QtGui.QPixmap.fromImage(image).scaled(320, 180, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                              QtCore.Qt.TransformationMode.SmoothTransformation)
            image_container.setPixmap(thumbnail)
            image_container.setScaledContents(True)
            image_container.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.layout().addWidget(image_container)
            self.thumbnails.append(image_container)

    def _clear(self):
        for widget in self.thumbnails:
            self.layout().removeWidget(widget)
            widget.destroy()
        self.thumbnails = []

    def new_images(self):
        self.randomize_images()
        self.populate_thumbnails()


def load_stylesheed():
    path = r".\stylesheets\darkorange.qss"
    with open(path, "r") as s:
        stylesheet = s.read()
    return stylesheet


app = QtWidgets.QApplication(sys.argv)
w = PractiseApp(exercises=api.exercises())
w.show()
sys.exit(app.exec_())
