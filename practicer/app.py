import practicer.api
import practicer.gui.pyside.app


if __name__ == '__main__':
    exercises = practicer.api.exercises()
    practicer.gui.pyside.app.run(exercises=exercises)
