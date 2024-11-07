from typing import Optional

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QCoreApplication, QObject, QEvent
import PySide6
import numpy as np
from motorDriver import MotorDriver, INT16_MIN, INT16_MAX, UINT16_MIN, UINT16_MAX



class SliderRow():
    cols = 3  # three widgets in a row: a QLineEdit for the title, a QSlider, and a value display QLabel

    def __init__(self, parent, name, sliderMin=INT16_MIN, sliderMax=INT16_MAX, sliderStart=0, displayMin=-1.0,
                 displayMax=1.0):

        self.parent = parent
        self.name = QLabel(parent)
        self.name.setText(name)
        self.name.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed))

        self.slider = QSlider(parent)
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.setMinimumWidth(400)
        self.slider.setMinimum(sliderMin)
        self.slider.setMaximum(sliderMax)
        self.slider.setSliderPosition(sliderStart)
        # pass scrolling event to parent to avoid changing value by scrolling
        self.slider.wheelEvent = lambda *args, **kwargs: self.parent.wheelEvent(*args, **kwargs)

        self.slider.valueChanged.connect(self.sliderValueChanged)

        self.displayMin = displayMin
        self.displayMax = displayMax
        self.valueLabel = QLabel(parent)
        self.displaySliderValue(sliderStart)

        self.widgets = [
            self.name,
            self.slider,
            self.valueLabel
        ]
        # format: [rowSpan, colSpan]
        self.spans = [
            [1, 1],
            [1, 2],
            [1, 1]
        ]

        if len(self.spans) != len(self.widgets):
            print("Error 97")
            exit(97)

    def displaySliderValue(self, value):
        # map value from interval [sliderMin, sliderMax] to [displayMin, displayMax]
        fvalue = np.interp(value, [self.slider.minimum(), self.slider.maximum()], [self.displayMin, self.displayMax])
        self.valueLabel.setText("{:.2f}".format(fvalue))

        return fvalue

    def sliderValueChanged(self, value):
        self.displaySliderValue(value)
        self.parent.drive()

    def addToGrid(self, grid: QGridLayout, startRow: int, startCol: int):

        for i in range(self.cols):
            colOffset = 0
            for j in range(i):
                colOffset += self.spans[j][1]
            grid.addWidget(self.widgets[i], startRow, startCol + colOffset, self.spans[i][0], self.spans[i][1])

    def retranslate(self):
        self.name.setText(QCoreApplication.translate("MainWindow", self.name.text(), None))
        self.valueLabel.setText(QCoreApplication.translate("MainWindow", self.valueLabel.text(), None))


class SliderBox(QWidget):

    def __init__(self, parent: (Optional[PySide6.QtWidgets.QWidget]), motorDriver: MotorDriver):

        super().__init__(parent)

        self.motorDriver = motorDriver

        self.mainLayout = QGridLayout()
        self.mainLayout.setObjectName(str(self) + "mainLayout")

        self.checkBoxAbsRel = QCheckBox(self)
        self.checkBoxAbsRel.setObjectName(str(self) + "checkBoxAbsRel")
        self.checkBoxAbsRel.setText("Relative")
        self.mainLayout.addWidget(self.checkBoxAbsRel, 2, 4, 1, 1)

        self.buttonParse = QPushButton(self)
        self.buttonParse.setObjectName(str(self) + "buttonParse")
        self.buttonParse.setText("Parse")
        self.buttonParse.setEnabled(False)
        self.mainLayout.addWidget(self.buttonParse, 2, 3, 1, 1)

        self.titleLine = QLineEdit(self)
        self.titleLine.setObjectName(str(self) + "titleLine")
        self.titleLine.setStyleSheet("""QLineEdit { background-color: rgba(20, 20, 20, 255); color: white }""")
        self.mainLayout.addWidget(self.titleLine, 0, 0, 1, 2)

        self.movementInputTextBox = QPlainTextEdit(self)
        self.movementInputTextBox.setObjectName(str(self) + "plainTextEdit")
        self.movementInputTextBox.setMaximumHeight(self.titleLine.height() + 10)
        self.movementInputTextBox.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.movementInputTextBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.mainLayout.addWidget(self.movementInputTextBox, 2, 0, 1, 3)

        self.sliders = [
            SliderRow(self, "Position", sliderMin=INT16_MIN, sliderMax=INT16_MAX),
            SliderRow(self, "Velocity", sliderMin=UINT16_MIN, sliderMax=UINT16_MAX,
                      sliderStart=(UINT16_MIN + UINT16_MAX) / 2),
            SliderRow(self, "Power", sliderMin=UINT16_MIN, sliderMax=UINT16_MAX,
                      sliderStart=(UINT16_MIN + UINT16_MAX) / 2)
        ]

        for index, i in enumerate(self.sliders):
            i.addToGrid(self.mainLayout, 3 + index, 0)

    def drive(self):
        movementIDs, movementRatioModifiers = self.parseMovements()
        self.motorDriver.driveMotors(movementIDs, movementRatioModifiers,
                                     self.sliders[0].slider.value(),
                                     self.sliders[1].slider.value(),
                                     self.sliders[2].slider.value(),
                                     self.getOptions())

    def getOptions(self):
        options = 0
        if not self.checkBoxAbsRel.isChecked():
            options |= 2  # set bit 1 of option byte if absolute mode is selected

        return options

    # noinspection PyBroadException
    def parseMovements(self):
        try:
            text = self.movementInputTextBox.toPlainText()
            splitText = [i.strip().split(" ") for i in text.split(";") if i != '']
            movementIDs = []
            movementRatioModifiers = []
            for movement in splitText:
                movementIDs.append(int(movement[0], 16))
                movementRatioModifiers.append(float(movement[1]))

            # normalize ratios

            m = max(movementRatioModifiers)
            movementRatioModifiers = [i / m for i in movementRatioModifiers]
            print(movementRatioModifiers)
            return movementIDs, movementRatioModifiers
        except:
            print("No movements defined")
            return [], []

    def getLayout(self):
        return self.mainLayout

    def retranslate(self):
        self.checkBoxAbsRel.setText(QCoreApplication.translate("MainWindow", self.checkBoxAbsRel.text(), None))
        self.buttonParse.setText(QCoreApplication.translate("MainWindow", self.buttonParse.text(), None))
        self.titleLine.setText("")
        self.titleLine.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Title", None))

        for i in self.sliders:
            i.retranslate()

    def saveToText(self):
        text = {
            "title": self.titleLine.text(),
            "movements": self.movementInputTextBox.toPlainText(),
            "absRel": str(self.checkBoxAbsRel.isChecked())
        }

        return str(text)

    def loadFromText(self, text):
        d = eval(text)
        if not isinstance(d, dict):
            print("Error loading sliderbox")
            return
        self.titleLine.setText(d["title"])
        self.movementInputTextBox.setPlainText(d["movements"])
        self.checkBoxAbsRel.setChecked(d["absRel"] == "True")
