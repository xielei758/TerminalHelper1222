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

## import some other components here.
from functools import partial
import subprocess

## import utilities here
## the following line caused some top-level import error

sys.path.append('..')
from Utils.Cleaner_Tool import general_cleaner_utils

## import resources files here
from UI import ui_image_assets


## this function contains the implementations on the in-progress cleaning page
## thus there is no entry point, can only be called from the Gen_Cleaner_Main file.

def cleaner_in_progress_visual(self):
    ## setting the icon on the left of the placeholder
    self.cleaner_in_progress_icon_placeholder.setFlat(True)
    # self.cleaner_in_progress_icon_placeholder.setIcon(QIcon(':/images/Cleaner/u829.png'))
    # self.cleaner_in_progress_icon_placeholder.setIconSize(QtCore.QSize(95, 95))
    # self.cleaner_in_progress_icon_placeholder.setLayoutDirection(Qt.RightToLeft)
    self.cleaner_in_progress_icon_placeholder.setStyleSheet('QPushButton \n'
                                                            '{font-size:18pt; \n'
                                                            # 'color: rgb(255, 255, 255); \n'
                                                            'border-radius: 15px; \n'
                                                            'border-image: url(":/images/Cleaner/u979.png"); \n}')

    ## define the style of the progressbar
    self.cleaner_in_progress_pgsBar.setTextVisible(False)
    self.cleaner_in_progress_pgsBar.setValue(0)
    self.cleaner_in_progress_pgsBar.setCursor(QCursor(QtCore.Qt.BusyCursor))
    self.cleaner_in_progress_pgsBar.setStyleSheet('selection-background-color: rgb(255, 153, 0);')
    # self.cleaner_in_progress_pgsBar.setMaximum(0)
    self.cleaner_in_progress_pgsBar.setMinimum(0)

    ## set the now_clean button
    self.cleaner_in_progress_btn_nowClean.setStyleSheet('QPushButton \n'
                                                        '{background-color: rgb(56, 223, 128); \n'
                                                        'font-size:22pt; \n'
                                                        'color: rgb(255, 255, 255)}'
                                                        'QPushButton:hover \n'
                                                        '{background-color: rgb(110, 223, 150); } \n'
                                                        'QPushButton:pressed \n'
                                                        '{background-color: rgb(39,156,90); } ')
    self.cleaner_in_progress_btn_nowClean.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    self.cleaner_in_progress_btn_nowClean.setVisible(False)

    ## set the prompt here.
    self.cleaner_in_progress_cleanProgress.setText('扫描文件中...马上就好，请稍等片刻！')
    self.cleaner_in_progress_sum_size = float(0)
    self.cleaner_in_progress_sum_postfix = str('MB')

    ## make the progress bar visible
    self.cleaner_in_progress_pgsBar.setVisible(True)


def cleaner_in_progress_util_caller(self):
    ## call the backend to support this function
    print('invoking the backend of cleaner utilities here. ')

    ## setting the flags to indicate if the components here have been added.
    self.cleaner_ip_redu_addable = True
    self.cleaner_ip_priv_addable = True
    self.cleaner_ip_huge_addable = True
    self.cleaner_ip_outd_addable = True

    ## setting up the patch var
    if not hasattr(self, 'cleaner_re_enter_patch'):
        self.cleaner_re_enter_patch = False

    ## detect page change and reset the layout
    par_on_going_leave_page = partial(on_going_leave_page, self)
    self.stackedWidget.currentChanged.connect(par_on_going_leave_page)
    self.cleaner_page_stackedWidget.currentChanged.connect(par_on_going_leave_page)

    ## init the backend class

    if not hasattr(self, 'cleaner_backend'):
        self.cleaner_backend = general_cleaner_utils.CleanerToolUtils()
        # self.cleaner_backend.target_dir = '~/Project/dup_test'
    # self.cleaner_backend = general_cleaner_utils.CleanerToolUtils()

    ## overwrite the threshold values in the sub process there.
    threshold_rewrite(self)

    ## overwrite the target directory

    ## binding the signals.
    par_on_status_cleaner_in_progress_pgsBar_setValue = partial(on_status_cleaner_in_progress_pgsBar_setValue, self)
    self.cleaner_backend.redundancy_det_progress.connect(par_on_status_cleaner_in_progress_pgsBar_setValue)

    par_on_status_cleaner_in_progress_sum_result = partial(on_status_cleaner_in_progress_sum_result, self)
    self.cleaner_backend.redundancy_size.connect(par_on_status_cleaner_in_progress_sum_result)

    ## binding for the buttons.
    par_on_going_clean_now_action = partial(on_going_clean_now_action, self)
    self.cleaner_in_progress_btn_nowClean.clicked.connect(par_on_going_clean_now_action)

    ## prepare for the layout to present the scanning result here.
    ## create the initiation layout.
    self.target_layout = self.cleaner_in_progress_result_display
    # print('first line', self.target_layout.count())

    ## add the scroll bar here
    # self.scrollbar = self.scroll
    self.cleaner_in_progress_filler_widget.setLayout(self.target_layout)
    self.cleaner_in_progress_scroll_basis.setWidget(self.cleaner_in_progress_filler_widget)

    ## only insert a spacer if there is no spacer in the target layout
    if self.target_layout.count() == 0:
        self.target_layout.addStretch()
    # self.target_layout.itemAt(0).setObjectName('spacer')

    ## start the scanning process
    self.cleaner_backend.start()

    # ## auto adjusting the layout here.
    # self.target_layout.addStretch()
    pass


def threshold_rewrite(self):
    text_huge_th = self.cleaner_page_huge_file_threshold_combo.currentText()[:-2]
    text_huge_pf = self.cleaner_page_huge_file_threshold_combo.currentText()[-2:]
    text_outd_th = self.cleaner_page_outd_file_threshold_combo.currentText()

    if text_huge_pf == 'MB':
        tar_huge_tx = int(text_huge_th) * 1024 * 1024
    elif text_huge_pf == 'GB':
        tar_huge_tx = int(text_huge_th) * 1024 * 1024 * 1024
    else:
        tar_huge_tx = 52428800

    self.cleaner_backend.huge_file_size_threshold = tar_huge_tx

    if text_outd_th == '三天':
        self.cleaner_backend.outd_file_time_threshold = 3
    elif text_outd_th == '五天':
        self.cleaner_backend.outd_file_time_threshold = 5
    elif text_outd_th == '半个月':
        self.cleaner_backend.outd_file_time_threshold = 15
    elif text_outd_th == '一个月':
        self.cleaner_backend.outd_file_time_threshold = 30
    elif text_outd_th == '三个月':
        self.cleaner_backend.outd_file_time_threshold = 90
    elif text_outd_th == '半年':
        self.cleaner_backend.outd_file_time_threshold = 180
    elif text_outd_th == '一年':
        self.cleaner_backend.outd_file_time_threshold = 365
    # print('text test', text_huge_th)
    # print('text test', text_huge_pf)
    # print('text test', text_outd_th) = QPushButton()


def on_going_leave_page(self):
    ## cleaner page refresh
    print('cleaner page refresh')
    self.cleaner_re_enter_patch = True

    for item_co in range(self.target_layout.count() - 1):
        # self.target_layout.itemAt(item_co).widget().deleteLater()
        try:
            # print('test')
            self.target_layout.itemAt(item_co).widget().deleteLater()
        except AttributeError as err_msg:
            print('Encountered problem while deleting the spacer. ', err_msg)
            # continue
    try:
        for btn_co in range(self.huge_file_len):
            target_btn_name = 'huge_file_button_' + str(btn_co)
            try:
                exec('del self.{}'.format(target_btn_name))
            except AttributeError as err_msg:
                print('Encountered problem while deleting the huge file button. ', err_msg)
                # continue
    except AttributeError as err_msg:
        print('now does not have the attribute', err_msg)

    # for btn_co in range(self.outd_file_len):
    #     target_btn_name = 'outd_file_button_' + str(btn_co)
    #     exec('del self.{}'.format(target_btn_name))

    # print('triggered on leave page')
    # print(self.huge_box_sub_lay.count())
    # del self.huge_box_sub_lay
    # print('last line', self.target_layout.count())

    pass


def on_status_cleaner_in_progress_pgsBar_setValue(self, value):
    self.cleaner_in_progress_pgsBar.setValue(value)

    ## can add functions to present sub results in the layout
    ## can add callers to alter the prompt message there.

    if (value > 0) & (value <= 25):
        self.cleaner_in_progress_cleanProgress.setText('正在全面扫描...已发现%2.2f%s可清理项。' % (self.cleaner_in_progress_sum_size,
                                                                                     self.cleaner_in_progress_sum_postfix))
        if value == 25:
            redundancy_file_result_disp(self)

            sum_size, postfix = file_size_helper(self.cleaner_backend.thumbnails_size)
            self.tbnl_result_button.setText('缩略图记录\n%2.2f%s' % (sum_size, postfix))
            redundancy_file_button_empty_helper(self, self.tbnl_result_button, sum_size, postfix)

            sum_size, postfix = file_size_helper(self.cleaner_backend.cache_size)
            self.cache_result_button.setText('系统缓存区域\n%2.2f%s' % (sum_size, postfix))
            redundancy_file_button_empty_helper(self, self.cache_result_button, sum_size, postfix)

            sum_size, postfix = file_size_helper(self.cleaner_backend.recycle_bin_size)
            self.recycle_bin_result_button.setText('回收站文件\n%2.2f%s' % (sum_size, postfix))
            redundancy_file_button_empty_helper(self, self.recycle_bin_result_button, sum_size, postfix)

            ## update the sub title: how many files are selected. 
            redundancy_file_subtitle_updater(self, True)

    if (value > 25) & (value <= 50):
        self.cleaner_in_progress_cleanProgress.setText('正在扫描使用记录...')

        if value == 50:
            priv_result_disp(self)
            if self.cleaner_backend.recently_used_record_flag is False:
                self.recently_used_button.setText('文件访问历史\n未检出')
                self.recently_used_button.setCheckable(False)

            if self.cleaner_backend.bash_history_flag is False:
                self.terminal_rec_button.setText('终端操作记录\n未检出')
                self.terminal_rec_button.setCheckable(False)

            if self.cleaner_backend.browser_flag is False:
                self.brsr_hist_button.setText('浏览器访问记录\n未检出')
                self.brsr_hist_button.setCheckable(False)

            priv_result_subtitle_updater(self, True)

    if (value > 50) & (value <= 75):
        self.cleaner_in_progress_cleanProgress.setText(
            '扫描大型文件中...累计发现%2.2f%s可清理项。' % (self.cleaner_in_progress_sum_size,
                                            self.cleaner_in_progress_sum_postfix))
        if value == 75:
            # print('entered')
            huge_file_result_disp(self)

            ## implement the updater here
            huge_file_result_subtitle_updater(self, True)

    ## if we do not use a bracket here, the value <= 100 will always be held
    if (value > 75) & (value <= 100):
        self.cleaner_in_progress_cleanProgress.setText(
            '扫描长期未访问文件中...累计发现%2.2f%s可清理项。' % (self.cleaner_in_progress_sum_size,
                                               self.cleaner_in_progress_sum_postfix))

        if value == 100:
            ## demonstrate the outdated files here.
            outd_file_result_disp(self)

            outd_file_result_subtitle_updater(self, True)

            self.cleaner_in_progress_cleanProgress.setText(
                '扫描结束。累计发现了%2.2f%s可清理项。\n请点击清理为电脑加速哦💗' % (self.cleaner_in_progress_sum_size,
                                                           self.cleaner_in_progress_sum_postfix))
            self.cleaner_in_progress_btn_nowClean.setVisible(True)

            self.cleaner_in_progress_pgsBar.setVisible(False)

    # ## unnecessary code here.
    # if value == 100:
    #     self.target_layout.addStretch()
    pass


def on_status_cleaner_in_progress_sum_result(self, value):
    ## in MB
    sum_size = round(int(value) / 1048576, 2)

    if sum_size >= 1024:
        ## in GiB
        sum_size = round(sum_size / 1024, 2)

        self.cleaner_in_progress_sum_size = float(sum_size)
        self.cleaner_in_progress_sum_postfix = str('GB')

        if sum_size >= 1024:
            sum_size = round(sum_size / 1024, 2)

            self.cleaner_in_progress_sum_size = float(sum_size)
            self.cleaner_in_progress_sum_postfix = str('TB')
    else:
        self.cleaner_in_progress_sum_size = float(sum_size)
        self.cleaner_in_progress_sum_postfix = str('MB')

    # if self.cleaner_in_progress_sum_size < 0:
    #     print(self.cleaner_backend.full_path)
    #     print(self.cleaner_backend.size)
    #     print(self.cleaner_backend.dump_size)
    #     print(value)
    #     raise ValueError

    ## call the update function to replace the contents displayed in the prompt
    # current_progress = self.cleaner_in_progress_pgsBar.value()
    # on_status_cleaner_in_progress_pgsBar_setValue(self, current_progress)
    pass


## to convert the file size for a single file
def file_size_helper(value):
    ## in MB
    sum_size = round(int(value) / 1048576, 2)

    if sum_size >= 1024:
        ## in GiB
        sum_size = round(sum_size / 1024, 2)
        postfix = str('GB')
    else:
        sum_size = float(sum_size)
        postfix = str('MB')
    return sum_size, postfix


def redundancy_file_button_empty_helper(self, target, sum_size, postfix):
    if (int(sum_size) == int(0)) & (postfix == str('MB')):
        if target == self.tbnl_result_button:
            self.tbnl_result_button.setText('缩略图记录\n未检出')
            self.tbnl_result_button.setCheckable(False)
            pass
        if target == self.cache_result_button:
            self.cache_result_button.setText('系统缓存区域\n未检出')
            self.cache_result_button.setCheckable(False)
            pass
        if target == self.recycle_bin_result_button:
            self.recycle_bin_result_button.setText('回收站文件\n未检出')
            self.recycle_bin_result_button.setCheckable(False)
            pass
    pass


def redundancy_file_subtitle_updater(self, manual_call = False):
    ## fetching the sender signal
    sender_info = self.sender()
    # print('name', sender_info.objectName())

    ## add the condition for this patch to work
    if (manual_call is False) & (self.cleaner_re_enter_patch is True):
        target_btn_name = str(sender_info.objectName())
        # print('patch applied. ')
        if getattr(self, target_btn_name).isChecked():
            getattr(self, target_btn_name).setChecked(False)
        else:
            getattr(self, target_btn_name).setChecked(True)

    ## update the text for the first subtitle

    selected_sum = 0
    total_sum = 0

    if self.tbnl_result_button.isChecked():
        selected_sum += self.cleaner_backend.thumbnails_size

    if self.cache_result_button.isChecked():
        selected_sum += self.cleaner_backend.cache_size

    if self.recycle_bin_result_button.isChecked():
        selected_sum += self.cleaner_backend.recycle_bin_size

    if self.tbnl_result_button.isCheckable():
        total_sum += self.cleaner_backend.thumbnails_size

    if self.cache_result_button.isCheckable():
        total_sum += self.cleaner_backend.cache_size

    if self.recycle_bin_result_button.isCheckable():
        total_sum += self.cleaner_backend.recycle_bin_size

    # total_sum = self.cleaner_backend.thumbnails_size + self.cleaner_backend.cache_size + \
    #             self.cleaner_backend.recycle_bin_size

    selected_size, selected_postfix = file_size_helper(selected_sum)
    total_size, total_postfix = file_size_helper(total_sum)

    # self.redu_box.toggle_button.setText('缓存 + 冗余文件  共%2.2f%s，已选中%2.2f%s' % (total_size, total_postfix,
    #                                                                         selected_size, selected_postfix))

    for item_co in range(self.target_layout.count() - 1):
        if self.target_layout.itemAt(item_co).widget().objectName() == 'redu_box':
            try:
                self.target_layout.itemAt(item_co).widget().toggle_button.setText(
                    '缓存 + 冗余文件  共%2.2f%s，已选中%2.2f%s' % (total_size, total_postfix,
                                                        selected_size, selected_postfix))
            except AttributeError as err_msg:
                print('subtitle update failed. ', err_msg)
    pass


def redundancy_file_result_disp(self):
    self.redu_box = CollapsibleBox('缓存 + 冗余文件')

    ## use the following line to set it automatically unfold
    self.redu_box.on_pressed()
    self.redu_box.toggle_button.setChecked(True)

    self.redu_box.setObjectName('redu_box')

    par_redundancy_file_subtitle_updater = partial(redundancy_file_subtitle_updater, self, False)
    # print('checking validation', self.target_layout.count(), self.cleaner_ip_redu_addable)
    # print((self.target_layout.count() <= 4) & (self.cleaner_ip_redu_addable))
    if (self.target_layout.count() <= 4) & (self.cleaner_ip_redu_addable):
        # self.target_layout.addWidget(self.redu_box)
        self.target_layout.insertWidget(self.target_layout.count() - 1, self.redu_box)
        self.cleaner_ip_redu_addable = False

    ## create a sub horizontal layout here
    sub_lay = QtWidgets.QHBoxLayout()
    # sub_lay.setContentsMargins(5)
    sub_lay.setSpacing(18)

    ## thumbnail button
    self.tbnl_result_button = QPushButton()
    self.tbnl_result_button.setObjectName('tbnl_result_button')
    self.tbnl_result_button.setMinimumSize(200, 100)
    self.tbnl_result_button.setMaximumSize(230, 100)
    self.tbnl_result_button.setText('缩略图记录\n20M')
    self.tbnl_result_button.setIcon(QIcon(':/images/Cleaner/u880.png'))
    self.tbnl_result_button.setIconSize(QtCore.QSize(55, 55))
    self.tbnl_result_button.setCheckable(True)
    self.tbnl_result_button.setChecked(True)
    self.tbnl_result_button.clicked.connect(par_redundancy_file_subtitle_updater)

    # self.tbnl_result_button.setDown()
    self.tbnl_result_button.setStyleSheet('QPushButton \n'
                                          '{font-size:14pt; \n'
                                          'color: rgb(51, 51, 51); \n'
                                          'border-radius: 10px; \n'
                                          # 'border-color: rgb(217,217,217); \n'
                                          'background-color: rgb(215, 215, 215); \n'
                                          '} \n'
                                          'QPushButton:hover \n'
                                          '{font-size:14pt; \n'
                                          'color: rgb(255, 255, 255); \n'
                                          'border-radius: 10px; \n'
                                          # 'border-color: rgb(217,217,217); \n'
                                          'background-color: rgb(165,215,235); \n'
                                          '} \n'
                                          'QPushButton:checked \n'
                                          '{font-size:14pt; \n'
                                          'color: rgb(255, 255, 255); \n'
                                          'border-radius: 10px; \n'
                                          # 'border-color: rgb(217,217,217); \n'
                                          'background-color: rgb(122,185,212); \n'
                                          '} ')
    sub_lay.addWidget(self.tbnl_result_button)

    ## cache button
    self.cache_result_button = QPushButton()
    self.cache_result_button.setObjectName('cache_result_button')
    self.cache_result_button.setMinimumSize(200, 100)
    self.cache_result_button.setMaximumSize(230, 100)
    self.cache_result_button.setText('系统缓存区域\n220M')
    self.cache_result_button.setIcon(QIcon(':/images/Cleaner/u917.png'))
    self.cache_result_button.setIconSize(QtCore.QSize(55, 55))
    self.cache_result_button.setCheckable(True)
    self.cache_result_button.setChecked(True)
    self.cache_result_button.clicked.connect(par_redundancy_file_subtitle_updater)

    # self.cache_result_button.setDown()
    self.cache_result_button.setStyleSheet('QPushButton \n'
                                           '{font-size:14pt; \n'
                                           'color: rgb(51, 51, 51); \n'
                                           'border-radius: 10px; \n'
                                           # 'border-color: rgb(217,217,217); \n'
                                           'background-color: rgb(215, 215, 215); \n'
                                           '} \n'
                                           'QPushButton:hover \n'
                                           '{font-size:14pt; \n'
                                           'color: rgb(255, 255, 255); \n'
                                           'border-radius: 10px; \n'
                                           # 'border-color: rgb(217,217,217); \n'
                                           'background-color: rgb(165,215,235); \n'
                                           '} \n'
                                           'QPushButton:checked \n'
                                           '{font-size:14pt; \n'
                                           'color: rgb(255, 255, 255); \n'
                                           'border-radius: 10px; \n'
                                           # 'border-color: rgb(217,217,217); \n'
                                           'background-color: rgb(122,185,212); \n'
                                           '} ')
    sub_lay.addWidget(self.cache_result_button)

    ## recycle bin button 
    self.recycle_bin_result_button = QPushButton()
    self.recycle_bin_result_button.setObjectName('recycle_bin_result_button')
    self.recycle_bin_result_button.setMinimumSize(200, 100)
    self.recycle_bin_result_button.setMaximumSize(230, 100)
    self.recycle_bin_result_button.setText('回收站文件\n120M')
    self.recycle_bin_result_button.setIcon(QIcon(':/images/Cleaner/u917.png'))
    self.recycle_bin_result_button.setIconSize(QtCore.QSize(55, 55))
    self.recycle_bin_result_button.setCheckable(True)
    self.recycle_bin_result_button.setChecked(True)
    self.recycle_bin_result_button.clicked.connect(par_redundancy_file_subtitle_updater)

    # self.recycle_bin_result_button.setDown()
    self.recycle_bin_result_button.setStyleSheet('QPushButton \n'
                                                 '{font-size:14pt; \n'
                                                 'color: rgb(51, 51, 51); \n'
                                                 'border-radius: 10px; \n'
                                                 # 'border-color: rgb(217,217,217); \n'
                                                 'background-color: rgb(215, 215, 215); \n'
                                                 '} \n'
                                                 'QPushButton:hover \n'
                                                 '{font-size:14pt; \n'
                                                 'color: rgb(255, 255, 255); \n'
                                                 'border-radius: 10px; \n'
                                                 # 'border-color: rgb(217,217,217); \n'
                                                 'background-color: rgb(165,215,235); \n'
                                                 '} \n'
                                                 'QPushButton:checked \n'
                                                 '{font-size:14pt; \n'
                                                 'color: rgb(255, 255, 255); \n'
                                                 'border-radius: 10px; \n'
                                                 # 'border-color: rgb(217,217,217); \n'
                                                 'background-color: rgb(122,185,212); \n'
                                                 '} ')
    sub_lay.addWidget(self.recycle_bin_result_button)

    ## in the end, add a stretch so that the contents will be arranged on the left
    sub_lay.addStretch()

    ##
    self.redu_box.setContentLayout(sub_lay)
    pass


def priv_result_subtitle_updater(self, manual_call = False):
    ## fetching the sender signal
    sender_info = self.sender()
    # print('name', sender_info.objectName())

    ## add the condition for this patch to work
    if (manual_call is False) & (self.cleaner_re_enter_patch is True):
        target_btn_name = str(sender_info.objectName())
        # print('patch applied. ')
        if getattr(self, target_btn_name).isChecked():
            getattr(self, target_btn_name).setChecked(False)
        else:
            getattr(self, target_btn_name).setChecked(True)

    ## update the text for the first subtitle

    selected_sum = 0
    total_sum = 0

    if self.recently_used_button.isChecked():
        selected_sum += 1
    if self.terminal_rec_button.isChecked():
        selected_sum += 1
    if self.brsr_hist_button.isChecked():
        selected_sum += 1

    if self.cleaner_backend.recently_used_record_flag & self.recently_used_button.isCheckable():
        total_sum += 1
    if self.cleaner_backend.bash_history_flag & self.terminal_rec_button.isCheckable():
        total_sum += 1
    if self.cleaner_backend.browser_flag & self.brsr_hist_button.isCheckable():
        total_sum += 1

    # self.priv_box.toggle_button.setText('隐私 + 使用记录  共%d项，已选中%d项' % (total_sum, selected_sum))

    for item_co in range(self.target_layout.count() - 1):
        if self.target_layout.itemAt(item_co).widget().objectName() == 'priv_box':
            try:
                self.target_layout.itemAt(item_co).widget().toggle_button.setText(
                    '隐私 + 使用记录  共%d项，已选中%d项' % (total_sum, selected_sum))
            except AttributeError as err_msg:
                print('subtitle update failed. ', err_msg)
    pass


def priv_result_disp(self):
    self.priv_box = CollapsibleBox('隐私 + 使用记录')

    self.priv_box.on_pressed()
    self.priv_box.toggle_button.setChecked(True)

    self.priv_box.setObjectName('priv_box')

    par_priv_result_subtitle_updater = partial(priv_result_subtitle_updater, self, False)

    if (self.target_layout.count() <= 4) & (self.cleaner_ip_priv_addable):
        # self.target_layout.addWidget(self.priv_box)
        self.target_layout.insertWidget(self.target_layout.count() - 1, self.priv_box)
        self.cleaner_ip_priv_addable = False

    ## create a sub horizontal layout here
    sub_lay = QtWidgets.QHBoxLayout()
    # sub_lay.setContentsMargins(5)
    sub_lay.setSpacing(18)

    ## recently used button
    self.recently_used_button = QPushButton()
    self.recently_used_button.setObjectName('recently_used_button')
    self.recently_used_button.setMinimumSize(200, 100)
    self.recently_used_button.setMaximumSize(230, 100)
    self.recently_used_button.setText('文件访问历史')
    self.recently_used_button.setIcon(QIcon(':/images/Cleaner/u880.png'))
    self.recently_used_button.setIconSize(QtCore.QSize(55, 55))
    self.recently_used_button.setCheckable(True)
    self.recently_used_button.setChecked(True)
    self.recently_used_button.clicked.connect(par_priv_result_subtitle_updater)

    # self.recently_used_button.setDown()
    self.recently_used_button.setStyleSheet('QPushButton \n'
                                            '{font-size:14pt; \n'
                                            'color: rgb(51, 51, 51); \n'
                                            'border-radius: 10px; \n'
                                            # 'border-color: rgb(217,217,217); \n'
                                            'background-color: rgb(215, 215, 215); \n'
                                            '} \n'
                                            'QPushButton:hover \n'
                                            '{font-size:14pt; \n'
                                            'color: rgb(255, 255, 255); \n'
                                            'border-radius: 10px; \n'
                                            # 'border-color: rgb(217,217,217); \n'
                                            'background-color: rgb(165,215,235); \n'
                                            '} \n'
                                            'QPushButton:checked \n'
                                            '{font-size:14pt; \n'
                                            'color: rgb(255, 255, 255); \n'
                                            'border-radius: 10px; \n'
                                            # 'border-color: rgb(217,217,217); \n'
                                            'background-color: rgb(122,185,212); \n'
                                            '} ')
    sub_lay.addWidget(self.recently_used_button)

    ## terminal (bash) access record
    self.terminal_rec_button = QPushButton()
    self.terminal_rec_button.setObjectName('terminal_rec_button')
    self.terminal_rec_button.setMinimumSize(200, 100)
    self.terminal_rec_button.setMaximumSize(230, 100)
    self.terminal_rec_button.setText('终端操作记录')
    self.terminal_rec_button.setIcon(QIcon(':/images/Cleaner/u880.png'))
    self.terminal_rec_button.setIconSize(QtCore.QSize(55, 55))
    self.terminal_rec_button.setCheckable(True)
    self.terminal_rec_button.setChecked(True)
    self.terminal_rec_button.clicked.connect(par_priv_result_subtitle_updater)

    # self.terminal_rec_button.setDown()
    self.terminal_rec_button.setStyleSheet('QPushButton \n'
                                           '{font-size:14pt; \n'
                                           'color: rgb(51, 51, 51); \n'
                                           'border-radius: 10px; \n'
                                           # 'border-color: rgb(217,217,217); \n'
                                           'background-color: rgb(215, 215, 215); \n'
                                           '} \n'
                                           'QPushButton:hover \n'
                                           '{font-size:14pt; \n'
                                           'color: rgb(255, 255, 255); \n'
                                           'border-radius: 10px; \n'
                                           # 'border-color: rgb(217,217,217); \n'
                                           'background-color: rgb(165,215,235); \n'
                                           '} \n'
                                           'QPushButton:checked \n'
                                           '{font-size:14pt; \n'
                                           'color: rgb(255, 255, 255); \n'
                                           'border-radius: 10px; \n'
                                           # 'border-color: rgb(217,217,217); \n'
                                           'background-color: rgb(122,185,212); \n'
                                           '} ')
    sub_lay.addWidget(self.terminal_rec_button)

    ## browser history
    self.brsr_hist_button = QPushButton()
    self.brsr_hist_button.setObjectName('brsr_hist_button')
    self.brsr_hist_button.setMinimumSize(200, 100)
    self.brsr_hist_button.setMaximumSize(230, 100)
    self.brsr_hist_button.setText('浏览器访问记录')
    self.brsr_hist_button.setIcon(QIcon(':/images/Cleaner/u880.png'))
    self.brsr_hist_button.setIconSize(QtCore.QSize(55, 55))
    self.brsr_hist_button.setCheckable(True)
    self.brsr_hist_button.setChecked(True)
    self.brsr_hist_button.clicked.connect(par_priv_result_subtitle_updater)

    # self.brsr_hist_button.setDown()
    self.brsr_hist_button.setStyleSheet('QPushButton \n'
                                        '{font-size:14pt; \n'
                                        'color: rgb(51, 51, 51); \n'
                                        'border-radius: 10px; \n'
                                        # 'border-color: rgb(217,217,217); \n'
                                        'background-color: rgb(215, 215, 215); \n'
                                        '} \n'
                                        'QPushButton:hover \n'
                                        '{font-size:14pt; \n'
                                        'color: rgb(255, 255, 255); \n'
                                        'border-radius: 10px; \n'
                                        # 'border-color: rgb(217,217,217); \n'
                                        'background-color: rgb(165,215,235); \n'
                                        '} \n'
                                        'QPushButton:checked \n'
                                        '{font-size:14pt; \n'
                                        'color: rgb(255, 255, 255); \n'
                                        'border-radius: 10px; \n'
                                        # 'border-color: rgb(217,217,217); \n'
                                        'background-color: rgb(122,185,212); \n'
                                        '} ')
    sub_lay.addWidget(self.brsr_hist_button)

    ## in the end, add a stretch so that the contents will be arranged on the left
    sub_lay.addStretch()

    ##
    self.priv_box.setContentLayout(sub_lay)
    pass


def huge_file_result_subtitle_updater(self, manual_call = False):
    # print('subtitle_updater activated. ')
    # print(self.cleaner_re_enter_patch)
    ## fetching the sender signal
    sender_info = self.sender()
    # print('name', sender_info.objectName())

    ## add the condition for this patch to work
    if (manual_call is False) & (self.cleaner_re_enter_patch is True):
        target_btn_name = 'huge_file_button_' + str(sender_info.objectName())
        # print('patch applied. ')
        if getattr(self, target_btn_name).isChecked():
            getattr(self, target_btn_name).setChecked(False)
        else:
            getattr(self, target_btn_name).setChecked(True)

    selected_sum = 0
    total_sum = self.cleaner_backend.huge_file_size

    for btn_co in range(self.huge_file_len):
        target_btn_name = 'huge_file_button_' + str(btn_co)
        # if btn_co < 3:
        #     print(target_btn_name, hasattr(self, target_btn_name), getattr(self, target_btn_name).isChecked())
        #     print(target_btn_name, getattr(self, target_btn_name).isCheckable())
        try:
            if getattr(self, target_btn_name).isChecked():
                current_item_size = int(self.cleaner_backend.huge_file[btn_co][1])
                selected_sum += current_item_size
        except AttributeError as err_msg:
            print('the checkbox is not working fine, ', err_msg)
            continue

    selected_fm_num, selected_fm_pof = file_size_helper(selected_sum)
    total_fm_sum, total_fm_pof = file_size_helper(total_sum)

    # self.huge_box.toggle_button.setText('超量大型文件  共%2.2f%s，已选中%2.2f%s' % (total_fm_sum, total_fm_pof,
    #                                                                      selected_fm_num, selected_fm_pof))

    for item_co in range(self.target_layout.count() - 1):
        if self.target_layout.itemAt(item_co).widget().objectName() == 'huge_box':
            try:
                self.target_layout.itemAt(item_co).widget().toggle_button.setText(
                    '超量大型文件  共%2.2f%s，已选中%2.2f%s' % (total_fm_sum, total_fm_pof,
                                                     selected_fm_num, selected_fm_pof))
            except AttributeError as err_msg:
                print('subtitle update failed. ', err_msg)


def huge_file_result_disp(self):
    ## adapting a horizontally distributed layout is needed here.

    self.huge_box = CollapsibleBox('超量大型文件')

    self.huge_box.on_pressed()
    self.huge_box.toggle_button.setChecked(True)
    self.huge_box.setObjectName('huge_box')

    par_huge_result_subtitle_updater = partial(huge_file_result_subtitle_updater, self, False)

    if (self.target_layout.count() <= 4) & (self.cleaner_ip_huge_addable):
        # self.target_layout.addWidget(self.huge_box)
        self.target_layout.insertWidget(self.target_layout.count() - 1, self.huge_box)
        self.cleaner_ip_huge_addable = False

    ## use a vertical layout here
    self.huge_box_sub_lay = QtWidgets.QVBoxLayout()
    # self.huge_box_sub_lay.setContentsMargins(5)
    self.huge_box_sub_lay.setSpacing(10)

    huge_file_len = len(self.cleaner_backend.huge_file)
    self.huge_file_len = huge_file_len

    for huge_item_index in range(huge_file_len):
        ## native information from the provider list
        item_path_info = self.cleaner_backend.huge_file[huge_item_index][0]
        item_size_info = self.cleaner_backend.huge_file[huge_item_index][1]
        last_access_info = self.cleaner_backend.huge_file[huge_item_index][2]
        last_modify_info = self.cleaner_backend.huge_file[huge_item_index][3]

        ## information about the huge file to be presented to the GUI
        item_name_info = item_path_info.split('/')[-1]
        item_rem_dir_info = item_path_info[:-len(item_name_info)]

        ## length restriction
        if len(item_rem_dir_info) >= 60:
            item_rem_dir_info = item_rem_dir_info[:60] + str('...')
        else:
            # elif len(item_rem_dir_info) < 60:
            padding_len = 80 - len(item_rem_dir_info)
            item_rem_dir_info = item_rem_dir_info + str(' ') * padding_len

            ## float, str
        item_size_fm_num, item_size_fm_pof = file_size_helper(item_size_info)

        # print(item_path_info, item_size_info, last_access_info, last_modify_info)
        # print(item_name_info, item_rem_dir_info, item_size_fm_num, item_size_fm_pof)

        target_btn_name = 'huge_file_button_' + str(huge_item_index)
        exec('self.{} = QPushButton()'.format(target_btn_name))
        getattr(self, target_btn_name).setObjectName(str(huge_item_index))
        getattr(self, target_btn_name).setMinimumSize(800, 75)
        getattr(self, target_btn_name).setMaximumSize(800, 100)
        getattr(self, target_btn_name).setText('文件名称 %s  \n占用大小 %2.2f %s \n存储位置 %s' % (item_name_info,
                                                                                       item_size_fm_num,
                                                                                       item_size_fm_pof,
                                                                                       item_rem_dir_info))
        getattr(self, target_btn_name).setIcon(QIcon(':/images/Cleaner/u880.png'))
        getattr(self, target_btn_name).setIconSize(QtCore.QSize(55, 55))
        getattr(self, target_btn_name).setCheckable(True)
        getattr(self, target_btn_name).setChecked(False)
        getattr(self, target_btn_name).clicked.connect(par_huge_result_subtitle_updater)
        getattr(self, target_btn_name).setStyleSheet('QPushButton \n'
                                                     '{font-size:12pt; \n'
                                                     'color: rgb(51, 51, 51); \n'
                                                     'border-radius: 10px; \n'
                                                     # 'border-color: rgb(217,217,217); \n'
                                                     'background-color: rgb(215, 215, 215); \n'
                                                     '} \n'
                                                     'QPushButton:hover \n'
                                                     '{font-size:12pt; \n'
                                                     'color: rgb(255, 255, 255); \n'
                                                     'border-radius: 10px; \n'
                                                     # 'border-color: rgb(217,217,217); \n'
                                                     'background-color: rgb(165,215,235); \n'
                                                     '} \n'
                                                     'QPushButton:checked \n'
                                                     '{font-size:12pt; \n'
                                                     'color: rgb(255, 255, 255); \n'
                                                     'border-radius: 10px; \n'
                                                     # 'border-color: rgb(217,217,217); \n'
                                                     'background-color: rgb(122,185,212); \n'
                                                     '} ')
        exec('self.huge_box_sub_lay.addWidget(self.{})'.format(target_btn_name))

    ## add a command to automatically adjust the layout
    self.huge_box.setContentLayout(self.huge_box_sub_lay)
    pass


def outd_file_result_subtitle_updater(self, manual_call = False):
    # print('huge file subtitle updater here. ')

    ## fetching the sender signal
    sender_info = self.sender()
    # print('name', sender_info.objectName())

    ## add the condition for this patch to work
    if (manual_call is False) & (self.cleaner_re_enter_patch is True):
        target_btn_name = 'outd_file_button_' + str(sender_info.objectName())
        # print('patch applied. ')
        if getattr(self, target_btn_name).isChecked():
            getattr(self, target_btn_name).setChecked(False)
        else:
            getattr(self, target_btn_name).setChecked(True)

    selected_sum = 0
    total_sum = self.cleaner_backend.outd_file_size

    for btn_co in range(self.outd_file_len):
        target_btn_name = 'outd_file_button_' + str(btn_co)
        # if btn_co < 3:
        #     print(target_btn_name, hasattr(self, target_btn_name), getattr(self, target_btn_name).isChecked())
        try:
            if getattr(self, target_btn_name).isChecked():
                current_item_size = int(self.cleaner_backend.outd_file[btn_co][1])
                selected_sum += current_item_size
        except AttributeError as err_msg:
            print('the checkbox is not working fine, ', err_msg)
            continue

    selected_fm_num, selected_fm_pof = file_size_helper(selected_sum)
    total_fm_sum, total_fm_pof = file_size_helper(total_sum)

    # self.outd_box.toggle_button.setText('长期未访问文件  共%2.2f%s，已选中%2.2f%s' % (total_fm_sum, total_fm_pof,
    #                                                                       selected_fm_num, selected_fm_pof))

    for item_co in range(self.target_layout.count() - 1):
        if self.target_layout.itemAt(item_co).widget().objectName() == 'outd_box':
            try:
                self.target_layout.itemAt(item_co).widget().toggle_button.setText(
                    '长期未访问文件  共%2.2f%s，已选中%2.2f%s' % (total_fm_sum, total_fm_pof,
                                                      selected_fm_num, selected_fm_pof))
            except AttributeError as err_msg:
                print('subtitle update failed. ', err_msg)
    pass


def outd_file_result_disp(self):
    self.outd_box = CollapsibleBox('长期未访问文件')

    self.outd_box.on_pressed()
    self.outd_box.toggle_button.setChecked(True)

    self.outd_box.setObjectName('outd_box')

    par_outd_result_subtitle_updater = partial(outd_file_result_subtitle_updater, self, False)

    if (self.target_layout.count() <= 4) & (self.cleaner_ip_outd_addable):
        # self.target_layout.addWidget(self.outd_box)
        self.target_layout.insertWidget(self.target_layout.count() - 1, self.outd_box)
        self.cleaner_ip_outd_addable = False

    ## use a vertical layout here
    self.outd_box_sub_lay = QtWidgets.QVBoxLayout()
    # self.outd_box_sub_lay.setContentsMargins(5)
    self.outd_box_sub_lay.setSpacing(10)

    outd_file_len = len(self.cleaner_backend.outd_file)
    self.outd_file_len = outd_file_len

    for outd_item_index in range(outd_file_len):
        ## native information from the provider list
        item_path_info = self.cleaner_backend.outd_file[outd_item_index][0]
        item_size_info = self.cleaner_backend.outd_file[outd_item_index][1]
        last_access_info = self.cleaner_backend.outd_file[outd_item_index][2]
        last_modify_info = self.cleaner_backend.outd_file[outd_item_index][3]

        ## information about the outd file to be presented to the GUI
        item_name_info = item_path_info.split('/')[-1]
        item_rem_dir_info = item_path_info[:-len(item_name_info)]

        ## length restriction
        if len(item_rem_dir_info) >= 60:
            item_rem_dir_info = item_rem_dir_info[:60] + str('...')
        else:
            # elif len(item_rem_dir_info) < 60:
            padding_len = 80 - len(item_rem_dir_info)
            item_rem_dir_info = item_rem_dir_info + str(' ') * padding_len

        ## float, str
        item_size_fm_num, item_size_fm_pof = file_size_helper(item_size_info)

        # print(item_path_info, item_size_info, last_access_info, last_modify_info)
        # print(item_name_info, item_rem_dir_info, item_size_fm_num, item_size_fm_pof)

        target_btn_name = 'outd_file_button_' + str(outd_item_index)
        exec('self.{} = QPushButton()'.format(target_btn_name))
        getattr(self, target_btn_name).setObjectName(str(outd_item_index))
        getattr(self, target_btn_name).setMinimumSize(800, 75)
        getattr(self, target_btn_name).setMaximumSize(800, 100)
        getattr(self, target_btn_name).setText('文件名称 %s  \n占用大小 %2.2f %s 最后访问时间 %s\n存储位置 %s' % (item_name_info,
                                                                                                item_size_fm_num,
                                                                                                item_size_fm_pof,
                                                                                                last_access_info,
                                                                                                item_rem_dir_info))
        getattr(self, target_btn_name).setIcon(QIcon(':/images/Cleaner/u880.png'))
        getattr(self, target_btn_name).setIconSize(QtCore.QSize(55, 55))
        getattr(self, target_btn_name).setCheckable(True)
        getattr(self, target_btn_name).setChecked(False)
        getattr(self, target_btn_name).clicked.connect(par_outd_result_subtitle_updater)
        getattr(self, target_btn_name).setStyleSheet('QPushButton \n'
                                                     '{font-size:12pt; \n'
                                                     'color: rgb(51, 51, 51); \n'
                                                     'border-radius: 10px; \n'
                                                     # 'border-color: rgb(217,217,217); \n'
                                                     'background-color: rgb(215, 215, 215); \n'
                                                     '} \n'
                                                     'QPushButton:hover \n'
                                                     '{font-size:12pt; \n'
                                                     'color: rgb(255, 255, 255); \n'
                                                     'border-radius: 10px; \n'
                                                     # 'border-color: rgb(217,217,217); \n'
                                                     'background-color: rgb(165,215,235); \n'
                                                     '} \n'
                                                     'QPushButton:checked \n'
                                                     '{font-size:12pt; \n'
                                                     'color: rgb(255, 255, 255); \n'
                                                     'border-radius: 10px; \n'
                                                     # 'border-color: rgb(217,217,217); \n'
                                                     'background-color: rgb(122,185,212); \n'
                                                     '} ')
        exec('self.outd_box_sub_lay.addWidget(self.{})'.format(target_btn_name))

    ## add a command to automatically adjust the layout
    self.outd_box.setContentLayout(self.outd_box_sub_lay)
    pass


def button_style_setter(tar_btn):
    ## can use some code to avoid the long code block for defining the stylesheet
    pass


def on_going_clean_now_action(self):
    print('clean now activated. ')

    self.cleaner_in_progress_cleanProgress.setText(
        '对选中的项目进行清理...🧹\n请稍后哦')

    # print(self.tbnl_result_button.isChecked())
    # print(self.cache_result_button.isChecked())
    # print(self.recycle_bin_result_button.isChecked())
    # print(self.recently_used_button.isChecked())
    # print(self.terminal_rec_button.isChecked())
    # print(self.brsr_hist_button.isChecked())

    ## redundancy check
    if self.tbnl_result_button.isChecked():
        self.cleaner_backend.thumbnails_clear()
        self.tbnl_result_button.setText('缩略图记录\n已清理')
        self.tbnl_result_button.setCheckable(False)
    if self.cache_result_button.isChecked():
        self.cleaner_backend.cache_dir_clear()
        self.cache_result_button.setText('系统缓存区域\n已清理')
        self.cache_result_button.setCheckable(False)
    if self.recycle_bin_result_button.isChecked():
        self.cleaner_backend.recycle_bin_clear()
        self.recycle_bin_result_button.setText('回收站文件\n已清理')
        self.recycle_bin_result_button.setCheckable(False)
        print(self.recycle_bin_result_button.isChecked())

    redundancy_file_subtitle_updater(self, True)

    ## priv check
    if self.recently_used_button.isChecked():
        self.cleaner_backend.recently_used_clear()
        self.recently_used_button.setText('文件访问历史\n已清理')
        self.recently_used_button.setCheckable(False)
    if self.terminal_rec_button.isChecked():
        self.cleaner_backend.bash_history_clear()
        self.terminal_rec_button.setText('终端操作记录\n已清理')
        self.terminal_rec_button.setCheckable(False)
    if self.brsr_hist_button.isChecked():
        self.cleaner_backend.browser_related_clean()
        self.brsr_hist_button.setText('浏览器访问记录\n已清理')
        self.brsr_hist_button.setCheckable(False)

    priv_result_subtitle_updater(self, True)

    ## huge files
    for btn_co in range(self.huge_file_len):
        target_btn_name = 'huge_file_button_' + str(btn_co)

        if getattr(self, target_btn_name).isChecked():
            current_item_path = str(self.cleanerc_backend.huge_file[btn_co][0])
            current_item_size = int(self.cleaner_backend.huge_file[btn_co][1])
            ## offload the clean function to the backend module
            self.cleaner_backend.remove_designated_file(current_item_path, dry_run = False)
            ## delete these button
            getattr(self, target_btn_name).deleteLater()
            self.cleaner_backend.huge_file_size -= int(current_item_size)

    # self.huge_box.setContentLayout(self.huge_box_sub_lay)
    huge_file_result_subtitle_updater(self, True)

    ## outdated files
    for btn_co in range(self.outd_file_len):
        target_btn_name = 'outd_file_button_' + str(btn_co)

        if getattr(self, target_btn_name).isChecked():
            current_item_path = str(self.cleaner_backend.outd_file[btn_co][0])
            current_item_size = int(self.cleaner_backend.outd_file[btn_co][1])
            ## offload the clean function to the backend module
            self.cleaner_backend.remove_designated_file(current_item_path, dry_run = False)
            ## delete these button
            getattr(self, target_btn_name).deleteLater()
            self.cleaner_backend.outd_file_size -= int(current_item_size)

    # self.outd_box.setContentLayout(self.outd_box_sub_lay)
    outd_file_result_subtitle_updater(self, True)

    self.cleaner_in_progress_cleanProgress.setText('选中的项目已经清理好啦💖')
    pass


## define the collapsible box class to present the clean results here.

class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, title = "", parent = None):
        super(CollapsibleBox, self).__init__(parent)

        self.toggle_button = QtWidgets.QToolButton(
            text = title, checkable = True, checked = False
        )
        # self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setStyleSheet('QToolButton \n'
                                         '{font-size: 12pt; \n'
                                         'color: rgb(51, 51, 51); \n'
                                         'border: none; }')
        self.toggle_button.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        self.content_area = QtWidgets.QScrollArea(
            maximumHeight = 0, minimumHeight = 0
        )
        self.content_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    @QtCore.pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow
        )
        self.toggle_animation.setDirection(
            QtCore.QAbstractAnimation.Forward
            if not checked
            else QtCore.QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (
                self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)
