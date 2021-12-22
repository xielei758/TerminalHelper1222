## import components from PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *


def side_button_style(self):
    # self.btn_toggle_Main.setStyleSheet("QPushButton {\n"
    #                                    "    background-position: left;\n"
    #                                    "    background-repeat: no-reperat;\n"
    #                                    "    background: transparent; \n"
    #                                    # "    background: transparent; \n"
    #                                    "    border: 0;  \n"
    #                                    "    font: 14pt \"Noto Mono\";\n"
    #                                    "    color: rgb(255, 255, 255);\n"
    #                                    "    /* padding-left: 15px; */\n"
    #                                    "    qproperty-icon: url(:/images/Side_Button/Main_Checked.png);"
    #                                    "}\n"
    #                                    "\n"
    #                                    "QPushButton:hover {\n"
    #                                    "    background-color: rgb(166, 135, 200);\n"
    #                                    "}\n"
    #                                    "\n"
    #                                    "QPushButton:pressed {    \n"
    #                                    "    background-color: rgb(118, 99, 136);\n"
    #                                    "}\n"
    #                                    "\n"
    #                                    "QPushButton:checked{\n"
    #                                    "    background-color: rgb(118, 99, 136);\n"
    #                                    "    /* background-color: rgba(255, 255, 255, 150); */\n"
    #                                    "    /* color: rgb(118, 99, 136);  */\n"
    #                                    "    border: none;\n"
    #                                    "    qproperty-icon: url(:/images/Side_Button/Main_Default.png);"
    #                                    "}")
    self.btn_toggle_Main.setIcon(QIcon(':/images/Side_Button/Main_Default.png'))
    self.btn_toggle_ProcManager.setIcon(QIcon(':/images/Side_Button/ProcManager_Default.png'))
    self.btn_toggle_CleanerTool_stack.setIcon(QIcon(':/images/Side_Button/CleanerTool_Default.png'))
    self.btn_toggle_PerfMonitor.setIcon(QIcon(':/images/Side_Button/PerfMonitor_Default.png'))
    self.btn_toggle_Utilities.setIcon(QIcon(':/images/Side_Button/Utilities_Default.png'))
    self.btn_toggle_AppStore.setIcon(QIcon(':/images/Side_Button/AppStore_Default.png'))
    pass
