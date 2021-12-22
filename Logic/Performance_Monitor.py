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


## import utilities here

## since we shifted the way to implement all the charts in this application
## this function is now being rewritten to adopt to QtCharts env.

def perf_mon_page_caller(self):
    ## set the visual style of this page
    ## besides, the widgets and charts are initialized here
    perf_mon_page_main_visual(self)

    ## the contents inside the charts are updated in this caller
    perf_mon_page_main_logic(self)

    perf_mon_page_settings(self)

    ## use this line to disable a specific tab
    # self.perf_mon_base_tabwidget.setTabEnabled(2, False)
    pass


def perf_mon_page_main_visual(self):
    # self.perf_mon_main_filler_widget.setLayout(self.perf_mon_dashboard_canvas)
    # self.perf_mon_main_scroll_basis.setWidget(self.perf_mon_main_filler_widget)

    self.perf_mon_base_tabwidget.setCurrentIndex(0)

    ## setting the graphic visual for the refresh button
    self.perf_mon_refresh_btn.setFlat(True)
    # self.perf_mon_refresh_btn.setStyleSheet('QPushButton \n'
    #                                         '{font-size:16pt; \n'
    #                                         # 'color: rgba(255, 255, 255, 0); \n'
    #                                         'background: transparent; \n}')

    ## so that when pressing this button there will not be a black background.
    self.perf_mon_refresh_btn.setStyleSheet("QPushButton {\n"
                                                  "    \n"
                                                  "    background-position: center;\n"
                                                  "    background-repeat: no-reperat;\n"
                                                  "    border: none;\n"
                                                  "\n"
                                                  "background: transparent;\n"
                                                  "\n"
                                                  "\n"
                                                  "font: 16pt \"Noto Mono\";\n"
                                                  "color: rgb(255, 255, 255);\n"
                                                  "}\n"
                                                  "QPushButton:hover {\n"
                                                  "background: transparent;\n"
                                                  "}\n"
                                                  "QPushButton:pressed {    \n"
                                                  "background: transparent;\n"
                                                  "}\n"
                                                  "")

    ## initiate the contents in the dashboard group and network flow track
    activate_dashboard_group(self)
    activate_network_flow_demo(self)
    activate_cpu_usage_line_graph(self)
    activate_mem_usage_line_graph(self)
    activate_mem_swap_usage_line_graph(self)

    ## setting visual style for the perform monitor detailed presentation
    self.perf_mon_gen_info.setStyleSheet('QPushButton \n'
                                         '{font-size:14pt; \n'
                                         'color: rgb(255, 255, 255); \n'
                                         'border-radius: 8px; \n'
                                         # 'border-color: rgb(143,188,143); \n'
                                         'background: transparent; \n'
                                         'text-align: left; }')

    self.perf_mon_hardware_cpu_spec_demo.setFlat(True)
    self.perf_mon_hardware_cpu_spec_demo.setEnabled(False)
    self.perf_mon_hardware_cpu_spec_demo.setStyleSheet('QPushButton \n'
                                                       '{font-size:13pt; \n'
                                                       'color: rgb(255, 255, 255); \n'
                                                       'border-radius: 4px; \n'
                                                       'text-align: left; }')
    self.perf_mon_hardware_cpu_spec_demo.setText('CPU相关数据载入中')

    self.perf_mon_hardware_mem_spec_demo.setFlat(True)
    self.perf_mon_hardware_mem_spec_demo.setEnabled(False)
    self.perf_mon_hardware_mem_spec_demo.setStyleSheet('QPushButton \n'
                                                       '{font-size:13pt; \n'
                                                       'color: rgb(255, 255, 255); \n'
                                                       'border-radius: 4px; \n'
                                                       'text-align: left; }')
    self.perf_mon_hardware_mem_spec_demo.setText('内存相关数据载入中')

    self.perf_mon_hardware_sto_spec_demo.setFlat(True)
    self.perf_mon_hardware_sto_spec_demo.setEnabled(False)
    self.perf_mon_hardware_sto_spec_demo.setStyleSheet('QPushButton \n'
                                                       '{font-size:13pt; \n'
                                                       'color: rgb(255, 255, 255); \n'
                                                       'border-radius: 4px; \n'
                                                       'text-align: left; }')
    self.perf_mon_hardware_sto_spec_demo.setText('硬盘相关数据载入中')

    self.perf_mon_gen_info.setText('系统运行状态检测中')

    pass


def perf_mon_page_main_logic(self):
    ## binding the function of the refresh button here
    par_on_click_perf_mon_refresh_btn = partial(on_click_perf_mon_refresh_btn, self)
    self.perf_mon_refresh_btn.clicked.connect(par_on_click_perf_mon_refresh_btn)

    ## binding the function to the buttons here
    par_update_refresh_delay = partial(update_refresh_delay, self)
    self.perf_mon_refresh_delay_setter_combo.currentIndexChanged.connect(par_update_refresh_delay)

    ## the function updates the contents in this page
    content_refresh_helper(self)

    ## the code for the strict mode trigger button
    try:
        par_perf_mon_strict_mode_simulator = partial(perf_mon_strict_mode_simulator, self)
        self.perf_mon_strict_mode_trigger.clicked.connect(par_perf_mon_strict_mode_simulator)
    except AttributeError as err_msg:
        print('the trigger may have been removed in this version', err_msg)

    pass


def on_click_perf_mon_refresh_btn(self):
    ## the core line here is
    refresh_perf_page_dashboard(self)

    current_invoke_time = time()

    if hasattr(self, 'record_invoke_time'):
        time_lapse = current_invoke_time - self.record_invoke_time
        if time_lapse < 3:
            print('too soon')
            QMessageBox.information(self, "手动刷新太快了哦", "刷新得太快程序会变慢哦，休息一下~", QMessageBox.Yes)
            return
        else:
            print('record refreshed')
            self.record_invoke_time = current_invoke_time
    else:
        self.record_invoke_time = current_invoke_time

    message_icon = '-i dialog-information'
    message_title = '蓝狐 - 性能监控'
    message_content = '程序中的数据已经刷新啦owo'
    subprocess.Popen(['notify-send', message_icon, message_title, message_content])
    refresh_perf_page_dashboard(self)



def update_refresh_delay(self):
    text_refresh_delay = self.perf_mon_refresh_delay_setter_combo.currentText()[:-1]

    # print(text_refresh_delay)
    self.perf_page_refresh_delay = float(text_refresh_delay)
    print('now the refresh delay has been changed to', self.perf_page_refresh_delay)
    pass


def activate_network_flow_demo(self):
    if self.perf_mon_network_flow_canvas.count() < 1:
        network_flow_demon_init(self)
    pass


def network_flow_demon_init(self):
    ## define the chartview
    self.perf_mon_net_flow_charView = QChartView(self)
    self.perf_mon_net_flow_charView.setRenderHints(QtGui.QPainter.Antialiasing)

    ## setting the x axis
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
    # self.perf_mon_net_flow_charView.chart().axisX().setLabelsColor(QColor(255, 255, 255, 180))
    # self.perf_mon_net_flow_charView.chart().axisX().setLabelsBrush(QColor(255, 255, 255, 180))
    # self.perf_mon_net_flow_charView.setStyleSheet('color: rgb(255, 255, 255); ')

    # self.perf_mon_net_flow_charView.chart().setTitle('网络流量记录')
    self.perf_mon_net_flow_charView.chart().setBackgroundVisible(False)
    self.perf_mon_net_flow_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    ## get relevant data here
    self.perf_mon_uplink_archive = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
                                    0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
                                    0.2, 0.2, 0.2, 0.2, 0.2, 0.2, self.perf_mon_net_flow_y_axis.max()]
    self.perf_mon_downlink_archive = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
                                      0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
                                      0.2, 0.2, 0.2, 0.2, 0.2, 0.2, self.perf_mon_net_flow_y_axis.max()]

    if hasattr(self.cons_repo, 'uplink_spd'):
        self.perf_mon_uplink_archive.append(self.cons_repo.uplink_spd)

    if hasattr(self.cons_repo, 'downlink_spd'):
        self.perf_mon_downlink_archive.append(self.cons_repo.downlink_spd)

    ## creating proper container for this line variable
    if not hasattr(self, 'perf_mon_uplink_record'):
        self.perf_mon_uplink_record = QLineSeries()
    else:
        self.perf_mon_uplink_record.clear()

    uplink_point_list = lineseries_pointer_filler(self, self.perf_mon_uplink_archive)

    self.perf_mon_uplink_record.append(uplink_point_list)
    self.perf_mon_uplink_record.setName('上行流量')

    if not hasattr(self.cons_repo, 'perf_mon_downlink_record'):
        self.perf_mon_downlink_record = QLineSeries()
    else:
        self.perf_mon_downlink_record.clear()

    downlink_point_list = lineseries_pointer_filler(self, self.perf_mon_downlink_archive)

    self.perf_mon_downlink_record.append(downlink_point_list)
    self.perf_mon_downlink_record.setName('下行流量')

    ## add data to the chart here
    self.perf_mon_net_flow_charView.chart().addSeries(self.perf_mon_uplink_record)
    self.perf_mon_net_flow_charView.chart().addSeries(self.perf_mon_downlink_record)

    ## setting the legend here
    # self.perf_mon_net_flow_charView.chart().legend().detachFromChart()
    self.perf_mon_net_flow_charView.chart().legend().setVisible(True)
    self.perf_mon_net_flow_charView.chart().legend().setBackgroundVisible(False)
    self.perf_mon_net_flow_charView.chart().legend().setLabelColor(QColor(255, 255, 255, 180))
    self.perf_mon_net_flow_charView.chart().layout().setContentsMargins(0, 0, 0, 0)
    # self.perf_mon_net_flow_charView.chart().legend().attachToChart()
    # self.perf_mon_net_flow_charView.chart().legend().setAlignment(Qt.AlignTop)
    # self.perf_mon_net_flow_charView.chart().legend().setGeometry(30, 650, 50, 10)
    self.perf_mon_net_flow_charView.chart().legend().update()

    self.perf_mon_network_flow_canvas.addWidget(self.perf_mon_net_flow_charView)

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
    # print('current value', round(incoming_list[-4] / upper_th, 3), round(incoming_list[-3] / upper_th, 3),
    #       round(incoming_list[-2] / upper_th, 3), round(incoming_list[-1] / upper_th, 3))

    return list([pointer_0, pointer_1, pointer_2, pointer_3, pointer_4, pointer_5, pointer_6, pointer_7,
                 pointer_8, pointer_9, pointer_10, pointer_11, pointer_12, pointer_13, pointer_14, pointer_15,
                 pointer_16, pointer_17, pointer_18, pointer_19, pointer_20, pointer_21])


def lineseries_pointer_filler_perc(self, incoming_list):
    upper_th = self.perf_mon_cpu_usage_y_axis.max()

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
    # print('current value', round(incoming_list[-4] / upper_th, 3), round(incoming_list[-3] / upper_th, 3),
    #       round(incoming_list[-2] / upper_th, 3), round(incoming_list[-1] / upper_th, 3))

    return list([pointer_0, pointer_1, pointer_2, pointer_3, pointer_4, pointer_5, pointer_6, pointer_7,
                 pointer_8, pointer_9, pointer_10, pointer_11, pointer_12, pointer_13, pointer_14, pointer_15,
                 pointer_16, pointer_17, pointer_18, pointer_19, pointer_20, pointer_21])


def activate_cpu_usage_line_graph(self):
    if self.perf_mon_cpu_flow_canvas.count() < 1:
        cpu_usage_line_graph_init(self)
    pass


def activate_mem_usage_line_graph(self):
    if self.perf_mon_mem_flow_canvas.count() < 1:
        mem_usage_line_graph_init(self)


def activate_mem_swap_usage_line_graph(self):
    if self.perf_mon_mem_swap_flow_canvas.count() < 1:
        mem_swap_usage_line_graph_init(self)


def cpu_usage_line_graph_init(self):
    ## define the chartview
    self.perf_mon_cpu_usage_charView = QChartView(self)
    self.perf_mon_cpu_usage_charView.setRenderHints(QtGui.QPainter.Antialiasing)

    ## setting the legend
    self.perf_mon_cpu_usage_charView.chart().legend().setVisible(False)

    ## setting the x axis
    self.perf_mon_cpu_usage_x_axis = QValueAxis()
    self.perf_mon_cpu_usage_x_axis.setRange(0.00, 21.00)
    self.perf_mon_cpu_usage_x_axis.setLabelFormat('%0.0f')
    self.perf_mon_cpu_usage_x_axis.setLabelsBrush(QColor(255, 255, 255, 180))
    self.perf_mon_cpu_usage_x_axis.setTickCount(9)
    self.perf_mon_cpu_usage_x_axis.setMinorTickCount(0)
    self.perf_mon_cpu_usage_x_axis.setTitleText('时间轴')
    self.perf_mon_cpu_usage_x_axis.setTitleBrush(QColor(255, 255, 255, 180))

    ## setting the y axis
    self.perf_mon_cpu_usage_y_axis = QValueAxis()
    self.perf_mon_cpu_usage_y_axis.setRange(0.00, 1.00)
    self.perf_mon_cpu_usage_y_axis.setLabelFormat('%0.2f')
    self.perf_mon_cpu_usage_y_axis.setLabelsBrush(QColor(255, 255, 255, 180))
    self.perf_mon_cpu_usage_y_axis.setTickCount(6)
    self.perf_mon_cpu_usage_y_axis.setMinorTickCount(0)
    self.perf_mon_cpu_usage_y_axis.setTitleText('CPU 使用率')
    self.perf_mon_cpu_usage_y_axis.setTitleBrush(QColor(255, 255, 255, 180))

    ## binding the chartview with the axis
    self.perf_mon_cpu_usage_charView.chart().setAxisX(self.perf_mon_cpu_usage_x_axis)
    self.perf_mon_cpu_usage_charView.chart().setAxisY(self.perf_mon_cpu_usage_y_axis)

    self.perf_mon_cpu_usage_charView.chart().setBackgroundVisible(False)
    self.perf_mon_cpu_usage_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    ## generating the init data here
    self.perf_mon_cpu_hist_archive = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                                      0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                                      0.05, 0.05, 0.05, 0.05, 0.05, 0.05, self.perf_mon_cpu_usage_y_axis.max()]

    if hasattr(self.cons_repo, 'CPU_perc'):
        self.perf_mon_cpu_hist_archive.append(float(self.cons_repo.CPU_perc))

    ## creating the series data container here. 
    if not hasattr(self, 'perf_mon_cpu_hist_record'):
        self.perf_mon_cpu_hist_record = QLineSeries()
    else:
        self.perf_mon_cpu_hist_record.clear()

    cpu_hist_data = lineseries_pointer_filler_perc(self, self.perf_mon_cpu_hist_archive)

    self.perf_mon_cpu_hist_record.append(cpu_hist_data)
    # self.perf_mon_cpu_hist_record.setName('CPU Hist')

    self.perf_mon_cpu_usage_charView.chart().addSeries(self.perf_mon_cpu_hist_record)
    self.perf_mon_cpu_usage_charView.chart().legend().setLabelColor(QColor(255, 255, 255, 180))
    self.perf_mon_cpu_usage_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    self.perf_mon_cpu_flow_canvas.addWidget(self.perf_mon_cpu_usage_charView)
    pass


def mem_usage_line_graph_init(self):
    ## define the chartview
    self.perf_mon_mem_usage_charView = QChartView(self)
    self.perf_mon_mem_usage_charView.setRenderHints(QtGui.QPainter.Antialiasing)

    ## setting the legend
    self.perf_mon_mem_usage_charView.chart().legend().setVisible(False)

    ## setting the x axis
    self.perf_mon_mem_usage_x_axis = QValueAxis()
    self.perf_mon_mem_usage_x_axis.setRange(0.00, 21.00)
    self.perf_mon_mem_usage_x_axis.setLabelFormat('%0.0f')
    self.perf_mon_mem_usage_x_axis.setLabelsBrush(QColor(255, 255, 255, 180))
    self.perf_mon_mem_usage_x_axis.setTickCount(9)
    self.perf_mon_mem_usage_x_axis.setMinorTickCount(0)
    self.perf_mon_mem_usage_x_axis.setTitleText('时间轴')
    self.perf_mon_mem_usage_x_axis.setTitleBrush(QColor(255, 255, 255, 180))

    ## setting the y axis
    self.perf_mon_mem_usage_y_axis = QValueAxis()
    self.perf_mon_mem_usage_y_axis.setRange(0.00, 1.00)
    self.perf_mon_mem_usage_y_axis.setLabelFormat('%0.2f')
    self.perf_mon_mem_usage_y_axis.setLabelsBrush(QColor(255, 255, 255, 180))
    self.perf_mon_mem_usage_y_axis.setTickCount(6)
    self.perf_mon_mem_usage_y_axis.setMinorTickCount(0)
    self.perf_mon_mem_usage_y_axis.setTitleText('物理内存使用率')
    self.perf_mon_mem_usage_y_axis.setTitleBrush(QColor(255, 255, 255, 180))

    ## binding the chartview with the axis
    self.perf_mon_mem_usage_charView.chart().setAxisX(self.perf_mon_mem_usage_x_axis)
    self.perf_mon_mem_usage_charView.chart().setAxisY(self.perf_mon_mem_usage_y_axis)

    self.perf_mon_mem_usage_charView.chart().setBackgroundVisible(False)
    self.perf_mon_mem_usage_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    ## generating the init data here
    self.perf_mon_mem_hist_archive = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                                      0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                                      0.05, 0.05, 0.05, 0.05, 0.05, 0.05, self.perf_mon_mem_usage_y_axis.max()]

    if hasattr(self.cons_repo, 'phy_mem_perc'):
        self.perf_mon_mem_hist_archive.append(float(self.cons_repo.phy_mem_perc))
        print(float(self.cons_repo.phy_mem_perc))

    ## creating the series data container here. 
    if not hasattr(self, 'perf_mon_mem_hist_record'):
        self.perf_mon_mem_hist_record = QLineSeries()
    else:
        self.perf_mon_mem_hist_record.clear()

    mem_hist_data = lineseries_pointer_filler_perc(self, self.perf_mon_mem_hist_archive)

    self.perf_mon_mem_hist_record.append(mem_hist_data)
    # self.perf_mon_mem_hist_record.setName('mem Hist')

    self.perf_mon_mem_usage_charView.chart().addSeries(self.perf_mon_mem_hist_record)
    self.perf_mon_mem_usage_charView.chart().legend().setLabelColor(QColor(255, 255, 255, 180))
    self.perf_mon_mem_usage_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    self.perf_mon_mem_flow_canvas.addWidget(self.perf_mon_mem_usage_charView)
    pass


def mem_swap_usage_line_graph_init(self):
    ## define the chartview
    self.perf_mon_mem_swap_usage_charView = QChartView(self)
    self.perf_mon_mem_swap_usage_charView.setRenderHints(QtGui.QPainter.Antialiasing)

    ## setting the legend
    self.perf_mon_mem_swap_usage_charView.chart().legend().setVisible(False)

    ## setting the x axis
    self.perf_mon_mem_swap_usage_x_axis = QValueAxis()
    self.perf_mon_mem_swap_usage_x_axis.setRange(0.00, 21.00)
    self.perf_mon_mem_swap_usage_x_axis.setLabelFormat('%0.0f')
    self.perf_mon_mem_swap_usage_x_axis.setLabelsBrush(QColor(255, 255, 255, 180))
    self.perf_mon_mem_swap_usage_x_axis.setTickCount(9)
    self.perf_mon_mem_swap_usage_x_axis.setMinorTickCount(0)
    self.perf_mon_mem_swap_usage_x_axis.setTitleText('时间轴')
    self.perf_mon_mem_swap_usage_x_axis.setTitleBrush(QColor(255, 255, 255, 180))

    ## setting the y axis
    self.perf_mon_mem_swap_usage_y_axis = QValueAxis()
    self.perf_mon_mem_swap_usage_y_axis.setRange(0.00, 1.00)
    self.perf_mon_mem_swap_usage_y_axis.setLabelFormat('%0.2f')
    self.perf_mon_mem_swap_usage_y_axis.setLabelsBrush(QColor(255, 255, 255, 180))
    self.perf_mon_mem_swap_usage_y_axis.setTickCount(6)
    self.perf_mon_mem_swap_usage_y_axis.setMinorTickCount(0)
    self.perf_mon_mem_swap_usage_y_axis.setTitleText('虚拟内存使用率')
    self.perf_mon_mem_swap_usage_y_axis.setTitleBrush(QColor(255, 255, 255, 180))

    ## binding the chartview with the axis
    self.perf_mon_mem_swap_usage_charView.chart().setAxisX(self.perf_mon_mem_swap_usage_x_axis)
    self.perf_mon_mem_swap_usage_charView.chart().setAxisY(self.perf_mon_mem_swap_usage_y_axis)

    self.perf_mon_mem_swap_usage_charView.chart().setBackgroundVisible(False)
    self.perf_mon_mem_swap_usage_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    ## generating the init data here
    self.perf_mon_mem_swap_hist_archive = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                                           0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                                           0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                                           self.perf_mon_mem_swap_usage_y_axis.max()]

    if hasattr(self.cons_repo, 'swap_mem_perc'):
        self.perf_mon_mem_swap_hist_archive.append(float(self.cons_repo.swap_mem_perc))

    ## creating the series data container here.
    if not hasattr(self, 'perf_mon_mem_swap_hist_record'):
        self.perf_mon_mem_swap_hist_record = QLineSeries()
    else:
        self.perf_mon_mem_swap_hist_record.clear()

    mem_swap_hist_data = lineseries_pointer_filler_perc(self, self.perf_mon_mem_swap_hist_archive)

    self.perf_mon_mem_swap_hist_record.append(mem_swap_hist_data)
    # self.perf_mon_mem_swap_hist_record.setName('mem_swap Hist')

    self.perf_mon_mem_swap_usage_charView.chart().addSeries(self.perf_mon_mem_swap_hist_record)
    self.perf_mon_mem_swap_usage_charView.chart().legend().setLabelColor(QColor(255, 255, 255, 180))
    self.perf_mon_mem_swap_usage_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    self.perf_mon_mem_swap_flow_canvas.addWidget(self.perf_mon_mem_swap_usage_charView)
    pass


def activate_dashboard_group(self):
    # print(self.perf_mon_dashboard_canvas.count())
    if self.perf_mon_dashboard_canvas.count() < 3:
        cpu_perf_mon_chart_update(self)
    # print(self.perf_mon_dashboard_canvas.count())
    if self.perf_mon_dashboard_canvas.count() < 3:
        mem_perf_mon_chart_update(self)
    # print(self.perf_mon_dashboard_canvas.count())
    if self.perf_mon_dashboard_canvas.count() < 3:
        sto_perf_mon_chart_update(self)


def content_refresh_helper(self):
    self.perf_page_left_flag = 0
    self.perf_page_refresh_delay = 1
    self.graph_clear_appending_flag = 0

    self.perf_mon_refresh_delay_setter_combo.setCurrentIndex(1)
    update_refresh_delay(self)

    ## bind the page change activity
    par_on_going_leave_page = partial(on_going_leave_page, self)
    self.stackedWidget.currentChanged.connect(par_on_going_leave_page)

    par_caller_refresh_perf_page_dashboard = partial(caller_refresh_perf_page_dashboard, self)
    refr_proc = Thread(target = par_caller_refresh_perf_page_dashboard,
                       name = 'refresh demon dashboard on perf monitor')
    refr_proc.start()

    pass


def on_going_leave_page(self):
    self.perf_page_left_flag = 1
    print('detect page changed. ')
    pass


def caller_refresh_perf_page_dashboard(self):
    while True:
        # print('refresh dashboard')
        if not hasattr(self.cons_repo, 'ip_addr'):
            try:
                ## consider offload these two tasks to a separate thread
                ## so that the task load on the main thread can be eased.
                self.cons_repo.network_property()
            except Exception as err_msg:
                print('error message while trying to call cons_repo: \n', err_msg)
        refresh_perf_page_dashboard(self)
        # try:
        #     refresh_perf_page_dashboard(self)
        # except Exception as err_msg:
        #     print('performance monitor, error message while trying to update the elements: \n', err_msg)
        # print('tend to be sleeping for', self.perf_page_refresh_delay, 'secs. ')
        sleep(float(self.perf_page_refresh_delay))

        ## if the stacked widget got changed, then stop this thread
        if self.perf_page_left_flag == 1:
            print('performance monitor, breaking the refresh thread')
            break
    pass


def space_counter_helper(value):
    ## in MB
    sum_size = int(value)

    if sum_size >= 1024:
        ## in GiB
        sum_size = round(sum_size / 1024, 2)
        postfix = str('TB')
    else:
        sum_size = float(sum_size)
        postfix = str('GB')
    return sum_size, postfix


def refresh_perf_page_dashboard(self):
    ## call the strict mode handler
    perf_mon_strict_mode_handler(self)

    ## fetch necessary values here

    ## network info
    ip_add = self.cons_repo.ip_addr
    gate_way = self.cons_repo.gateway
    dns = self.cons_repo.dns

    ## process counter
    try:
        process_count = len(self.cons_repo.process_list)
        network_count = len(self.cons_repo.network_comm_list)
    except AttributeError as err_msg:
        process_count = 1
        network_count = 1
        print('the backend may still be loading, thus triggered', err_msg)

    ## first fetch the info to be loaded in these charts
    ## cpu info
    cpu_model = self.cons_repo.CPU_model_full
    cpu_core_count_phy = self.cons_repo.CPU_count_physical
    cpu_core_count_logical = self.cons_repo.CPU_count_logical
    if not hasattr(self.cons_repo, 'CPU_perc'):
        self.cons_repo.operating_elapsed_time()
    cpu_perc = self.cons_repo.CPU_perc
    cpu_perc_hd = round(cpu_perc * 100, 2)
    # cpu_perc_per_core = self.cons_repo.CPU_perc_core
    if not hasattr(self.cons_repo, 'CPU_perc_core'):
        self.cons_repo.CPU_monitor()
    cpu_perc_per_core = list(map(lambda x: round((x / 100), 4), self.cons_repo.CPU_perc_core))
    cpu_freq_cur = self.cons_repo.CPU_freq_cur
    cpu_freq_min = self.cons_repo.CPU_freq_min
    cpu_freq_max = self.cons_repo.CPU_freq_max

    ## load information
    load_1_min = self.cons_repo.load_1_min
    load_5_min = self.cons_repo.load_5_min
    load_15_min = self.cons_repo.load_15_min

    ## physical memory
    phy_mem_total = self.cons_repo.phy_mem_total
    phy_mem_perc = self.cons_repo.phy_mem_perc
    phy_mem_perc_hd = round(phy_mem_perc * 100, 2)
    phy_mem_avial = self.cons_repo.phy_mem_avail
    phy_mem_free = self.cons_repo.phy_mem_free

    ## swap memory
    swap_mem_total = self.cons_repo.swap_mem_total
    swap_mem_perc = self.cons_repo.swap_mem_perc
    swap_mem_perc_hd = round(swap_mem_perc * 100, 2)

    ## io status
    sto_total = self.cons_repo.sto_info_total
    sto_perc = self.cons_repo.sto_info_perc
    sto_perc_hd = sto_perc * 100
    sto_used = self.cons_repo.sto_info_used

    ## operating timing count
    up_time_day = int(self.cons_repo.up_time_day)
    up_time_hr = int(self.cons_repo.up_time_hr)
    up_time_min = int(self.cons_repo.up_time_min)

    ## calculating relevant values here
    sto_proc_free_num, sto_proc_free_pf = space_counter_helper(sto_total)
    sto_proc_used_num, sto_proc_used_pf = space_counter_helper(sto_used)

    io_read_count = self.cons_repo.io_info_read_count
    io_write_count = self.cons_repo.io_info_write_count

    network_outflow_count = self.cons_repo.outcome_flow
    network_inflow_count = self.cons_repo.income_flow

    ## updating the performance chart

    ## check if updates are appending
    if self.home_logic_cpu_update_append == 1:
        cpu_core_count = int(self.cons_repo.CPU_count_logical)
        self.perf_mon_cpu_charView.chart().setTitle('%d核心CPU' % cpu_core_count)
        self.home_logic_cpu_update_append = 0

    if self.home_logic_mem_update_append == 1:
        mem_total = self.cons_repo.phy_mem_total
        self.perf_mon_mem_charView.chart().setTitle('内存总量%2.1fGB' % mem_total)
        self.home_logic_mem_update_append = 0

    if self.home_logic_sto_update_append == 1:
        sto_total = self.cons_repo.sto_info_total
        sto_unit = str('GB')

        if sto_total > 1024:
            sto_total = round(sto_total / 1024, 1)
            sto_unit = str('TB')

        self.perf_mon_sto_charView.chart().setTitle('硬盘总量%d%s' % (sto_total, sto_unit))
        self.home_logic_sto_update_append = 0

    ## get relevant variables for the implement of the dashboard

    cpu_usage_perc = float(self.cons_repo.CPU_perc)
    # print(cpu_usage_perc)
    # print(cpu_perc_per_core)
    cpu_free_perc = 1 - cpu_usage_perc
    mem_usage_perc = float(self.cons_repo.phy_mem_perc)
    mem_free_perc = 1 - mem_usage_perc
    # print(mem_usage_perc)
    sto_usage_perc = float(self.cons_repo.sto_info_perc)
    sto_free_perc = 1 - sto_usage_perc

    ## setting the values
    self.perf_mon_cpu_series.slices()[0].setValue(cpu_usage_perc)
    self.perf_mon_cpu_series.slices()[1].setValue(cpu_free_perc)
    self.perf_mon_dashboard_cpu_prompt.setText('%2.1f%%' % cpu_perc_hd)

    self.perf_mon_mem_series.slices()[0].setValue(mem_usage_perc)
    self.perf_mon_mem_series.slices()[1].setValue(mem_free_perc)
    self.perf_mon_dashboard_mem_prompt.setText('%2.1f%%' % phy_mem_perc_hd)

    self.sto_series.slices()[0].setValue(sto_usage_perc)
    self.sto_series.slices()[1].setValue(sto_free_perc)
    self.perf_mon_dashboard_sto_prompt.setText('%2.1f%%' % sto_perc_hd)

    ## refreshing the content in the detailed button
    # self.perf_mon_gen_info.setText('IP地址 %s\n网关 %s\n启用的DNS %s\n进程数 %d 网络连接数 %d\nCPU型号 %s\n'
    #                                '物理内存总量 %2.2fGB\n物理内存可用 %2.2fGB\n物理内存空闲 %2.2fGB\n'
    #                                '虚拟内存总量 %2.2fGB\n虚拟内存可用 %2.2fGB\n'
    #                                '硬盘总量 %2.2f%s\n硬盘空闲率 %s%%'
    #                                % (ip_add, gate_way, dns, process_count, network_count, cpu_model,
    #                                   phy_mem_total, phy_mem_avial, phy_mem_free, swap_mem_total, swap_mem_perc,
    #                                   sto_proc_free_num, sto_proc_free_pf, sto_perc))
    # self.perf_mon_gen_info.setText('IP地址 %s\n网关 %s\n启用的DNS %s\n进程数 %d 网络连接数 %d\n'
    #                                '物理内存总量 %2.2fGB\n物理内存可用 %2.2fGB\n'
    #                                '硬盘总量 %2.2f%s\n硬盘空闲率 %s%%'
    #                                % (ip_add, gate_way, dns, process_count, network_count,
    #                                   phy_mem_total, phy_mem_avial,
    #                                   sto_proc_free_num, sto_proc_free_pf, sto_perc))
    self.perf_mon_gen_info.setText('IP地址 %s\n网关 %s\n启用的DNS %s\n'
                                   '物理内存总量 %2.2fGB\n物理内存可用 %2.2fGB\n'
                                   '硬盘总量 %2.2f%s'
                                   % (ip_add, gate_way, dns,
                                      phy_mem_total, phy_mem_avial,
                                      sto_proc_free_num, sto_proc_free_pf))

    # print('CPU型号 %s' % (cpu_model))
    # print('CPU物理核心数 %d核' % (cpu_core_count_phy))
    # print('逻辑核心数 %d核' % (cpu_core_count_logical))
    # print('CPU当前占用 %2.2f%% ' % (cpu_perc_hd))
    # print('分核心占用\n%s' % (cpu_perc_per_core))
    # print('CPU当前频率 %2.2f MHz' % (cpu_freq_cur))
    # print('CPU最小频率 %2.2f' % (cpu_freq_min))
    # print('CPU最大频率 %2.2f' % (cpu_freq_max))

    self.perf_mon_hardware_cpu_spec_demo.setText('CPU型号 %s\nCPU物理核心数 %d核；逻辑核心数 %d核\n'
                                                 'CPU当前占用 %2.2f%% \n 分核心占用\n%s\n'
                                                 'CPU当前频率 %2.2f MHz\nCPU最小/最大频率 %2.2f, %2.2f MHz\n'
                                                 % (cpu_model, cpu_core_count_phy, cpu_core_count_logical,
                                                    cpu_perc_hd, cpu_perc_per_core, cpu_freq_cur,
                                                    cpu_freq_min, cpu_freq_max))

    self.perf_mon_hardware_mem_spec_demo.setText('一分钟/五分钟/十五分钟负载\n %s/%s/%s\n'
                                                 '运行时间 %d天%d时%d分\n'
                                                 '物理内存总量 %2.2fGB\n物理内存可用 %2.2fGB (%2.1f%%)\n物理内存空闲 %2.2fGB\n'
                                                 '虚拟内存总量 %2.2fGB\n虚拟内存可用 %2.1f%%\n'
                                                 % (load_1_min, load_5_min, load_15_min, up_time_day, up_time_hr,
                                                    up_time_min, phy_mem_total, phy_mem_avial, phy_mem_perc_hd,
                                                    phy_mem_free, swap_mem_total, swap_mem_perc_hd))

    self.perf_mon_hardware_sto_spec_demo.setText('硬盘总量 %2.2f%s，已用 %2.2f%s (%2.2f%%)\n'
                                                 'IO总写入/总读取 %2.2fGB, %2.2fGB\n'
                                                 'IP地址 %s\n网关 %s\n启用的DNS %s\n'
                                                 '网卡总发送/接收 %2.2fGB, %2.2fGB'
                                                 % (sto_proc_free_num, sto_proc_free_pf, sto_proc_used_num,
                                                    sto_proc_used_pf, sto_perc_hd, io_write_count, io_read_count,
                                                    ip_add, gate_way, dns, network_outflow_count, network_inflow_count))

    ## refresh the information in the network flow chart
    if self.graph_clear_appending_flag == 0:
        on_called_graph_chart_clean(self)

    network_flow_chart_refresh(self)

    cpu_usage_line_graph_refresh(self)

    mem_usage_line_graph_refresh(self)

    mem_swap_usage_line_graph_refresh(self)

    pass


def on_called_graph_chart_clean(self):
    ## prepare the series
    for append_iter in range(21):
        self.perf_mon_uplink_archive.append(0)
        self.perf_mon_downlink_archive.append(0)
        self.perf_mon_cpu_hist_archive.append(0)
        self.perf_mon_mem_hist_archive.append(0)
        self.perf_mon_mem_swap_hist_archive.append(0)

    ## network flow chart
    # for append_iter in range(21):
    #     self.perf_mon_uplink_archive.append(0)

    if len(self.perf_mon_uplink_archive) > 30:
        self.perf_mon_uplink_archive = self.perf_mon_uplink_archive[-30:]

    uplink_point_list = lineseries_pointer_filler(self, self.perf_mon_uplink_archive)
    self.perf_mon_uplink_record.clear()
    self.perf_mon_uplink_record.append(uplink_point_list)

    # for append_iter in range(21):
    #     self.perf_mon_downlink_archive.append(0)

    if len(self.perf_mon_downlink_archive) > 30:
        self.perf_mon_downlink_archive = self.perf_mon_downlink_archive[-30:]

    downlink_point_list = lineseries_pointer_filler(self, self.perf_mon_downlink_archive)
    self.perf_mon_downlink_record.clear()
    self.perf_mon_downlink_record.append(downlink_point_list)

    ## cpu flow chart
    # for append_iter in range(21):
    #     self.perf_mon_cpu_hist_archive.append(0)

    if len(self.perf_mon_cpu_hist_archive) > 30:
        self.perf_mon_cpu_hist_archive = self.perf_mon_cpu_hist_archive[-30:]

    cpu_hist_data = lineseries_pointer_filler_perc(self, self.perf_mon_cpu_hist_archive)
    self.perf_mon_cpu_hist_record.clear()
    self.perf_mon_cpu_hist_record.append(cpu_hist_data)

    ## mem flow chart
    # for append_iter in range(21):
    #     self.perf_mon_mem_hist_archive.append(0)

    if len(self.perf_mon_mem_hist_archive) > 30:
        self.perf_mon_mem_hist_archive = self.perf_mon_mem_hist_archive[-30:]

    mem_hist_data = lineseries_pointer_filler_perc(self, self.perf_mon_mem_hist_archive)
    self.perf_mon_mem_hist_record.clear()
    self.perf_mon_mem_hist_record.append(mem_hist_data)

    ## swap mem flow chart
    # for append_iter in range(21):
    #     self.perf_mon_mem_swap_hist_archive.append(0)

    if len(self.perf_mon_mem_swap_hist_archive) > 30:
        self.perf_mon_mem_swap_hist_archive = self.perf_mon_mem_swap_hist_archive[-30:]

    mem_swap_hist_data = lineseries_pointer_filler_perc(self, self.perf_mon_mem_swap_hist_archive)
    self.perf_mon_mem_swap_hist_record.clear()
    self.perf_mon_mem_swap_hist_record.append(mem_swap_hist_data)

    ## setting the var
    self.graph_clear_appending_flag = 1


def network_flow_chart_refresh(self):
    #### if the current self.perf_page_refresh_delay is smaller than
    #### the update frequency in the base thread, then call the update function.
    if self.perf_page_refresh_delay <= float(self.cons_repo.ins_freq):
        self.cons_repo.network_monitor()

    ## to check if the y axis should be scaled here
    series_len = len(self.perf_mon_uplink_record)
    uplink_max_value = max(self.perf_mon_uplink_archive[-series_len:])
    downlink_max_value = max(self.perf_mon_downlink_archive[-series_len:])
    record_max_value = max(uplink_max_value, downlink_max_value)
    # print('web flow info', series_len, type(series_len), record_max_value)
    # print('record max', record_max_value)

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
    self.perf_mon_uplink_archive.append(self.cons_repo.uplink_spd)

    if len(self.perf_mon_uplink_archive) > 30:
        self.perf_mon_uplink_archive = self.perf_mon_uplink_archive[-30:]

    uplink_point_list = lineseries_pointer_filler(self, self.perf_mon_uplink_archive)
    self.perf_mon_uplink_record.clear()
    self.perf_mon_uplink_record.append(uplink_point_list)

    ## updating the downlink info
    self.perf_mon_downlink_archive.append(self.cons_repo.downlink_spd)

    if len(self.perf_mon_downlink_archive) > 30:
        self.perf_mon_downlink_archive = self.perf_mon_downlink_archive[-30:]

    downlink_point_list = lineseries_pointer_filler(self, self.perf_mon_downlink_archive)
    self.perf_mon_downlink_record.clear()
    self.perf_mon_downlink_record.append(downlink_point_list)

    pass


def cpu_usage_line_graph_refresh(self):
    if self.perf_page_refresh_delay <= float(self.cons_repo.ins_freq):
        self.cons_repo.CPU_load_monitor_lite()

    ## no need to scale the y axis
    ## updating the usage information here
    self.perf_mon_cpu_hist_archive.append(float(self.cons_repo.CPU_perc))

    if len(self.perf_mon_cpu_hist_archive) > 30:
        self.perf_mon_cpu_hist_archive = self.perf_mon_cpu_hist_archive[-30:]
        # print('truncation activated. ')

    cpu_hist_data = lineseries_pointer_filler_perc(self, self.perf_mon_cpu_hist_archive)
    self.perf_mon_cpu_hist_record.clear()
    self.perf_mon_cpu_hist_record.append(cpu_hist_data)

    pass


def mem_usage_line_graph_refresh(self):
    if self.perf_page_refresh_delay <= float(self.cons_repo.ins_freq):
        self.cons_repo.mem_load_monitor_lite()

    ## no need to scale the y axis
    ## updating the usage information here
    self.perf_mon_mem_hist_archive.append(float(self.cons_repo.phy_mem_perc))

    if len(self.perf_mon_mem_hist_archive) > 30:
        self.perf_mon_mem_hist_archive = self.perf_mon_mem_hist_archive[-30:]

    mem_hist_data = lineseries_pointer_filler_perc(self, self.perf_mon_mem_hist_archive)
    self.perf_mon_mem_hist_record.clear()
    self.perf_mon_mem_hist_record.append(mem_hist_data)


def mem_swap_usage_line_graph_refresh(self):
    if self.perf_page_refresh_delay <= float(self.cons_repo.ins_freq):
        self.cons_repo.mem_virtual_load_monitor_lite()

    ## no need to scale the y axis
    ## updating the usage information here
    self.perf_mon_mem_swap_hist_archive.append(float(self.cons_repo.swap_mem_perc))

    if len(self.perf_mon_mem_swap_hist_archive) > 30:
        self.perf_mon_mem_swap_hist_archive = self.perf_mon_mem_swap_hist_archive[-30:]

    mem_swap_hist_data = lineseries_pointer_filler_perc(self, self.perf_mon_mem_swap_hist_archive)
    self.perf_mon_mem_swap_hist_record.clear()
    self.perf_mon_mem_swap_hist_record.append(mem_swap_hist_data)
    pass


def cpu_perf_mon_chart_update(self):
    ## define the chartview widget
    self.perf_mon_cpu_charView = QChartView(self)
    # self.perf_mon_cpu_charView = QChartViewHomeDashboard(self)
    self.perf_mon_cpu_charView.setRenderHints(QtGui.QPainter.Antialiasing)
    # self.perf_mon_cpu_charView.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    ## setting the visual effects
    self.perf_mon_cpu_charView.chart().setBackgroundVisible(False)
    # self.cpu_charView.chart().legend().setVisible(False)
    self.perf_mon_cpu_charView.chart().legend().setAlignment(Qt.AlignBottom)
    self.perf_mon_cpu_charView.chart().legend().setLabelColor(QColor(255, 255, 255, 180))
    self.perf_mon_cpu_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    font = QtGui.QFont()
    font.setPixelSize(16)
    font.setPointSize(16)

    self.perf_mon_cpu_charView.chart().setTitleFont(font)
    self.perf_mon_cpu_charView.chart().setTitleBrush(QColor(255, 255, 255, 180))

    ## prepare for data
    if hasattr(self.cons_repo, 'cpu_core_count'):
        cpu_core_count = int(self.cons_repo.CPU_count_logical)
        cpu_usage_perc = float(self.cons_repo.CPU_perc)
        cpu_free_perc = 1 - cpu_usage_perc
    else:
        cpu_core_count = int(2)
        cpu_usage_perc = float(0.2)
        cpu_free_perc = 1 - cpu_usage_perc
        self.home_logic_cpu_update_append = 1

    ## set the series for cpu
    self.perf_mon_cpu_series = QPieSeries()
    self.perf_mon_cpu_series.setHoleSize(0.7)
    # self.perf_mon_cpu_series.setPieSize(0.63)
    self.perf_mon_cpu_series.setPieSize(0.89)
    self.perf_mon_cpu_series.append('使用', cpu_usage_perc)
    self.perf_mon_cpu_series.append('空闲', cpu_free_perc)

    ## stylish the information of usage
    ## Pen changes the color of the border
    ## Brush changes the color filling the chart
    cpu_usage_slice = self.perf_mon_cpu_series.slices()[0]
    # cpu_usage_slice.setLabelFont()
    # cpu_usage_slice.setLabelVisible(True)
    cpu_usage_slice.setPen(QtGui.QPen(QColor(37, 226, 119, 220), 5))
    cpu_usage_slice.setBrush(QColor(85, 255, 158, 200))
    # cpu_usage_slice.setExploded()

    ## stylish the information of free
    cpu_free_slice = self.perf_mon_cpu_series.slices()[1]
    # cpu_free_slice.setLabelVisible(True)
    # cpu_free_slice.setLabelPosition(QPieSlice.LabelOutside)
    cpu_free_slice.setPen(QtGui.QPen(QColor(81, 85, 133, 150), 7))
    cpu_free_slice.setBrush(QColor(120, 110, 126, 210))
    # cpu_free_slice.setExploded()

    self.perf_mon_cpu_charView.chart().addSeries(self.perf_mon_cpu_series)
    # self.perf_mon_cpu_charView.chart().legend().setVisible(False)

    self.perf_mon_cpu_charView.chart().setTitle('%d核心CPU' % cpu_core_count)

    self.perf_mon_dashboard_canvas.addWidget(self.perf_mon_cpu_charView)

    self.perf_mon_dashboard_cpu_prompt.move(97, 115)
    self.perf_mon_dashboard_cpu_prompt.setText(' ')
    self.perf_mon_dashboard_cpu_prompt.setStyleSheet('QPushButton {\n'
                                                     'background-position: center; \n'
                                                     'background-repeat: no-repeat; \n'
                                                     'border: none; \n'
                                                     'background: transparent; \n'
                                                     'font: 22pt "Noto Mono"; \n'
                                                     'color: rgba(255, 255, 255, 170); \n'
                                                     'font-weight: bold; \n'
                                                     '}')
    self.perf_mon_dashboard_cpu_prompt.setGraphicsEffect(self.blur_effect)

    pass


def mem_perf_mon_chart_update(self):
    ## define the chartview widget
    self.perf_mon_mem_charView = QChartView(self)
    # self.perf_mon_mem_charView = QChartViewHomeDashboard(self)
    self.perf_mon_mem_charView.setRenderHints(QtGui.QPainter.Antialiasing)
    # self.perf_mon_mem_charView.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    ## setting the visual effects
    self.perf_mon_mem_charView.chart().setBackgroundVisible(False)
    # self.mem_charView.chart().legend().setVisible(False)
    self.perf_mon_mem_charView.chart().legend().setAlignment(Qt.AlignBottom)
    self.perf_mon_mem_charView.chart().legend().setLabelColor(QColor(255, 255, 255, 180))
    self.perf_mon_mem_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    font = QtGui.QFont()
    font.setPixelSize(16)
    font.setPointSize(16)

    self.perf_mon_mem_charView.chart().setTitleFont(font)
    self.perf_mon_mem_charView.chart().setTitleBrush(QColor(255, 255, 255, 180))

    ## prepare for data
    if hasattr(self.cons_repo, 'phy_mem_total'):
        mem_total = self.cons_repo.phy_mem_total
        mem_usage_perc = float(self.cons_repo.phy_mem_perc)
        mem_free_perc = 1 - mem_usage_perc
    else:
        mem_total = int(8)
        mem_usage_perc = float(0.51)
        mem_free_perc = 1 - mem_usage_perc
        self.home_logic_mem_update_append = 1

    ## set the series for memory
    self.perf_mon_mem_series = QPieSeries()
    self.perf_mon_mem_series.setHoleSize(0.7)
    self.perf_mon_mem_series.setPieSize(0.89)
    # self.perf_mon_mem_series.setPieSize(0.63)
    self.perf_mon_mem_series.append('使用', mem_usage_perc)
    self.perf_mon_mem_series.append('空闲', mem_free_perc)

    ## stylish the information of usage
    ## Pen changes the color of the border
    ## Brush changes the color filling the chart
    mem_usage_slice = self.perf_mon_mem_series.slices()[0]
    # mem_usage_slice.setLabelVisible(True)
    mem_usage_slice.setPen(QtGui.QPen(QColor(37, 226, 119, 220), 5))
    mem_usage_slice.setBrush(QColor(85, 255, 158, 200))
    # mem_usage_slice.setExploded()

    ## stylish the information of free
    mem_free_slice = self.perf_mon_mem_series.slices()[1]
    # mem_free_slice.setLabelVisible(True)
    mem_free_slice.setPen(QtGui.QPen(QColor(81, 85, 133, 150), 7))
    mem_free_slice.setBrush(QColor(120, 110, 126, 210))
    # mem_free_slice.setExploded()

    self.perf_mon_mem_charView.chart().addSeries(self.perf_mon_mem_series)
    # self.perf_mon_mem_charView.chart().setBackgroundVisible(False)
    # self.perf_mon_mem_charView.chart().legend().setVisible(False)
    self.perf_mon_mem_charView.chart().setTitle('内存总量%2.1fGB' % mem_total)

    self.perf_mon_dashboard_canvas.addWidget(self.perf_mon_mem_charView)

    self.perf_mon_dashboard_mem_prompt.move(387, 115)
    self.perf_mon_dashboard_mem_prompt.setText(' ')
    self.perf_mon_dashboard_mem_prompt.setStyleSheet('QPushButton {\n'
                                                     'background-position: center; \n'
                                                     'background-repeat: no-repeat; \n'
                                                     'border: none; \n'
                                                     'background: transparent; \n'
                                                     'font: 22pt "Noto Mono"; \n'
                                                     'color: rgba(255, 255, 255, 170); \n'
                                                     'font-weight: bold; \n'
                                                     '}')
    self.perf_mon_dashboard_mem_prompt.setGraphicsEffect(self.blur_effect)

    pass


def sto_perf_mon_chart_update(self):
    ## define the chartview widget

    self.perf_mon_sto_charView = QChartView(self)
    # self.perf_mon_sto_charView = QChartViewHomeDashboard(self)
    self.perf_mon_sto_charView.setRenderHints(QtGui.QPainter.Antialiasing)
    # self.perf_mon_sto_charView.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    ## setting the visual effects
    self.perf_mon_sto_charView.chart().setBackgroundVisible(False)
    # self.sto_charView.chart().legend().setVisible(False)
    self.perf_mon_sto_charView.chart().legend().setAlignment(Qt.AlignBottom)
    self.perf_mon_sto_charView.chart().legend().setLabelColor(QColor(255, 255, 255, 180))
    self.perf_mon_sto_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    font = QtGui.QFont()
    font.setPixelSize(16)
    font.setPointSize(16)

    self.perf_mon_sto_charView.chart().setTitleFont(font)
    self.perf_mon_sto_charView.chart().setTitleBrush(QColor(255, 255, 255, 180))

    ## prepare for data
    if hasattr(self.cons_repo, 'phy_sto_total'):
        sto_total = self.cons_repo.sto_info_total
        sto_usage_perc = float(self.cons_repo.sto_info_perc)
        sto_free_perc = 1 - sto_usage_perc
        sto_unit = str('GB')

        if sto_total > 1024:
            sto_total = round(sto_total / 1024, 1)
            sto_unit = str('TB')
    else:
        sto_total = int(500)
        sto_usage_perc = float(0.3)
        sto_free_perc = 1 - sto_usage_perc
        sto_unit = str('GB')
        self.home_logic_sto_update_append = 1

    ## set the series for stoory
    self.sto_series = QPieSeries()
    self.sto_series.setHoleSize(0.7)
    # self.sto_series.setPieSize(0.63)
    self.sto_series.setPieSize(0.89)
    self.sto_series.append('使用', sto_usage_perc)
    self.sto_series.append('空闲', sto_free_perc)

    ## stylish the information of usage
    ## Pen changes the color of the border
    ## Brush changes the color filling the chart
    sto_usage_slice = self.sto_series.slices()[0]
    # sto_usage_slice.setLabelVisible(True)
    sto_usage_slice.setPen(QtGui.QPen(QColor(37, 226, 119, 220), 5))
    sto_usage_slice.setBrush(QColor(85, 255, 158, 200))
    # sto_usage_slice.setExploded()

    ## stylish the information of free
    sto_free_slice = self.sto_series.slices()[1]
    # sto_free_slice.setLabelVisible(True)
    sto_free_slice.setPen(QtGui.QPen(QColor(81, 85, 133, 150), 7))
    sto_free_slice.setBrush(QColor(120, 110, 126, 210))
    # sto_free_slice.setExploded()

    self.perf_mon_sto_charView.chart().addSeries(self.sto_series)
    # self.perf_mon_sto_charView.chart().setBackgroundVisible(False)
    # self.perf_mon_sto_charView.chart().legend().setVisible(False)
    self.perf_mon_sto_charView.chart().setTitle('硬盘总量%d%s' % (sto_total, sto_unit))

    font = QtGui.QFont()
    font.setPixelSize(16)
    font.setPointSize(16)
    self.perf_mon_sto_charView.chart().setTitleFont(font)

    self.perf_mon_dashboard_canvas.addWidget(self.perf_mon_sto_charView)

    self.perf_mon_dashboard_sto_prompt.move(673, 115)
    self.perf_mon_dashboard_sto_prompt.setText(' ')
    self.perf_mon_dashboard_sto_prompt.setStyleSheet('QPushButton {\n'
                                                     'background-position: center; \n'
                                                     'background-repeat: no-repeat; \n'
                                                     'border: none; \n'
                                                     'background: transparent; \n'
                                                     'font: 22pt "Noto Mono"; \n'
                                                     'color: rgba(255, 255, 255, 170); \n'
                                                     'font-weight: bold; \n'
                                                     '}')
    self.perf_mon_dashboard_sto_prompt.setGraphicsEffect(self.blur_effect)

    pass


def perf_mon_page_settings(self):
    par_perf_mon_page_settings_applier = partial(perf_mon_page_settings_applier, self)

    for key, value in self.__dict__.items():
        if key.startswith('perf_mon_set_'):
            getattr(self, key).clicked.connect(par_perf_mon_page_settings_applier)
            getattr(self, key).setChecked(True)

    pass


def perf_mon_page_settings_applier(self):
    ## use setattr to sync the status of these flags
    setattr(self.cons_repo, 'repo_CPU_flag', self.perf_mon_set_cpu.isChecked())
    setattr(self.cons_repo, 'repo_process_list_flag', self.perf_mon_set_proc_list.isChecked())
    setattr(self.cons_repo, 'repo_network_list_flag', self.perf_mon_set_network_list.isChecked())
    setattr(self.cons_repo, 'repo_storage_flag', self.perf_mon_set_storage.isChecked())
    setattr(self.cons_repo, 'repo_network_adapter_flag', self.perf_mon_set_net_adapt.isChecked())
    setattr(self.cons_repo, 'repo_phy_memory_flag', self.perf_mon_set_phy_mem.isChecked())
    setattr(self.cons_repo, 'repo_swap_memory_flag', self.perf_mon_set_swap_mem.isChecked())
    setattr(self.cons_repo, 'repo_sys_load_flag', self.perf_mon_set_sys_load.isChecked())
    setattr(self.cons_repo, 'repo_boot_time_flag', self.perf_mon_set_boot_time.isChecked())

    pass


def perf_mon_strict_mode_handler(self):
    strict_mode_var = self.cons_repo.strict_mode
    # print('perf mon strict mode', strict_mode_var)

    if strict_mode_var:
        perf_mon_strict_mode_applier(self)
    pass


def perf_mon_strict_mode_simulator(self):
    self.cons_repo.strict_mode = True
    self.perf_mon_strict_mode_trigger.setVisible(False)
    self.perf_mon_base_tabwidget.setTabText(2, '特殊模式')
    pass


def perf_mon_strict_mode_applier(self):
    self.perf_mon_report_setting_promt.setText('由于国产信创主机现处于部署初期，维护人员需要基于终端的运行指标进行状态分析。\n'
                                               '基于这样的需求，信创主机默认会上报硬件相关的非隐私数据支撑这一目标。\n'
                                               '\n'
                                               '受限于管理员下发的配置策略，此页面中的设置参数暂时无法进行调整，请您谅解。\n'
                                               '若您确信管理员已经调整过配置策略，烦请重新启动电脑后再试。\n\n'
                                               'Adjustments under this specific page are currently unavailable. \n'
                                               'Please contact with the IT dept for more information. ')
    self.perf_mon_report_setting_promt.move(20, 160)
    self.perf_mon_report_setting_promt.setMinimumSize(831, 220)
    self.perf_mon_report_setting_promt.setStyleSheet('font: 16pt "Noto Mono"; \n'
                                                     'color: rgb(250, 250, 250);')

    self.perf_mon_set_cpu.setVisible(False)
    self.perf_mon_set_proc_list.setVisible(False)
    self.perf_mon_set_network_list.setVisible(False)
    self.perf_mon_set_storage.setVisible(False)
    self.perf_mon_set_net_adapt.setVisible(False)
    self.perf_mon_set_phy_mem.setVisible(False)
    self.perf_mon_set_swap_mem.setVisible(False)
    self.perf_mon_set_sys_load.setVisible(False)
    self.perf_mon_set_boot_time.setVisible(False)
    pass
