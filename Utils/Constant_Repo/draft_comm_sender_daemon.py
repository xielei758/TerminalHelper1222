## import python dependencies
import copy
import os
from glob import glob
import subprocess
from time import sleep, perf_counter
import psutil
import threading
import subprocess
from threading import Timer
from datetime import timedelta, datetime
from time import time, sleep, strftime
import platform
import json
import re
import socket
import copy
import signal

## some dependencies that may not be necessary.
import zipfile
import random
from psutil import NoSuchProcess
from socket import gaierror


## import PyQt5 dependencies
# from PyQt5 import QtCore
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *


class SystemInspect(threading.Thread):
    ## reserve the signals here.
    # CPU_signal_1 = QtCore.pyqtSignal(int)

    def __init__(self, ins_flag = True, ins_freq = 600, strict_mode = False):
        super().__init__()

        self.ins_flag = ins_flag

        ## ins_freq should be in ms
        self.ins_freq = ins_freq / 1000

        ## some vars for the inner use
        self.CPU_perc_arc = float(0.2)
        self.bytes_sent_arc = int(0)
        self.bytes_recv_arc = int(0)

        ## initiate the socket
        ## since it is in LAN, the socket is set to use UDP
        # self.ul = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # ## switch to TCP
        # self.ul = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.recv_addr = ('127.0.0.1', 8999)
        # self.ul.connect(self.recv_addr)
        # # self.recv_addr = ('service.local', 8999)

        ## this var should be defined by the server's configure.
        self.blacklist_process = ['firefox']

        ## allow the user to alter the report content
        self.strict_mode = strict_mode
        self.report_item_setter()

    def run(self) -> None:

        ## workflow of this module here should be
        ## first it runs the inspection sequentially to ensure that all the variables are inited
        ## then the TCP connection should be established, so that the receiving and sending information is possible
        ## then the inspection should be run under parallel mode, to ensure performance
        ## load the configuration from the server, and start the reporting process here.

        self._first_run_inspection()
        self._establish_connection()

        ## start the inspection daemon in a sub-threading
        ## avoid threading block here
        self.__parallel_inspection_daemon = threading.Thread(target = self.__parallel_inspection_caller, daemon = True)
        self.__parallel_inspection_daemon.start()
        # self.__parallel_inspection_caller()

        self.__into_sender_daemon = threading.Thread(target = self.__info_sender_caller, daemon = True)
        self.__into_sender_daemon.start()

        # while True:
        #     self.process_check()
        #     self.network_comm_check()
        #     sleep(self.ins_freq)
        # self.__info_sender_caller()

        # self.timer = threading.Timer(self.ins_freq, self._parallel_inspection)
        # self.timer.start()

        # while True:
        #     self.inspection_caller()
        #     sleep(float(self.ins_freq))

    def __del__(self):
        self.ul.close()
        print('killed daemon')
        pass

    def timerEvent(self, QTimerEvent):
        pass

    def _first_run_inspection(self):

        Pids = psutil.pids()
        self.process_list_out = []
        self.network_list_out = []
        self.p_list = []
        for pid in Pids:
            try:
                p = psutil.Process(pid)
                p.cpu_percent()
                self.p_list.append(p)
            except NoSuchProcess:
                pass

        self.CPU_monitor()
        self.phy_memory_monitor()
        self.swap_memory_monitor()
        self.storage_monitor()
        self.network_monitor()
        self.process_check()
        self.network_comm_check()
        self.network_property()
        # self.packages_check()
        self.packages_num_check_lite()
        pass

    def _establish_connection(self):
        try:
            print('estimating to establish the connection')
            ## code for establishing the connection
        except Exception as err_msg:
            print('connection to servers failed to be established due to', err_msg)
        pass

    def _setting_applier(self):
        ## make sure the self.setting_json is not void
        load_json = json.loads(self.setting_json[0].decode('utf-8'))

        ## after decoding this json, read corresponding content and thus make adjustment here.
        pass

    def __parallel_inspection_caller(self):
        while True:
            self._parallel_inspection()
            sleep(float(self.ins_freq))
        pass

    def _parallel_inspection(self):
        # print('parallel activated')
        cpu_monitor_call = threading.Thread(target = self.CPU_monitor)
        cpu_monitor_call.start()

        phy_memory_monitor_call = threading.Thread(target = self.phy_memory_monitor)
        phy_memory_monitor_call.start()

        swap_memory_monitor_call = threading.Thread(target = self.swap_memory_monitor)
        swap_memory_monitor_call.start()

        storage_monitor_call = threading.Thread(target = self.storage_monitor)
        storage_monitor_call.start()

        network_monitor_call = threading.Thread(target = self.network_monitor)
        network_monitor_call.start()

        process_monitor_call = threading.Thread(target = self.process_check)
        process_monitor_call.start()

        network_flow_monitor_call = threading.Thread(target = self.network_comm_check)
        network_flow_monitor_call.start()

        network_property_monitor_call = threading.Thread(target = self.network_property)
        network_property_monitor_call.start()

        # packages_monitor_call = threading.Thread(target = self.packages_check)
        # packages_monitor_call.start()

        packages_monitor_call_lite = threading.Thread(target = self.packages_num_check_lite)
        packages_monitor_call_lite.start()
        pass

    def __info_sender_caller(self):
        print('info sender')
        pass

    def inspection_caller(self):
        ## add the sub functions here
        self.CPU_monitor()
        self.phy_memory_monitor()
        self.swap_memory_monitor()
        self.storage_monitor()
        self.network_monitor()
        self.process_check()
        self.network_comm_check()
        self.network_property()
        # self.packages_check()
        self.packages_num_check_lite()

        # sub_proc_ins = threading.Thread(target = self.sub_proc_inspection_caller)
        # sub_proc_ins.start()
        # sub_proc_ins.join()

        ## to decide if the information needs to be uploaded
        if self.ins_flag == True:
            self.report_info_basic()
            sleep(1)
            ## add this sleep function to avoid the receiver mistakes two sequential messages as one
            self.report_info_process()
            sleep(1)
            self.report_info_network()
        pass

    def report_info_basic(self):
        ## wrapping those information into a dict
        ## then convert it to a json string.

        packed_upload_msg = {}
        # packed_upload_msg['type'] = str('client_report_basic')
        packed_upload_msg['type'] = str('report_basic')
        packed_upload_msg['send_timestamp'] = str(datetime.fromtimestamp(time())).split('.')[0]

        upload_msg = {}
        ## used to identity the client's working status
        ## cannot be masked.
        upload_msg['Clt_IP'] = self.ip_addr
        upload_msg['Clt_Conf_DNS'] = self.dns
        upload_msg['Clt_Gateway'] = self.gateway

        # ## process list
        # upload_msg['Process_List'] = self.process_list
        # ## network list
        # upload_msg['Network_List'] = self.network_comm_list

        ## cpu information
        upload_msg['CPU_Model'] = self.CPU_model_full
        upload_msg['CPU_Perc'] = self.CPU_perc
        upload_msg['CPU_Perc_Core'] = self.CPU_perc_core
        upload_msg['CPU_Freq_Cur'] = self.CPU_freq_cur
        upload_msg['CPU_Freq_Min'] = self.CPU_freq_min
        upload_msg['CPU_Freq_Max'] = self.CPU_freq_max

        ## load information
        upload_msg['Load_Info'] = self.load_info
        upload_msg['Load_1_Min'] = self.load_1_min
        upload_msg['Load_5_Min'] = self.load_5_min
        upload_msg['Load_15_Min'] = self.load_15_min

        ## the operating time since last boot up
        upload_msg['Uptime_Gen'] = self.up_time

        ## physical memory
        upload_msg['Phy_Mem_Total'] = self.phy_mem_total
        upload_msg['Phy_Mem_Avil'] = self.phy_mem_avail
        upload_msg['Phy_Mem_Perc'] = self.phy_mem_perc
        upload_msg['Phy_Mem_Used'] = self.phy_mem_used
        upload_msg['Phy_Mem_Free'] = self.phy_mem_free

        ## swap memory
        upload_msg['Swap_Mem_Total'] = self.swap_mem_total
        upload_msg['Swap_Mem_Perc'] = self.swap_mem_perc

        ## information about the IO status
        upload_msg['Stor_Total'] = self.sto_info_total
        upload_msg['Stor_Used'] = self.sto_info_used
        upload_msg['Stor_Perc'] = self.sto_info_perc

        ## packages through the network adapter
        upload_msg['Net_Outflow_Sum'] = self.outcome_flow
        upload_msg['Net_Inflow_Sum'] = self.income_flow
        upload_msg['Net_Outflow_Spd'] = self.uplink_spd
        upload_msg['Net_Inflow_Spd'] = self.downlink_spd

        if self.strict_mode is False:
            if not self.repo_CPU_flag:
                for key in upload_msg.keys():
                    if key.startswith('CPU'):
                        upload_msg[key] = 'Masked'

            # if not self.repo_process_list_flag:
            #     # for key in upload_msg.keys():
            #     #     if key.startswith('Process_List'):
            #     upload_msg['Process_List'] = 'Masked'
            #
            # if not self.repo_network_list_flag:
            #     # for key in upload_msg.keys():
            #     #     if key.startswith('Network_List'):
            #     upload_msg['Network_List'] = 'Masked'

            if not self.repo_storage_flag:
                for key in upload_msg.keys():
                    if key.startswith('Stor'):
                        upload_msg[key] = 'Masked'

            if not self.repo_network_adapter_flag:
                for key in upload_msg.keys():
                    if key.startswith('Net_'):
                        upload_msg[key] = 'Masked'

            if not self.repo_phy_memory_flag:
                for key in upload_msg.keys():
                    if key.startswith('Phy_Mem'):
                        upload_msg[key] = 'Masked'

            if not self.repo_swap_memory_flag:
                for key in upload_msg.keys():
                    if key.startswith('Swap_Mem'):
                        upload_msg[key] = 'Masked'

            if not self.repo_sys_load_flag:
                for key in upload_msg.keys():
                    if key.startswith('Load_'):
                        upload_msg[key] = 'Masked'

            if not self.repo_boot_time_flag:
                # for key in upload_msg.keys():
                #     if key.startswith('Uptime_Gen'):
                upload_msg['Uptime_Gen'] = 'Masked'

        ## enclose the above content to the dict with necessary information.
        packed_upload_msg['msg_body'] = [upload_msg]

        self.upload_json = json.dumps(packed_upload_msg, sort_keys = False)

        # self.ul.sendto(self.upload_json.encode('utf-8'), self.recv_addr)
        self.ul.sendall(self.upload_json.encode('utf-8'))
        ## the close function should obviously be put to the del function.
        # self.ul.close()

        ## TODO(Leon): exist a problem of packages being potentially truncated thus need further process

        pass

    def report_info_process(self):
        ## wrapping those information into a dict
        ## then convert it to a json string.

        ## this function is to set considering the length limitation of json.

        packed_upload_msg = {}
        # packed_upload_msg['type'] = str('client_report_process')
        packed_upload_msg['type'] = str('report_process')
        packed_upload_msg['send_timestamp'] = str(datetime.fromtimestamp(time())).split('.')[0]

        upload_msg = {}
        ## used to identity the client's working status
        ## cannot be masked.
        upload_msg['Clt_IP'] = self.ip_addr
        # upload_msg['Clt_Conf_DNS'] = self.dns
        # upload_msg['Clt_Gateway'] = self.gateway

        ## process list
        upload_msg['Process_List'] = self.process_list

        if self.strict_mode is False:

            if not self.repo_process_list_flag:
                # for key in upload_msg.keys():
                #     if key.startswith('Process_List'):
                upload_msg['Process_List'] = 'Masked'

        ## enclose the above content to the dict with necessary information.
        packed_upload_msg['msg_body'] = [upload_msg]

        self.upload_json = json.dumps(packed_upload_msg, sort_keys = False)

        # self.ul.sendto(self.upload_json.encode('utf-8'), self.recv_addr)
        self.ul.sendall(self.upload_json.encode('utf-8'))
        ## the close function should obviously be put to the del function.
        # self.ul.close()

        pass

    def report_info_network(self):
        ## wrapping those information into a dict
        ## then convert it to a json string.

        ## this function is to set considering the length limitation of json.

        packed_upload_msg = {}
        # packed_upload_msg['type'] = str('client_report_network')
        packed_upload_msg['type'] = str('report_network')
        packed_upload_msg['send_timestamp'] = str(datetime.fromtimestamp(time())).split('.')[0]

        upload_msg = {}
        ## used to identity the client's working status
        ## cannot be masked.
        upload_msg['Clt_IP'] = self.ip_addr
        # upload_msg['Clt_Conf_DNS'] = self.dns
        # upload_msg['Clt_Gateway'] = self.gateway

        ## network list
        upload_msg['Network_List'] = self.network_comm_list

        if self.strict_mode is False:
            if not self.repo_network_list_flag:
                # for key in upload_msg.keys():
                #     if key.startswith('Network_List'):
                upload_msg['Network_List'] = 'Masked'

        ## enclose the above content to the dict with necessary information.
        packed_upload_msg['msg_body'] = [upload_msg]

        self.upload_json = json.dumps(packed_upload_msg, sort_keys = False)

        # self.ul.sendto(self.upload_json.encode('utf-8'), self.recv_addr)
        self.ul.sendall(self.upload_json.encode('utf-8'))
        ## the close function should obviously be put to the del function.
        # self.ul.close()

        pass

    def report_item_setter(self):
        self.repo_CPU_flag = True
        self.repo_process_list_flag = True
        self.repo_network_list_flag = True
        self.repo_storage_flag = True
        self.repo_network_adapter_flag = True
        self.repo_phy_memory_flag = True
        self.repo_swap_memory_flag = True
        self.repo_sys_load_flag = True
        self.repo_boot_time_flag = True
        pass

    def CPU_monitor(self):
        ## CPU count
        if hasattr(psutil, 'cpu_count'):
            self.CPU_count_logical = int(psutil.cpu_count())
            self.CPU_count_physical = int(psutil.cpu_count(logical = False))
        else:
            self.CPU_count_logical = int(0)
            self.CPU_count_physical = int(0)

        # print('the flag in the module', self.repo_CPU_flag)
        if self.strict_mode is False:
            if not self.repo_CPU_flag:
                print('cpu masked', self.strict_mode)

        ## CPU model name
        ## zan4 shi2 bu2 dui4 dan1 ge4 de0 CPU he2 xin1 jin4 xing2 chu4 li3
        ## the implementation through a custom function is not that emm
        # cpu_info = self._CPU_info_fetcher()
        # self.CPU_model_full = cpu_info['proc0']['model name']
        try:
            CPU_model_raw = open('/proc/cpuinfo', 'r').readlines()[4]
            if CPU_model_raw.startswith('model name'):
                self.CPU_model_full = CPU_model_raw.split(':')[1].strip()
            else:
                self.CPU_model_full = 'General ARM CPU'
        except:
            self.CPU_model_full = 'General CPU'

        if self.CPU_model_full.endswith('GHz'):
            self.CPU_model_full = self.CPU_model_full[:-10]

        ## system load information (alike to top)
        if hasattr(psutil, 'getloadavg'):
            self.load_info = [round(x / self.CPU_count_logical * 100, 2) for x in psutil.getloadavg()]
            self.load_1_min = self.load_info[0]
            self.load_5_min = self.load_info[1]
            self.load_15_min = self.load_info[2]
        else:
            self.load_info = str('na')
            self.load_1_min = int(0)
            self.load_5_min = int(0)
            self.load_15_min = int(0)
        ## 1 min, 5 min, 15 min, in percentage.

        ## CPU percentage
        CPU_perc = round(psutil.cpu_percent(interval = 1, percpu = False) / 100, 4)

        if CPU_perc != 0:
            self.CPU_perc = CPU_perc
            self.CPU_perc_arc = self.CPU_perc
        else:
            self.CPU_perc = self.CPU_perc_arc

        self.CPU_perc_core = psutil.cpu_percent(interval = 0.7, percpu = True)

        ## for testing the timer
        # print('the current 1 min load is', self.load_1_min, '%')
        # print('the current CPU load is', self.CPU_perc, '%')

        ## CPU frequency
        ## we want to make sure that the frequency is displayed in MHz.
        if (hasattr(psutil, 'cpu_freq')) & (psutil.cpu_freq() is not None):
            cpu_freq = psutil.cpu_freq()
            if hasattr(cpu_freq, 'current'):
                freq_cur = float(cpu_freq.current)
                self.CPU_freq_cur = round(freq_cur * (1 if freq_cur > 10 else 1000))
            else:
                freq_cur = int(0)
                self.CPU_freq_cur = str('na')
            if hasattr(cpu_freq, 'min'):
                freq_min = float(psutil.cpu_freq().min)
                self.CPU_freq_min = round(freq_min * (1 if freq_cur > 10 else 1000))
            else:
                self.CPU_freq_min = str('na')
            if hasattr(cpu_freq, 'max'):
                freq_max = float(psutil.cpu_freq().max)
                self.CPU_freq_max = round(freq_max * (1 if freq_cur > 10 else 1000))
            else:
                self.CPU_freq_max = str('na')
        else:
            self.CPU_freq_cur, self.CPU_freq_min, self.CPU_freq_max = float(0), float(0), float(0)

        ## up time
        # self.up_time = str(timedelta(seconds = round(time() - psutil.boot_time(), 0)))[:-3].\
        #     replace(" days,", "d").replace(" day", "d")
        if hasattr(psutil, 'boot_time'):
            self.up_time = str(timedelta(seconds = round(time() - psutil.boot_time(),
                                                         0)))[:-3].replace(":", " hours, ") + " mins"
        else:
            self.up_time = str('na')

        # print(self.up_time)

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
        # for item in self.up_time.split(', '):
        #     print(type(item))
        #     print(item.split())
        # pass

    def operating_elapsed_time(self):
        ## lite monitor for cpu percentage
        CPU_perc = round(psutil.cpu_percent(interval = 1, percpu = False) / 100, 4)

        if CPU_perc != 0:
            self.CPU_perc = CPU_perc
            self.CPU_perc_arc = self.CPU_perc
        else:
            self.CPU_perc = self.CPU_perc_arc

        ## up time
        # self.up_time = str(timedelta(seconds = round(time() - psutil.boot_time(), 0)))[:-3].\
        #     replace(" days,", "d").replace(" day", "d")
        if hasattr(psutil, 'boot_time'):
            self.up_time = str(timedelta(seconds = round(time() - psutil.boot_time(),
                                                         0)))[:-3].replace(":", " hours, ") + " mins"
        else:
            self.up_time = str('na')

        # print(self.up_time)

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

    def CPU_load_monitor_lite(self):
        ## added a lite monitor function for the usage of performance monitor refresh
        CPU_perc = round(psutil.cpu_percent(interval = 1, percpu = False) / 100, 4)

        if CPU_perc != 0:
            self.CPU_perc = CPU_perc
            self.CPU_perc_arc = self.CPU_perc
        else:
            self.CPU_perc = self.CPU_perc_arc

    def phy_memory_monitor(self):
        ## examine the physical memory

        ## not sure if some ARM based system can provide with this API so
        ## we would first check if this attribute is available
        if hasattr(psutil, 'virtual_memory'):
            phy_mem = psutil.virtual_memory()
            ## total available percent used
            ## the percent refers to the actual occupied space, while available means the space can be invoked by apps
            ## though it may be currently in use.

            ## presented in GiB.
            self.phy_mem_total = round(int(phy_mem.total) / 1073741824, 2)
            self.phy_mem_avail = round(int(phy_mem.available) / 1073741824, 2)  ## ke3 diao4 yong4 de0 nei4 cun2
            # self.phy_mem_perc = phy_mem.percent
            self.phy_mem_used = round(int(phy_mem.used) / 1073741824, 2)
            self.phy_mem_free = round(int(phy_mem.free) / 1073741824, 2)  ## wu4 li3 kong4 xian2 de0 nei4 cun2

            if hasattr(phy_mem, 'percent'):
                self.phy_mem_perc = round(phy_mem.percent / 100, 4)
            else:
                self.phy_mem_perc = round(1 - self.phy_mem_avail / self.phy_mem_total, 4)

            ## to avoid confusion, the free memory can be considered not presented to UI
        else:
            self.phy_mem_total = str('na')
            self.phy_mem_avail = str('na')
            self.phy_mem_used = str('na')
            self.phy_mem_free = str('na')
            self.phy_mem_perc = str('na')
            # pass

    def mem_load_monitor_lite(self):
        if hasattr(psutil, 'virtual_memory'):
            phy_mem = psutil.virtual_memory()
            if hasattr(phy_mem, 'percent'):
                self.phy_mem_perc = round(phy_mem.percent / 100, 4)
            else:
                self.phy_mem_total = round(int(phy_mem.total) / 1073741824, 2)
                self.phy_mem_avail = round(int(phy_mem.available) / 1073741824, 2)
                self.phy_mem_perc = round(1 - self.phy_mem_avail / self.phy_mem_total, 4)
        pass

    def mem_virtual_load_monitor_lite(self):
        if hasattr(psutil, 'swap_memory'):
            swap_mem = psutil.swap_memory()
            if hasattr(swap_mem, 'percent'):
                self.swap_mem_perc = round(swap_mem.percent / 100, 4)
            else:
                self.swap_mem_total = round(int(swap_mem.total) / 1073741824, 2)
                self.swap_mem_used = round(int(swap_mem.used) / 1073741824, 2)
                self.swap_mem_perc = round(self.swap_mem_used / self.swap_mem_total, 4)
        pass

    def swap_memory_monitor(self):
        ## swap memory
        ## swap memory should be documented to disk information
        if hasattr(psutil, 'swap_memory'):
            swap_mem = psutil.swap_memory()
            self.swap_mem_total = round(int(swap_mem.total) / 1073741824, 2)
            self.swap_mem_used = round(int(swap_mem.used) / 1073741824, 2)
            self.swap_mem_free = round(int(swap_mem.free) / 1073741824, 2)

            if hasattr(swap_mem, 'percent'):
                self.swap_mem_perc = round(swap_mem.percent / 100, 4)
            else:
                self.swap_mem_perc = round(self.swap_mem_used / self.swap_mem_total, 4)
        else:
            self.swap_mem_total = int(0)
            self.swap_mem_used = int(0)
            self.swap_mem_free = int(0)
            self.swap_mem_perc = int(0)
            # pass

    def storage_monitor(self):
        sto_info = psutil.disk_usage('/')
        self.sto_info_total = round(int(sto_info.total) / 1073741824, 2)
        self.sto_info_used = round(int(sto_info.used) / 1073741824, 2)
        self.sto_info_free = round(int(sto_info.free) / 1073741824, 2)
        if hasattr(sto_info, 'percent'):
            self.sto_info_perc = round(sto_info.percent / 100, 4)
        else:
            self.sto_info_perc = round(self.sto_info_used / self.sto_info_total, 4)

        ## we then invoke the API for IO status.
        ## this var counts for the IO activity since the system installation
        ## thus if there has been any system re-installation, the reported value might be inaccurate.
        ## presented in GiB
        if hasattr(psutil, 'disk_io_counters'):
            io_info = psutil.disk_io_counters(perdisk = False)
            self.io_info_read_count = round(int(io_info.read_bytes) / 1073741824, 2)
            self.io_info_write_count = round(int(io_info.write_bytes) / 1073741824, 2)
        else:
            self.io_info_read_count = int(0)
            self.io_info_write_count = int(0)

    def network_monitor(self):
        ## the four variables are the target here in this sub function
        # self.outcome_flow = int('0')
        # self.income_flow = int('0')
        # self.uplink_spd = int(0)
        # self.downlink_spd = int(0)
        if not hasattr(self, 'net_time_arc'):
            ## which means this script is running for the first time so no history information here
            self.net_time_arc = time()
            current_traffic_info = psutil.net_io_counters()
            self.bytes_sent_arc = current_traffic_info.bytes_sent
            self.bytes_recv_arc = current_traffic_info.bytes_recv
            self.outcome_flow = round(int(self.bytes_sent_arc) / 1073741824, 2)
            self.income_flow = round(int(self.bytes_recv_arc) / 1073741824, 2)
            self.uplink_spd = 0
            self.downlink_spd = 0
        else:
            ## which means that there are history records to calculate the netflow speed.
            net_time_now = time()
            # print('elapsed time since the last check:', net_time_now - self.net_time_arc)
            current_traffic_info = psutil.net_io_counters()
            bytes_sent = current_traffic_info.bytes_sent
            bytes_recv = current_traffic_info.bytes_recv
            self.uplink_spd = round(((bytes_sent - self.bytes_sent_arc) / (net_time_now - self.net_time_arc))
                                    / 1048576, 3)
            self.downlink_spd = round(((bytes_recv - self.bytes_recv_arc) / (net_time_now - self.net_time_arc))
                                      / 1048576, 3)
            ## in MiB/s
            self.bytes_sent_arc = bytes_sent
            self.bytes_recv_arc = bytes_recv
            self.outcome_flow = round(int(self.bytes_sent_arc) / 1073741824, 3)
            self.income_flow = round(int(self.bytes_recv_arc) / 1073741824, 3)
            self.net_time_arc = net_time_now
            # print('self.uplink_spd', self.uplink_spd)
            # print('self.downlink_spd', self.downlink_spd)
        pass

    def process_check(self):
        # start = perf_counter()

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
              'SYSTEMD-JOURNALD', 'NETWORKMANAGER', 'SYSTEMD-LOGIND', 'SYSTEMD-UDEVD', 'POLKITD', 'TUNED',
              'RSYSLOGD',
              'BASH', 'YDSERVICE', 'SYSTEMD']

        processList = []
        Pids = psutil.pids()
        for pid in Pids:
            try:
                p = psutil.Process(pid)
                if p not in self.p_list:
                    self.p_list.append(p)
            except NoSuchProcess:
                continue
                # print('the process list is appending', err_msg)
        for p in self.p_list:
            try:
                tmp = {}
                # 进程列表表单内容
                tmp['name'] = p.name()  # 进程名称
                ## actual application does not involve windows
                ## so the following line can be skipped.
                if platform.system().upper() == 'WINDOWS':
                    if tmp['name'].upper().replace(' ', '') in wink:
                        continue
                else:
                    if tmp['name'].upper() in ps:
                        continue

                tmp['pid'] = p.pid

                tmp['user'] = os.path.split(p.username())[1]  # 执行用户
                tmp['status'] = p.status()
                cpu = p.cpu_percent()
                tmp['cpu'] = str(round(cpu, 3)) + '%'
                tmp['mem'] = str(round(p.memory_percent(), 3)) + '%'  # 进程占用的内存比例
                processList.append(tmp)
                self.banned_software_screen(p.name(), p.pid)
                del p, tmp
            except:
                continue
        processList = sorted(processList, key = lambda x: x['mem'], reverse = False)

        self.process_list = processList

        self.process_list_out.clear()
        ## returned variable is a dict
        for i in range(len(processList)):
            list_temp = [processList[i]['name'], processList[i]['pid'], processList[i]['user'],
                         processList[i]['status'], processList[i]['cpu'], processList[i]['mem']]
            self.process_list_out.append(list_temp)

        # print('the length of process list is', len(self.process_list_out))

        processList.clear()

        # elapsed = (perf_counter() - start)
        # print("proc time used:", elapsed)
        pass

    def network_comm_check(self):
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

        netkey = {
            'SYN_SENT': '请求',
            'LISTEN': '监听',
            'ESTABLISHED': '已建立',
            'NONE': '未知',
            'CLOSE_WAIT': '中断',
            'LAST_ACK': '等待关闭'
        }

        netstats = psutil.net_connections()
        networkList = []
        # self.network_list_out = [[0] * 6 for i in range(len(netstats) + 1)]
        for netstat in netstats:
            try:
                if (netstat.pid == 0) or not netstat.pid:
                    continue
                tmp = {}
                # 进程网络连接列表表单内容
                p = psutil.Process(netstat.pid)
                tmp_name = p.name()
                # 根据系统平台的不同，过滤系统进程
                if platform.system().upper() == 'WINDOWS':
                    if tmp_name.upper().replace(' ', '') in wink:
                        continue
                else:
                    if tmp_name.upper() in ps:
                        continue
                tmp['process'] = tmp_name
                tmp['pid'] = netstat.pid
                tmp['type'] = ('tcp' if netstat.type == 1 else 'udp')
                tmp['laddr'] = netstat.laddr.ip
                tmp['raddr'] = netstat.raddr.ip or 'None'
                # tmp['status'] = netstat.status
                ## adding chinese in the json packages can cause the message to be over long.
                tmp['status'] = netkey.get(netstat.status, netstat.status)
                networkList.append(tmp)
                del p, tmp
            except:
                continue
        networkList = sorted(networkList, key = lambda x: x['pid'], reverse = False)

        self.network_comm_list = networkList

        ## the returned thing is also a dict
        self.network_list_out.clear()

        for i in range(len(networkList)):
            list_temp = [networkList[i]['process'], networkList[i]['pid'], networkList[i]['type'],
                         networkList[i]['status'], networkList[i]['laddr'], networkList[i]['raddr']]
            self.network_list_out.append(list_temp)
        # print("len of net work:", len(self.network_list_out))
        # print(self.network_list_out)
        networkList.clear()

        pass

    def network_property(self):

        gateway_raw = str(subprocess.Popen('ip r | grep ^def', shell = True,
                                           stdout = subprocess.PIPE).communicate()[0], 'utf8')

        try:
            gateway = re.findall(r'[0-9]+(?:\.[0-9]+){3}', gateway_raw)[0]
        except IndexError:
            if len(gateway_raw) == 0:
                gateway = str('unconnected')
            else:
                gateway = str('unsupported')

        def dns_fetching_caller():
            raw_output = subprocess.Popen('echo $XDG_CURRENT_DESKTOP', shell = True,
                                          stdout = subprocess.PIPE).communicate()[0]
            de_output = str(raw_output, 'utf-8')

            if 'Deepin' in de_output:
                dns_raw = dns_fetching_non_service()
            else:
                dns_raw = dns_fetching_normal()

            try:
                dns_info = re.findall(r'[0-9]+(?:\.[0-9]+){3}', dns_raw)[0]
            except IndexError:
                if len(dns_raw) == 0:
                    dns_info = str('unconnected')
                else:
                    dns_info = str('unsupported')

            return dns_info

        def dns_fetching_normal():
            dns_raw = str(subprocess.Popen('systemd-resolve --status | grep "Current DNS"', shell = True,
                                           stdout = subprocess.PIPE).communicate()[0], 'utf8')

            if len(dns_raw) <= 1:
                dns_raw = str(subprocess.Popen('systemd-resolve --status | grep "DNS Servers"', shell = True,
                                               stdout = subprocess.PIPE).communicate()[0], 'utf8')

            return dns_raw

        def dns_fetching_non_service():
            dns_raw = str(subprocess.Popen('cat /etc/resolv.conf | grep nameserver', shell = True,
                                           stdout = subprocess.PIPE).communicate()[0], 'utf8')
            return dns_raw

        def access_local():
            host_name = socket.gethostname()
            try:
                IP = socket.gethostbyname(host_name + ".local")

                if IP.startswith('127.0'):
                    IP = get_ip()
            except gaierror:
                IP = get_ip()

            return IP

        def get_ip():
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # doesn't even have to be reachable
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            except Exception:
                try:
                    ip_raw = str(subprocess.Popen('ifconfig | grep "255.255.*.*"', shell = True,
                                                  stdout = subprocess.PIPE).communicate()[0], 'utf8')
                    IP = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ip_raw)[0]
                except:
                    IP = '127.0.0.1'
            finally:
                s.close()
            return IP

        dns_info = dns_fetching_caller()

        ip_addr = access_local()

        self.gateway = gateway
        self.dns = dns_info
        self.ip_addr = ip_addr
        # print(self.ip_addr)packages_num_check_lite
        pass

    def packages_num_check_lite(self):
        apt_count_raw = str(subprocess.Popen('dpkg --list | wc --lines', shell = True,
                                             stdout = subprocess.PIPE).communicate()[0], 'utf8')
        try:
            self.installed_pac_num = int(apt_count_raw)
        except ValueError as err_msg:
            print('the package checking number is not valid', err_msg)
        pass

    ## the following way of detecting the number of packages has been deprecated.
    def packages_check(self):
        # pac_list_raw = str(subprocess.Popen('apt-get list', shell = True,
        #                                 stdout = subprocess.PIPE).communicate()[0], 'utf8')
        import apt
        import numpy as np

        cache = apt.Cache()
        installed_pac_list = []
        upgradable_pac_list = []

        for pkg in cache:
            # a = str(pkg.versions[0])
            if pkg.is_installed:
                # print(pkg.name, pkg.versions[0])
                installed_pac_list.append([pkg.name, str(pkg.versions[0])])
                if pkg.is_upgradable:
                    upgradable_pac_list.append(pkg.name)

        # print(len(installed_pac_list))
        self.installed_pac_list = installed_pac_list
        self.upgradable_pac_list = upgradable_pac_list

        # self.arr_installed_pac = np.array(installed_pac_list)
        # self.test = self.arr_installed_pac[:, 0]

        ## making all the installed packages into a series
        self.installed_pac_name = np.array(installed_pac_list)[:, 0]
        ## setting the required packages
        self.required_pac = ['bash', 'firefox']
        self.remain_required_pac = copy.deepcopy(self.required_pac)

        for pac_iter in range(len(self.required_pac)):
            # print(pac_iter)
            # print(self.required_pac[pac_iter])
            cur_pac = self.required_pac[pac_iter]
            # print(cur_pac, cur_pac in self.installed_pac_name)
            if cur_pac in self.installed_pac_name:
                self.remain_required_pac.remove(cur_pac)

        if len(self.remain_required_pac) == 0:
            # print('all required dependencies have been installed. ')
            pass

        # if len(self.upgradable_pac_list) > 0:
        #     update_message_title = 'Updates Available. '
        #     update_message_content = '%d available updates detected in this environment. ' % len(
        #         self.upgradable_pac_list)
        #     subprocess.Popen(['notify-send', update_message_title, update_message_content])

        pass

    def banned_software_screen(self, proc_name, proc_pid):

        ## examine if there are multiple instances of a program

        if '/' in proc_name:
            proc_name = proc_name.split('/')[0]

        if proc_name in self.blacklist_process:
            os.kill(int(proc_pid), signal.SIGKILL)
            print('banned program', proc_name, 'been found and terminated. ')
            print('this event may be recorded. ')
            self.on_going_banned_software(proc_pid)
        # pass

    def on_going_banned_software(self, pid):
        print('additional operations on hold for', pid)
