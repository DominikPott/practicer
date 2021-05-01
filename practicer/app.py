import practicer.api
import practicer.gui.pyside.app
import practicer.gui.web.app

ui_factory = {'desktop': practicer.gui.pyside.app.run, "web": practicer.gui.web.app.run}

if __name__ == '__main__':
    exercises = practicer.api.exercises()

    ui = ui_factory['desktop']
    ui(exercises=exercises)
