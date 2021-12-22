import sys
import platform
import os
import time
import threading
import psutil, datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent, QModelIndex, QAbstractTableModel, QVariant, QThread,
                          pyqtSignal, QSortFilterProxyModel)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from functools import partial
from threading import Thread

sys.path.append('..')
from UI.sub_pages.ui_process_details import Ui_Detail_widget

NetHeaderLabel = ['进程名', 'PID', '类型', '状态', '本地IP', '远程IP', '操作']


def Nettable_Call(self):
    self.Net_data_model = NetMyModel(self)

    # 设置sorted model
    self.sortermodel_net = QSortFilterProxyModel()
    self.net_table_view.setModel(self.sortermodel_net)
    self.sortermodel_net.setDynamicSortFilter(True)
    self.sortermodel_net.setSourceModel(self.Net_data_model)

    ## adjusting the behavior of table
    self.net_table_view.horizontalHeader().setStretchLastSection(True)
    self.net_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.net_table_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    self.net_table_view.verticalHeader().hide()
    set_net_style(self)
    self.net_table_view.setSortingEnabled(True)

    # 刷新线程
    call_net_thread(self)


class NetMyModel(QAbstractTableModel):
    def __init__(self, UI, parent = None):
        super(NetMyModel, self).__init__(parent)
        self.UI = UI
        # self.datalist = list

    def rowCount(self, QModelIndex):
        row_count = len(self.UI.cons_repo.network_list_out)
        return row_count

    def columnCount(self, QModelIndex):
        return 7

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def data(self, index, role):
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            if (col != 6):
                value = self.UI.cons_repo.network_list_out[row][col]
                self.UI.net_table_view.setItemDelegateForColumn(6, MyButtonDelegate(self.UI))
                return value
        elif role == Qt.TextAlignmentRole:
            if (col != 0):
                return QVariant(Qt.AlignRight | Qt.AlignCenter)
            elif col == 0:
                return QVariant(Qt.AlignLeft | Qt.AlignCenter)
        return QVariant()

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return NetHeaderLabel[section]
        elif role == Qt.TextAlignmentRole:
            if (section != 0) & (section != 6):
                return QVariant(Qt.AlignCenter)
                # return QVariant(Qt.AlignRight | Qt.AlignCenter)
        return QAbstractTableModel.headerData(self, section, orientation, role)


class MyButtonDelegate(QItemDelegate):
    def __init__(self, parent = None):
        super(MyButtonDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().net_table_view.indexWidget(index):
            button_detail = QPushButton(self.tr('详情'), self.parent().net_table_view)
            button_stop = QPushButton(self.tr('终止'), self.parent().net_table_view)
            buttonstyle = "QPushButton{" \
                          "color: rgb(255, 255, 255); background: transparent; border-radius:5px; font-weight: bold;}" \
                          "QPushButton:hover{" \
                          "color:rgb(44,137,255); background: transparent; font-weight: bold;}" \
                          "QPushButton:pressed{" \
                          "color:rgb(14,135,228); background: transparent; font-weight: bold; " \
                          "padding-left:3px; padding-top:3px;}"
            button_detail.setStyleSheet(buttonstyle)
            button_stop.setStyleSheet(buttonstyle)

            button_detail.clicked.connect(lambda: GetNetDetails(self, self.parent()))
            button_stop.clicked.connect(lambda: KillConnect(self, self.parent()))

            button_detail.index = [index.row(), index.column()]
            button_stop.index = [index.row(), index.column()]

            self.parent().net_box_layout = QHBoxLayout()
            self.parent().net_widget = QWidget()
            self.parent().net_box_layout.addWidget(button_detail)
            self.parent().net_box_layout.addWidget(button_stop)

            self.parent().net_box_layout.setContentsMargins(0, 0, 0, 0)
            self.parent().net_box_layout.setAlignment(Qt.AlignCenter)
            self.parent().net_widget.setLayout(self.parent().net_box_layout)

            self.parent().net_table_view.setIndexWidget(index, self.parent().net_widget)
            self.parent().net_table_view.updateGeometries()


class update_netdata(QThread):
    netchange = pyqtSignal(str)

    def run(self):
        cnt = 0
        while True:
            cnt += 1
            self.netchange.emit(str(cnt))  # 发射信号
            time.sleep(0.5)


# 创建进程详细界面
class NetworkDetailWidget(QWidget, Ui_Detail_widget):
    def __init__(self, parent):
        super(NetworkDetailWidget, self).__init__()
        self.setupUi(self)

        self.parent = parent

        self.Logic()
        self.Visual()

    def Logic(self):
        pass

    def Visual(self):
        self.setWindowTitle('进程 - 详细信息')

        screen_geo = QDesktopWidget().screenGeometry()
        ## get the geometry of the current window
        window_geo = self.geometry()
        target_left_point = int((screen_geo.width() - window_geo.width()) / 2)
        target_top_point = int((screen_geo.height() - window_geo.height()) / 2)
        ## move the window
        self.move(target_left_point, target_top_point)

        # ## set the background color
        # if hasattr(self.parent, 'interactive_area_stylesheet'):
        #     # print('activated. ')
        #     self.Detail_widget.setStyleSheet(self.parent.interactive_area_stylesheet)
        # else:
        #     self.Detail_widget.setStyleSheet(
        #         'background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(132, 110, 160), stop:1 rgb(55, 80, 110)); \n'
        #         'color: rgb(255, 255, 255); ')

        pass


def updateNetData(self):
    self.Net_data_model.beginResetModel()
    # self.cons_repo.network_list_out = self.cons_repo.network_list
    # self.setData(self.index(),self.UI.cons_repo.network_list,role=Qt.DisplayRole)
    # self.dataChanged.emit(self.index(), self.index())
    self.Net_data_model.endResetModel()


def call_net_thread(self):
    self.NetConnect_table_refresh_thread = threading.Thread(target = updateNetData(self))
    self.NetConnect_table_refresh_thread.start()
    # self.Net_thread = update_netdata()
    # update_net = partial(updateNetData, self)
    # self.Net_thread.netchange.connect(update_net)
    # self.Net_thread.start()


# 操作1：获取进程详情
def GetNetDetails(self, UI):
    # 获取点击行号
    row = UI.sender().index[0]
    # 获取选中行的内容
    list = []
    for i in range(6):
        index = UI.net_table_view.model().index(row, i)
        list.append(UI.net_table_view.model().data(index))

    # print("data for row",list)
    pid = list[1]
    p = psutil.Process(pid)
    tmp = []
    tmp.append("进程名:" + list[0])
    tmp.append("进程PID:" + str(list[1]))
    tmp.append("进程状态:" + list[3])
    tmp.append("执行用户:" + list[2])
    tmp.append("进程占用CPU:" + list[4])
    tmp.append("进程占用内存:" + list[5])
    # tmp.append("进程IO读取次数:" + str(p.io_counters().read_count))
    # tmp.append("进程IO写入次数:" + str(p.io_counters().write_count))
    # tmp.append("进程IO读取bytes:" + str(p.io_counters().read_bytes))
    # tmp.append("进程IO写入bytes:" + str(p.io_counters().write_bytes))
    tmp.append("进程线程数:" + str(p.num_threads()))
    tmp.append("进程创建时间:" + str(datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S")))
    tmp.append("进程处理时间:" + str(sum(p.cpu_times()[:2])) + "秒")
    # tmp.append("进程路径:" + p.cwd())
    user_id = os.geteuid()
    if user_id == 0:
        tmp.append("进程IO读取次数:" + str(p.io_counters().read_count))
        tmp.append("进程IO写入次数:" + str(p.io_counters().write_count))
        tmp.append("进程IO读取bytes:" + str(p.io_counters().read_bytes))
        tmp.append("进程IO写入bytes:" + str(p.io_counters().write_bytes))
        tmp.append("进程路径:" + p.cwd())

    if not hasattr(self, 'Detail_window'):
        self.Detail_window = NetworkDetailWidget(self)

    self.Detail_text = QTextEdit()
    for item in tmp:
        self.Detail_text.append(item)

    ## stylesheet for detail information
    textstyle = 'font: 12pt "Noto Mono";'

    self.Detail_text.setStyleSheet(textstyle)
    self.Detail_text.setReadOnly(True)
    self.Detail_window.Detail_Layout.addWidget(self.Detail_text)

    self.Detail_window.button_back.setDefault(False)
    self.Detail_window.button_kill.setDefault(False)
    # window_style = "QWidget{" \
    #                "background-color:rgb(255,255,255);}"



    buttonstyle = "QPushButton{" \
                  "color: rgb(14,150,254); background-color: white; " \
                  "border-radius:5px;border: 1px solid rgb(232,232,232);}" \
                  "QPushButton:hover{" \
                  "color:rgb(44,137,255);background-color:white;}" \
                  "QPushButton:pressed{" \
                  "color:rgb(14,135,228);background-color:white;" \
                  "padding-left:3px; padding-top:3px;}"
    self.Detail_window.button_back.setStyleSheet(buttonstyle)
    self.Detail_window.button_kill.setStyleSheet(buttonstyle)
    # self.Detail_window.setStyleSheet(window_style)
    self.Detail_window.button_kill.clicked.connect(lambda: KillConnect_FromDetail(self, UI, pid, row))
    self.Detail_window.button_back.clicked.connect(self.Detail_window.close)

    ## make the window to the center of the screen
    ## get the geometry of the screen
    screen_geo = QDesktopWidget().screenGeometry()
    ## get the geometry of the current window
    window_geo = self.Detail_window.geometry()
    ## this line is dedicated for the main window,
    ## since the interactive area is on the right of the main window
    target_left_point = int((screen_geo.width() - window_geo.width()) / 2 - 100)
    target_top_point = int((screen_geo.height() - window_geo.height()) / 2)
    ## move the window
    self.Detail_window.move(target_left_point, target_top_point)

    self.Detail_window.show()


# 操作2：终止进程
def KillConnect(self, UI):
    UI.Net_data_model.beginResetModel()
    # 获取点击行号
    row = UI.sender().index[0]
    index = UI.net_table_view.model().index(row, 1)
    pid = UI.net_table_view.model().data(index)
    p = psutil.Process(pid)
    p.kill()

    UI.Net_data_model.removeRow(row)
    print("Kill Proc Button Clicked", pid)
    UI.Net_data_model.endResetModel()


# 操作2：终止进程，从详情那里进行终止
def KillConnect_FromDetail(self, UI, pid, row):
    UI.Net_data_model.beginResetModel()
    p = psutil.Process(pid)
    p.kill()

    UI.Net_data_model.removeRow(row)
    print("Kill Proc Button Clicked", pid)
    UI.Net_data_model.endResetModel()


# style设置
def set_net_style(self):
    # tableviewstyle = "QTableView{" \
    #                  "color: black; gridline-color: white; " \
    #                  "background-color: rgb(255, 255, 255); " \
    #                  "alternate-background-color: rgb(255, 255, 255); " \
    #                  "selection-color: black; selection-background-color: rgb(255,250,250); " \
    #                  "border: 2px;border-radius: 0px;" \
    #                  "padding: 2px 4px;}" \
    #                  "QTableView:Item{" \
    #                  "border:0px;border-right:1px solid rgb(232,232,232);" \
    #                  "}" \
    #                  "QHeaderView{" \
    #                  "color:black; font:bold 12pt;" \
    #                  "background-color:rgb(255, 255, 255);" \
    #                  "border: 0px solid rgb(255,255,255);" \
    #                  "border-left-color: rgba(255, 255, 255, 0);" \
    #                  "border-top-color: rgba(255, 255, 255, 0);" \
    #                  "border-radius:0px;" \
    #                  "min-height:29px;}" \
    #                  "QHeaderView::section, QTableCornerButton::section {" \
    #                  "padding: 1px;border: none;" \
    #                  "border-bottom: 1px solid rgb(75, 120, 154);" \
    #                  "border-right: 1px solid rgb(255, 255, 255);" \
    #                  "border-bottom: 1px solid gray;" \
    #                  "background-color:rgb(255, 255, 255);}" \
    #                  "QScrollBar:vertical{" \
    #                  "background:#FFFFFF;}" \
    #                  "QScrollBar::handle:vertical{" \
    #                  "background:#dbdbdb;" \
    #                  "border-radius:6px;" \
    #                  "min-height:80px;}" \
    #                  "QScrollBar::handle:vertical:hover{" \
    #                  "background:#d0d0d0;}" \
    #                  "QScrollBar::add-line:vertical{background:#d0d0d0;}" \
    #                  "QScrollBar::sub-line:vertical{background:#d0d0d0;}"
    tableviewstyle = "QTableView{" \
                     "color: white; gridline-color: white; " \
                     "background: transparent; " \
                     "alternate-background-color: rgba(255, 255, 255, 70); " \
                     "selection-color: black; selection-background-color: rgb(255,250,250); " \
                     "border: 2px;border-radius: 0px;" \
                     "padding: 2px 4px;}" \
                     "QTableView:Item{" \
                     "border:0px;border-right:1px solid rgb(232,232,232);" \
                     "}" \
                     "QHeaderView{" \
                     "color:white; font:bold 12pt;" \
                     "background: transparent;" \
                     "border: 0px solid rgb(255,255,255);" \
                     "border-left-color: rgba(255, 255, 255, 0);" \
                     "border-top-color: rgba(255, 255, 255, 0);" \
                     "border-radius:0px;" \
                     "min-height:29px;}" \
                     "QHeaderView::section, QTableCornerButton::section {" \
                     "padding: 1px;border: none;" \
                     "border-bottom: 1px solid rgb(75, 120, 154);" \
                     "border-right: 1px solid rgb(255, 255, 255);" \
                     "border-bottom: 1px solid gray;" \
                     "background: transparent;}" \
                     "QScrollBar:vertical{" \
                     "background:#FFFFFF;}" \
                     "QScrollBar::handle:vertical{" \
                     "background:#dbdbdb;" \
                     "border-radius:6px;" \
                     "min-height:80px;}" \
                     "QScrollBar::handle:vertical:hover{" \
                     "background:#d0d0d0;}" \
                     "QScrollBar::add-line:vertical{background:#d0d0d0;}" \
                     "QScrollBar::sub-line:vertical{background:#d0d0d0;}"

    self.net_table_view.verticalHeader().setDefaultSectionSize(40)
    # self.net_table_view.verticalHeader().setMinimumSectionSize(35)
    self.net_table_view.setAlternatingRowColors(True)
    self.net_table_view.setStyleSheet(tableviewstyle)

    pass
