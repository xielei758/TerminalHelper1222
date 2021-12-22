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

## import some other components here.
from functools import partial
import subprocess

## import utilities here
## the following line caused some top-level import error

sys.path.append('..')
# from Utils.Cleaner_Tool import general_cleaner_utils

## import the ui layout of sub pages
from UI.sub_pages.ui_app_store import Ui_AppStore

## import resources files here
from UI import ui_image_assets


class AppStore_Sep(QMainWindow, Ui_AppStore):
    def __init__(self, parent = None):
        super().__init__()
        # super(AppStore_Sep, self).__init__(parent)
        self.setupUi(self)

        self.parent = parent

        self.sub_window_visual()

        self.fetch_info()

        self.app_store_init_visual()
        self.app_store_init_logic()

    def sub_window_visual(self):
        self.setWindowTitle('蓝狐 - 应用中心')

        # ## make the window top on the desktop
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        ## shadow effect
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)
        self.effect_shadow.setBlurRadius(30)
        self.effect_shadow.setColor(Qt.gray)
        # self.setGraphicsEffect(self.effect_shadow)
        # self.centralwidget.setGraphicsEffect(self.effect_shadow)
        # self.centralwidget.setStyleSheet('background-color: rgb(240, 250, 254); \n')

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

    def app_store_init_visual(self):
        # target_background = self.parent.frame_content_right.styleSheet() + '\ncolor: rgb(255, 255, 255); '
        # # print(target_background)
        # # print(type(target_background))
        # self.centralwidget.setStyleSheet(target_background)

        # print('func activated ')
        # self.centralwidget.setStyleSheet('background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(105,202,155), stop: 1 rgb(225,207,163)); \n' \
        #                         'color: rgb(255, 255, 255); ')

        self.search_bar_empty_sheet = 'QLineEdit{ \n' \
                                      'border: 3px solid rgba(255, 255, 255, 180); \n' \
                                      'border-radius: 8px; \n' \
                                      'background: transparent; \n' \
                                      'font: 12pt "Noto Mono"; \n' \
                                      'color: rgba(255, 255, 255, 110); \n' \
                                      '}'
        self.search_bar_filled_sheet = 'QLineEdit{ \n' \
                                      'border: 3px solid rgba(255, 255, 255, 180); \n' \
                                      'border-radius: 8px; \n' \
                                      'background: transparent; \n' \
                                      'font: 12pt "Noto Mono"; \n' \
                                      'color: rgba(255, 255, 255, 190); \n' \
                                      '}'
        self.search_bar_edit.textChanged.connect(self.search_bar_reset_stylesheet)
        pass

    def app_store_init_logic(self):
        pass

    def fetch_info(self):
        pass

    def closeEvent(self, event) -> None:
        ## rewrite the close event to cooperate with the system tray
        event.ignore()
        # print('AppStore hidden. ')
        self.hide()

    def search_bar_reset_stylesheet(self):
        if not self.search_bar_edit.text():
            self.search_bar_edit.setStyleSheet(self.search_bar_empty_sheet)
        else:
            self.search_bar_edit.setStyleSheet(self.search_bar_filled_sheet)
        pass
