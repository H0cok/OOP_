# This Python file uses the following encoding: utf-8
import sys
import os

import PySide2.QtCore
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile, QObject
from PySide2.QtUiTools import QUiLoader


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.load_ui()


    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()




if __name__ == "__main__":
    app = QApplication([])
    widget = Window()
    widget.show()
    sys.exit(app.exec_())

