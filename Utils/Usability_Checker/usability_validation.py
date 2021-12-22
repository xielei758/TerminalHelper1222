## import python dependencies
import os
from glob import glob
import subprocess

import psutil
import threading
import platform

from threading import Timer
from datetime import datetime
from datetime import timedelta

import time
from time import time, sleep, strftime

## import PyQt5 dependencies
# from PyQt5 import QtCore
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *


class UsabilityValidation(threading.Thread):
    ## may need to send back the result as Qt signal, in which case switching to PyQt is needed.

    def __init__(self):
        super().__init__()

        self.service1_status = None
        self.service2_status = None
        self.service3_status = None
        pass

    def run(self) -> bool:
        self.service1_status = self.service_checker('www.bupt.edu.cn')
        self.service2_status = self.service_checker('www.bjtu.edu.cn')
        self.service3_status = self.service_checker('www.tsinghua.edu.cn')

    def service_checker(self, target_service_add):

        host = target_service_add

        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        
        if the target address responds to ping, then returns True
        otherwise, returns False
        """

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower() == 'windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '1', host]

        return subprocess.call(command) == 0
        # pass

#
# if __name__ == '__main__':
#     ub_valid = UsabilityValidation()
#     ub_valid.start()
#
#     # test = ub_valid.service_checker('www.bjtu.edu.cn')
#     pass
