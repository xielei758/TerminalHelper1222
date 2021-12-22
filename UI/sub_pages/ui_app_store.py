# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app_store.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AppStore(object):
    def setupUi(self, AppStore):
        AppStore.setObjectName("AppStore")
        AppStore.resize(875, 715)
        AppStore.setMinimumSize(QtCore.QSize(875, 715))
        AppStore.setMaximumSize(QtCore.QSize(875, 715))
        self.centralwidget = QtWidgets.QWidget(AppStore)
        self.centralwidget.setStyleSheet("background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(132, 110, 160), stop:1 rgb(55, 80, 110));\n"
"\n"
"color: rgb(255, 255, 255); ")
        self.centralwidget.setObjectName("centralwidget")
        self.AppStore_stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.AppStore_stackedWidget.setGeometry(QtCore.QRect(0, 0, 871, 711))
        self.AppStore_stackedWidget.setStyleSheet("background: transparent; ")
        self.AppStore_stackedWidget.setObjectName("AppStore_stackedWidget")
        self.welcome_page = QtWidgets.QWidget()
        self.welcome_page.setObjectName("welcome_page")
        self.label = QtWidgets.QLabel(self.welcome_page)
        self.label.setGeometry(QtCore.QRect(30, 260, 581, 51))
        self.label.setStyleSheet("font: 16pt \"Noto Mono\";\n"
"color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.appstore_header = QtWidgets.QLabel(self.welcome_page)
        self.appstore_header.setGeometry(QtCore.QRect(30, 20, 411, 41))
        font = QtGui.QFont()
        font.setFamily("Noto Mono")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.appstore_header.setFont(font)
        self.appstore_header.setStyleSheet("font: 18pt \"Noto Mono\";")
        self.appstore_header.setObjectName("appstore_header")
        self.appstore_subheader = QtWidgets.QLabel(self.welcome_page)
        self.appstore_subheader.setGeometry(QtCore.QRect(30, 80, 731, 31))
        font = QtGui.QFont()
        font.setFamily("Noto Mono")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.appstore_subheader.setFont(font)
        self.appstore_subheader.setStyleSheet("font: 12pt \"Noto Mono\";")
        self.appstore_subheader.setWordWrap(True)
        self.appstore_subheader.setObjectName("appstore_subheader")
        self.AppStore_stackedWidget.addWidget(self.welcome_page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.AppStore_stackedWidget.addWidget(self.page_2)
        AppStore.setCentralWidget(self.centralwidget)

        self.retranslateUi(AppStore)
        QtCore.QMetaObject.connectSlotsByName(AppStore)

    def retranslateUi(self, AppStore):
        _translate = QtCore.QCoreApplication.translate
        AppStore.setWindowTitle(_translate("AppStore", "MainWindow"))
        self.label.setText(_translate("AppStore", "应用中心页面。（独立子窗口）"))
        self.appstore_header.setText(_translate("AppStore", "应用中心"))
        self.appstore_subheader.setText(_translate("AppStore", "你所钟爱的应用程序，汇集此地。"))
