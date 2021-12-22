## import python dependencies
import os
from glob import glob
import subprocess

import psutil
import threading
import re

from threading import Timer
from datetime import datetime
from datetime import timedelta

import time
from time import time, sleep, strftime

## import PyQt5 dependencies
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class NetworkSpeedTest(threading.Thread):
    ## the server and the client need to install iperf3: sudo apt install iperf3
    def __init__(self, parent_self):
        super().__init__()

        ## set the target address for testing
        self.parent = parent_self
        self.target_dir = self.parent.server_addr
        self.target_port = self.parent.server_port
        self.time_duration = self.parent.spd_test_duration

        self.mode = self.parent.test_mode

        ## pre allocating the variables.
        self.downlink_speed, self.downlink_jitter, self.downlink_loss_rate = 0, None, None
        self.uplink_speed, self.uplink_jitter, self.uplink_loss_rate = 0, None, None
        pass

    def run(self) -> None:
        # self.network_checker()
        self.latency_test()
        self.network_checker()
        pass

    def latency_test(self):
        raw_latency = str(subprocess.Popen('ping -c 1 %s | grep avg' % self.target_dir, shell = True,
                                           stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        if len(raw_latency) == 0:
            self.network_latency = 'failed'
        else:
            latency = raw_latency.split('=')[1].split('/')[1]
            self.network_latency = latency

        print('network latency', self.network_latency)

    def network_speedtest_workflow(self):

        ## after finishing the test, update elements on the UI
        ##
        ## call the caller function here.
        try:
            if self.mode == 'oneside':
                self.oneside_speed_test()
            else:
                self.bidirectional_speed_test()
        except Exception as err_msg:
            print('speed test error, due to', err_msg)
            self.parent.speed_test_error_GUI_handler()

        ## update the elements on the subtitle
        self.parent.util_network_speed_on_going_header.setText('网络测速结束')
        self.parent.util_network_speed_on_going_subheader.setText('关于您网络的性能表现已经呈现于本页面上，请您参考。')

        pass

    def oneside_speed_test(self):
        self.download_speed_test()

        self.parent.downspd_prompt_handler(self.downlink_speed)

        if int(self.downlink_speed) == 0:
            self.parent.util_network_speed_on_going_header.setText('测速服务繁忙')

            self.parent.util_network_speed_on_going_subheader.setText('您的网络与测速服务器之间通信正常，但测速服务器当前负载过大，暂时无法响应您的请求。')
            self.parent.util_network_speed_on_going_subheader.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                            'color: rgb(255,77,77);')
        self.parent.perf_mon_net_flow_charView.setVisible(False)
        pass

    def bidirectional_speed_test(self):
        self.download_speed_test_iperf3()

        ## after finishing the test, update elements on the UI
        self.parent.downspd_prompt_handler(self.downlink_speed)

        ## set the visibility of such elements related to uploading test
        self.parent.util_network_speed_on_going_upspd_prompt.setVisible(True)
        self.parent.util_network_speed_on_going_upspd_value.setVisible(True)
        self.parent.util_network_speed_on_going_upspd_tip.setVisible(True)
        # self.parent.util_network_speed_on_going_upspd_prompt.setVisible(True)
        # self.parent.util_network_speed_on_going_upspd_prompt.setVisible(True)
        # self.parent.util_network_speed_on_going_upspd_prompt.setVisible(True)

        self.upload_speed_test_iperf3()

        ## examine if the downlink and the uplink is nearly equal
        peered_thres = float(self.downlink_speed) * 0.2
        peered_status = abs(float(self.downlink_speed) - float(self.uplink_speed)) < peered_thres
        peered_flag = True if peered_status else False

        self.parent.upspd_prompt_handler(self.uplink_speed, peered_flag)

        ## add the reaction to the iperf server error, e.g., the latency test is ok, but test failed
        if int(self.uplink_speed) == 0 and int(self.downlink_speed) == 0:
            self.parent.util_network_speed_on_going_header.setText('测速服务繁忙')

            self.parent.util_network_speed_on_going_subheader.setText('您的网络与测速服务器之间通信正常，但测速服务器当前负载过大，暂时无法响应您的请求。')
            self.parent.util_network_speed_on_going_subheader.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                            'color: rgb(255,77,77);')
        self.parent.perf_mon_net_flow_charView.setVisible(False)
        pass

    def download_speed_test_iperf3(self):
        # print(self.target_dir, self.target_port)
        raw_downspd = str(subprocess.Popen('iperf3 -c %s -b 10g -t %s -i %s -p %s -f m -R'
                                           % (
                                               self.target_dir, self.time_duration, self.time_duration,
                                               self.target_port),
                                           shell = True,
                                           stdout = subprocess.PIPE).communicate()[0], 'utf-8')
        result_array = raw_downspd.split('\n')
        for item_var in result_array:
            if 'sender' in item_var:
                sender_line = item_var
            if 'receiver' in item_var:
                receiver_line = item_var

        try:
            receiver_arr = re.findall(r'\d+.?\d*', receiver_line)
            self.downlink_speed = receiver_arr[4]
        except UnboundLocalError as err_msg:
            self.downlink_speed = 0
            print('The download speed test failed. ', err_msg)
        # downlink_speed, downlink_jitter, downlink_loss_rate = receiver_arr[4], receiver_arr[5], receiver_arr[7]
        #
        # self.downlink_speed, self.downlink_jitter, self.downlink_loss_rate = downlink_speed, downlink_jitter, downlink_loss_rate
        print('download test done. ', self.downlink_speed)
        pass

    def upload_speed_test_iperf3(self):
        raw_upspd = str(subprocess.Popen('iperf3 -c %s -b 10g -t %s -i %s -p %s -f m'
                                         % (
                                             self.target_dir, self.time_duration, self.time_duration,
                                             self.target_port),
                                         shell = True,
                                         stdout = subprocess.PIPE).communicate()[0], 'utf-8')
        result_array = raw_upspd.split('\n')
        for item_var in result_array:
            if 'sender' in item_var:
                sender_line = item_var
            if 'receiver' in item_var:
                receiver_line = item_var

        try:
            sender_arr = re.findall(r'\d+.?\d*', sender_line)
            self.uplink_speed = sender_arr[4]
        except UnboundLocalError as err_msg:
            self.uplink_speed = 0
            print('The upload speed test failed. ', err_msg)
        # uplink_speed, uplink_jitter, uplink_loss_rate = sender_arr[4], sender_arr[5], sender_arr[7]
        #
        # self.uplink_speed, self.uplink_jitter, self.uplink_loss_rate = uplink_speed, uplink_jitter, uplink_loss_rate
        pass

    def download_speed_test(self):
        raw_testspeed = str(subprocess.Popen('iperf -c %s -t %s -i %s -p %s -f m'
                                             % (
                                                 self.target_dir, self.time_duration, self.time_duration,
                                                 self.target_port),
                                             shell = True,
                                             stdout = subprocess.PIPE).communicate()[0], 'utf-8')
        try:
            send_speed = re.findall(r'\d+.?\d*', raw_testspeed.split(']')[-2])[-2]
            rec_speed = re.findall(r'\d+.?\d*', raw_testspeed.split(']')[-1])[-1]
            # self.uplink_speed = send_speed
            self.downlink_speed = rec_speed
        except:
            send_speed = str('na')
            rec_speed = str('na')
            # self.uplink_speed = 0
            self.downlink_speed = 0
        pass

    ## archived due to logic change here.
    # def download_speed_test(self):
    #     raw_downspd = str(subprocess.Popen('iperf3 -c %s -b 10g -t %s -i %s -p %s -f m -R'
    #                                        % (
    #                                            self.target_dir, self.time_duration, self.time_duration,
    #                                            self.target_port),
    #                                        shell = True,
    #                                        stdout = subprocess.PIPE).communicate()[0], 'utf-8')
    #     result_array = raw_downspd.split('\n')
    #     for item_var in result_array:
    #         if 'sender' in item_var:
    #             sender_line = item_var
    #         if 'receiver' in item_var:
    #             receiver_line = item_var
    #
    #     try:
    #         receiver_arr = re.findall(r'\d+.?\d*', receiver_line)
    #         self.downlink_speed = receiver_arr[4]
    #     except UnboundLocalError as err_msg:
    #         self.downlink_speed = 0
    #         print('The download speed test failed. ', err_msg)
    #     # downlink_speed, downlink_jitter, downlink_loss_rate = receiver_arr[4], receiver_arr[5], receiver_arr[7]
    #     #
    #     # self.downlink_speed, self.downlink_jitter, self.downlink_loss_rate = downlink_speed, downlink_jitter, downlink_loss_rate
    #     pass
    #
    # def upload_speed_test(self):
    #     raw_upspd = str(subprocess.Popen('iperf3 -c %s -b 10g -t %s -i %s -p %s -f m'
    #                                      % (
    #                                          self.target_dir, self.time_duration, self.time_duration,
    #                                          self.target_port),
    #                                      shell = True,
    #                                      stdout = subprocess.PIPE).communicate()[0], 'utf-8')
    #     result_array = raw_upspd.split('\n')
    #     for item_var in result_array:
    #         if 'sender' in item_var:
    #             sender_line = item_var
    #         if 'receiver' in item_var:
    #             receiver_line = item_var
    #
    #     try:
    #         sender_arr = re.findall(r'\d+.?\d*', sender_line)
    #         self.uplink_speed = sender_arr[4]
    #     except UnboundLocalError as err_msg:
    #         self.uplink_speed = 0
    #         print('The upload speed test failed. ', err_msg)
    #     # uplink_speed, uplink_jitter, uplink_loss_rate = sender_arr[4], sender_arr[5], sender_arr[7]
    #     #
    #     # self.uplink_speed, self.uplink_jitter, self.uplink_loss_rate = uplink_speed, uplink_jitter, uplink_loss_rate
    #     pass

    def network_checker(self):
        ## insert the iperf 3 module here.

        raw_test_result = str(subprocess.Popen('iperf3 -c %s -p 5201 -t 30 -i 30 -f m -u' % self.target_dir,
                                               shell = True, stdout = subprocess.PIPE).communicate()[0], 'utf-8')

        ## add the length check here: if the connection is failed, then the reported string should be ''
        result_array = raw_test_result.split('\n')
        for item_var in result_array:
            if 'sender' in item_var:
                sender_line = item_var
            if 'receiver' in item_var:
                receiver_line = item_var

        ## the output should be ID, interval(start/end), transfer_total, bitrate, jitter, package_count, percentage
        ## speed is presented in Mbps

        sender_arr = re.findall(r'\d+.?\d*', sender_line)
        downlink_speed, downlink_jitter, downlink_loss_rate = sender_arr[4], sender_arr[5], sender_arr[7]
        receiver_arr = re.findall(r'\d+.?\d*', receiver_line)
        uplink_speed, uplink_jitter, uplink_loss_rate = receiver_arr[4], receiver_arr[5], receiver_arr[7]

        self.downlink_speed, self.downlink_jitter, self.downlink_loss_rate = downlink_speed, downlink_jitter, downlink_loss_rate
        self.uplink_speed, self.uplink_jitter, self.uplink_loss_rate = uplink_speed, uplink_jitter, uplink_loss_rate
        # print('test')
        # pass
