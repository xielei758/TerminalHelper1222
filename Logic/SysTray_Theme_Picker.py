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
from UI.sub_pages.ui_tray_theme_picker import Ui_Theme_Picker


class SysTray_Theme(QMainWindow, Ui_Theme_Picker):
    def __init__(self, parent = None):
        super(SysTray_Theme, self).__init__(parent)
        self.setupUi(self)

        self.parent = parent

        self.Visual()
        self.Logic()

    def Visual(self):
        self.setWindowTitle('蓝狐 - 风格切换')

        ## make the window property
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.FramelessWindowHint)

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

        if hasattr(self.parent, 'interactive_area_stylesheet'):
            print('activated. ')
            self.centralwidget.setStyleSheet(self.parent.interactive_area_stylesheet)
        pass

    def Logic(self):
        ## binding the buttons here
        self.tp_preview_btn.clicked.connect(self.on_click_tp_preview_btn)
        self.tp_apply_btn.clicked.connect(self.on_click_tp_apply_btn)

        ## binding the combo
        self.tp_combo.currentIndexChanged.connect(self.combo_reader)

        ## init the vars
        self.combo_reader()
        pass

    def theme_purple_meteor(self):
        self.side_area_style = 'background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(139, 128, 173), stop: 1 rgb(81, 110, 133));'

        self.sub_window_style = 'background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(132, 110, 160), stop:1 rgb(55, 80, 110)); \n' \
                                '\n' \
                                'color: rgb(255, 255, 255); '

        self.button_style = ("QPushButton {\n"
                             "    background-position: left;\n"
                             "    background-repeat: no-reperat;\n"
                             "    background: transparent; \n"
                             "    border: 0;  \n"
                             "    font: 14pt \"Noto Mono\";\n"
                             "    color: rgb(255, 255, 255);\n"
                             "    /* padding-left: 15px; */\n"
                             "}\n"
                             "\n"
                             "QPushButton:hover {\n"
                             "    background-color: rgb(166, 135, 200);\n"
                             "}\n"
                             "\n"
                             "QPushButton:pressed {    \n"
                             "    background-color: rgb(118, 99, 136);\n"
                             "}\n"
                             "\n"
                             "QPushButton:checked{\n"
                             "    background-color: rgb(118, 99, 136);\n"
                             "    /* background-color: rgba(255, 255, 255, 150); */\n"
                             "    /* color: rgb(118, 99, 136);  */\n"
                             "    border: none;\n"
                             "    font-weight: bold; \n"
                             "}")

    def theme_tangerine(self):
        # self.sub_window_style = 'background-color: qlineargradient(y1: 0, y2: 0.93, y3: 1, stop: 0 rgb(222, 195, 220), stop: 0.93 rgb(255,224,149), stop:1 rgb(105,160,76)); \n' \
        #                         '\n' \
        #                         'color: rgb(255, 255, 255); '
        self.side_area_style = 'background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(111,213,163), stop: 1 rgb(231,213,167));'

        self.sub_window_style = 'background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(105,202,155), stop: 1 rgb(225,207,163)); \n' \
                                '\n' \
                                'color: rgb(255, 255, 255); '

        self.button_style = ("QPushButton {\n"
                             "    background-position: left;\n"
                             "    background-repeat: no-reperat;\n"
                             "    background: transparent; \n"
                             "    border: 0;  \n"
                             "    font: 14pt \"Noto Mono\";\n"
                             "    color: rgb(255, 255, 255);\n"
                             "    /* padding-left: 15px; */\n"
                             "}\n"
                             "\n"
                             "QPushButton:hover {\n"
                             "    background-color: rgb(142, 192, 149);\n"
                             "}\n"
                             "\n"
                             "QPushButton:pressed {    \n"
                             "    background-color: rgb(111, 149, 115);\n"
                             "}\n"
                             "\n"
                             "QPushButton:checked{\n"
                             "    background-color: rgb(111, 149, 115);\n"
                             "    /* background-color: rgba(255, 255, 255, 150); */\n"
                             "    /* color: rgb(118, 99, 136);  */\n"
                             "    border: none;\n"
                             "    font-weight: bold; \n"
                             "}")
        pass

    def theme_pink(self):
        self.side_area_style = 'background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(234,155,159), stop: 1 rgb(187,155,188));'

        self.sub_window_style = 'background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(229,152,155), stop: 1 rgb(170,141,171)); \n' \
                                '\n' \
                                'color: rgb(255, 255, 255); '

        self.button_style = ("QPushButton {\n"
                             "    background-position: left;\n"
                             "    background-repeat: no-reperat;\n"
                             "    background: transparent; \n"
                             "    border: 0;  \n"
                             "    font: 14pt \"Noto Mono\";\n"
                             "    color: rgb(255, 255, 255);\n"
                             "    /* padding-left: 15px; */\n"
                             "}\n"
                             "\n"
                             "QPushButton:hover {\n"
                             "    background-color: rgb(216,167,179);\n"
                             "}\n"
                             "\n"
                             "QPushButton:pressed {    \n"
                             "    background-color: rgb(182,140,161);\n"
                             "}\n"
                             "\n"
                             "QPushButton:checked{\n"
                             "    background-color: rgb(182,140,161);\n"
                             "    /* background-color: rgba(255, 255, 255, 150); */\n"
                             "    /* color: rgb(118, 99, 136);  */\n"
                             "    border: none;\n"
                             "    font-weight: bold; \n"
                             "}")
        pass

    def theme_aqua_green(self):
        self.side_area_style = 'background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(0,129,204), stop: 0.8 rgb(0,121,191), stop: 1 rgb(1,77,161));'

        self.sub_window_style = 'background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(0,204,188), stop: 0.8 rgb(0,111,175), stop: 1 rgb(1,66,137)); \n' \
                                '\n' \
                                'color: rgb(255, 255, 255); '

        self.button_style = ("QPushButton {\n"
                             "    background-position: left;\n"
                             "    background-repeat: no-reperat;\n"
                             "    background: transparent; \n"
                             "    border: 0;  \n"
                             "    font: 14pt \"Noto Mono\";\n"
                             "    color: rgb(255, 255, 255);\n"
                             "    /* padding-left: 15px; */\n"
                             "}\n"
                             "\n"
                             "QPushButton:hover {\n"
                             "    background-color: rgb(36,152,180);\n"
                             "}\n"
                             "\n"
                             "QPushButton:pressed {    \n"
                             "    background-color: rgb(0,116,129);\n"
                             "}\n"
                             "\n"
                             "QPushButton:checked{\n"
                             "    background-color: rgb(0,116,129);\n"
                             "    /* background-color: rgba(255, 255, 255, 150); */\n"
                             "    /* color: rgb(118, 99, 136);  */\n"
                             "    border: none;\n"
                             "    font-weight: bold; \n"
                             "}")
        pass

    def theme_firework(self):
        self.side_area_style = 'background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(203,203,102), stop: 0.8 rgb(255,166,88), stop: 1 rgb(205,205,205));'

        self.sub_window_style = 'background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(190,190,95), stop: 0.8 rgb(255,166,88), stop: 1 rgb(198,198,198)); \n' \
                                '\n' \
                                'color: rgb(255, 255, 255); '

        self.button_style = ("QPushButton {\n"
                             "    background-position: left;\n"
                             "    background-repeat: no-reperat;\n"
                             "    background: transparent; \n"
                             "    border: 0;  \n"
                             "    font: 14pt \"Noto Mono\";\n"
                             "    color: rgb(255, 255, 255);\n"
                             "    /* padding-left: 15px; */\n"
                             "}\n"
                             "\n"
                             "QPushButton:hover {\n"
                             "    background-color: rgb(205,167,86);\n"
                             "}\n"
                             "\n"
                             "QPushButton:pressed {    \n"
                             "    background-color: rgb(182,149,76);\n"
                             "}\n"
                             "\n"
                             "QPushButton:checked{\n"
                             "    background-color: rgb(182,149,76);\n"
                             "    /* background-color: rgba(255, 255, 255, 150); */\n"
                             "    /* color: rgb(118, 99, 136);  */\n"
                             "    border: none;\n"
                             "    font-weight: bold; \n"
                             "}")
        pass

    def combo_reader(self):
        current_index = self.tp_combo.currentIndex()

        target_preset = ['theme_purple_meteor', 'theme_tangerine', 'theme_pink', 'theme_aqua_green', 'theme_firework']
        target_theme = target_preset[current_index]

        exec('self.%s()' % target_theme)

        pass

    def on_click_tp_preview_btn(self):
        self.centralwidget.setStyleSheet(self.sub_window_style)
        pass

    def on_click_tp_apply_btn(self):
        print('apply button clicked')
        ## sub_window_style is the style that will be applied to the interaction area
        self.centralwidget.setStyleSheet(self.sub_window_style)
        self.parent.frame_content_right.setStyleSheet(self.sub_window_style)
        if hasattr(self.parent, 'general_settings'):
            self.parent.general_settings.setStyleSheet(self.sub_window_style)

        ## side_area_style is the style that will be applied to the side button area of the main window
        self.parent.frame_center.setStyleSheet(self.side_area_style)

        ## create a new target
        self.parent.interactive_area_stylesheet = self.sub_window_style

        ## set the stylesheet of the buttons on the main screen
        for key, value in self.parent.__dict__.items():
            if key.startswith('btn_toggle'):
                getattr(self.parent, key).setStyleSheet(self.button_style)
        pass

    def closeEvent(self, event) -> None:
        ## rewrite the close event to cooperate with the system tray
        event.ignore()
        # print('AppStore hidden. ')
        self.hide()
