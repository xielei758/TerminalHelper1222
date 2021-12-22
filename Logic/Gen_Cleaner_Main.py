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
from .Gen_Cleaner_In_Progress import cleaner_in_progress_visual
from .Gen_Cleaner_In_Progress import cleaner_in_progress_util_caller

from .Gen_Cleaner_Sep import Gen_Cleaner_Sep

## import resources files here
sys.path.append('..')
from UI import ui_image_assets


## the entry function here.
def cleaner_page_caller(self):
    ## define the visual details
    gen_cleaner_visual(self)

    ## define the logic details
    gen_cleaner_logic(self)

    pass


def gen_cleaner_visual(self):
    ## init the visual effects

    # ## setting up the icon dirs
    # if getattr(sys, 'frozen', False):
    #     cur_path = sys._MEIPASS
    # else:
    #     cur_path = os.path.dirname(__file__)
    #
    # cleaner_icon_path = os.path.join(cur_path, 'Assets/images/Cleaner/u829.png')
    # cleaner_background_path = os.path.join(cur_path, 'Assets/images/Cleaner/u828.png')

    ## the icon placeholder
    self.cleaner_main_icon_placeholder.setFlat(True)
    self.cleaner_main_icon_placeholder.setIcon(QIcon(':/images/Cleaner/u829.png'))
    self.cleaner_main_icon_placeholder.setIconSize(QtCore.QSize(95, 95))
    self.cleaner_main_icon_placeholder.setLayoutDirection(Qt.RightToLeft)
    self.cleaner_main_icon_placeholder.setStyleSheet('QPushButton \n'
                                                     '{font-size:18pt; \n'
                                                     # 'color: rgb(255, 255, 255); \n'
                                                     'border-radius: 5px; \n'
                                                     'border-image: url(":/images/Cleaner/u828.svg"); \n}')
    self.cleaner_main_icon_placeholder.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    ## the actual trigger button
    self.cleaner_main_btn_triggerClean.setStyleSheet('QPushButton \n'
                                                     '{background-color: rgb(56, 223, 128); \n'
                                                     'font-size:22pt; \n'
                                                     'color: rgb(255, 255, 255)}'
                                                     'QPushButton:hover \n'
                                                     '{background-color: rgb(110, 223, 150); } \n'
                                                     'QPushButton:pressed \n'
                                                     '{background-color: rgb(39,156,90); } ')
    self.cleaner_main_btn_triggerClean.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    ## set the background color
    # self.sub_cleaner_page_main.setStyleSheet('background-color: rgb(236,252,243); ')

    ## set the separator
    self.cleaner_page_main_sep_enabler.setVisible(False)

    ## set default value of the combo
    self.cleaner_page_huge_file_threshold_combo.setCurrentIndex(4)
    self.cleaner_page_outd_file_threshold_combo.setCurrentIndex(2)

    # self.cleaner_page_huge_file_threshold_combo.setStyleSheet("QComboBox {\n"
    #                                                           "    border: 2px solid rgb(185, 179, 255);\n"
    #                                                           "    border-radius: 8px;\n"
    #                                                           "    padding: 1px 18px 1px 3px;\n"
    #                                                           "        color: rgb(51, 51, 51);\n"
    #                                                           "}\n"
    #                                                           "\n"
    #                                                           "QComboBox:editable {\n"
    #                                                           "    background: rgb(240, 250, 254);\n"
    #                                                           "}\n"
    #                                                           "\n"
    #                                                           "QComboBox:!editable, QComboBox::drop-down:editable {\n"
    #                                                           "        background: white;\n"
    #                                                           "}\n"
    #                                                           "\n"
    #                                                           "/* QComboBox gets the \"on\" state when the popup is open */\n"
    #                                                           "QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
    #                                                           "    background: white;\n"
    #                                                           "        color: rgb(147, 123, 171);\n"
    #                                                           "        font-weight: bold;\n"
    #                                                           "        /* color: rgb(255, 255, 255); */\n"
    #                                                           "}\n"
    #                                                           "\n"
    #                                                           "QComboBox:!enabled {\n"
    #                                                           "    background: white;\n"
    #                                                           "}\n"
    #                                                           "\n"
    #                                                           "QComboBox:on { /* shift the text when the popup opens */\n"
    #                                                           "    padding-top: 3px;\n"
    #                                                           "    padding-left: 4px;\n"
    #                                                           "}\n"
    #                                                           "\n"
    #                                                           "QComboBox::drop-down {\n"
    #                                                           "    subcontrol-origin: padding;\n"
    #                                                           "    subcontrol-position: top right;\n"
    #                                                           "    width: 16px;\n"
    #                                                           "\n"
    #                                                           "    border-left-width: 1px;\n"
    #                                                           "    border-left-color: green;\n"
    #                                                           "    border-left-style: solid; /* just a single line */\n"
    #                                                           "    border-top-right-radius: 6px; /* same radius as the QComboBox */\n"
    #                                                           "    border-bottom-right-radius: 3px;\n"
    #                                                           "}\n"
    #                                                           "\n"
    #                                                           "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
    #                                                           "    top: 1px;\n"
    #                                                           "    left: 1px;\n"
    #                                                           "}\n"
    #                                                           "QComboBox::down-arrow: {\n"
    #                                                           "    image: url(':/images/Home_Page/down-arrow.png');\n"
    #                                                           "    width: 16px;\n"
    #                                                           "    height: 16px;\n"
    #                                                           "}\n"
    #                                                           "")
    pass


def gen_cleaner_logic(self):
    ## setting the sub stack widget
    self.cleaner_page_stackedWidget.setCurrentWidget(self.sub_cleaner_page_main)

    ## binding the buttons
    cleaner_page_main_sep_enabler(self)

    ## if the checkbox changes
    par_on_click_cleaner_page_main_sep_enabler = partial(cleaner_page_main_sep_enabler, self)
    self.cleaner_page_main_sep_enabler.clicked.connect(par_on_click_cleaner_page_main_sep_enabler)

    pass


def cleaner_page_main_sep_enabler(self):
    if self.cleaner_page_main_sep_enabler.isChecked():
        on_going_link_to_separated(self)
    else:
        on_going_link_to_integrated(self)
    pass


def on_going_link_to_integrated(self):
    ## remove previous bindings here
    try:
        self.cleaner_main_btn_triggerClean.clicked.disconnect()
        self.cleaner_main_icon_placeholder.clicked.disconnect()
    except TypeError as err_msg:
        print('this is a clean call, no connections already set. ')

    par_on_going_triggered_cleaning = partial(on_going_triggered_cleaning_int, self)
    self.cleaner_main_btn_triggerClean.clicked.connect(par_on_going_triggered_cleaning)
    self.cleaner_main_icon_placeholder.clicked.connect(par_on_going_triggered_cleaning)
    pass


def on_going_link_to_separated(self):
    ## remove previous bindings here
    try:
        self.cleaner_main_btn_triggerClean.clicked.disconnect()
        self.cleaner_main_icon_placeholder.clicked.disconnect()
    except TypeError as err_msg:
        print('this is a clean call, no connections already set. ')

    par_on_going_triggered_cleaning = partial(on_going_triggered_cleaning_sep, self)
    self.cleaner_main_btn_triggerClean.clicked.connect(par_on_going_triggered_cleaning)
    self.cleaner_main_icon_placeholder.clicked.connect(par_on_going_triggered_cleaning)
    pass


def on_going_triggered_cleaning_int(self):
    ## the button contains the functions to be called when the go2clean button on main is pressed.
    cleaner_in_progress_visual(self)
    self.cleaner_page_stackedWidget.setCurrentWidget(self.sub_cleaner_in_progress)

    ## init cleaner process
    cleaner_in_progress_util_caller(self)
    pass


def on_going_triggered_cleaning_sep(self):
    print('triggering a separate window. ')
    if not hasattr(self, 'cleaner_sub_sep'):
        self.cleaner_sub_sep = Gen_Cleaner_Sep(self)

    threshold_reader(self)

    self.cleaner_sub_sep.cleaner_backend.start()
    self.cleaner_sub_sep.show()

    pass


def threshold_reader(self):
    text_huge_th = self.cleaner_page_huge_file_threshold_combo.currentText()[:-2]
    text_huge_pf = self.cleaner_page_huge_file_threshold_combo.currentText()[-2:]
    text_outd_th = self.cleaner_page_outd_file_threshold_combo.currentText()
    self.cleaner_sub_sep.threshold_rewrite(text_huge_th, text_huge_pf, text_outd_th)
