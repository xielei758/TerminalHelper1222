import sys
import platform
import time

## import components from PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *

## import some other components here.
from functools import partial
from time import time, sleep, strftime
from threading import Thread
import subprocess

sys.path.append('..')
## import the ui layout of sub pages
from UI.sub_pages.ui_tray_report_problem import Ui_ReportProblem


class SysTray_RP(QMainWindow, Ui_ReportProblem):
    def __init__(self, parent = None):
        super(SysTray_RP, self).__init__(parent)
        self.setupUi(self)

        self.parent = parent

        self.Visual()
        self.Logic()

    def Visual(self):
        self.setWindowTitle('蓝狐 - 上报问题')

        ## shadow effect
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)
        self.effect_shadow.setBlurRadius(30)
        self.effect_shadow.setColor(Qt.gray)
        self.centralwidget.setGraphicsEffect(self.effect_shadow)

        ## make the window to the center of the screen
        ## get the geometry of the screen
        screen_geo = QDesktopWidget().screenGeometry()
        ## get the geometry of the current window
        window_geo = self.geometry()
        target_left_point = int((screen_geo.width() - window_geo.width()) / 2)
        target_top_point = int((screen_geo.height() - window_geo.height()) / 2)
        ## move the window
        self.move(target_left_point, target_top_point)
        pass

    def Logic(self):
        ## restrict the input content of the line edit
        self.content_validator()

        ## binding the buttons here
        self.rp_submit_btn.clicked.connect(self.submit_report)

        pass

    def content_validator(self):
        ## the int validator can have restrictions on the length of the input number
        # self.phone_edit.setValidator(QtGui.QIntValidator())

        ## the double validator does not reject the input of letter e
        # self.phone_edit.setValidator(QtGui.QDoubleValidator())

        ## use a customized regular expression command here
        num_regx = QtCore.QRegExp("[0-9]")
        # num_regx = QtCore.QRegExp("^[a-zA-Z][0-9A-Za-z]{14}$")
        cust_validator = QtGui.QRegExpValidator(self)
        cust_validator.setRegExp(num_regx)
        self.phone_edit.setValidator(cust_validator)

        pass

    def submit_report(self):
        print('submit report function called. ')
        pass

    def closeEvent(self, event) -> None:
        ## rewrite the close event to cooperate with the system tray
        event.ignore()
        # print('AppStore hidden. ')
        self.hide()
