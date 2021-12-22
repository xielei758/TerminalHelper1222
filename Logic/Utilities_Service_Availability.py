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

sys.path.append('..')
## import the ui layout of sub pages
from UI.sub_pages.ui_util_service_availability import Ui_ServiceAvailability

## import resources files here
from UI import ui_image_assets

## import necesary backend
from Utils.Usability_Checker.usability_validation import UsabilityValidation


class Service_Avai_Sub_Window(QMainWindow, Ui_ServiceAvailability):
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
        self.setWindowTitle('蓝狐 - 服务可用性测试')

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

        pass

    def Logic(self):
        self.backend = UsabilityValidation()
        pass

    def closeEvent(self, event) -> None:
        ## rewrite the close event to cooperate with the system tray
        event.ignore()
        # print('AppStore hidden. ')
        self.hide()
