import ctypes
import operator
import sys
import platform
import os
from time import sleep

import psutil, datetime

import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent, QModelIndex, QAbstractTableModel, QVariant, QThread,
                          pyqtSignal, QSortFilterProxyModel, QStringListModel)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from functools import partial
import threading

sys.path.append('..')
from UI.sub_pages.ui_process_details import Ui_Detail_widget

HeaderLabel = ['进程名', 'PID', '执行用户', '进程状态', 'CPU占用', '内存占用', '操作']


def Processtable_Call(self):
    ## set the stylesheet of the table
    set_tabstyle(self)
    ## binding the model
    self.proc_data_model = MyModel(self)

    # 设置sorted model
    self.sortermodel = QSortFilterProxyModel()
    self.process_mng_table_view.setModel(self.sortermodel)
    self.sortermodel.setDynamicSortFilter(True)
    self.sortermodel.setSourceModel(self.proc_data_model)

    ## adjusting the behavior of table
    self.process_mng_table_view.horizontalHeader().setStretchLastSection(True)
    self.process_mng_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.process_mng_table_view.verticalHeader().hide()  # 隐藏序号
    self.process_mng_table_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    self.process_mng_table_view.setSortingEnabled(True)
    ## tableview style setting
    set_proc_style(self)

    # make an instance of this window
    if not hasattr(self, 'Detail_window'):
        self.Detail_window = ProcDetailWidget(self)

    # 刷新线程
    call_proc_thread(self)

    # ## the added process for controlling the data update.
    # data_update_controller(self)


# def data_update_controller(self):
#     self.table_update_daemon = threading.Thread(target = update_daemon_on_tableview(self))
#     # self.table_update_daemon.start()
#     pass
#
#
# def update_daemon_on_tableview(self):
#     while True:
#         QApplication.processEvents()
#         self.process_mng_table_view.setUpdatesEnabled(False)
#         sleep(0.2)
#         QApplication.processEvents()
#         if self.proc_manager_terminate is True:
#             break
#         self.process_mng_table_view.setUpdatesEnabled(True)
#         QApplication.processEvents()
#         sleep(5)
#     pass


class MyModel(QAbstractTableModel):
    def __init__(self, UI, parent = None):
        super(MyModel, self).__init__(parent)
        self.UI = UI
        # self.datalist = list

    def rowCount(self, QModelIndex):
        row_count = len(self.UI.cons_repo.process_list_out)
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
                value = self.UI.cons_repo.process_list_out[row][col]
                self.UI.process_mng_table_view.setItemDelegateForColumn(6, MyButtonDelegate(self.UI))
                return value
        elif role == Qt.TextAlignmentRole:
            if (col != 0):
                return QVariant(Qt.AlignRight | Qt.AlignCenter)
            elif col == 0:
                return QVariant(Qt.AlignLeft | Qt.AlignCenter)
        return QVariant()

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return HeaderLabel[section]
        elif role == Qt.TextAlignmentRole:
            if (section != 0) & (section != 6):
                return QVariant(Qt.AlignCenter)
                # return QVariant(Qt.AlignRight | Qt.AlignCenter)
        return QAbstractTableModel.headerData(self, section, orientation, role)


class MyButtonDelegate(QItemDelegate):
    def __init__(self, parent = None):
        super(MyButtonDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().process_mng_table_view.indexWidget(index):
            # proc_box_layout = QHBoxLayout()
            # self.parent().process_mng_table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            button_detail = QPushButton(self.tr('详情'), self.parent().process_mng_table_view)
            button_stop = QPushButton(self.tr('终止'), self.parent().process_mng_table_view)
            buttonstyle = "QPushButton{" \
                          "color: rgb(255, 255, 255); background: transparent; border-radius:5px; font-weight: bold;}" \
                          "QPushButton:hover{" \
                          "color:rgb(44,137,255); background: transparent; font-weight: bold;}" \
                          "QPushButton:pressed{" \
                          "color:rgb(14,135,228); background: transparent; font-weight: bold; " \
                          "padding-left:3px; padding-top:3px;}"
            button_detail.setStyleSheet(buttonstyle)
            button_stop.setStyleSheet(buttonstyle)

            button_detail.clicked.connect(lambda: GetProcDetails(self, self.parent()))
            button_stop.clicked.connect(lambda: KillProcess(self, self.parent()))

            button_detail.index = [index.row(), index.column()]
            button_stop.index = [index.row(), index.column()]

            self.parent().proc_box_layout = QHBoxLayout()
            self.parent().proc_widget = QWidget()
            self.parent().proc_box_layout.addWidget(button_detail)
            self.parent().proc_box_layout.addWidget(button_stop)

            self.parent().proc_box_layout.setContentsMargins(0, 0, 0, 0)
            self.parent().proc_box_layout.setAlignment(Qt.AlignCenter)
            self.parent().proc_widget.setLayout(self.parent().proc_box_layout)

            self.parent().process_mng_table_view.setIndexWidget(index, self.parent().proc_widget)
            self.parent().process_mng_table_view.updateGeometries()

            # self.parent().process_mng_table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)


# class update_data(QThread):
#     update = pyqtSignal(str)
#
#     # handle = -1
#     def run(self):
#         cnt = 0
#         # self.handle = ctypes.windll.kernel32.OpenThread(win32com.PROCESS_ALL_ACCESS, False, int(QThread.currentThreadId()))
#         while True:
#             cnt += 1
#             self.update.emit(str(cnt))  # 发射信号
#             time.sleep(0.5)
#             print('process manager, update func')


# 创建进程详细界面
class ProcDetailWidget(QWidget, Ui_Detail_widget):
    def __init__(self, parent):
        super(ProcDetailWidget, self).__init__()
        self.setupUi(self)

        self.setObjectName(str(0))

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


def updateData(self):
    print('update data called')
    self.proc_data_model.beginResetModel()
    # QApplication.processEvents()
    # self.process_mng_table_view.setItemDelegateForColumn(6, MyButtonDelegate(self))
    # self.cons_repo.process_list = self.cons_repo.process_list
    # self.setData(self.index(),self.UI.cons_repo.process_list,role=Qt.DisplayRole)
    # self.dataChanged.emit(self.index(), self.index())
    self.proc_data_model.endResetModel()


def call_proc_thread(self):
    self.proc_table_refresh_thread = threading.Thread(target = updateData(self))
    # self.proc_table_refresh_thread.start()


# 操作1：获取进程详情
def GetProcDetails(self, UI):
    ## stylesheet for detail information
    textstyle = 'font: 12pt "Noto Mono";'

    ## stylesheet for button
    buttonstyle = "QPushButton{" \
                  "color: rgb(14,150,254); background: transparent; " \
                  "border-radius:5px;border: 1px solid rgb(232,232,232);}" \
                  "QPushButton:hover{" \
                  "color:rgb(44,137,255); background: transparent;}" \
                  "QPushButton:pressed{" \
                  "color:rgb(14,135,228); background: transparent;" \
                  "padding-left:3px; padding-top:3px;}"
    # 获取点击行号
    row = UI.sender().index[0]
    # 获取选中行的内容
    list = []
    for i in range(6):
        index = UI.process_mng_table_view.model().index(row, i)
        list.append(UI.process_mng_table_view.model().data(index))

    pid = list[1]
    p = psutil.Process(pid)
    try:
        current_obj_name = int(UI.Detail_window.objectName())
    except ValueError:
        current_obj_name = int(0)
    if current_obj_name != pid:
        # 先把原来的元素删除
        for i in range(UI.Detail_window.Detail_Layout.count()):
            UI.Detail_window.Detail_Layout.itemAt(i).widget().deleteLater()
        UI.Detail_window.setObjectName(str(pid))
        try:
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
            self.Detail_text = QTextEdit()
            for item in tmp:
                self.Detail_text.append(item)
            self.Detail_text.setReadOnly(True)

            self.Detail_text.setStyleSheet(textstyle)
            UI.Detail_window.Detail_Layout.addWidget(self.Detail_text)
            UI.Detail_window.button_kill.setDefault(False)
            UI.Detail_window.button_kill.setStyleSheet(buttonstyle)
            UI.Detail_window.button_kill.clicked.connect(lambda: KillProcess_FromDetail(self, UI, pid, row))

            UI.Detail_window.button_back.setDefault(False)
            UI.Detail_window.button_back.setStyleSheet(buttonstyle)
            UI.Detail_window.button_back.clicked.connect(UI.Detail_window.close)
            # UI.Detail_window.setStyleSheet(window_style)

            # self.Detail_window.setGeometry(300,300)

            ## make the window to the center of the screen
            ## get the geometry of the screen
            screen_geo = QDesktopWidget().screenGeometry()
            ## get the geometry of the current window
            window_geo = UI.Detail_window.geometry()
            ## this line is dedicated for the main window,
            ## since the interactive area is on the right of the main window
            target_left_point = int((screen_geo.width() - window_geo.width()) / 2 - 100)
            target_top_point = int((screen_geo.height() - window_geo.height()) / 2)
            ## move the window
            UI.Detail_window.move(target_left_point, target_top_point)

            UI.Detail_window.show()
        except Exception as err_msg:
            error_msg = QMessageBox(QMessageBox.Warning, "抱歉。", "该进程由系统创建，当前账户未提权，不能获取相关信息。")
            error_msg.exec_()
            pass


# 操作2：终止进程
def KillProcess(self, UI):
    UI.proc_data_model.beginResetModel()
    # 获取点击行号
    row = UI.sender().index[0]
    index = UI.process_mng_table_view.model().index(row, 1)
    pid = UI.process_mng_table_view.model().data(index)
    p = psutil.Process(pid)
    p.kill()

    UI.proc_data_model.removeRow(row)
    print("Kill Proc Button Clicked", pid)
    UI.proc_data_model.endResetModel()


# 操作2：终止进程，从详情那里进行终止
def KillProcess_FromDetail(self, UI, pid, row):
    UI.proc_data_model.beginResetModel()
    p = psutil.Process(pid)
    p.kill()

    UI.proc_data_model.removeRow(row)
    print("Kill Proc Button Clicked", pid)
    UI.proc_data_model.endResetModel()


# style设置
def set_proc_style(self):
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

    self.process_mng_table_view.verticalHeader().setDefaultSectionSize(40)
    # self.process_mng_table_view.verticalHeader().setMinimumSectionSize(35)
    self.process_mng_table_view.setAlternatingRowColors(True)
    self.process_mng_table_view.setStyleSheet(tableviewstyle)

    pass


def set_tabstyle(self):
    tabstyle = str("QTabWidget::pane {\n"
                   "    border: 2px solid rgba(102, 138, 210, 120);\n"
                   "    border-radius:8px;\n"
                   "    background: transparent;\n"
                   "}\n"
                   "\n"
                   "QTabWidget::tab-bar:top {\n"
                   "    top: 2px;\n"
                   "    left:8px;\n"
                   "}\n"
                   "\n"
                   "QTabWidget::tab-bar:bottom {\n"
                   "    bottom: 8px;\n"
                   "}\n"
                   "\n"
                   "QTabWidget::tab-bar:left {\n"
                   "    right: 8px;\n"
                   "}\n"
                   "\n"
                   "QTabWidget::tab-bar:right {\n"
                   "    left: 8px;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab {\n"
                   "    border: 2px solid rgb(81, 85, 133);\n"
                   "    background: rgb(255, 255, 255); \n"
                   "    width: 90 px;\n"
                   "    font-size : 16px;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:selected {\n"
                   "    background: rgba(255, 255, 255, 170);\n"
                   "    color: rgb(81, 85, 133);\n"
                   "    font-weight: bold; \n"
                   "    border-bottom-color: none;\n"
                   "    margin-bottom: -2px; \n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:!selected {\n"
                   "    background: rgba(157, 128, 173, 220);\n"
                   "    color:rgba(255, 255, 255, 165);\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:!selected:hover {\n"
                   "    background: rgba(208, 176, 255, 160);\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:top:!selected {\n"
                   "    margin-top: 3px;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:bottom:!selected {\n"
                   "    margin-bottom: 3px;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:top, QTabBar::tab:bottom {\n"
                   "    min-width: 8px;\n"
                   "    margin-right: -1px;\n"
                   "    padding: 5px 10px 5px 10px;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:top:selected {\n"
                   "    border-bottom-color: none;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:bottom:selected {\n"
                   "    border-top-color: none;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:top:last, QTabBar::tab:bottom:last,\n"
                   "QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {\n"
                   "    margin-right: 0;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:left:!selected {\n"
                   "    margin-right: 3px;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:right:!selected {\n"
                   "    margin-left: 3px;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:left, QTabBar::tab:right {\n"
                   "    min-height: 8ex;\n"
                   "    margin-bottom: -1px;\n"
                   "    padding: 10px 5px 10px 5px;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:left:selected {\n"
                   "    border-left-color: none;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:right:selected {\n"
                   "    border-right-color: none;\n"
                   "}\n"
                   "\n"
                   "QTabBar::tab:left:last, QTabBar::tab:right:last,\n"
                   "QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {\n"
                   "    margin-bottom: 0;\n"
                   "}")
    self.ProcessManager_tab.setStyleSheet(tabstyle)
    pass
