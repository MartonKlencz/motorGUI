# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerWznHBU.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import PySide6
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from GUIBehavior import SliderBox
from motorDriver import MotorDriver
import json

class Ui_MainWindow(object):
    defaultNumOfSliderBoxes = 6
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(806, 613)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_Serial = QWidget()  # --------------------------------- TAB 1 --------------------------------------
        self.tab_Serial.setObjectName(u"tab")
        self.tabWidget.addTab(self.tab_Serial, "")
        self.tab_Control = QWidget()  # -------------------------------- TAB 2 ----------------------------------------
        self.tab_Control.setObjectName(u"tab_2")
        self.gridLayout_3 = QGridLayout(self.tab_Control)
        self.gridLayout_3.setObjectName(u"gridLayout_3")

        self.scrollArea = QScrollArea(self.tab_Control)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)

        self.createSliderBoxScrollArea(self.defaultNumOfSliderBoxes)
        self.numofSliderBoxes = self.defaultNumOfSliderBoxes

        self.gridLayout_3.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_Control, "")

        self.tab_Options = QWidget()  # ------------------------------------------- TAB 3 ----------------------------

        self.gridLayout_4 = QGridLayout(self.tab_Options)

        self.saveLabel = QLabel(text="Save current control scheme")
        self.gridLayout_4.addWidget(self.saveLabel, 0, 0, 1, 2)
        self.button_Save = QPushButton(self.tab_Options)
        self.button_Save.setText("Save")
        self.button_Save.clicked.connect(lambda: self.saveConfig())

        self.gridLayout_4.addWidget(self.button_Save, 1, 0, 1, 1)


        self.loadLabel = QLabel(text="Load control scheme")
        self.gridLayout_4.addWidget(self.loadLabel, 2, 0, 1, 2)
        self.button_Load = QPushButton(self.tab_Options)
        self.button_Load.setText("Load")
        self.button_Load.clicked.connect(lambda: self.loadConfig())
        self.gridLayout_4.addWidget(self.button_Load, 3, 0, 1, 1)

        self.label_sliderCountSet = QLabel(text="Set number of slider boxes")
        self.gridLayout_4.addWidget(self.label_sliderCountSet, 4, 0, 1, 2)

        self.spinBox = QSpinBox(self.tab_Options)
        self.spinBox.setValue(self.defaultNumOfSliderBoxes)
        self.spinBox.valueChanged.connect(lambda n: self.createSliderBoxScrollArea(n))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(100)
        self.gridLayout_4.addWidget(self.spinBox, 5, 0, 1, 1)

        # horizontal spacer on the right of options tab, pushes everything to the left
        self.spacer_optionsTabHorizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gridLayout_4.addItem(self.spacer_optionsTabHorizontal, 0, self.gridLayout_4.columnCount())

        # vertical spacer on bottom of options tab, pushes everything up
        self.spacer_optionsTabVertical = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayout_4.addItem(self.spacer_optionsTabVertical, self.gridLayout_4.rowCount(), 0)

        self.tabWidget.addTab(self.tab_Options, "")  # ------------------------------ /TAB3 ---------------------------

        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 806, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)

    def createSliderBoxScrollArea(self, numOfBoxes):

        print("creating")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 762, 492))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.sliderBoxParent = QWidget()
        self.sliderBoxes = [SliderBox(self.sliderBoxParent, self.motorDriver) for i in range(numOfBoxes)]
        self.numofSliderBoxes = numOfBoxes

        for i in self.sliderBoxes:
            self.verticalLayout_2.addLayout(i.getLayout())

        self.scrollSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(self.scrollSpacer)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Serial),
                                  QCoreApplication.translate("MainWindow", u"Connect", None))

        for i in self.sliderBoxes:
            i.retranslate()

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Control),
                                  QCoreApplication.translate("MainWindow", u"Control", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Options),
                                  QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

    def addMotorDriver(self, motorDriver: MotorDriver):
        self.motorDriver = motorDriver


    def saveConfig(self):

        print("Saving config...")
        with open("configFileName.txt", "w") as file:

            file.write(str(len(self.sliderBoxes)) + "\n")

            for i in self.sliderBoxes:
                file.write(i.saveToText() + "\n")

    def loadConfig(self):

        print("Loading config...")

        filename = QFileDialog.getOpenFileName(caption="Choose config file", filter="*.txt")[0]

        with open(filename, "r") as file:

            self.createSliderBoxScrollArea(int(file.readline()))
            self.spinBox.blockSignals(True)
            self.spinBox.setValue(self.numofSliderBoxes)
            self.spinBox.blockSignals(False)
            print(f"Found {self.numofSliderBoxes} slider boxes")

            for i in range(self.numofSliderBoxes):
                line = (file.readline())
                self.sliderBoxes[i].loadFromText(line)
