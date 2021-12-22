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
from time import time, sleep, strftime, localtime
from threading import Thread

## import utilities here

## import resources files here
sys.path.append('..')
from UI import ui_image_assets


def home_page_caller(self):
    print('some time reminds yourself a thing. ')
    print("perhaps. that's not how things are working. ")

    ## set the top bar greetings here
    greetings_preparation(self)

    ## set the visual effects of the three buttons on the home page.
    visual_home_sub_stat_group(self)

    ## set the visual effects of the button dashboard group
    visual_home_dashboard_group(self)

    content_refresh_helper(self)
    pass


def greetings_preparation(self):
    self.home_greeting_prompt.setGraphicsEffect(self.blur_effect)

    current_hour = localtime(time()).tm_hour
    if hasattr(self, 'home_greeting_prompt'):
        if (current_hour >= 7) & (current_hour < 10):
            self.home_greeting_prompt.setText('早上好。祝您工作顺利！')
        elif (current_hour >= 10) & (current_hour < 15):
            self.home_greeting_prompt.setText('午间光照较为强烈，记得及时补充水分。')
        elif (current_hour >= 15) & (current_hour < 18):
            self.home_greeting_prompt.setText('到下午了，定时活动活动身体~')
        elif (current_hour >= 18) & (current_hour < 21):
            self.home_greeting_prompt.setText('呼呼，到晚上啦，注意身体哟。')
        elif (current_hour >= 21) & (current_hour <= 23):
            self.home_greeting_prompt.setText('夜深了，提前祝您晚安。')
        else:
            self.home_greeting_prompt.setText('工作之余也请注意休息！')
    pass


def visual_home_sub_stat_group(self):
    ## init the dashboard mask
    ## so that the clickable area is narrowed down.
    dashboard_mask_init(self)

    ## changing the visual effects of the three elements on the home page
    ## for the sub stat 1
    self.home_sub_stat_1.setFlat(True)
    self.home_sub_stat_1.setText('主机IP 地址 \n\n\n 电脑运行时间 \n ')
    # self.home_sub_stat_1.setText('主机IP 地址 \n 载入中 \n\n 电脑运行时间 \n 载入中')
    self.home_sub_stat_1.setStyleSheet('QPushButton \n'
                                       '{font-size:16pt; \n'
                                       'color: rgb(255, 255, 255); \n'
                                       'border-image: url(":/images/Home_Page/Home_Sub1_Pure_Background.png"); \n'
                                       'border-radius: 12px; \n}')
    # 'border-image: url(":/images/Home_Page/Home_Sub1_Background.png"); \n}')
    # 'border-image: url(":/images/Home_Page/u269.png"); \n}')
    self.home_sub_stat_1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    # self.home_sub_stat_1.setAutoFillBackground(True)
    par_on_click_home_sub_stat_1 = partial(on_click_home_sub_stat_1, self)
    self.home_sub_stat_1.clicked.connect(par_on_click_home_sub_stat_1)

    ## for the sub stat 2
    self.home_sub_stat_2.setFlat(True)
    self.home_sub_stat_2.setText('    软件包总数 \n \n ')
    # self.home_sub_stat_2.setText('软件总数 \n 载入中')
    self.home_sub_stat_2.setIcon(QIcon(':/images/Home_Page/Home_Sub2_Alpha.png'))
    self.home_sub_stat_2.setIconSize(QtCore.QSize(105, 105))
    # self.home_sub_stat_2.setIcon(QIcon(':/images/Home_Page/u264.png'))
    # self.home_sub_stat_2.setIconSize(QtCore.QSize(85, 85))
    self.home_sub_stat_2.setLayoutDirection(Qt.RightToLeft)
    self.home_sub_stat_2.setStyleSheet('QPushButton \n'
                                       '{font-size:16pt; \n'
                                       'color: rgb(255, 255, 255); \n'
                                       'border-image: url(":/images/Home_Page/Home_Sub2_Pure_Background.png"); \n'
                                       'border-radius: 12px; \n}')
    # 'border-image: url(":/images/Home_Page/Home_Sub2_Background.png"); \n}')
    # 'border-image: url(":/images/Home_Page/u220.png"); \n}')
    self.home_sub_stat_2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    par_on_click_home_sub_stat_2 = partial(on_click_home_sub_stat_2, self)
    self.home_sub_stat_2.clicked.connect(par_on_click_home_sub_stat_2)

    ## for the sub stat 3
    self.home_sub_stat_3.setFlat(True)
    self.home_sub_stat_3.setText('    健康度 \n \n ')
    # self.home_sub_stat_3.setText('健康度 \n 待评估')
    self.home_sub_stat_3.setIcon(QIcon(':/images/Home_Page/Home_Sub3_Alpha.png'))
    self.home_sub_stat_3.setIconSize(QtCore.QSize(95, 95))
    # self.home_sub_stat_3.setIcon(QIcon(':/images/Home_Page/u268.png'))
    # self.home_sub_stat_3.setIconSize(QtCore.QSize(85, 85))
    self.home_sub_stat_3.setLayoutDirection(Qt.RightToLeft)
    self.home_sub_stat_3.setStyleSheet('QPushButton \n'
                                       '{font-size:16pt; \n'
                                       'color: rgb(255, 255, 255); \n'
                                       'border-image: url(":/images/Home_Page/Home_Sub3_Pure_Background.png"); \n'
                                       'border-radius: 12px; \n}')
    # 'border-image: url(":/images/Home_Page/Home_Sub3_Background.png");}')
    # 'border-image: url(":/images/Home_Page/u265.png");}')
    self.home_sub_stat_3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    par_on_click_home_sub_stat_3 = partial(on_click_home_sub_stat_3, self)
    self.home_sub_stat_3.clicked.connect(par_on_click_home_sub_stat_3)

    ## filler text
    self.home_sub_filler_text_ip.move(20, 165)
    self.home_sub_filler_text_ip.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    self.home_sub_filler_text_ip.clicked.connect(par_on_click_home_sub_stat_1)
    self.home_sub_filler_text_ip.setStyleSheet('QPushButton {\n'
                                               'background-position: center; \n'
                                               'background-repeat: no-repeat; \n'
                                               'border: none; \n'
                                               'background: transparent; \n'
                                               'font: 22pt "Noto Mono"; \n'
                                               'color: rgb(255, 255, 255); \n'
                                               'font-weight: bold; \n'
                                               '}')

    self.home_sub_filler_text_operate_time.move(15, 245)
    self.home_sub_filler_text_operate_time.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    self.home_sub_filler_text_operate_time.clicked.connect(par_on_click_home_sub_stat_1)
    self.home_sub_filler_text_operate_time.setStyleSheet('QPushButton {\n'
                                                         'background-position: center; \n'
                                                         'background-repeat: no-repeat; \n'
                                                         'border: none; \n'
                                                         'background: transparent; \n'
                                                         'font: 22pt "Noto Mono"; \n'
                                                         'color: rgb(255, 255, 255); \n'
                                                         'font-weight: bold; \n'
                                                         '}')

    self.home_sub_filler_text_software_num.move(300, 195)
    self.home_sub_filler_text_software_num.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    self.home_sub_filler_text_software_num.clicked.connect(par_on_click_home_sub_stat_2)
    self.home_sub_filler_text_software_num.setStyleSheet('QPushButton {\n'
                                                         'background-position: center; \n'
                                                         'background-repeat: no-repeat; \n'
                                                         'border: none; \n'
                                                         'background: transparent; \n'
                                                         'font: 28pt "Noto Mono"; \n'
                                                         'color: rgb(255, 255, 255); \n'
                                                         'font-weight: bold; \n'
                                                         '}')

    self.home_sub_filler_text_health_score.move(583, 195)
    self.home_sub_filler_text_health_score.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    self.home_sub_filler_text_health_score.clicked.connect(par_on_click_home_sub_stat_3)
    self.home_sub_filler_text_health_score.setStyleSheet('QPushButton {\n'
                                                         'background-position: center; \n'
                                                         'background-repeat: no-repeat; \n'
                                                         'border: none; \n'
                                                         'background: transparent; \n'
                                                         'font: 28pt "Noto Mono"; \n'
                                                         'color: rgb(255, 255, 255); \n'
                                                         'font-weight: bold; \n'
                                                         '}')

    self.home_sub_filler_text_ip.setGraphicsEffect(self.blur_effect)
    self.home_sub_filler_text_operate_time.setGraphicsEffect(self.blur_effect)
    self.home_sub_filler_text_software_num.setGraphicsEffect(self.blur_effect)
    self.home_sub_filler_text_health_score.setGraphicsEffect(self.blur_effect)

    pass


def dashboard_mask_init(self):
    self.home_dashboard_mask_top.setFlat(True)
    self.home_dashboard_mask_top.setDisabled(True)
    self.home_dashboard_mask_top.setStyleSheet('QPushButton \n'
                                               '{font-size:16pt; \n'
                                               'color: rgba(255, 255, 255, 0); \n'
                                               'background: transparent; \n}')

    self.home_dashboard_mask_bottom.setFlat(True)
    self.home_dashboard_mask_bottom.setDisabled(True)
    self.home_dashboard_mask_bottom.setStyleSheet('QPushButton \n'
                                                  '{font-size:16pt; \n'
                                                  'color: rgba(255, 255, 255, 0); \n'
                                                  'background: transparent; \n}')

    self.home_dashboard_mask_left.setFlat(True)
    self.home_dashboard_mask_left.setDisabled(True)
    self.home_dashboard_mask_left.setStyleSheet('QPushButton \n'
                                                '{font-size:16pt; \n'
                                                'color: rgba(255, 255, 255, 0); \n'
                                                'background: transparent; \n}')

    self.home_dashboard_mask_right.setFlat(True)
    self.home_dashboard_mask_right.setDisabled(True)
    self.home_dashboard_mask_right.setStyleSheet('QPushButton \n'
                                                 '{font-size:16pt; \n'
                                                 'color: rgba(255, 255, 255, 0); \n'
                                                 'background: transparent; \n}')

    self.home_dashboard_mask_middle_1.setFlat(True)
    self.home_dashboard_mask_middle_1.setDisabled(True)
    self.home_dashboard_mask_middle_1.setStyleSheet('QPushButton \n'
                                                    '{font-size:16pt; \n'
                                                    'color: rgba(255, 255, 255, 0); \n'
                                                    'background: transparent; \n}')

    self.home_dashboard_mask_middle_2.setFlat(True)
    self.home_dashboard_mask_middle_2.setDisabled(True)
    self.home_dashboard_mask_middle_2.setStyleSheet('QPushButton \n'
                                                    '{font-size:16pt; \n'
                                                    'color: rgba(255, 255, 255, 0); \n'
                                                    'background: transparent; \n}')

    # self.home_sub_stat_3.setFlat(True)
    # self.home_sub_stat_3.setText('健康度 \n \n ')
    # # self.home_sub_stat_3.setText('健康度 \n 待评估')
    # self.home_sub_stat_3.setIcon(QIcon(':/images/Home_Page/Home_Sub3_Alpha.png'))
    # self.home_sub_stat_3.setIconSize(QtCore.QSize(95, 95))
    # # self.home_sub_stat_3.setIcon(QIcon(':/images/Home_Page/u268.png'))
    # # self.home_sub_stat_3.setIconSize(QtCore.QSize(85, 85))
    # self.home_sub_stat_3.setLayoutDirection(Qt.RightToLeft)
    # self.home_sub_stat_3.setStyleSheet('QPushButton \n'
    #                                    '{font-size:16pt; \n'
    #                                    'color: rgb(255, 255, 255); \n'
    #                                    'border-image: url(":/images/Home_Page/Home_Sub3_Pure_Background.png"); \n'
    #                                    'border-radius: 12px; \n}')


def on_click_home_sub_stat_1(self):
    self.btn_toggle_PerfMonitor.click()


def on_click_home_sub_stat_2(self):
    self.btn_toggle_AppStore.click()


def on_click_home_sub_stat_3(self):
    self.btn_toggle_CleanerTool_stack.click()


def visual_home_dashboard_group(self):
    ## the bottom three graph here.
    ## first initiate information in the elements
    cpu_home_perf_chart_update(self)
    mem_home_perf_chart_update(self)
    sto_home_perf_chart_update(self)

    ## besides, do the binding here.
    ## binding the charts to an event of shifting the window
    par_go2perf_mon = partial(on_click_home_sub_stat_1, self)
    self.cpu_series.clicked.connect(par_go2perf_mon)
    self.mem_series.clicked.connect(par_go2perf_mon)
    self.sto_series.clicked.connect(par_go2perf_mon)

    pass


class QChartViewHomeDashboard(QChartView):
    def __init__(self, outer_self):
        super().__init__()
        self.outer_self = outer_self

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.outer_self.btn_toggle_PerfMonitor.click()


def on_click_dashboard(self):
    self.btn_toggle_PerfMonitor.click()
    pass


def cpu_home_perf_chart_update(self):
    ## define the chartview widget
    # self.cpu_charView = QChartView(self)
    self.cpu_charView = QChartViewHomeDashboard(self)
    self.cpu_charView.setRenderHints(QtGui.QPainter.Antialiasing)
    self.cpu_charView.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    ## setting the visual effects
    self.cpu_charView.chart().setBackgroundVisible(False)
    # self.cpu_charView.chart().legend().setVisible(False)
    self.cpu_charView.chart().legend().setAlignment(Qt.AlignBottom)
    self.cpu_charView.chart().legend().setLabelColor(QColor(255, 255, 255, 180))
    self.cpu_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    font = QtGui.QFont()
    font.setPixelSize(16)
    font.setPointSize(16)

    self.cpu_charView.chart().setTitle('CPU')

    self.cpu_charView.chart().setTitleFont(font)
    self.cpu_charView.chart().setTitleBrush(QColor(255, 255, 255, 180))

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
    self.cpu_series = QPieSeries()
    self.cpu_series.setHoleSize(0.6)
    # self.cpu_series.setPieSize(0.63)
    self.cpu_series.setPieSize(0.78)
    self.cpu_series.append('使用', cpu_usage_perc)
    self.cpu_series.append('空闲', cpu_free_perc)

    ## stylish the information of usage
    ## Pen changes the color of the border
    ## Brush changes the color filling the chart
    cpu_usage_slice = self.cpu_series.slices()[0]
    # cpu_usage_slice.setLabelFont()
    # cpu_usage_slice.setLabelVisible(True)
    cpu_usage_slice.setPen(QtGui.QPen(QColor(37, 226, 119, 220), 5))
    # cpu_usage_slice.setPen(QtGui.QPen(QColor(240, 250, 254, 150), 5))
    cpu_usage_slice.setBrush(QColor(85, 255, 158, 200))
    # cpu_usage_slice.setBrush(QColor(75, 226, 140, 200))
    # cpu_usage_slice.setExploded()

    ## stylish the information of free
    cpu_free_slice = self.cpu_series.slices()[1]
    # cpu_free_slice.setLabelVisible(True)
    cpu_free_slice.setPen(QtGui.QPen(QColor(81, 85, 133, 150), 7))
    cpu_free_slice.setBrush(QColor(120, 110, 126, 210))
    # cpu_free_slice.setBrush(QColor(127, 127, 127, 210))
    # cpu_free_slice.setExploded()

    self.cpu_charView.chart().addSeries(self.cpu_series)
    # self.cpu_charView.chart().setTitle('%d核心CPU' % cpu_core_count)

    # self.cpu_charView.chart().setTitleBrush(Qt.white)

    self.home_page_status_hor_layout.addWidget(self.cpu_charView)

    partial_on_click_dashboard = partial(on_click_dashboard, self)

    self.home_dashboard_cpu_prompt.move(98, 495)
    self.home_dashboard_cpu_prompt.setText(' ')
    self.home_dashboard_cpu_prompt.clicked.connect(partial_on_click_dashboard)
    self.home_dashboard_cpu_prompt.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    self.home_dashboard_cpu_prompt.setStyleSheet('QPushButton {\n'
                                                 'background-position: center; \n'
                                                 'background-repeat: no-repeat; \n'
                                                 'border: none; \n'
                                                 'background: transparent; \n'
                                                 'font: 22pt "Noto Mono"; \n'
                                                 'color: rgba(255, 255, 255, 170); \n'
                                                 'font-weight: bold; \n'
                                                 '}')
    self.home_dashboard_cpu_prompt.setGraphicsEffect(self.blur_effect)

    pass


def mem_home_perf_chart_update(self):
    ## define the chartview widget
    # self.mem_charView = QChartView(self)
    self.mem_charView = QChartViewHomeDashboard(self)
    self.mem_charView.setRenderHints(QtGui.QPainter.Antialiasing)
    self.mem_charView.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    ## setting the visual effects
    self.mem_charView.chart().setBackgroundVisible(False)
    # self.mem_charView.chart().legend().setVisible(False)
    self.mem_charView.chart().legend().setAlignment(Qt.AlignBottom)
    self.mem_charView.chart().legend().setLabelColor(QColor(255, 255, 255, 180))
    self.mem_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    font = QtGui.QFont()
    font.setPixelSize(16)
    font.setPointSize(16)

    self.mem_charView.chart().setTitle('内存总量检测中')

    self.mem_charView.chart().setTitleFont(font)
    self.mem_charView.chart().setTitleBrush(QColor(255, 255, 255, 180))

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
    self.mem_series = QPieSeries()
    self.mem_series.setHoleSize(0.6)
    self.mem_series.setPieSize(0.78)
    self.mem_series.append('使用', mem_usage_perc)
    self.mem_series.append('空闲', mem_free_perc)

    ## stylish the information of usage
    ## Pen changes the color of the border
    ## Brush changes the color filling the chart
    mem_usage_slice = self.mem_series.slices()[0]
    # mem_usage_slice.setLabelVisible(True)
    mem_usage_slice.setPen(QtGui.QPen(QColor(37, 226, 119, 220), 5))
    mem_usage_slice.setBrush(QColor(85, 255, 158, 200))
    # mem_usage_slice.setExploded()

    ## stylish the information of free
    mem_free_slice = self.mem_series.slices()[1]
    # mem_free_slice.setLabelVisible(True)
    mem_free_slice.setPen(QtGui.QPen(QColor(81, 85, 133, 150), 7))
    mem_free_slice.setBrush(QColor(120, 110, 126, 210))
    # mem_free_slice.setExploded()

    self.mem_charView.chart().addSeries(self.mem_series)

    self.home_page_status_hor_layout.addWidget(self.mem_charView)

    partial_on_click_dashboard = partial(on_click_dashboard, self)

    self.home_dashboard_mem_prompt.move(385, 495)
    self.home_dashboard_mem_prompt.setText(' ')
    self.home_dashboard_mem_prompt.clicked.connect(partial_on_click_dashboard)
    self.home_dashboard_mem_prompt.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    self.home_dashboard_mem_prompt.setStyleSheet('QPushButton {\n'
                                                 'background-position: center; \n'
                                                 'background-repeat: no-repeat; \n'
                                                 'border: none; \n'
                                                 'background: transparent; \n'
                                                 'font: 22pt "Noto Mono"; \n'
                                                 'color: rgba(255, 255, 255, 170); \n'
                                                 'font-weight: bold; \n'
                                                 '}')
    # self.home_dashboard_mem_prompt.setStyleSheet('font: 22pt "Noto Mono"; \n'
    #                                              'color: rgba(255, 255, 255, 170); \n'
    #                                              'font-weight: bold')
    self.home_dashboard_mem_prompt.setGraphicsEffect(self.blur_effect)

    pass


def sto_home_perf_chart_update(self):
    ## define the chartview widget

    # self.sto_charView = QChartView(self)
    self.sto_charView = QChartViewHomeDashboard(self)
    self.sto_charView.setRenderHints(QtGui.QPainter.Antialiasing)
    self.sto_charView.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    ## setting the visual effects
    self.sto_charView.chart().setBackgroundVisible(False)
    # self.sto_charView.chart().legend().setVisible(False)
    self.sto_charView.chart().legend().setAlignment(Qt.AlignBottom)
    self.sto_charView.chart().legend().setLabelColor(QColor(255, 255, 255, 180))
    self.sto_charView.chart().layout().setContentsMargins(0, 0, 0, 0)

    font = QtGui.QFont()
    font.setPixelSize(16)
    font.setPointSize(16)

    self.sto_charView.chart().setTitle('硬盘总量检测中')

    self.sto_charView.chart().setTitleFont(font)
    self.sto_charView.chart().setTitleBrush(QColor(255, 255, 255, 180))

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
    self.sto_series.setHoleSize(0.6)
    self.sto_series.setPieSize(0.78)
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

    self.sto_charView.chart().addSeries(self.sto_series)

    self.home_page_status_hor_layout.addWidget(self.sto_charView)

    partial_on_click_dashboard = partial(on_click_dashboard, self)

    self.home_dashboard_sto_prompt.move(672, 495)
    self.home_dashboard_sto_prompt.setText(' ')
    self.home_dashboard_sto_prompt.clicked.connect(partial_on_click_dashboard)
    self.home_dashboard_sto_prompt.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    self.home_dashboard_sto_prompt.setStyleSheet('QPushButton {\n'
                                                 'background-position: center; \n'
                                                 'background-repeat: no-repeat; \n'
                                                 'border: none; \n'
                                                 'background: transparent; \n'
                                                 'font: 22pt "Noto Mono"; \n'
                                                 'color: rgba(255, 255, 255, 170); \n'
                                                 'font-weight: bold; \n'
                                                 '}')
    # self.home_dashboard_sto_prompt.setStyleSheet('font: 22pt "Noto Mono"; \n'
    #                                              'color: rgba(255, 255, 255, 170); \n'
    #                                              'font-weight: bold')
    self.home_dashboard_sto_prompt.setGraphicsEffect(self.blur_effect)
    pass


def content_refresh_helper(self):
    '''
    there should be a function run in the background that helps to update the content on this page
    :param self:
    :return:
    '''
    self.home_page_left_flag = 0
    self.home_page_refresh_delay = 1

    ## bind the page change activity
    par_on_going_leave_page = partial(on_going_leave_page, self)
    self.stackedWidget.currentChanged.connect(par_on_going_leave_page)

    ## refresh the stat 3 content
    ## one-time action. 
    ## TODO: implement on this.

    # print('content refresh helper start')

    par_caller_refresh_home_page_dashboard = partial(caller_refresh_home_page_dashboard, self)

    ## if the element refresh helper has not been created, do the following line:
    if not hasattr(self, 'refr_proc'):
        self.refr_proc = Thread(target = par_caller_refresh_home_page_dashboard,
                                name = 'refresh home dashboard', daemon = True)
        self.refr_proc.start()

    pass


def on_going_leave_page(self):
    self.home_page_left_flag = 1
    print('detect page changed. ')
    # print(hasattr(self, 'refr_proc'))
    pass


def caller_refresh_home_page_dashboard(self):
    ## considering the cons_repo might not be fully initiated
    ## when this page is called
    if not hasattr(self.cons_repo, 'ip_addr'):
        try:
            ## ensure that the functions called here are light function.
            self.cons_repo.operating_elapsed_time()
            self.cons_repo.network_property()
            self.cons_repo.packages_num_check_lite()
            self.cons_repo.phy_memory_monitor()
            self.cons_repo.storage_monitor()

        except Exception as err_msg:
            print('error message while trying to call cons_repo: \n', err_msg)

    while True:

        ## if the refresh delay in this module is less than the one in the cons_repo module,
        ## do the following:

        if self.home_page_refresh_delay < self.cons_repo.ins_freq:
            try:
                ## refresh the information manually.
                self.cons_repo.operating_elapsed_time()
                self.cons_repo.network_property()
                self.cons_repo.packages_num_check_lite()
                self.cons_repo.phy_memory_monitor()
                self.cons_repo.storage_monitor()

            except Exception as err_msg:
                print('error message while trying to call cons_repo: \n', err_msg)

        ## fill in the elements here in this page.
        try:
            greetings_preparation(self)
            refresh_home_page_dashboard(self)
        except AttributeError as err_msg:
            print('error message while trying to update the elements: \n', err_msg,
                  '\nthe backend is still appending for refresh. ')

        # print('tend to be sleeping for', self.home_page_refresh_delay, 'secs. ')
        sleep(int(self.home_page_refresh_delay))
        # if self.home_page_left_flag == 1:
        #     print('breaking the refresh thread')
        #     break
    pass


def refresh_home_page_dashboard(self):
    ip_add = self.cons_repo.ip_addr
    up_time_day = int(self.cons_repo.up_time_day)
    up_time_hr = int(self.cons_repo.up_time_hr)
    up_time_min = int(self.cons_repo.up_time_min)
    pack_num = self.cons_repo.installed_pac_num
    # try:
    #     up_time_day = int(self.cons_repo.up_time_day)
    #     up_time_hr = int(self.cons_repo.up_time_hr)
    #     up_time_min = int(self.cons_repo.up_time_min)
    # except AttributeError:
    #     up_time_day, up_time_hr, up_time_min = 0, 0, 0

    # ## updating the sub stat 1
    # self.home_sub_stat_1.setText('主机IP 地址 \n %s \n\n 电脑运行时间 \n %2.d天%2.d小时%2.d分钟'
    #                              % (ip_add, up_time_day, up_time_hr, up_time_min))
    #
    # ## updating the sub stat 2
    # pack_num = self.cons_repo.installed_pac_num
    # self.home_sub_stat_2.setText('软件总数 \n %2.d个' % pack_num)
    #
    # ## updating the sub stat 3
    # ## no need to frequently update this thing

    ## updating the text filler for home sub stat
    self.home_sub_filler_text_ip.setText('%s' % ip_add)
    self.home_sub_filler_text_ip.setGraphicsEffect(self.blur_effect)
    self.home_sub_filler_text_operate_time.setText('%d天%d小时%d分钟' % (up_time_day, up_time_hr, up_time_min))
    self.home_sub_filler_text_operate_time.setGraphicsEffect(self.blur_effect)
    self.home_sub_filler_text_software_num.setText('%2.d个' % pack_num)
    self.home_sub_filler_text_software_num.setGraphicsEffect(self.blur_effect)
    self.home_sub_filler_text_health_score.setText('待评估')
    self.home_sub_filler_text_health_score.setGraphicsEffect(self.blur_effect)

    ## updating the button dashboard chart

    ## check if updates are appending
    if self.home_logic_cpu_update_append == 1:
        cpu_core_count = int(self.cons_repo.CPU_count_logical)
        self.cpu_charView.chart().setTitle('%d核心CPU' % cpu_core_count)
        self.home_logic_cpu_update_append = 0

    if self.home_logic_mem_update_append == 1:
        mem_total = self.cons_repo.phy_mem_total
        self.mem_charView.chart().setTitle('内存总量%2.1fGB' % mem_total)
        self.home_logic_mem_update_append = 0

    if self.home_logic_sto_update_append == 1:
        sto_total = self.cons_repo.sto_info_total
        sto_unit = str('GB')

        if sto_total > 1024:
            sto_total = round(sto_total / 1024, 1)
            sto_unit = str('TB')

        self.sto_charView.chart().setTitle('硬盘总量%d%s' % (sto_total, sto_unit))
        self.home_logic_sto_update_append = 0

    ## get relevant variables. 
    cpu_usage_perc = float(self.cons_repo.CPU_perc)
    cpu_free_perc = 1 - cpu_usage_perc
    cpu_usage_perc_hd = round(cpu_usage_perc * 100, 2)
    mem_usage_perc = float(self.cons_repo.phy_mem_perc)
    mem_free_perc = 1 - mem_usage_perc
    mem_usage_perc_hd = round(mem_usage_perc * 100, 2)
    sto_usage_perc = float(self.cons_repo.sto_info_perc)
    sto_free_perc = 1 - sto_usage_perc
    sto_usage_perc_hd = round(sto_usage_perc * 100, 2)

    ## setting the values 
    self.cpu_series.slices()[0].setValue(cpu_usage_perc)
    self.cpu_series.slices()[1].setValue(cpu_free_perc)
    self.home_dashboard_cpu_prompt.setText('%2.1f%%' % cpu_usage_perc_hd)
    self.home_dashboard_cpu_prompt.setGraphicsEffect(self.blur_effect)

    self.mem_series.slices()[0].setValue(mem_usage_perc)
    self.mem_series.slices()[1].setValue(mem_free_perc)
    self.home_dashboard_mem_prompt.setText('%2.1f%%' % mem_usage_perc_hd)
    self.home_dashboard_mem_prompt.setGraphicsEffect(self.blur_effect)

    self.sto_series.slices()[0].setValue(sto_usage_perc)
    self.sto_series.slices()[1].setValue(sto_free_perc)
    self.home_dashboard_sto_prompt.setText('%2.1f%%' % sto_usage_perc_hd)
    self.home_dashboard_sto_prompt.setGraphicsEffect(self.blur_effect)
    pass
