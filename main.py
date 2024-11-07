
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from ui_mainwindow import Ui_MainWindow
from motorDriver import MotorDriver

class MainWindow(QMainWindow):
    def __init__(self, motorDriver):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.addMotorDriver(motorDriver)
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    motorDriver = MotorDriver()

    window = MainWindow(motorDriver)
    window.show()



    sys.exit(app.exec())