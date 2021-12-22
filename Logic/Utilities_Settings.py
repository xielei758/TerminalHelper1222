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
from UI.sub_pages.ui_util_settings import Ui_GenSettings


## import utilities here


class Gen_Settings_Sub_Window(QMainWindow, Ui_GenSettings):
    def __init__(self, parent = None):
        super(Gen_Settings_Sub_Window, self).__init__(parent)
        self.setupUi(self)

        self.Visual()
        self.Logic()

    def Visual(self):
        self.setWindowTitle('蓝狐 - 设置')

        ## shadow effect
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)
        self.effect_shadow.setBlurRadius(30)
        self.effect_shadow.setColor(Qt.gray)
        # self.centralwidget.setGraphicsEffect(self.effect_shadow)

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
        ## binding logic for theme changing test
        self.settings_theme_changing_test.clicked.connect(self.on_click_theme_changing_test)
        pass

    def on_click_theme_changing_test(self):
        print('activated. ')
        print(self.centralwidget.styleSheet())
        self.centralwidget.setProperty('background-color',
                                       'qlineargradient(y1: 0, y2: 1, stop: 0 rgb(0,204,188), stop: 0.8 rgb(0,111,175), stop: 1 rgb(1,66,137))')
        # self.centralwidget.setStyleSheet(
        #     '{background-color: qlineargradient (y1: 0, y2: 1, stop: 0 rgb (105,202,155), stop: 1 rgb (225,207,163)); }')

        pass

    def closeEvent(self, event) -> None:
        ## rewrite the close event to cooperate with the system tray
        event.ignore()
        # print('AppStore hidden. ')
        self.hide()
