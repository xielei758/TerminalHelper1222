# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_util_settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GenSettings(object):
    def setupUi(self, GenSettings):
        GenSettings.setObjectName("GenSettings")
        GenSettings.resize(800, 600)
        GenSettings.setMinimumSize(QtCore.QSize(800, 600))
        GenSettings.setMaximumSize(QtCore.QSize(800, 600))
        GenSettings.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(GenSettings)
        self.centralwidget.setStyleSheet("background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(132, 110, 160), stop:1 rgb(55, 80, 110));\n"
"\n"
"color: rgb(255, 255, 255); ")
        self.centralwidget.setObjectName("centralwidget")
        self.settings_stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.settings_stackedWidget.setGeometry(QtCore.QRect(0, 0, 791, 591))
        self.settings_stackedWidget.setStyleSheet("background: transparent; ")
        self.settings_stackedWidget.setObjectName("settings_stackedWidget")
        self.page_main = QtWidgets.QWidget()
        self.page_main.setObjectName("page_main")
        self.settings_avai_header = QtWidgets.QLabel(self.page_main)
        self.settings_avai_header.setGeometry(QtCore.QRect(30, 20, 411, 41))
        font = QtGui.QFont()
        font.setFamily("Noto Mono")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.settings_avai_header.setFont(font)
        self.settings_avai_header.setStyleSheet("font: 18pt \"Noto Mono\";")
        self.settings_avai_header.setObjectName("settings_avai_header")
        self.ProcessManager_tab = QtWidgets.QTabWidget(self.page_main)
        self.ProcessManager_tab.setGeometry(QtCore.QRect(10, 60, 781, 531))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ProcessManager_tab.setFont(font)
        self.ProcessManager_tab.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.ProcessManager_tab.setAutoFillBackground(False)
        self.ProcessManager_tab.setStyleSheet("QTabWidget::pane {\n"
"    border: 2px solid rgba(102, 138, 210, 120);\n"
"    border-radius:8px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QTabWidget::tab-bar:top {\n"
"    top: 2px;\n"
"    left:8px;\n"
"}\n"
"\n"
"QTabWidget::tab-bar:bottom {\n"
"    bottom: 8px;\n"
"}\n"
"\n"
"QTabWidget::tab-bar:left {\n"
"    right: 8px;\n"
"}\n"
"\n"
"QTabWidget::tab-bar:right {\n"
"    left: 8px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    border: 2px solid rgb(81, 85, 133);\n"
"    background: rgb(255, 255, 255); \n"
"    width: 90 px;\n"
"    font-size : 18px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: rgba(255, 255, 255, 170);\n"
"    color: rgb(81, 85, 133);\n"
"    font-weight: bold; \n"
"    border-bottom-color: none;\n"
"    margin-bottom: -2px; \n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    background: rgba(157, 128, 173, 220);\n"
"    color:rgba(255, 255, 255, 165);\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover {\n"
"    background: rgba(208, 176, 255, 160);\n"
"}\n"
"\n"
"QTabBar::tab:top:!selected {\n"
"    margin-top: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:bottom:!selected {\n"
"    margin-bottom: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:top, QTabBar::tab:bottom {\n"
"    min-width: 8px;\n"
"    margin-right: -1px;\n"
"    padding: 5px 10px 5px 10px;\n"
"}\n"
"\n"
"QTabBar::tab:top:selected {\n"
"    border-bottom-color: none;\n"
"}\n"
"\n"
"QTabBar::tab:bottom:selected {\n"
"    border-top-color: none;\n"
"}\n"
"\n"
"QTabBar::tab:top:last, QTabBar::tab:bottom:last,\n"
"QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {\n"
"    margin-right: 0;\n"
"}\n"
"\n"
"QTabBar::tab:left:!selected {\n"
"    margin-right: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:right:!selected {\n"
"    margin-left: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:left, QTabBar::tab:right {\n"
"    min-height: 8ex;\n"
"    margin-bottom: -1px;\n"
"    padding: 10px 5px 10px 5px;\n"
"}\n"
"\n"
"QTabBar::tab:left:selected {\n"
"    border-left-color: none;\n"
"}\n"
"\n"
"QTabBar::tab:right:selected {\n"
"    border-right-color: none;\n"
"}\n"
"\n"
"QTabBar::tab:left:last, QTabBar::tab:right:last,\n"
"QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {\n"
"    margin-bottom: 0;\n"
"}")
        self.ProcessManager_tab.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.ProcessManager_tab.setTabBarAutoHide(False)
        self.ProcessManager_tab.setObjectName("ProcessManager_tab")
        self.process_list_tab = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.process_list_tab.setFont(font)
        self.process_list_tab.setAutoFillBackground(False)
        self.process_list_tab.setStyleSheet("background-color = rgb(255, 255, 255);")
        self.process_list_tab.setObjectName("process_list_tab")
        self.settings_avai_dev_prog = QtWidgets.QLabel(self.process_list_tab)
        self.settings_avai_dev_prog.setGeometry(QtCore.QRect(10, 50, 761, 31))
        font = QtGui.QFont()
        font.setFamily("Noto Mono")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.settings_avai_dev_prog.setFont(font)
        self.settings_avai_dev_prog.setStyleSheet("font: 12pt \"Noto Mono\";")
        self.settings_avai_dev_prog.setWordWrap(True)
        self.settings_avai_dev_prog.setObjectName("settings_avai_dev_prog")
        self.settings_theme_changing_test = QtWidgets.QPushButton(self.process_list_tab)
        self.settings_theme_changing_test.setGeometry(QtCore.QRect(10, 130, 89, 25))
        self.settings_theme_changing_test.setObjectName("settings_theme_changing_test")
        self.ProcessManager_tab.addTab(self.process_list_tab, "")
        self.network_list_tab = QtWidgets.QWidget()
        self.network_list_tab.setAutoFillBackground(False)
        self.network_list_tab.setObjectName("network_list_tab")
        self.net_table_view = QtWidgets.QTableView(self.network_list_tab)
        self.net_table_view.setGeometry(QtCore.QRect(5, 1, 841, 631))
        self.net_table_view.setObjectName("net_table_view")
        self.settings_avai_dev_prog_2 = QtWidgets.QLabel(self.network_list_tab)
        self.settings_avai_dev_prog_2.setGeometry(QtCore.QRect(10, 50, 761, 31))
        font = QtGui.QFont()
        font.setFamily("Noto Mono")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.settings_avai_dev_prog_2.setFont(font)
        self.settings_avai_dev_prog_2.setStyleSheet("font: 12pt \"Noto Mono\";")
        self.settings_avai_dev_prog_2.setWordWrap(True)
        self.settings_avai_dev_prog_2.setObjectName("settings_avai_dev_prog_2")
        self.ProcessManager_tab.addTab(self.network_list_tab, "")
        self.settings_stackedWidget.addWidget(self.page_main)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.settings_stackedWidget.addWidget(self.page_2)
        GenSettings.setCentralWidget(self.centralwidget)

        self.retranslateUi(GenSettings)
        self.ProcessManager_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(GenSettings)

    def retranslateUi(self, GenSettings):
        _translate = QtCore.QCoreApplication.translate
        GenSettings.setWindowTitle(_translate("GenSettings", "MainWindow"))
        self.settings_avai_header.setText(_translate("GenSettings", "?????? - ??????"))
        self.settings_avai_dev_prog.setText(_translate("GenSettings", "????????????"))
        self.settings_theme_changing_test.setText(_translate("GenSettings", "????????????"))
        self.ProcessManager_tab.setTabText(self.ProcessManager_tab.indexOf(self.process_list_tab), _translate("GenSettings", "?????????"))
        self.settings_avai_dev_prog_2.setText(_translate("GenSettings", "????????????"))
        self.ProcessManager_tab.setTabText(self.ProcessManager_tab.indexOf(self.network_list_tab), _translate("GenSettings", "?????????"))
