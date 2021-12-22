## import python dependencies
import os
from glob import glob
import subprocess

import psutil
import threading

from threading import Timer
from datetime import datetime
from datetime import timedelta

import time
from time import time, sleep, strftime

## import PyQt5 dependencies
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Greenify(threading.Thread):
    ## if reporting the scan progress is necessary, then switch to PyQt toolkit

    def __init__(self):
        super().__init__()

        ## to check is the terminal is equipped with a battery
        self.battery_flag = bool(psutil.sensors_battery())

        ## use this var to examine if the system is running under sudo
        self.euid = os.geteuid()
        ## if euid is 0, then the program is under sudo.

        ## checking the desktop environment software in the host environment
        self.desktop_environment_checker()

        # self.current_lock_setting()

        # self.check_power_consumption()
        pass

    def run(self) -> None:
        # while True:
        #     self.check_power_consumption()
        #     ## the arg is in seconds
        #     sleep(float(1))
        self.desktop_environment_checker()
        pass

    def desktop_environment_checker(self):
        raw_output = subprocess.Popen('echo $XDG_CURRENT_DESKTOP', shell = True,
                                      stdout = subprocess.PIPE).communicate()[0]
        self.de_output = str(raw_output, 'utf-8')

        ## deciding the actual desktop environment software.
        if 'UKUI' in self.de_output:
            self.de_var = 'kylin'
        elif 'GNOME' in self.de_output:
            self.de_var = 'gnome'
        elif 'MATE' in self.de_output:
            self.de_var = 'mate'
        elif 'Deepin' in self.de_output:
            self.de_var = 'uos'
        else:
            self.de_var = 'na'

        pass

    def check_power_consumption(self):
        ## boot time
        if hasattr(psutil, 'boot_time'):
            self.up_time = str(timedelta(seconds = round(time() - psutil.boot_time(),
                                                         0)))[:-3].replace(":", " hours, ") + " mins"
        else:
            self.up_time = str('Not available. ')

        split_var = self.up_time.split(', ')
        if len(split_var) == 1:
            self.up_time_day = int(0)
            self.up_time_hr = int(0)
            if split_var[0].split(' ')[0].startswith('0'):
                self.up_time_min = split_var[0].split(' ')[0][1:]
            else:
                self.up_time_min = split_var[0].split(' ')[0]
        elif len(split_var) == 2:
            self.up_time_day = int(0)
            self.up_time_hr = split_var[0].split(' ')[0]
            if split_var[1].split(' ')[0].startswith('0'):
                self.up_time_min = split_var[1].split(' ')[0][1:]
            else:
                self.up_time_min = split_var[1].split(' ')[0]
        elif len(split_var) == 3:
            self.up_time_day = split_var[0].split(' ')[0]
            self.up_time_hr = split_var[1].split(' ')[0]
            if split_var[2].split(' ')[0].startswith('0'):
                self.up_time_min = split_var[2].split(' ')[0][1:]
            else:
                self.up_time_min = split_var[2].split(' ')[0]
        else:
            self.up_time_day = str('na')
            self.up_time_hr = str('na')
            self.up_time_min = str('na')

        #######################################
        ## battery information
        if self.battery_flag:
            bat_info = psutil.sensors_battery()
            ## 24 hrs = 86400 secs

            if hasattr(bat_info, 'percent'):
                self.bat_perc = bat_info.percent
            else:
                self.bat_perc = str('DC Power')

            if hasattr(bat_info, 'power_plugged'):
                self.bat_plugin = bat_info.power_plugged
            else:
                self.bat_plugin = str('DC Power')

            if hasattr(bat_info, 'secsleft'):
                if type(bat_info.secsleft) == int:
                    if bat_info.secsleft >= 86400:
                        self.bat_time = str('Calculating. ')
                        self.bat_hr = str('nan')
                        self.bat_min = str('nan')
                    else:
                        self.bat_time = bat_info.secsleft
                        self.bat_hr = round(int(bat_info.secsleft) / 3600)
                        self.bat_min = round(int(bat_info.secsleft) % 3600 / 60)
                else:
                    self.bat_time = str('DC Power')
                    self.bat_hr = str('nan')
                    self.bat_min = str('nan')
            else:
                self.bat_time = str('nan')
                self.bat_hr = str('nan')
                self.bat_min = str('nan')
        else:
            self.bat_perc = int('100')
            self.bat_time = str('DC Power')
            self.bat_plugin = str('DC Power')
            self.bat_hr = str('nan')
            self.bat_min = str('nan')

        print(self.up_time)
        pass

    def gnome_get_current_lock_setting(self):
        ## adapting the gnome desktop environment

        blank_screen_delay = str(subprocess.Popen('dconf read /org/gnome/desktop/session/idle-delay',
                                                  shell = True, stdout = subprocess.PIPE).communicate()[0],
                                 'utf-8')
        ## the actual returning value is like 'uint32 180'
        self.blank_screen_delay = blank_screen_delay.split(' ')[-1]
        if len(self.blank_screen_delay) < 1:
            self.blank_screen_delay = str('180')

        self.auto_lock_status = str(subprocess.Popen('dconf read /org/gnome/desktop/screensaver/lock-enabled',
                                                     shell = True, stdout = subprocess.PIPE).communicate()[0],
                                    'utf-8')[:-1]
        if self.auto_lock_status.endswith('\n'):
            self.auto_lock_status = self.auto_lock_status[:-1]
        if len(self.auto_lock_status) < 1:
            self.auto_lock_status = str('true')

        auto_lock_delay = str(subprocess.Popen('dconf read /org/gnome/desktop/screensaver/lock-delay',
                                               shell = True, stdout = subprocess.PIPE).communicate()[0],
                              'utf-8')
        self.auto_lock_delay = auto_lock_delay.split(' ')[-1]
        if len(self.auto_lock_delay) < 1:
            self.auto_lock_delay = str('180')

        self.auto_suspend_status = str(
            subprocess.Popen('dconf read /org/gnome/settings-daemon/plugins/power/sleep-inactive-ac-type',
                             shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
        if self.auto_suspend_status.endswith('\n'):
            self.auto_suspend_status = self.auto_suspend_status[:-1]
        if len(self.auto_suspend_status) < 1:
            self.auto_suspend_status = str("'suspend'")

        if 'nothing' not in self.auto_suspend_status:
            self.auto_suspend_delay = str(
                subprocess.Popen('dconf read /org/gnome/settings-daemon/plugins/power/sleep-inactive-ac-timeout',
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
            if len(self.auto_suspend_delay) < 1:
                self.auto_suspend_delay = str('3600')
        else:
            self.auto_suspend_delay = str('0')

        self.lock_on_suspend = str(
            subprocess.Popen('dconf read /org/gnome/desktop/screensaver/ubuntu-lock-on-suspend',
                             shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
        if self.lock_on_suspend.endswith('\n'):
            self.lock_on_suspend = self.lock_on_suspend[:-1]
        if len(self.lock_on_suspend) < 1:
            self.lock_on_suspend = str('true')
            pass

    def ukui_get_current_lock_setting(self):
        ## adapting the ukui desktop environment for kylin software distribution here.

        self.locks_rest_time = str(subprocess.Popen('dconf read /org/ukui/screensaver/show-rest-time',
                                                    shell = True, stdout = subprocess.PIPE).communicate()[0],
                                   'utf-8')
        if self.locks_rest_time.endswith('\n'):
            self.locks_rest_time = self.locks_rest_time[:-1]
        if len(self.locks_rest_time) < 1:
            self.locks_rest_time = str('false')

        self.locks_custom_plan = str(subprocess.Popen('dconf read /org/ukui/control-center/personalise/custompower',
                                                      shell = True, stdout = subprocess.PIPE).communicate()[0],
                                     'utf-8')
        if self.locks_custom_plan.endswith('\n'):
            self.locks_custom_plan = self.locks_custom_plan[:-1]
        if len(self.locks_custom_plan) < 1:
            self.locks_custom_plan = str('true')

        self.locks_display_sleep = str(subprocess.Popen('dconf read /org/ukui/power-manager/sleep-display-ac',
                                                        shell = True, stdout = subprocess.PIPE).communicate()[0],
                                       'utf-8')
        if len(self.locks_display_sleep) < 1:
            self.locks_display_sleep = str('300')

        self.locks_computer_sleep = str(subprocess.Popen('dconf read /org/ukui/power-manager/sleep-computer-ac',
                                                         shell = True, stdout = subprocess.PIPE).communicate()[0],
                                        'utf-8')
        if len(self.locks_computer_sleep) < 1:
            self.locks_computer_sleep = str('600')

    def mate_get_current_lock_setting(self):
        self.locks_display_sleep = str(subprocess.Popen('dconf read /org/mate/power-manager/sleep-display-ac',
                                                        shell = True, stdout = subprocess.PIPE).communicate()[0],
                                       'utf-8')
        if len(self.locks_display_sleep) < 1:
            self.locks_display_sleep = str('10')

        self.locks_computer_sleep = str(subprocess.Popen('dconf read /org/mate/power-manager/sleep-computer-ac',
                                                         shell = True, stdout = subprocess.PIPE).communicate()[0],
                                        'utf-8')
        if len(self.locks_computer_sleep) < 1:
            self.locks_computer_sleep = str('30')

        self.power_button_behavior = str(subprocess.Popen('dconf read /org/mate/power-manager/button-power',
                                                          shell = True, stdout = subprocess.PIPE).communicate()[0],
                                         'utf-8')

        if self.power_button_behavior.endswith('\n'):
            self.power_button_behavior = self.power_button_behavior[:-1]
        if len(self.power_button_behavior) < 1:
            self.power_button_behavior = str('suspend')
        pass

    def uos_get_current_lock_setting(self):
        self.auto_blank_delay = str(subprocess.Popen('dconf read /com/deepin/dde/power/line-power-screen-black-delay',
                                                     shell = True, stdout = subprocess.PIPE).communicate()[0],
                                    'utf-8')
        if len(self.auto_blank_delay) < 1:
            self.auto_blank_delay = str('600')

        self.auto_lock_delay = str(subprocess.Popen('dconf read /com/deepin/dde/power/line-power-lock-delay',
                                                    shell = True, stdout = subprocess.PIPE).communicate()[0],
                                   'utf-8')
        if len(self.auto_lock_delay) < 1:
            self.auto_lock_delay = str('600')

        self.auto_sleep_delay = str(subprocess.Popen('dconf read /com/deepin/dde/power/line-power-sleep-delay',
                                                     shell = True, stdout = subprocess.PIPE).communicate()[0],
                                    'utf-8')
        if len(self.auto_sleep_delay) < 1:
            self.auto_sleep_delay = str('900')

        self.power_button_behavior = str(
            subprocess.Popen('dconf read /com/deepin/dde/power/line-power-press-power-button',
                             shell = True, stdout = subprocess.PIPE).communicate()[0],
            'utf-8')

        if self.power_button_behavior.endswith('\n'):
            self.power_button_behavior = self.power_button_behavior[:-1]
        if len(self.power_button_behavior) < 1:
            self.power_button_behavior = str('suspend')
        pass

    def override_setting_ukui(self, rest_time_bool = None, custom_power = True,
                              dis_sleep_ac = None, sys_sleep_ac = None):

        ## display time count on lock screen
        ## this setting is functioning, but it seems not to adjust anything
        ## should be a bug from the UKUI

        if rest_time_bool == True:
            rest_time_target = 'true'
        else:
            rest_time_target = 'false'
        rest_time_mod = str(
            subprocess.Popen('dconf write /org/ukui/screensaver/show-rest-time %s' % rest_time_target,
                             shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        ## custom power setting
        if custom_power == True:
            custom_power_target = 'true'
        else:
            custom_power_target = 'false'
        enable_cust_power_plan = str(
            subprocess.Popen('dconf write /org/ukui/control-center/personalise/custompower %s' % custom_power_target,
                             shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        ## autoblank setting
        if dis_sleep_ac is not None:
            ## convert to seconds
            dis_sleep_ac = str(60 * int(dis_sleep_ac))
            dis_sleep_ac_mod = str(
                subprocess.Popen('dconf write /org/ukui/power-manager/sleep-display-ac %s' % dis_sleep_ac,
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        ## auto suspend setting
        if sys_sleep_ac is not None:
            ## convert to senconds
            sys_sleep_ac = str(60 * int(sys_sleep_ac))
            sys_sleep_ac_mod = str(
                subprocess.Popen('dconf write /org/ukui/power-manager/sleep-computer-ac %s' % sys_sleep_ac,
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
            # print('system sleep ac', sys_sleep_ac, 'secs. ')

        pass

    def override_setting_gnome(self, blank_delay = None, auto_lock_flag = True, auto_lock_delay = None,
                               sys_sleep_flag = True, sys_sleep_ac = None, lock_on_suspend_flag = False):
        ## blank screen delay
        if blank_delay is not None:
            blank_delay = str(60 * int(blank_delay))
            blank_delay_mod = str(
                subprocess.Popen('dconf write /org/gnome/desktop/session/idle-delay "uint32 %s"' % blank_delay,
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
            # print('blank screen delay adjusted to ', blank_delay, 'secs. ')

        ## auto lock setting here
        if auto_lock_flag == True:
            auto_lock_enable = str(subprocess.Popen('dconf write /org/gnome/desktop/screensaver/lock-enabled true',
                                                    shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
        elif auto_lock_flag == False:
            auto_lock_enable = str(subprocess.Popen('dconf write /org/gnome/desktop/screensaver/lock-enabled false',
                                                    shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
        # print('auto lock enabled. ')

        if auto_lock_delay is not None:
            auto_lock_delay = str(60 * int(auto_lock_delay))
            auto_lock_delay_mod = str(
                subprocess.Popen('dconf write /org/gnome/desktop/screensaver/lock-delay "uint32 %s"' % auto_lock_delay,
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
            # print('system will be automatically locked after the blank screen goes for ', auto_lock_delay, 'secs. ')

        ## set the auto suspend status
        # auto_suspend_command = 'dconf write /org/gnome/settings-daemon/plugins/power/sleep-inactive-ac-type "\'suspend\'"'

        if sys_sleep_flag == True:
            as_command_type = "'suspend'"
        elif sys_sleep_flag == False:
            as_command_type = "'nothing'"

        as_command = (
                'dconf write /org/gnome/settings-daemon/plugins/power/sleep-inactive-ac-type "%s"' % as_command_type)
        auto_suspend = str(subprocess.Popen(as_command, shell = True, stdout = subprocess.PIPE).communicate()[0],
                           'utf-8')
        # print('auto', as_command_type, 'now enabled. ')

        if sys_sleep_ac is not None:
            sys_sleep_ac = str(60 * int(sys_sleep_ac))
            sys_sleep_mod = str(subprocess.Popen(
                'dconf write /org/gnome/settings-daemon/plugins/power/sleep-inactive-ac-timeout %s' % sys_sleep_ac,
                shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
            # print('auto sleep now set to ', sys_sleep_ac)

        ## autolock on suspend setting here

        if lock_on_suspend_flag is True:
            auto_lock_on_suspend = str(
                subprocess.Popen('dconf write /org/gnome/desktop/screensaver/ubuntu-lock-on-suspend true',
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
        elif lock_on_suspend_flag is False:
            auto_lock_on_suspend = str(
                subprocess.Popen('dconf write /org/gnome/desktop/screensaver/ubuntu-lock-on-suspend false',
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        pass

    def override_setting_mate(self, dis_sleep_ac = None, sys_sleep_ac = None, power_btn_fuc = None):
        ## autoblank setting
        if dis_sleep_ac is not None:
            ## convert to seconds
            dis_sleep_ac = str(60 * int(dis_sleep_ac))
            dis_sleep_ac_mod = str(
                subprocess.Popen('dconf write /org/mate/power-manager/sleep-display-ac %s' % dis_sleep_ac,
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        ## auto suspend setting
        if sys_sleep_ac is not None:
            ## convert to senconds
            sys_sleep_ac = str(60 * int(sys_sleep_ac))
            sys_sleep_ac_mod = str(
                subprocess.Popen('dconf write /org/mate/power-manager/sleep-computer-ac %s' % sys_sleep_ac,
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
            # print('system sleep ac', sys_sleep_ac, 'secs. ')

        ## power button function
        if power_btn_fuc is not None:
            power_btn_command_type = "'%s'" % power_btn_fuc
            power_btn_command = ('dconf write /org/mate/power-manager/button-power "%s"' % power_btn_command_type)
            power_btn_mod = str(
                subprocess.Popen(power_btn_command, shell = True, stdout = subprocess.PIPE).communicate()[0],
                'utf-8')
        pass

    def override_setting_uos(self, dis_sleep_ac = None, sys_lock_ac = None, sys_sleep_ac = None, power_btn_fuc = None):

        if dis_sleep_ac is not None:
            ## convert to seconds
            dis_sleep_ac = str(60 * int(dis_sleep_ac))
            dis_sleep_ac_mod = str(
                subprocess.Popen('dconf write /com/deepin/dde/power/line-power-screen-black-delay %s' % dis_sleep_ac,
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        if sys_lock_ac is not None:
            ## convert to senconds
            sys_lock_ac = str(60 * int(sys_lock_ac))
            sys_lock_ac_mod = str(
                subprocess.Popen('dconf write /com/deepin/dde/power/line-power-lock-delay %s' % sys_lock_ac,
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        if sys_sleep_ac is not None:
            ## convert to senconds
            sys_sleep_ac = str(60 * int(sys_sleep_ac))
            sys_sleep_ac_mod = str(
                subprocess.Popen('dconf write /com/deepin/dde/power/line-power-sleep-delay %s' % sys_sleep_ac,
                                 shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        if power_btn_fuc is not None:
            power_btn_command_type = "'%s'" % power_btn_fuc
            power_btn_command = (
                    'dconf write /com/deepin/dde/power/line-power-press-power-button "%s"' % power_btn_command_type)
            power_btn_mod = str(
                subprocess.Popen(power_btn_command, shell = True, stdout = subprocess.PIPE).communicate()[0],
                'utf-8')
