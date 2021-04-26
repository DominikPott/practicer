from PySide2 import QtWidgets, QtCore, QtGui


class ExerciseList(QtWidgets.QWidget):
    changed = QtCore.Signal(object)
    double_clicked = QtCore.Signal(object)

    def __init__(self, exercises, parent=None):
        super(ExerciseList, self).__init__(parent)
        self._exercises = exercises

        self.filter = QtWidgets.QLineEdit()
        self.filter.setPlaceholderText("tag filter")

        self.exercise_model = ExerciseModel(exercises=self._exercises)
        self.filter_proxy = QtCore.QSortFilterProxyModel()
        self.filter_proxy.setSourceModel(self.exercise_model)

        self.exercise_view = QtWidgets.QTreeView()
        self.exercise_view.setModel(self.filter_proxy)
        self.exercise_view.setHeaderHidden(True)
        self.exercise_view.setItemsExpandable(False)
        self.exercise_view.setRootIsDecorated(False)
        self.exercise_view.expandAll()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.filter)
        layout.addWidget(self.exercise_view)
        self.setLayout(layout)

        # self.filter.textChanged.connect(self._populate)
        self.exercise_view.clicked.connect(self._changed_signal)
        self.exercise_view.doubleClicked.connect(self._double_clicked)

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

    def _changed_signal(self, item):
        exercise = item.data(QtCore.Qt.UserRole)
        if exercise:
            self.changed.emit(exercise)

    def _double_clicked(self, item):
        exercise = item.data(QtCore.Qt.UserRole)
        if exercise:
            self.double_clicked.emit(exercise)


class ExerciseModel(QtGui.QStandardItemModel):
    def __init__(self, exercises):
        super(ExerciseModel, self).__init__()

        root = self.invisibleRootItem()

        sections = {}
        for exercise in exercises:
            categorie = exercise.get('categories', ["uncategoriezed"])[0].title()
            sections.setdefault(categorie, []).append(exercise)

        for section, exercises in sorted(sections.items()):
            section_item = ExerciseItem(section, bold=True)
            section_item.setSelectable(False)
            for exercise in exercises:
                name = exercise.get("label", "No Label").title()
                item = ExerciseItem(name)
                item.setData(exercise, QtCore.Qt.UserRole)
                item.setToolTip(" | ".join(exercise.get("tags", [])))
                section_item.appendRow(item)

            root.appendRow(section_item)


class ExerciseItem(QtGui.QStandardItem):
    def __init__(self, text="", bold=False):
        super(ExerciseItem, self).__init__()
        font = QtGui.QFont("Arial")
        font.setBold(bold)
        self.setText(text)
        self.setEditable(False)
        self.setFont(font)


class TagFilterProxyModel(QtCore.QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row, source_parent):
        pass
