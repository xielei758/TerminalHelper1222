import sys
import platform
import time
import os

## import components from PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

## import some other components here.
from functools import partial

## import utilities here
# from .AppStore_Func import AppStore_Sep
from .AppStore_Gen import AppStore_Gen

## import resources files here
sys.path.append('..')
from UI import ui_image_assets

def app_store_init(self):
    app_store_content_init(self)

    app_store_trigger(self)
    pass

def app_store_content_init(self):
    '''
    this function serves to start the process of fetching necessary information
    from the server, so that the layout of app store can be filled
    :param self:
    :return:
    '''
    pass

def app_store_trigger(self):
    ## call the AppStore sub page.
    if not hasattr(self, 'appstore_sep'):
        # self.appstore_sep = AppStore_Sep(self)
        self.appstore_sep = AppStore_Gen(self)
    else:
        self.appstore_sep.app_store_init_logic()
        self.appstore_sep.sub_window_element_setter()

    # target_background = self.frame_content_right.styleSheet() + '\ncolor: rgb(255, 255, 255); '
    # print(target_background)
    # self.appstore_sep.setStyleSheet(target_background)
    # self.appstore_sep.setStyleSheet(self.frame_content_right.styleSheet())

    ## out of some unknown reason, the following lines cannot correctly set the stylesheet
    # print(self.frame_content_right.styleSheet())
    # print(type(self.frame_content_right.styleSheet()))

    ## use the alternative way of dealing with this:
    # if hasattr(self, 'interactive_area_stylesheet'):
    #     print(self.interactive_area_stylesheet)
    #     self.appstore_sep.setStyleSheet(self.interactive_area_stylesheet)

    # print(self.appstore_sep.centralwidget.styleSheet())
    # self.appstore_sep.centralwidget.setStyleSheet('background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(105,202,155), stop: 1 rgb(225,207,163)); \n' \
    #                             '\n' \
    #                             'color: rgb(255, 255, 255); ')
    # print(self.appstore_sep.AppStore_stackedWidget.currentIndex())
    self.appstore_sep.show()

    pass