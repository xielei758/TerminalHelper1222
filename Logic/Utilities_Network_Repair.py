import sys
import platform
import time

import subprocess

import psutil
import threading
import re

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

sys.path.append('..')
## import the ui layout of sub pages
from UI.sub_pages.ui_util_network_auto_repair import Ui_NetworkAutoRepair
from .SysTray_Report import SysTray_RP

## import resources files here
from UI import ui_image_assets


## import necesary backend

class Network_Auto_Repair_Sub_Window(QMainWindow, Ui_NetworkAutoRepair):
    # def __init__(self, parent = None):
    #     super(Network_Speed_Sub_Window, self).__init__(parent)
    def __init__(self, parent_self):
        super().__init__()
        self.setupUi(self)

        self.parent = parent_self

        self.Visual()
        self.main_window_init()
        self.Logic()

    def Visual(self):
        ## visual effects about the general window presentation
        self.setWindowTitle('蓝狐 - 网络自动诊断')

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

    def main_window_init(self):
        ## visual effects about the contents in the window

        self.util_auto_repair_report.setStyleSheet('QPushButton \n'
                                                   '{background-color: rgb(255,83,83); \n'
                                                   'font-size:20pt; \n'
                                                   'color: rgb(255, 255, 255)}'
                                                   'QPushButton:hover \n'
                                                   '{background-color: rgb(255,121,121); } \n'
                                                   'QPushButton:pressed \n'
                                                   '{background-color: rgb(205,51,51); } ')

        pass

    def Logic(self):
        ## binding the button here.
        self.util_auto_repair_report.clicked.connect(self.on_click_util_auto_repair_report)
        pass

    def on_click_util_auto_repair_report(self):
        if not hasattr(self, 'report_sub_window'):
            self.report_sub_window = SysTray_RP(self.parent)
        self.report_sub_window.show()
        pass

    def target_latency_test(self, target_add, target_port = None):
        if target_port is not None:
            raise NotImplementedError
        else:
            raw_latency = str(subprocess.Popen('ping -c 3 %s | grep avg' % target_add, shell = True,
                                               stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        if len(raw_latency) == 0:
            self.network_latency = 'failed'
        else:
            latency = raw_latency.split('=')[1].split('/')[1]
            self.network_latency = latency

        print('network latency', self.network_latency)
        pass

    def closeEvent(self, event) -> None:
        ## rewrite the close event to cooperate with the system tray
        event.ignore()
        # print('AppStore hidden. ')
        self.hide()
