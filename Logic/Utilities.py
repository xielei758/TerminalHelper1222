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

## call the sub-window classes

## replacing the redundant way to write this call
# import Utilities_Greenify
from .Utilities_Greenify import Greenify_Sub_Window
from .Utilities_Network_Speed import Network_Speed_Sub_Window
from .Utilities_Network_Repair import Network_Auto_Repair_Sub_Window
from .Utilities_Service_Availability import Service_Avai_Sub_Window
from .Utilities_Settings import Gen_Settings_Sub_Window


def utilities_page_caller(self):
    utilities_page_visual(self)

    utilities_page_logic(self)
    pass


def utilities_page_visual(self):

    ## hide the network automatic repair
    self.utilities_go2btn_network_auto_repair.setVisible(False)
    ## hide the setting button
    self.utilities_go2btn_settings.setVisible(False)
    pass


def utilities_page_logic(self):
    par_on_click_utilities_go2btn_power_saver = partial(on_click_utilities_go2btn_power_saver, self)
    self.utilities_go2btn_power_saver.clicked.connect(par_on_click_utilities_go2btn_power_saver)

    par_on_click_utilities_go2btn_network_test = partial(on_click_utilities_go2btn_network_test, self)
    self.utilities_go2btn_network_test.clicked.connect(par_on_click_utilities_go2btn_network_test)

    par_on_click_utilities_go2btn_service_avai = partial(on_click_utilities_go2btn_service_avai, self)
    self.utilities_go2btn_service_avai.clicked.connect(par_on_click_utilities_go2btn_service_avai)

    par_on_click_utilities_go2btn_network_auto_repair = partial(on_click_utilities_go2btn_network_auto_repair, self)
    self.utilities_go2btn_network_auto_repair.clicked.connect(par_on_click_utilities_go2btn_network_auto_repair)

    par_on_click_utilities_go2btn_settings = partial(on_click_utilities_go2btn_settings, self)
    self.utilities_go2btn_settings.clicked.connect(par_on_click_utilities_go2btn_settings)
    pass


def on_click_utilities_go2btn_power_saver(self):
    # self.util_greenify = Utilities_Greenify.Greenify_Sub_Window()
    if not hasattr(self, 'util_greenify'):
        self.util_greenify = Greenify_Sub_Window()
    self.util_greenify.show()
    # print('logic called. ')
    pass


def on_click_utilities_go2btn_network_test(self):
    if not hasattr(self, 'util_speedtest'):
        self.util_speedtest = Network_Speed_Sub_Window(self)
    self.util_speedtest.show()
    pass


def on_click_utilities_go2btn_service_avai(self):
    # print('logic called. ')
    if not hasattr(self, 'util_serv_avai'):
        self.util_serv_avai = Service_Avai_Sub_Window(self)
    self.util_serv_avai.show()
    pass


def on_click_utilities_go2btn_network_auto_repair(self):
    if not hasattr(self, 'util_net_auto_repair'):
        self.util_net_auto_repair = Network_Auto_Repair_Sub_Window(self)
    self.util_net_auto_repair.show()
    pass


def on_click_utilities_go2btn_settings(self):
    if not hasattr(self, 'general_settings'):
        self.general_settings = Gen_Settings_Sub_Window(self)
    self.general_settings.show()
    pass
