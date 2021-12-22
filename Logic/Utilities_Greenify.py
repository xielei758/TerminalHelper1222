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
from UI.sub_pages.ui_util_greenify import Ui_Greenify

## import utilities here
from Utils.Greenify import greenify


class Greenify_Sub_Window(QMainWindow, Ui_Greenify):
    def __init__(self, parent = None):
        super(Greenify_Sub_Window, self).__init__(parent)
        self.setupUi(self)

        self.Visual()
        self.Logic()

    def Visual(self):
        self.setWindowTitle('蓝狐 - 节电优能')

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
        ## shift the default page according to the current desktop environment here\
        self.backend = greenify.Greenify()

        ## get the detection result of desktop environment
        # self.backend.start()
        self.backend.desktop_environment_checker()
        self.current_de = self.backend.de_var

        if self.current_de == 'kylin':
            self.util_greenify_stackpages.setCurrentWidget(self.util_greenify_stack_ukui)
            self.ukui_init()
        elif self.current_de == 'gnome':
            self.util_greenify_stackpages.setCurrentWidget(self.util_greenify_stack_gnome)
            self.gnome_init()
        elif self.current_de == 'mate':
            self.util_greenify_stackpages.setCurrentWidget(self.util_greenify_stack_mate)
            self.mate_init()
        elif self.current_de == 'uos':
            self.util_greenify_stackpages.setCurrentWidget(self.util_greenify_stack_uos)
            self.uos_init()
        else:
            # self.util_greenify_stackpages.setCurrentWidget(self.util_greenify_stack_gnome)
            # self.gnome_init()
            self.util_greenify_stackpages.setCurrentWidget(self.util_greenify_stack_others)
            self.others_init()
        pass

    def gnome_init(self):
        self.gnome_visual()
        self.gnome_logic()
        pass

    def gnome_visual(self):
        ## set the visibility of the switch button here
        self.util_greenify_stack_gnome_prompt_go2_ukui_temp.setVisible(False)
        # self.util_greenify_stack_gnome_prompt_go2_ukui_temp.setVisible(True)
        self.util_greenify_stack_gnome_prompt_go2_mate_temp.setVisible(False)
        # self.util_greenify_stack_gnome_prompt_go2_mate_temp.setVisible(True)

        pass

    def gnome_logic(self):
        ## getting current setting value
        self.backend.gnome_get_current_lock_setting()
        # print(self.backend.blank_screen_delay)
        # print(self.backend.auto_lock_status)  ## true
        # print(self.backend.auto_lock_delay)
        # print(self.backend.auto_suspend_status)  ## suspend
        # print(self.backend.auto_suspend_delay)

        self.gnome_autoblank_delay_current = int(int(self.backend.blank_screen_delay) / 60)
        self.gnome_autolock_status_current = self.backend.auto_lock_status
        self.gnome_autolock_delay_current = float(int(self.backend.auto_lock_delay) / 60)
        self.gnome_auto_suspend_status_current = self.backend.auto_suspend_status
        self.gnome_auto_suspend_delay_current = int(int(self.backend.auto_suspend_delay) / 60)
        self.gnome_autolock_on_suspend_status = self.backend.lock_on_suspend

        self.gnome_combo_reader()

        ## binding the temp go-to-button
        self.util_greenify_stack_gnome_prompt_go2_ukui_temp.clicked.connect(
            self.on_click_util_greenify_stack_gnome_prompt_go2_ukui_temp)

        self.util_greenify_stack_gnome_prompt_go2_mate_temp.clicked.connect(
            self.on_click_util_greenify_stack_gnome_prompt_go2_mate_temp)
        pass

    def on_click_util_greenify_stack_gnome_prompt_go2_ukui_temp(self):
        self.util_greenify_stackpages.setCurrentWidget(self.util_greenify_stack_ukui)
        pass

    def on_click_util_greenify_stack_gnome_prompt_go2_mate_temp(self):
        self.util_greenify_stackpages.setCurrentWidget(self.util_greenify_stack_mate)
        pass

    def gnome_combo_reader(self):
        ## update gnome_autoblank_combobox_setting
        autoblank_preset_list = [1, 2, 3, 4, 5, 8, 10, 12, 15, 0]
        gnome_autoblank_combobox_index = autoblank_preset_list.index(self.gnome_autoblank_delay_current)
        self.gnome_autoblank_combobox_setting.setCurrentIndex(gnome_autoblank_combobox_index)

        ## update gnome_autolock_status
        autolock_status_preset_list = ['true', 'false']
        gnome_autolock_status_index = autolock_status_preset_list.index(self.gnome_autolock_status_current)
        self.gnome_lock_afterblank_combo_enable.setCurrentIndex(gnome_autolock_status_index)

        ## update gnome_autolock_delay
        autolock_delay_preset_list = [0, 0.5, 1, 2, 3, 5, 30, 60]
        gnome_autolock_delay_index = autolock_delay_preset_list.index(self.gnome_autolock_delay_current)
        # print(self.gnome_autolock_delay_current)
        # print(gnome_autolock_delay_index)
        self.gnome_lock_afterblank_combo_setting.setCurrentIndex(gnome_autolock_delay_index)

        ## update gnome_auto_suspend_status
        auto_suspend_status_preset_list = ["'suspend'", "'nothing'"]
        gnome_auto_suspend_status_index = auto_suspend_status_preset_list.index(self.gnome_auto_suspend_status_current)
        self.gnome_auto_suspend_combo_enable.setCurrentIndex(gnome_auto_suspend_status_index)

        ## update gnome_auto_suspend_delay
        auto_suspend_delay_preset_list = [15, 20, 25, 30, 45, 60, 80, 90, 100, 120]
        try:
            gnome_auto_suspend_delay_index = auto_suspend_delay_preset_list.index(self.gnome_auto_suspend_delay_current)
        except ValueError:
            gnome_auto_suspend_delay_index = 0
        # print(self.gnome_auto_suspend_delay_current)
        # print(gnome_auto_suspend_delay_index)
        self.gnome_auto_suspend_combo_setting.setCurrentIndex(gnome_auto_suspend_delay_index)

        ## update gnome_autolock_on_suspend
        autolock_on_suspend_status_preset_list = ['true', 'false']
        gnome_autolock_on_suspend_status_index = autolock_on_suspend_status_preset_list.index(
            self.gnome_autolock_on_suspend_status)
        self.gnome_autolock_on_suspend_combo_enable.setCurrentIndex(gnome_autolock_on_suspend_status_index)

        ## if the autolock or auto suspend is disabled already, such value combo box should also be disabled.
        self.gnome_combo_mask_on_first_run()

        self.gnome_autoblank_combobox_setting.currentIndexChanged.connect(self.gnome_combo_applier)
        self.gnome_lock_afterblank_combo_enable.currentIndexChanged.connect(self.gnome_combo_applier)
        self.gnome_lock_afterblank_combo_setting.currentIndexChanged.connect(self.gnome_combo_applier)
        self.gnome_auto_suspend_combo_enable.currentIndexChanged.connect(self.gnome_combo_applier)
        self.gnome_auto_suspend_combo_setting.currentIndexChanged.connect(self.gnome_combo_applier)
        self.gnome_autolock_on_suspend_combo_enable.currentIndexChanged.connect(self.gnome_combo_applier)

        pass

    def gnome_combo_mask_on_first_run(self):
        ## should the setting already been disabled, the combo box should be disabled either
        if self.gnome_lock_afterblank_combo_enable.currentIndex() == 0:
            self.gnome_lock_afterblank_combo_setting.setEnabled(True)
            self.gnome_lock_afterblank_tip.setText('在显示器关闭后，自动锁定电脑当前登入的账户。您当前打开的文档不会因此丢失。')
        else:
            self.gnome_lock_afterblank_combo_setting.setEnabled(False)
            self.gnome_lock_afterblank_tip.setText('在显示器关闭后，自动锁定电脑当前登入的账户。您当前打开的文档不会因此丢失。要修改此项设置，请先启用功能。')

        if self.gnome_auto_suspend_combo_enable.currentIndex() == 0:
            self.gnome_auto_suspend_combo_setting.setEnabled(True)
            self.gnome_auto_suspend_tip.setText('长期未使用电脑时，使其自动睡眠以减少能源消耗。您当前打开的文档不会因此丢失。')
        else:
            self.gnome_auto_suspend_combo_setting.setEnabled(False)
            self.gnome_auto_suspend_tip.setText('长期未使用电脑时，使其自动睡眠以减少能源消耗。您当前打开的文档不会因此丢失。要修改此项设置，请先启用功能。')

        pass

    def gnome_combo_applier(self):
        # print('activated. ')

        ## autoblank screen
        autoblank_preset_list = [1, 2, 3, 4, 5, 8, 10, 12, 15, 0]
        autoblank_delay_target = autoblank_preset_list[self.gnome_autoblank_combobox_setting.currentIndex()]

        ## auto lock
        if self.gnome_lock_afterblank_combo_enable.currentIndex() == 0:
            autolock_flag_target = True
            self.gnome_lock_afterblank_combo_setting.setEnabled(True)
            self.gnome_lock_afterblank_tip.setText('在显示器关闭后，自动锁定电脑当前登入的账户。您当前打开的文档不会因此丢失。')
        else:
            autolock_flag_target = False
            self.gnome_lock_afterblank_combo_setting.setEnabled(False)
            self.gnome_lock_afterblank_tip.setText('在显示器关闭后，自动锁定电脑当前登入的账户。您当前打开的文档不会因此丢失。要修改此项设置，请先启用功能。')

        autolock_delay_preset_list = [0, 0.5, 1, 2, 3, 5, 30, 60]
        autolock_delay_target = autolock_delay_preset_list[self.gnome_lock_afterblank_combo_setting.currentIndex()]

        ## auto suspend
        if self.gnome_auto_suspend_combo_enable.currentIndex() == 0:
            auto_suspend_flag_target = True
            self.gnome_auto_suspend_combo_setting.setEnabled(True)
            self.gnome_auto_suspend_tip.setText('长期未使用电脑时，使其自动睡眠以减少能源消耗。您当前打开的文档不会因此丢失。')
        else:
            auto_suspend_flag_target = False
            self.gnome_auto_suspend_combo_setting.setEnabled(False)
            self.gnome_auto_suspend_tip.setText('长期未使用电脑时，使其自动睡眠以减少能源消耗。您当前打开的文档不会因此丢失。要修改此项设置，请先启用功能。')
        auto_suspend_delay_preset_list = [15, 20, 25, 30, 45, 60, 80, 90, 100, 120]
        auto_suspend_delay_target = auto_suspend_delay_preset_list[self.gnome_auto_suspend_combo_setting.currentIndex()]

        ## autolock on suspend
        if self.gnome_autolock_on_suspend_combo_enable.currentIndex() == 0:
            autolock_on_suspend_flag_target = True
            self.gnome_autolock_on_suspend_tip.setText('当用户在电源选项中选择睡眠时，电脑将会自动锁定当前登入的账户。您当前打开的文档不会因此丢失。')
        else:
            autolock_on_suspend_flag_target = False
            self.gnome_autolock_on_suspend_tip.setText('当用户在电源选项中选择睡眠时，电脑不会对当前登入账户的状态进行额外操作。')

        # print(autoblank_delay_target, autolock_flag_target, autolock_delay_target,
        #       auto_suspend_flag_target, auto_suspend_delay_target)

        ## apply these settings to the system
        self.backend.override_setting_gnome(autoblank_delay_target, autolock_flag_target, autolock_delay_target,
                                            auto_suspend_flag_target, auto_suspend_delay_target,
                                            autolock_on_suspend_flag_target)
        # self.backend.override_setting_gnome(blank_delay = None, auto_lock_flag = True, auto_lock_delay = None,
        #                        sys_sleep_flag = True, sys_sleep_ac = None)

        self.system_notification_generator()
        pass

    def ukui_init(self):
        self.ukui_visual()
        self.ukui_logic()
        pass

    def ukui_visual(self):
        pass

    def ukui_logic(self):

        ## getting current setting value
        self.backend.ukui_get_current_lock_setting()

        self.ukui_display_lock_count_current = self.backend.locks_rest_time
        self.ukui_custom_power_current = self.backend.locks_custom_plan
        self.ukui_autoblank_delay_current = int(int(self.backend.locks_display_sleep) / 60)
        self.ukui_auto_suspend_delay_current = int(int(self.backend.locks_computer_sleep) / 60)

        self.ukui_combo_reader()

        pass

    def ukui_combo_reader(self):
        print('ukui reader activated. ')
        ## display lock count on the system
        display_lock_count_preset_list = ['true', 'false']
        ukui_display_lock_count_status_index = display_lock_count_preset_list.index(
            self.ukui_display_lock_count_current)
        self.ukui_display_time_count_on_lock_combo_enable.setCurrentIndex(ukui_display_lock_count_status_index)

        ## customized power plan
        custom_power_preset_list = ['true', 'false']
        ukui_custom_power_status_index = custom_power_preset_list.index(
            self.ukui_custom_power_current)
        self.ukui_custom_power_combo_enable.setCurrentIndex(ukui_custom_power_status_index)

        self.ukui_combo_mask_on_first_run()

        ## autoblank delay
        autoblank_preset_list = [0, 1, 5, 10, 20, 30, 60, 120]
        ukui_autoblank_combobox_index = autoblank_preset_list.index(self.ukui_autoblank_delay_current)
        self.ukui_autoblank_combo_setting.setCurrentIndex(ukui_autoblank_combobox_index)

        ## auto suspend delay
        auto_suspend_preset_list = [0, 10, 20, 30, 60, 120, 300]
        ukui_auto_suspend_combobox_index = auto_suspend_preset_list.index(self.ukui_auto_suspend_delay_current)
        self.ukui_auto_suspend_combo_setting.setCurrentIndex(ukui_auto_suspend_combobox_index)

        self.ukui_display_time_count_on_lock_combo_enable.currentIndexChanged.connect(self.ukui_combo_applier)
        self.ukui_custom_power_combo_enable.currentIndexChanged.connect(self.ukui_combo_applier)
        self.ukui_autoblank_combo_setting.currentIndexChanged.connect(self.ukui_combo_applier)
        self.ukui_auto_suspend_combo_setting.currentIndexChanged.connect(self.ukui_combo_applier)
        pass

    def ukui_combo_mask_on_first_run(self):
        print('ukui first run activated. ')
        ## should the setting already been disabled, the combo box should be disabled either
        if self.ukui_custom_power_combo_enable.currentIndex() == 0:
            self.ukui_autoblank_combo_setting.setEnabled(True)
            self.ukui_auto_suspend_combo_setting.setEnabled(True)

            self.ukui_autoblank_tip.setText('如果您在一段时间内未使用电脑，则自动关闭显示器。')
            self.ukui_auto_suspend_tip.setText('长期未使用电脑时，使其自动睡眠以减少能源消耗。您当前打开的文档不会因此丢失。')
        else:
            self.ukui_autoblank_combo_setting.setEnabled(False)
            self.ukui_auto_suspend_combo_setting.setEnabled(False)

            self.ukui_autoblank_tip.setText('如果您在一段时间内未使用电脑，则自动关闭显示器。若要启用此功能，请首先开启自定义电源模式。')
            self.ukui_auto_suspend_tip.setText('长期未使用电脑时，使其自动睡眠以减少能源消耗。您当前打开的文档不会因此丢失。若要启用此功能，请首先开启自定义电源模式。')
        pass

    def ukui_combo_applier(self):
        print('ukui applier activated. ')
        ## lock screen display time count
        if self.ukui_display_time_count_on_lock_combo_enable.currentIndex() == 0:
            display_time_count_flag_target = True
        else:
            display_time_count_flag_target = False
            pass

        ## customs power flag
        if self.ukui_custom_power_combo_enable.currentIndex() == 0:
            self.ukui_autoblank_combo_setting.setEnabled(True)
            self.ukui_auto_suspend_combo_setting.setEnabled(True)

            self.ukui_autoblank_tip.setText('如果您在一段时间内未使用电脑，则自动关闭显示器。')
            self.ukui_auto_suspend_tip.setText('长期未使用电脑时，使其自动睡眠以减少能源消耗。您当前打开的文档不会因此丢失。')
            custom_power_flag_target = True
        else:
            self.ukui_autoblank_combo_setting.setEnabled(False)
            self.ukui_auto_suspend_combo_setting.setEnabled(False)

            self.ukui_autoblank_tip.setText('如果您在一段时间内未使用电脑，则自动关闭显示器。若要启用此功能，请首先开启自定义电源模式。')
            self.ukui_auto_suspend_tip.setText('长期未使用电脑时，使其自动睡眠以减少能源消耗。您当前打开的文档不会因此丢失。若要启用此功能，请首先开启自定义电源模式。')
            custom_power_flag_target = False

        ## autoblank delay
        autoblank_preset_list = [0, 1, 5, 10, 20, 30, 60, 120]
        autoblank_delay_target = autoblank_preset_list[self.ukui_autoblank_combo_setting.currentIndex()]

        ## auto suspend delay
        auto_suspend_preset_list = [0, 10, 20, 30, 60, 120, 300]
        auto_suspend_delay_target = auto_suspend_preset_list[self.ukui_auto_suspend_combo_setting.currentIndex()]

        self.backend.override_setting_ukui(display_time_count_flag_target, custom_power_flag_target,
                                           autoblank_delay_target, auto_suspend_delay_target)

        self.system_notification_generator()
        pass

    def mate_init(self):
        self.mate_visual()
        self.mate_logic()
        pass

    def mate_visual(self):
        pass

    def mate_logic(self):
        ## getting current setting value
        self.backend.mate_get_current_lock_setting()

        self.mate_autoblank_delay_current = int(int(self.backend.locks_display_sleep) / 60)
        self.mate_auto_suspend_delay_current = int(int(self.backend.locks_computer_sleep) / 60)
        self.mate_power_btn_action = self.backend.power_button_behavior

        self.mate_combo_reader()
        pass

    def mate_combo_reader(self):
        print('mate reader activated. ')

        ## autoblank delay
        autoblank_preset_list = [0, 1, 5, 10, 30, 60]
        mate_autoblank_combobox_index = autoblank_preset_list.index(self.mate_autoblank_delay_current)
        self.mate_autoblank_combo_setting.setCurrentIndex(mate_autoblank_combobox_index)

        ## auto suspend delay
        auto_suspend_preset_list = [0, 10, 30, 60, 120]
        mate_auto_suspend_combobox_index = auto_suspend_preset_list.index(self.mate_auto_suspend_delay_current)
        self.mate_auto_suspend_combo_setting.setCurrentIndex(mate_auto_suspend_combobox_index)

        ## power button behavior
        power_btn_preset_list = ['interactive', 'suspend', 'shutdown', 'nothing']
        mate_custom_power_status_index = power_btn_preset_list.index(
            self.mate_power_btn_action)
        self.mate_power_btn_combo_setting.setCurrentIndex(mate_custom_power_status_index)

        ## connecting buttons to functions here
        self.mate_autoblank_combo_setting.currentIndexChanged.connect(self.mate_combo_applier)
        self.mate_auto_suspend_combo_setting.currentIndexChanged.connect(self.mate_combo_applier)
        self.mate_power_btn_combo_setting.currentIndexChanged.connect(self.mate_combo_applier)
        pass

    def mate_combo_applier(self):

        ## autoblank delay
        autoblank_preset_list = [0, 1, 5, 10, 30, 60]
        autoblank_delay_target = autoblank_preset_list[self.mate_autoblank_combo_setting.currentIndex()]

        ## auto suspend delay
        auto_suspend_preset_list = [0, 10, 30, 60, 120]
        auto_suspend_delay_target = auto_suspend_preset_list[self.mate_auto_suspend_combo_setting.currentIndex()]

        ## power button function
        power_btn_preset_list = ['interactive', 'suspend', 'shutdown', 'nothing']
        power_btn_target = power_btn_preset_list[self.mate_power_btn_combo_setting.currentIndex()]

        self.backend.override_setting_mate(autoblank_delay_target, auto_suspend_delay_target,
                                           power_btn_target)

        self.system_notification_generator()
        pass

    def uos_init(self):
        self.uos_visual()
        self.uos_logic()
        pass

    def uos_visual(self):
        pass

    def uos_logic(self):
        self.backend.uos_get_current_lock_setting()

        self.uos_auto_blank_delay_current = int(int(self.backend.auto_blank_delay) / 60)
        # print('blank前端设置', self.uos_auto_blank_delay_current, '后端返回', self.backend.auto_blank_delay)
        self.uos_auto_lock_delay_current = int(int(self.backend.auto_lock_delay) / 60)
        # print('lock前端设置', self.uos_auto_lock_delay_current, '后端返回', self.backend.auto_lock_delay)
        self.uos_auto_sleep_delay_current = int(int(self.backend.auto_sleep_delay) / 60)
        # print('sleep前端设置', self.uos_auto_sleep_delay_current, '后端返回', self.backend.auto_sleep_delay)
        self.uos_power_btn_action = self.backend.power_button_behavior

        self.uos_combo_reader()

        pass

    def uos_combo_reader(self):
        print('uos reader activated. ')

        ## autoblank delay
        autoblank_preset_list = [1, 5, 10, 15, 30, 60, 0]
        uos_autoblank_combobox_index = autoblank_preset_list.index(self.uos_auto_blank_delay_current)
        self.uos_autoblank_combobox_setting.setCurrentIndex(uos_autoblank_combobox_index)

        ## autolock delay
        autolock_present_list = [1, 5, 10, 15, 30, 60, 0]
        uos_autolock_combobox_index = autolock_present_list.index(self.uos_auto_lock_delay_current)
        self.uos_autolock_combobox_setting.setCurrentIndex(uos_autolock_combobox_index)

        ## autosleep delay
        autosleep_present_list = [1, 5, 10, 15, 30, 60, 0]
        uos_autosleep_combo_index = autosleep_present_list.index(self.uos_auto_sleep_delay_current)
        self.uos_autosleep_combobox_setting.setCurrentIndex(uos_autosleep_combo_index)

        # print('1, 5, 10, 15, 30, 60, 0')
        # print('blank, lock, sleep index', uos_autoblank_combobox_index, uos_autolock_combobox_index,
        #       uos_autosleep_combo_index)

        ## power button behavior
        power_btn_preset_list = ["'shutdown'", "'suspend'", "'hibernate'", "'turnOffScreen'", "'showSessionUI'"]
        try:
            uos_custom_power_status_index = power_btn_preset_list.index(
                self.uos_power_btn_action)
        except ValueError:
            ## handling if the index cannot be located.
            uos_custom_power_status_index = 0
        self.uos_power_btn_combo_setting.setCurrentIndex(uos_custom_power_status_index)

        ## connecting buttons to functions here
        self.uos_autoblank_combobox_setting.currentIndexChanged.connect(self.uos_combo_applier)
        self.uos_autolock_combobox_setting.currentIndexChanged.connect(self.uos_combo_applier)
        self.uos_autosleep_combobox_setting.currentIndexChanged.connect(self.uos_combo_applier)
        self.uos_power_btn_combo_setting.currentIndexChanged.connect(self.uos_combo_applier)
        pass

    def uos_combo_applier(self):
        ## autoblank delay
        autoblank_preset_list = [1, 5, 10, 15, 30, 60, 0]
        autoblank_delay_target = autoblank_preset_list[self.uos_autoblank_combobox_setting.currentIndex()]

        ## autolock_delay
        autolock_preset_list = [1, 5, 10, 15, 30, 60, 0]
        autolock_delay_target = autolock_preset_list[self.uos_autolock_combobox_setting.currentIndex()]

        ## autosleep_delay
        autosleep_preset_list = [1, 5, 10, 15, 30, 60, 0]
        autosleep_delay_target = autosleep_preset_list[self.uos_autosleep_combobox_setting.currentIndex()]

        ## power button function
        power_btn_preset_list = ['shutdown', 'suspend', 'hibernate', 'turnOffScreen', 'showSessionUI']
        power_btn_target = power_btn_preset_list[self.uos_power_btn_combo_setting.currentIndex()]

        # print('1, 5, 10, 15, 30, 60, 0')
        # print('blank, lock, sleep target', autoblank_delay_target, autolock_delay_target, autosleep_delay_target,
        #       power_btn_target)

        self.backend.override_setting_uos(autoblank_delay_target, autolock_delay_target, autosleep_delay_target,
                                          power_btn_target)

        self.system_notification_generator()
        pass

    def others_init(self):
        self.others_visual()
        self.others_logic()
        pass

    def others_visual(self):
        self.util_greenify_stack_other_push_btn.setVisible(False)
        self.util_greenify_stack_other_push_btn_prompt.setVisible(False)
        pass

    def others_logic(self):

        pass

    def system_notification_generator(self):
        message_icon = '-i process-working'
        message_title = '蓝狐 - 节电优能'
        message_content = '已经成功为您更新系统中与节能相关的设定。'
        subprocess.Popen(['notify-send', message_icon, message_title, message_content])

    def closeEvent(self, event) -> None:
        ## rewrite the close event to cooperate with the system tray
        event.ignore()
        # print('AppStore hidden. ')
        self.hide()
