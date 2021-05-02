from PySide2 import QtWidgets, QtCore


class ExerciseList(QtWidgets.QWidget):
    changed = QtCore.Signal(object)
    double_clicked = QtCore.Signal(object)

    def __init__(self, exercises, parent=None):
        super(ExerciseList, self).__init__(parent)
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
        self.exercises_widget.currentItemChanged.connect(self._changed_signal)
        self.exercises_widget.itemDoubleClicked.connect(self._double_clicked)

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

        for section, exercises in sorted(sections.items()):
            section_item = QtWidgets.QTreeWidgetItem(self.exercises_widget, [section])
            for exercise in exercises:
                name = exercise.get("label", "No Label").title()
                item = QtWidgets.QTreeWidgetItem(section_item, [name])
                item.setData(0, QtCore.Qt.UserRole, exercise)
                item.setToolTip(0, " | ".join(exercise.get("tags", [])))
        self.exercises_widget.expandAll()
        self.exercises_widget.setItemsExpandable(False)
        self.exercises_widget.setRootIsDecorated(False)

    def _changed_signal(self, item):
        exercise = item.data(0, QtCore.Qt.UserRole)
        if exercise:
            self.changed.emit(exercise)

    def _double_clicked(self, item):
        exercise = item.data(0, QtCore.Qt.UserRole)
        if exercise:
            self.double_clicked.emit(exercise)
