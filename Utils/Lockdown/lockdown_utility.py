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


## in this application
## we intend to activate the hidden lockdown function
## under different Ubuntu Desktop Environments (DEs)

class Lockdown(threading.Thread):

    def __init__(self):
        super().__init__()

        ## use this var to check if the application is running under admin
        self.euid = os.geteuid()

        ## check DE
        self.desktop_environment_checker()

    def run(self) -> None:

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
        else:
            self.de_var = 'na'

        pass

    def string_feedback_handler(self, target):
        target = str(target)

        ## handling the input content
        if target.endswith('\n'):
            target = target[:-1]
        if len(target) < 1:
            target = str('false')

        return target

    def gnome_get_current_lockdown_setting(self):

        ## disable lock screen
        self.disable_lock_screen = str(subprocess.Popen('dconf read /org/gnome/desktop/lockdown/disable-lock-screen',
                                                        shell = True, stdout = subprocess.PIPE).communicate()[0],
                                       'utf-8')
        self.disable_lock_screen = self.string_feedback_handler(self.disable_lock_screen)

        ## disable log out
        self.disable_log_out = str(subprocess.Popen('dconf read /org/gnome/desktop/lockdown/disable-log-out',
                                                    shell = True, stdout = subprocess.PIPE).communicate()[0],
                                   'utf-8')
        self.disable_log_out = self.string_feedback_handler(self.disable_log_out)

        ## disable print
        self.disable_printing = str(subprocess.Popen('dconf read /org/gnome/desktop/lockdown/disable-printing',
                                                     shell = True, stdout = subprocess.PIPE).communicate()[0],
                                    'utf-8')
        self.disable_printing = self.string_feedback_handler(self.disable_printing)

        ## disable save to disk
        self.disable_save_to_disk = str(subprocess.Popen('dconf read /org/gnome/desktop/lockdown/disable-save-to-disk',
                                                         shell = True, stdout = subprocess.PIPE).communicate()[0],
                                        'utf-8')
        self.disable_save_to_disk = self.string_feedback_handler(self.disable_save_to_disk)

        ## disable user switching
        self.disable_user_switching = str(
            subprocess.Popen('dconf read /org/gnome/desktop/lockdown/disable-user-switching',
                             shell = True, stdout = subprocess.PIPE).communicate()[0],
            'utf-8')
        self.disable_user_switching = self.string_feedback_handler(self.disable_user_switching)

        ## mount removable as read only
        self.mount_removable_storage_read_only = str(
            subprocess.Popen('dconf read /org/gnome/desktop/lockdown/mount-removable-storage-devices-as-read-only',
                             shell = True, stdout = subprocess.PIPE).communicate()[0],
            'utf-8')
        self.mount_removable_storage_read_only = self.string_feedback_handler(self.mount_removable_storage_read_only)

    def gnome_lockdown_setting_applier(self, disable_lock_screen_tar = 'false', disable_log_out_tar = 'false',
                                       disable_printing_tar = 'false', disable_save_to_disk_tar = 'false',
                                       disable_user_switching_tar = 'false',
                                       mount_removable_storage_read_only_tar = 'false'):
        disable_lock_screen_mod = str(
            subprocess.Popen('dconf write /org/gnome/desktop/lockdown/disable-lock-screen %s' % disable_lock_screen_tar,
                             shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        disable_log_out_mod = str(
            subprocess.Popen('dconf write /org/gnome/desktop/lockdown/disable-log-out %s' % disable_log_out_tar,
                             shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        disable_printing_mod = str(
            subprocess.Popen('dconf write /org/gnome/desktop/lockdown/disable-printing %s' % disable_printing_tar,
                             shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        disable_save_to_disk_mod = str(
            subprocess.Popen(
                'dconf write /org/gnome/desktop/lockdown/disable-save-to-disk %s' % disable_save_to_disk_tar,
                shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        disable_user_switching_mod = str(
            subprocess.Popen(
                'dconf write /org/gnome/desktop/lockdown/disable-user-switching %s' % disable_user_switching_tar,
                shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        mount_removable_storage_read_only_mod = str(
            subprocess.Popen('dconf write /org/gnome/desktop/lockdown/disable-log-out %s' % disable_log_out_tar,
                             shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        disable_log_out_mod = str(
            subprocess.Popen(
                'dconf write /org/gnome/desktop/lockdown/mount-removable-storage-devices-as-read-only %s' % mount_removable_storage_read_only_tar,
                shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')
        pass

    def kylin_get_current_lockdown_setting(self):
        ## initiate the lockdown setting loading here
        ## prepare for different de var
        if self.de_output == 'kylin':
            de_var = 'ukui'
        if self.de_output == 'mate':
            de_var = 'mate'

        ## read corresponding content here.
