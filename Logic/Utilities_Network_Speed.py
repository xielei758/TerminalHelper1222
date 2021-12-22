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

sys.path.append('..')
## import the ui layout of sub pages
from UI.sub_pages.ui_util_network_speed import Ui_SpeedTest

## import resources files here
from UI import ui_image_assets

## import backend here
from Utils.Network_Speed.network_speed_test import NetworkSpeedTest


class Network_Speed_Sub_Window(QMainWindow, Ui_SpeedTest):
    # def __init__(self, parent = None):
    #     super(Network_Speed_Sub_Window, self).__init__(parent)
    def __init__(self, parent_self):

        super().__init__()
        self.setupUi(self)

        self.parent = parent_self

        self.test_mode = 'bidirectional'
        # self.test_mode = 'oneside'

        self.Visual()
        self.main_window_init()
        self.Logic()

    def Visual(self):
        ## visual effects about the general window presentation
        self.setWindowTitle('蓝狐 - 网络测速')

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

    def main_window_init(self):
        ## visual effects about the contents in the window

        ## the prompt
        if self.test_mode == 'oneside':
            self.util_network_speed_on_going_downspd_prompt.setText('网络连接速度：')
            self.util_network_speed_on_going_downspd_tip.setText('网络连接速度决定您从网络获取数据的速度。'
                                                                 '测试速度越大，则您进行网络操作的速度越快。')

        ## the placeholder
        self.network_spd_icon_placeholder.setFlat(True)
        # self.network_spd_icon_placeholder.setIcon(QIcon(':/images/Utilities/network_dash_icon.png'))
        # self.network_spd_icon_placeholder.setIconSize(QtCore.QSize(95, 95))
        self.network_spd_icon_placeholder.setLayoutDirection(Qt.RightToLeft)
        self.network_spd_icon_placeholder.setStyleSheet('QPushButton \n'
                                                        '{font-size:18pt; \n'
                                                        # 'color: rgb(255, 255, 255); \n'
                                                        'border-radius: 15px; \n'
                                                        'border-image: url(":/images/Utilities/network_dash_icon.png"); \n}')
        self.network_spd_icon_placeholder.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        ## the actual trigger button
        self.network_spd_main_btn_tiggerTest.setStyleSheet('QPushButton \n'
                                                           '{background-color: rgb(58,120,160); \n'
                                                           'font-size:22pt; \n'
                                                           'color: rgb(255, 255, 255)}'
                                                           'QPushButton:hover \n'
                                                           '{background-color: rgb(81,167,223); } \n'
                                                           'QPushButton:pressed \n'
                                                           '{background-color: rgb(35,72,96); } ')
        self.network_spd_main_btn_tiggerTest.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        ## adding the network test flow chart
        self.perf_mon_net_flow_charView = QChartView(self)
        ## by default set the chart invisible
        self.perf_mon_net_flow_charView.setVisible(False)
        self.perf_mon_net_flow_charView.setRenderHints(QtGui.QPainter.Antialiasing)

        self.perf_mon_net_flow_x_axis = QValueAxis()
        self.perf_mon_net_flow_x_axis.setRange(0.00, 21.00)
        self.perf_mon_net_flow_x_axis.setLabelFormat('%0.0f')
        self.perf_mon_net_flow_x_axis.setLabelsBrush(QColor(255, 255, 255, 180))
        self.perf_mon_net_flow_x_axis.setTickCount(9)
        self.perf_mon_net_flow_x_axis.setMinorTickCount(0)
        self.perf_mon_net_flow_x_axis.setTitleText('时间轴')
        self.perf_mon_net_flow_x_axis.setTitleBrush(QColor(255, 255, 255, 180))

        ## setting the y axis
        ## assuming the fastest speed will be
        self.perf_mon_net_flow_y_axis = QValueAxis()
        self.perf_mon_net_flow_y_axis.setRange(0.00, 10.00)
        self.perf_mon_net_flow_y_axis.setLabelFormat('%3.0f')
        self.perf_mon_net_flow_y_axis.setLabelsColor(QColor(255, 255, 255, 180))
        # self.perf_mon_net_flow_y_axis.setLabelsBrush(QColor(255, 255, 255, 180))
        self.perf_mon_net_flow_y_axis.setTickCount(6)
        self.perf_mon_net_flow_y_axis.setMinorTickCount(0)
        self.perf_mon_net_flow_y_axis.setTitleText('MB/s')
        self.perf_mon_net_flow_y_axis.setTitleBrush(QColor(255, 255, 255, 180))

        ## set up the chart
        self.perf_mon_net_flow_charView.chart().setAxisX(self.perf_mon_net_flow_x_axis)
        self.perf_mon_net_flow_charView.chart().setAxisY(self.perf_mon_net_flow_y_axis)

        ## get relevant data here
        self.perf_mon_uplink_archive = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
                                        0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
                                        0.2, 0.2, 0.2, 0.2, 0.2, 0.2, self.perf_mon_net_flow_y_axis.max()]
        self.perf_mon_downlink_archive = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
                                          0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
                                          0.2, 0.2, 0.2, 0.2, 0.2, 0.2, self.perf_mon_net_flow_y_axis.max()]

        if hasattr(self.parent.cons_repo, 'uplink_spd'):
            self.perf_mon_uplink_archive.append(self.parent.cons_repo.uplink_spd)

        if hasattr(self.parent.cons_repo, 'downlink_spd'):
            self.perf_mon_downlink_archive.append(self.parent.cons_repo.downlink_spd)

        ## creating proper container for this line variable
        if not hasattr(self, 'perf_mon_uplink_record'):
            self.perf_mon_uplink_record = QLineSeries()
        else:
            self.perf_mon_uplink_record.clear()

        uplink_point_list = self.lineseries_pointer_filler(self.perf_mon_uplink_archive)

        self.perf_mon_uplink_record.append(uplink_point_list)
        self.perf_mon_uplink_record.setName('上行流量')

        if not hasattr(self.parent.cons_repo, 'perf_mon_downlink_record'):
            self.perf_mon_downlink_record = QLineSeries()
        else:
            self.perf_mon_downlink_record.clear()

        downlink_point_list = self.lineseries_pointer_filler(self.perf_mon_downlink_archive)

        self.perf_mon_downlink_record.append(downlink_point_list)
        self.perf_mon_downlink_record.setName('下行流量')

        ## add data to the chart here
        self.perf_mon_net_flow_charView.chart().addSeries(self.perf_mon_uplink_record)

        if not self.test_mode == 'oneside':
            self.perf_mon_net_flow_charView.chart().addSeries(self.perf_mon_downlink_record)

        ## setting the legend here
        # self.perf_mon_net_flow_charView.chart().legend().detachFromChart()
        if not self.test_mode == 'oneside':
            self.perf_mon_net_flow_charView.chart().legend().setVisible(True)
        else:
            self.perf_mon_net_flow_charView.chart().legend().setVisible(False)

        ## set the stylesheet of the chart
        self.perf_mon_net_flow_charView.chart().setBackgroundVisible(False)
        self.perf_mon_net_flow_charView.chart().legend().setBackgroundVisible(False)
        self.perf_mon_net_flow_charView.chart().legend().setLabelColor(QColor(255, 255, 255, 180))
        self.perf_mon_net_flow_charView.chart().layout().setContentsMargins(0, 0, 0, 0)
        # self.perf_mon_net_flow_charView.chart().legend().attachToChart()
        self.perf_mon_net_flow_charView.chart().legend().setAlignment(Qt.AlignTop)
        self.perf_mon_net_flow_charView.chart().legend().setGeometry(30, 650, 50, 10)
        self.perf_mon_net_flow_charView.chart().legend().update()

        self.util_network_speed_flow_canvas.addWidget(self.perf_mon_net_flow_charView)
        pass

    def Logic(self):
        ## the local test environment
        # self.server_addr = str('192.168.65.1')
        # self.server_port = str('5678')

        ## the arm server held speedtest service
        self.server_addr = str('47.94.229.37')
        self.server_port = str('5900')

        self.network_spd_monitor_delay = float(0.3)

        self.util_network_spd_stacked.setCurrentWidget(self.welcome_page)

        ## binding the buttons
        self.network_spd_main_btn_tiggerTest.clicked.connect(self.on_going_trigger_speedtest)
        self.network_spd_icon_placeholder.clicked.connect(self.on_going_trigger_speedtest)

        ## start the network flow monitoring
        self.net_spd_monitor_thread = Thread(target = self.on_going_network_flow_chart_refresh_caller,
                                             name = 'SpeedtestMonitor')
        self.net_spd_monitor_thread.start()

    def on_going_trigger_speedtest(self):

        self.on_going_speedtest_visual_init()
        self.on_going_speedtest_logic_init()
        pass

    def lineseries_pointer_filler(self, incoming_list):
        upper_th = self.perf_mon_net_flow_y_axis.max()

        pointer_0 = QtCore.QPointF(0, round(incoming_list[-22] / upper_th, 3))
        pointer_1 = QtCore.QPointF(1, round(incoming_list[-21] / upper_th, 3))
        pointer_2 = QtCore.QPointF(2, round(incoming_list[-20] / upper_th, 3))
        pointer_3 = QtCore.QPointF(3, round(incoming_list[-19] / upper_th, 3))
        pointer_4 = QtCore.QPointF(4, round(incoming_list[-18] / upper_th, 3))
        pointer_5 = QtCore.QPointF(5, round(incoming_list[-17] / upper_th, 3))
        pointer_6 = QtCore.QPointF(6, round(incoming_list[-16] / upper_th, 3))
        pointer_7 = QtCore.QPointF(7, round(incoming_list[-15] / upper_th, 3))
        pointer_8 = QtCore.QPointF(8, round(incoming_list[-14] / upper_th, 3))
        pointer_9 = QtCore.QPointF(9, round(incoming_list[-13] / upper_th, 3))
        pointer_10 = QtCore.QPointF(10, round(incoming_list[-12] / upper_th, 3))
        pointer_11 = QtCore.QPointF(11, round(incoming_list[-11] / upper_th, 3))
        pointer_12 = QtCore.QPointF(12, round(incoming_list[-10] / upper_th, 3))
        pointer_13 = QtCore.QPointF(13, round(incoming_list[-9] / upper_th, 3))
        pointer_14 = QtCore.QPointF(14, round(incoming_list[-8] / upper_th, 3))
        pointer_15 = QtCore.QPointF(15, round(incoming_list[-7] / upper_th, 3))
        pointer_16 = QtCore.QPointF(16, round(incoming_list[-6] / upper_th, 3))
        pointer_17 = QtCore.QPointF(17, round(incoming_list[-5] / upper_th, 3))
        pointer_18 = QtCore.QPointF(18, round(incoming_list[-4] / upper_th, 3))
        pointer_19 = QtCore.QPointF(19, round(incoming_list[-3] / upper_th, 3))
        pointer_20 = QtCore.QPointF(20, round(incoming_list[-2] / upper_th, 3))
        pointer_21 = QtCore.QPointF(21, round(incoming_list[-1] / upper_th, 3))

        return list([pointer_0, pointer_1, pointer_2, pointer_3, pointer_4, pointer_5, pointer_6, pointer_7,
                     pointer_8, pointer_9, pointer_10, pointer_11, pointer_12, pointer_13, pointer_14, pointer_15,
                     pointer_16, pointer_17, pointer_18, pointer_19, pointer_20, pointer_21])

    def on_going_network_flow_chart_refresh_caller(self):
        while True:
            self.on_going_network_flow_chart_refresh()
            sleep(self.network_spd_monitor_delay)
        pass

    def on_going_network_flow_chart_refresh(self):
        #### if the current self.perf_page_refresh_delay is smaller than
        #### the update frequency in the base thread, then call the update function.
        if self.network_spd_monitor_delay <= float(self.parent.cons_repo.ins_freq):
            self.parent.cons_repo.network_monitor()

        ## to check if the y axis should be scaled here
        series_len = len(self.perf_mon_uplink_record)
        uplink_max_value = max(self.perf_mon_uplink_archive[-series_len:])
        downlink_max_value = max(self.perf_mon_downlink_archive[-series_len:])
        record_max_value = max(uplink_max_value, downlink_max_value)
        # print('web flow info', series_len, type(series_len), record_max_value)
        # print('record max', record_max_value)

        ## scaling the vertical axis here.
        if record_max_value > self.perf_mon_net_flow_y_axis.max():
            print('auto scale now performed. ')
            target_up_th = record_max_value + 1
            self.perf_mon_net_flow_y_axis.setRange(0.00, target_up_th)
            # self.perf_mon_net_flow_charView.chart().setAxisY(self.perf_mon_net_flow_y_axis)
            pass
        elif record_max_value <= float(9.5):
            if self.perf_mon_net_flow_y_axis.max() != float(10.0):
                print('auto scale now performed. ')
                target_up_th = float(10.0)
                self.perf_mon_net_flow_y_axis.setRange(0.00, target_up_th)

        ## updating the uplink info
        self.perf_mon_uplink_archive.append(self.parent.cons_repo.uplink_spd)

        ## if the list is too long, then trim it.
        if len(self.perf_mon_uplink_archive) > 30:
            self.perf_mon_uplink_archive = self.perf_mon_uplink_archive[-30:]

        uplink_point_list = self.lineseries_pointer_filler(self.perf_mon_uplink_archive)
        self.perf_mon_uplink_record.clear()
        self.perf_mon_uplink_record.append(uplink_point_list)

        ## updating the downlink info
        self.perf_mon_downlink_archive.append(self.parent.cons_repo.downlink_spd)

        ## if the list is too long, then trim it.
        if len(self.perf_mon_downlink_archive) > 30:
            self.perf_mon_downlink_archive = self.perf_mon_downlink_archive[-30:]

        downlink_point_list = self.lineseries_pointer_filler(self.perf_mon_downlink_archive)
        self.perf_mon_downlink_record.clear()
        self.perf_mon_downlink_record.append(downlink_point_list)

        pass

    def on_going_speedtest_visual_init(self):
        ## select the stacked widget
        self.util_network_spd_stacked.setCurrentWidget(self.on_going_test_page)

        ## the automatic fix button
        self.network_automatical_repair.setVisible(False)
        self.network_automatical_repair.setStyleSheet('QPushButton \n'
                                                      '{background-color: rgb(255,83,83); \n'
                                                      'font-size:16pt; \n'
                                                      'color: rgb(255, 255, 255)}'
                                                      'QPushButton:hover \n'
                                                      '{background-color: rgb(255,121,121); } \n'
                                                      'QPushButton:pressed \n'
                                                      '{background-color: rgb(205,51,51); } ')
        self.network_automatical_repair.clicked.connect(self.on_click_network_automatical_repair)

        ## setting the labels
        ## on call of this page, automatically hide all the elements related to results
        self.util_network_speed_on_going_latency_comment.setVisible(False)
        self.util_network_speed_on_going_downspd_comment.setVisible(False)
        self.util_network_speed_on_going_upspd_comment.setVisible(False)

        self.util_network_speed_on_going_latency_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                     'color: rgb(255, 255, 255);')
        self.util_network_speed_on_going_downspd_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                     'color: rgb(255, 255, 255);')
        self.util_network_speed_on_going_upspd_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                   'color: rgb(255, 255, 255);')

        ## since the upload will be tested later, hereby hide them
        for key, value in self.__dict__.items():
            if key.startswith('util_network_speed_on_going_upspd'):
                try:
                    getattr(self, key).setVisible(False)
                except AttributeError:
                    pass

        QApplication.processEvents()
        pass

    def on_going_speedtest_logic_init(self):

        ## the caller function that controls the speedtest workflow.

        ## setting the speedtest duration here
        # speedtest_duration = int(int(self.network_spd_duration_combo.currentText()) / 2)
        speedtest_duration = int(int(self.network_spd_duration_combo.currentText()))
        self.spd_test_duration = speedtest_duration

        ## start the testing backend here
        self.backend = NetworkSpeedTest(self)

        ## the following line actually controls the behavior of the speedtest process
        ## handle with care.
        ## init the network test workflow
        self.on_going_speedtest_workflow()

        pass

    def on_going_network_flow_chart_clear(self):

        ## prepare the series

        for append_iter in range(21):
            self.perf_mon_uplink_archive.append(0)
            self.perf_mon_downlink_archive.append(0)

        if len(self.perf_mon_uplink_archive) > 30:
            self.perf_mon_uplink_archive = self.perf_mon_uplink_archive[-30:]

        uplink_point_list = self.lineseries_pointer_filler(self.perf_mon_uplink_archive)
        self.perf_mon_uplink_record.clear()
        self.perf_mon_uplink_record.append(uplink_point_list)

        if len(self.perf_mon_downlink_archive) > 30:
            self.perf_mon_downlink_archive = self.perf_mon_downlink_archive[-30:]

        downlink_point_list = self.lineseries_pointer_filler(self.perf_mon_downlink_archive)
        self.perf_mon_downlink_record.clear()
        self.perf_mon_downlink_record.append(downlink_point_list)

    def on_going_speedtest_workflow(self):
        ## first operate the latency test
        ## so as to make sure if the connection to speedtest server is normal.

        try:
            self.backend.latency_test()
        except Exception as err_msg:
            self.backend.network_latency = 'failed'
            print('network latency failed ', err_msg)

        # self.backend.start()
        # QApplication.processEvents()

        if self.backend.network_latency == 'failed':
            self.speed_test_error_GUI_handler()

        else:
            ## update the current latency here
            present_latency = round(float(self.backend.network_latency), 2)
            self.util_network_speed_on_going_latency_value.setText('%s 毫秒' % present_latency)
            self.util_network_speed_on_going_header.setText('正在测试网络')
            self.util_network_speed_on_going_subheader.setText('与测速服务器通信成功。正在为您测试网络连接速度。')

            ## present the results as classified here
            ## if the latency is less than 10 ms
            ## the info element should be green

            ## judge the threshold according to the location of the server
            ## if the server is also under the same LAN, then the threshold should be low
            ## else higher.

            if self.server_addr.startswith('47'):
                ## service on WAN
                latency_threshold = 60
            else:
                ## service on LAN
                latency_threshold = 10

            if present_latency <= latency_threshold:
                self.util_network_speed_on_going_latency_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                             'color: rgb(111,200,77);')
                self.util_network_speed_on_going_latency_comment.setVisible(True)
                self.util_network_speed_on_going_latency_comment.setText('网络环境畅通，延迟理想。网络应用能迅速响应。')
                self.util_network_speed_on_going_latency_comment.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                               'color: rgb(111,200,77);')

            ## else, present in red.
            else:
                self.util_network_speed_on_going_latency_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                             'color: rgb(255,77,77);')
                self.util_network_speed_on_going_latency_comment.setVisible(True)
                self.util_network_speed_on_going_latency_comment.setText('网络较为堵塞。网络应用可能迟缓。')
                self.util_network_speed_on_going_latency_comment.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                               'color: rgb(255,77,77);')

            ## if the latency is normal, which indicates that the network connection is capable of speedtest here
            ## perform the following speedtest.

            # QApplication.processEvents()
            ## set the network flow chart visible and proceed further operations
            self.on_going_network_flow_chart_clear()
            self.perf_mon_net_flow_charView.setVisible(True)

            ## offload some task to the separate thread to avoid window freezing
            ## the actual test workflow is taken over by the backend

            test_workflow = Thread(target = self.backend.network_speedtest_workflow,
                                   name = 'network_speedtest_backend')
            test_workflow.start()

    def speed_test_error_GUI_handler(self):
        self.util_network_speed_on_going_header.setText('信号失踪了...')
        self.util_network_speed_on_going_latency_value.setText('未能连接到服务器')
        self.util_network_speed_on_going_latency_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                     'color: rgb(255,77,77);')
        self.util_network_speed_on_going_subheader.setText('暂时无法建立至测速服务器的有效连接，当前网络访问可能受到限制或不可用。')
        self.util_network_speed_on_going_downspd_value.setText('测试服务不可用')
        self.util_network_speed_on_going_downspd_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                     'color: rgb(255,77,77);')
        self.util_network_speed_on_going_upspd_prompt.setVisible(True)
        self.util_network_speed_on_going_upspd_value.setVisible(True)
        self.util_network_speed_on_going_upspd_tip.setVisible(True)
        self.util_network_speed_on_going_upspd_value.setText('测试服务不可用')
        self.util_network_speed_on_going_upspd_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                   'color: rgb(255,77,77);')
        self.perf_mon_net_flow_charView.setVisible(False)
        self.network_automatical_repair.setVisible(True)
        pass

    def downspd_prompt_handler(self, downspd_raw):
        downspd_raw = float(downspd_raw)
        if int(downspd_raw) != 0:
            present_result = str(downspd_raw) + ' 兆比特每秒'
            # present_result = downspd_raw + '兆比特每秒 (Mbits/s)'
            self.util_network_speed_on_going_downspd_value.setText(present_result)

            ## by default set this prompt green
            self.util_network_speed_on_going_downspd_comment.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                           'color: rgb(111,200,77);')
            self.util_network_speed_on_going_downspd_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                         'color: rgb(111,200,77);')

            num_test_result = float(downspd_raw)
            if num_test_result <= 5:
                comment_text = '当前带宽偏小，能正常进行文字处理、网页浏览。'
                self.util_network_speed_on_going_downspd_comment.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                               'color: rgb(255,77,77);')
                self.util_network_speed_on_going_downspd_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                             'color: rgb(255,77,77);')
            elif num_test_result <= 10:
                comment_text = '当前带宽在10M左右，能流畅进行在线会议。'
            elif num_test_result <= 20:
                comment_text = '当前带宽在20M左右，能流畅观看4K超高清视频。'
            elif num_test_result <= 30:
                comment_text = '当前带宽在30M左右，能在线无卡顿观看蓝光电影。'
            elif num_test_result <= 50:
                comment_text = '当前带宽在50M左右，网速超快，可以进行高并发业务。'
            elif num_test_result <= 90:
                comment_text = '当前带宽接近100M啦。专线般的速度！'
            elif num_test_result <= 300:
                comment_text = '光纤网络足以让您迅速完成所有网络任务。'
            else:
                comment_text = '您的网络连接快于绝大部分宽带用户。'

            self.util_network_speed_on_going_downspd_comment.setText(comment_text)
            self.util_network_speed_on_going_downspd_comment.setVisible(True)
        else:
            present_result = '下行测试失败'
            self.util_network_speed_on_going_downspd_value.setText(present_result)
            self.util_network_speed_on_going_downspd_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                         'color: rgb(255,77,77);')

    def upspd_prompt_handler(self, upspd_raw, peered_flag):
        upspd_raw = float(upspd_raw)
        if int(upspd_raw) != 0:
            present_result = str(upspd_raw) + ' 兆比特每秒'

            self.util_network_speed_on_going_upspd_value.setText(present_result)

            ## by default set it green
            self.util_network_speed_on_going_upspd_comment.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                         'color: rgb(111,200,77);')
            self.util_network_speed_on_going_upspd_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                       'color: rgb(111,200,77);')

            ## setting the value placeholder
            num_test_result = float(upspd_raw)
            if num_test_result <= 2:
                comment_text = '上传带宽较小，在办公平台上传文件时可能遇到问题。'
                self.util_network_speed_on_going_downspd_comment.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                               'color: rgb(255,77,77);')
                self.util_network_speed_on_going_upspd_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                           'color: rgb(255,77,77);')
            elif num_test_result <= 5:
                comment_text = '上传带宽正常，能够较为迅速地分享文件。'
            elif num_test_result <= 15:
                comment_text = '上传带宽速度较快，能够流畅发起多人在线会议。'
            elif num_test_result <= 30:
                comment_text = '上传带宽非常充足，能够流畅发起多人在线会议。'
            else:
                comment_text = '上传带宽达到专线水平，能够满足各项业务需求。'

            if peered_flag == True:
                comment_text += '当前网络上下行对等。'
            else:
                comment_text += '网络上下行不对等。'

            self.util_network_speed_on_going_upspd_comment.setText(comment_text)
            self.util_network_speed_on_going_upspd_comment.setVisible(True)

            ## if latency is reasonable, then proceed the speedtest

            # self.perf_mon_net_flow_charView.setVisible(True)
            ## fill 0 to the series for 20 times here
        else:
            present_result = '上行测试失败'
            self.util_network_speed_on_going_upspd_value.setText(present_result)
            self.util_network_speed_on_going_upspd_value.setStyleSheet('font: 12pt "Noto Mono"; \n'
                                                                       'color: rgb(255,77,77);')

        pass

    def on_click_network_automatical_repair(self):
        self.parent.utilities_go2btn_network_auto_repair.click()
        pass

    def closeEvent(self, event) -> None:
        ## rewrite the close event to cooperate with the system tray
        event.ignore()
        # print('AppStore hidden. ')
        self.hide()
