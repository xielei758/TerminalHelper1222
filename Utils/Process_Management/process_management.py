## import python dependencies
import os
from glob import glob
import subprocess

import psutil
import threading
import platform
import signal

from threading import Timer
from datetime import datetime
from datetime import timedelta

import time
from time import time, sleep, strftime

## import PyQt5 dependencies
# from PyQt5 import QtCore
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *


class ProcessManagement(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        while True:
            self.get_process_list()
            ## the arg is in seconds
            sleep(float(5))
        pass

    def get_process_list(self):
        '''
        this sub function delivers the currently running process.
        the reason why we split a standalone function is that we do not want external commands to
        have any inference with the constant report process.

        in actual application, if a light resource consumption is needed, the source of process list
        can be mapped to the constant report process.
        :return: a list of process.
        '''

        ## filter for some system process
        wink = ['SYSTEM', 'SYSTEMIDLEPROCESS', 'SMSS.EXE',
                'CSRSS.EXE', 'WININIT.EXE', 'WINLOGON.EXE', 'SERVICES.EXE',
                'LSASS.EXE', 'SVCHOST.EXE', 'DWM.EXE', 'MEMORYCOMPRESSION',
                'TASKHOSTW.EXE', 'RUNTIMEBROKER.EXE', 'EXPLORER.EXE', 'SHELLEXPERIENCEHOST.EXE',
                'APPLICATIONFRAMEHOST.EXE', 'SYSTEMSETTINGS.EXE', 'WMIPRVSE.EXE', 'PLUGIN_HOST.EXE',
                'SPOOLSV.EXE', 'DASHOST.EXE', 'SIHOST.EXE', 'CONHOST.EXE', 'DLLHOST.EXE', 'TASKLIST.EXE',
                'NVCONTAINER.EXE', 'SEARCHUI.EXE', 'REGISTRY', 'FONTDRVHOST.EXE', 'IGFXCUISERVICE.EXE',
                'NVTELEMETRYCONTAINER.EXE', 'SECURITYHEALTHSERVICE.EXE', 'PRESENTATIONFONTCACHE.EXE',
                'SEARCHINDEXER.EXE', 'IGFXEM.EXE', 'IGFXHK.EXE', 'CTFMON.EXE', 'SMARTSCREEN.EXE', 'CTFMON.EXE',
                'SETTINGSYNCHOST.EXE', 'WINDOWSINTERNAL.COMPOSABLESHELL.EXPERIENCES.TEXTINPUT.INPUTAPP.EXE',
                'CHSIME.EXE', 'AUDIODG.EXE', 'USYSDIAG.EXE', 'SEARCHPROTOCOLHOST.EXE', 'SEARCHFILTERHOST.EXE']

        ps = ['SFTP-SERVER', 'LOGIN', 'NM-DISPATCHER', 'IRQBALANCE', 'QMGR', 'WPA_SUPPLICANT',
              'LVMETAD', 'AUDITD', 'MASTER', 'DBUS-DAEMON', 'TAPDISK', 'SSHD', 'INIT', 'KSOFTIRQD',
              'KWORKER', 'KMPATHD', 'KMPATH_HANDLERD', 'PYTHON', 'KDMFLUSH', 'BIOSET', 'CROND', 'KTHREADD',
              'MIGRATION', 'RCU_SCHED', 'KJOURNALD', 'IPTABLES', 'SYSTEMD', 'NETWORK', 'DHCLIENT',
              'SYSTEMD-JOURNALD', 'NETWORKMANAGER', 'SYSTEMD-LOGIND', 'SYSTEMD-UDEVD', 'POLKITD', 'TUNED', 'RSYSLOGD',
              'BASH', 'YDSERVICE', 'SYSTEMD']

        Pids = psutil.pids()
        processList = []
        for pid in Pids:
            try:
                tmp = {}
                # 进程列表表单内容
                p = psutil.Process(pid)
                tmp['name'] = p.name()  # 进程名称
                if platform.system().upper() == 'WINDOWS':
                    if tmp['name'].upper().replace(' ', '') in wink:
                        continue
                else:
                    if tmp['name'].upper() in ps:
                        continue
                tmp['pid'] = pid
                tmp['user'] = os.path.split(p.username())[1]  # 执行用户
                tmp['status'] = p.status()
                tmp['cpu_percent'] = str(round(p.cpu_percent(), 3)) + '%'
                tmp['memory_percent'] = str(round(p.memory_percent(), 3)) + '%'  # 进程占用的内存比例
                processList.append(tmp)
                del p, tmp
            except:
                continue
        processList = sorted(processList, key = lambda x: x['cpu_percent'], reverse = True)

        ## returned variable is a dict
        self.process_list = processList
        print('the length of process list is', len(processList))
        # print(self.process_list[120])

        pass

    def terminate_process_by_pid(self, target_pid):
        '''
        takes target pid and terminate the corresponding terminal in the system environment.
        :param target_pid:
        :return:
        '''
        target_pid = int(target_pid)
        try:
            os.kill(target_pid, signal.SIGKILL)
            print('process with PID', target_pid, 'has been killed. ')
        except ProcessLookupError:
            print('the target process with PID', target_pid, 'does not exist in this environment. ')
        pass


# if __name__ == '__main__':
#     psm = ProcessManagement()
#     psm.start()
#     psm.terminate_process_by_pid('9709')
#     pass