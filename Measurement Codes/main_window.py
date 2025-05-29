# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file
# Created by: PyQt5 UI code generator

from PyQt5 import QtCore, QtGui, QtWidgets
from RoundCap import thickness_roundcap

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1384, 852)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(10, 0, 1361, 781))
        self.stackedWidget.setObjectName("stackedWidget")

        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.page_home = QtWidgets.QWidget(self.page)
        self.page_home.setGeometry(QtCore.QRect(20, 20, 761, 511))
        self.page_home.setObjectName("page_home")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.page)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 40, 1231, 671))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.matchbox_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.matchbox_button.setObjectName("matchbox_button")
        self.verticalLayout.addWidget(self.matchbox_button)

        self.roundcap_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.roundcap_button.setObjectName("roundcap_button")
        self.verticalLayout.addWidget(self.roundcap_button)

        self.stackedWidget.addWidget(self.page)

        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.page_measurement = QtWidgets.QWidget(self.page_2)
        self.page_measurement.setGeometry(QtCore.QRect(0, 0, 1351, 791))
        self.page_measurement.setObjectName("page_measurement")

        self.label_selected_object = QtWidgets.QLabel(self.page_measurement)
        self.label_selected_object.setGeometry(QtCore.QRect(0, 0, 171, 21))
        self.label_selected_object.setObjectName("label_selected_object")

        self.btn_upload_side = QtWidgets.QPushButton(self.page_measurement)
        self.btn_upload_side.setGeometry(QtCore.QRect(0, 30, 191, 28))
        self.btn_upload_side.setObjectName("btn_upload_side")

        self.btn_upload_top = QtWidgets.QPushButton(self.page_measurement)
        self.btn_upload_top.setGeometry(QtCore.QRect(0, 270, 191, 28))
        self.btn_upload_top.setObjectName("btn_upload_top")

        self.result_display = QtWidgets.QLabel(self.page_measurement)
        self.result_display.setGeometry(QtCore.QRect(210, 20, 601, 721))
        self.result_display.setObjectName("result_display")

        self.btn_back = QtWidgets.QPushButton(self.page_measurement)
        self.btn_back.setGeometry(QtCore.QRect(1210, 740, 111, 31))
        self.btn_back.setObjectName("btn_back")

        self.label_side_image = QtWidgets.QLabel(self.page_measurement)
        self.label_side_image.setGeometry(QtCore.QRect(0, 80, 181, 171))
        self.label_side_image.setObjectName("label_side_image")
        self.label_side_image.setScaledContents(True)

        self.label_top_image = QtWidgets.QLabel(self.page_measurement)
        self.label_top_image.setGeometry(QtCore.QRect(10, 310, 161, 191))
        self.label_top_image.setObjectName("label_top_image")
        self.label_top_image.setScaledContents(True)

        self.btn_upload_stl = QtWidgets.QPushButton(self.page_measurement)
        self.btn_upload_stl.setGeometry(QtCore.QRect(10, 630, 83, 29))
        self.btn_upload_stl.setObjectName("btn_upload_stl")

        self.label_result_diff = QtWidgets.QLabel(self.page_measurement)
        self.label_result_diff.setGeometry(QtCore.QRect(890, 100, 451, 571))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_result_diff.setFont(font)
        self.label_result_diff.setObjectName("label_result_diff")
        self.label_result_diff.setWordWrap(True)

        self.stackedWidget.addWidget(self.page_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1384, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.matchbox_button.setText(_translate("MainWindow", "Matchbox"))
        self.roundcap_button.setText(_translate("MainWindow", "Round Cap"))
        self.label_selected_object.setText(_translate("MainWindow", "TextLabel"))
        self.btn_upload_side.setText(_translate("MainWindow", "Upload Side View"))
        self.btn_upload_top.setText(_translate("MainWindow", "Upload Top View"))
        self.result_display.setText(_translate("MainWindow", ""))
        self.btn_back.setText(_translate("MainWindow", "Back"))
        self.label_side_image.setText(_translate("MainWindow", ""))
        self.label_top_image.setText(_translate("MainWindow", ""))
        self.btn_upload_stl.setText(_translate("MainWindow", "Upload STL"))
        self.label_result_diff.setText(_translate("MainWindow", ""))
