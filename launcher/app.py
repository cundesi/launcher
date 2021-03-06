"""Application entry-point"""

# Standard library
import os
import sys

# Dependencies
from avalon import io
from PyQt5 import QtCore, QtGui, QtQml

# Local libraries
from . import control, terminal, lib

QML_IMPORT_DIR = lib.resource("qml")
APP_PATH = lib.resource("qml", "main.qml")
ICON_PATH = lib.resource("icon", "main.png")


class Application(QtGui.QGuiApplication):

    def __init__(self, root, source):
        super(Application, self).__init__(sys.argv)
        self.setWindowIcon(QtGui.QIcon(ICON_PATH))

        engine = QtQml.QQmlApplicationEngine()
        engine.objectCreated.connect(self.on_object_created)
        engine.warnings.connect(self.on_warnings)
        engine.addImportPath(QML_IMPORT_DIR)

        try:
            io.install()
        except IOError:
            raise  # Server refused to connect

        terminal.init()

        controller = control.Controller(root, self)
        engine.rootContext().setContextProperty("controller", controller)
        engine.rootContext().setContextProperty("terminal", terminal.model)

        self.engine = engine
        self.controller = controller

        engine.load(QtCore.QUrl.fromLocalFile(source))

    def on_object_created(self, object, url):
        if object is None:
            print("Could not load QML file..")
            sys.exit(1)

        else:
            self.controller.init()
            print("Success")

    def on_warnings(self, warnings):
        for warning in warnings:
            print(warning.toString())


def main(root, demo=False):
    """Start the Qt-runtime and show the window"""

    root = os.path.realpath(root)

    print("Starting avalon-launcher")
    app = Application(root, APP_PATH)
    return app.exec_()
