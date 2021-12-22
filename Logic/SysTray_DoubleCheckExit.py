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
from UI.sub_pages.ui_tray_doublecheck_exit import Ui_DoubleCheckExit


class SysTray_DCE(QMainWindow, Ui_DoubleCheckExit):
    def __init__(self, parent = None):
        super(SysTray_DCE, self).__init__(parent)
        self.setupUi(self)

        self.parent = parent

        self.Visual()
        self.btn_visual()
        self.Logic()

    def Visual(self):
        self.setWindowTitle('蓝狐 - 退出')

        ## make the window property
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        ## the following line is working
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

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
    
    def btn_visual(self):
        self.dce_keep_on_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.dce_quit_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        pass

    def Logic(self):

        ## binding the buttons here
        self.dce_keep_on_btn.clicked.connect(self.on_click_dce_keep_on_btn)
        self.dce_quit_btn.clicked.connect(self.on_click_dce_quit_btn)
        pass

    def on_click_dce_keep_on_btn(self):
        self.hide()
        pass

    def on_click_dce_quit_btn(self):
        self.parent.on_trigger_quit()
        pass

    ## take the action of closing this specific window as to keep app running

    def closeEvent(self, event) -> None:
        ## rewrite the close event to cooperate with the system tray
        event.ignore()
        # print('AppStore hidden. ')
        self.hide()

    ## rewrite the mouse related functions here.

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
