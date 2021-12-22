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
import qtawesome as qta

from .SysTray_Report import SysTray_RP
from .SysTray_DoubleCheckExit import SysTray_DCE
from .SysTray_Theme_Picker import SysTray_Theme
from .SysTray_About import SysTray_About


class CyanFoxTray(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.Visual()
        self.Logic()

    def Visual(self):
        ## set the icon
        self.setIcon(QIcon(":/images/Home_Page/CyanFox_Icon_64px_White.svg"))
        # self.setIcon(qta.icon('fa5b.firefox', color = 'skyblue'))
        pass

    def Logic(self):
        # self.activated.connect(self.on_going_icon_activated)

        self.init_context_menu()
        pass

    def on_going_icon_activated(self, action):
        ## defining the behavior when the icon is clicked
        if action == QSystemTrayIcon.DoubleClick:
            print('double click')
            self.parent.show()
        # elif action == QSystemTrayIcon.Trigger:
            ## add action for single click
            pass
        pass

    def init_context_menu(self):
        cont_menu = QMenu()

        cm0 = QAction('蓝狐 - 竭诚服务。', self)
        # cm0 = QAction('蓝狐 - 竭诚为您服务。', self)
        # cm0.setIcon(QIcon(":/images/Home_Page/CyanFox_Icon_64px_Aqua.svg"))
        cm0.setIcon(QIcon(":/images/Home_Page/CyanFox_Icon.png"))
        # cm0.setIcon(qta.icon('fa5b.firefox', color = 'skyblue'))
        cm0.setEnabled(False)

        cm1 = QAction('打开 首页概览', self)
        cm1.setIcon(QIcon(':/images/Side_Button/Main_Checked.png'))
        cm1.triggered.connect(self.on_triggered_cm1)

        cm2 = QAction('打开 进程管理', self)
        cm2.setIcon(QIcon(':/images/Side_Button/ProcManager_Checked.png'))
        cm2.triggered.connect(self.on_triggered_cm2)

        cm3 = QAction('打开 全面清理', self)
        cm3.setIcon(QIcon(':/images/Side_Button/CleanerTool_Checked.png'))
        cm3.triggered.connect(self.on_triggered_cm3)

        cm4 = QAction('打开 性能监控', self)
        cm4.setIcon(QIcon(':/images/Side_Button/PerfMonitor_Checked.png'))
        cm4.triggered.connect(self.on_triggered_cm4)

        cm5 = QAction('打开 实用工具', self)
        cm5.setIcon(QIcon(':/images/Side_Button/Utilities_Checked.png'))
        cm5.triggered.connect(self.on_triggered_cm5)

        cm6 = QAction('打开 应用中心', self)
        cm6.setIcon(QIcon(':/images/Side_Button/AppStore_Checked.png'))
        cm6.triggered.connect(self.on_triggered_cm6)

        # cm_floater = self.on_status_floater()
        cm_floater = QAction('显示/隐藏 加速球', self)
        cm_floater.setIcon(qta.icon('mdi.chart-bubble', color = (150, 124, 169)))
        cm_floater.setEnabled(False)

        cm_theme = QAction('打开 风格切换', self)
        cm_theme.setIcon(qta.icon('fa5.window-restore', color = (150, 124, 169)))
        cm_theme.triggered.connect(self.on_triggered_cm_theme)

        cm_repo = QAction('打开 故障呈报', self)
        cm_repo.setIcon(qta.icon('mdi.account-question', color = (150, 124, 169)))
        cm_repo.triggered.connect(self.on_trigger_cm_repo)
        # cm_repo.setEnabled(False)

        cm_about = QAction('关于 蓝狐', self)
        cm_about.setIcon(qta.icon('mdi.unfold-more-vertical', color = (150, 124, 169)))
        cm_about.triggered.connect(self.on_trigger_cm_about)

        cm_end = QAction('退出 蓝狐', self)
        cm_end.setIcon(qta.icon('mdi.exit-to-app', color = 'red'))
        cm_end.triggered.connect(self.on_tiggered_cm_end)

        cont_menu.addAction(cm0)
        cont_menu.addSeparator()
        for cm_iter in range(1, 7):
            exec('cont_menu.addAction(cm%d)' % cm_iter)
        # cont_menu.addAction(cm0)
        cont_menu.addSeparator()
        cont_menu.addAction(cm_floater)
        cont_menu.addAction(cm_theme)
        cont_menu.addAction(cm_repo)
        cont_menu.addAction(cm_about)
        cont_menu.addSeparator()
        cont_menu.addAction(cm_end)

        self.setContextMenu(cont_menu)
        pass

    def on_status_floater(self):
        if hasattr(self, 'testdafsasdf'):
            if self.test.isVisible():
                action = QAction('隐藏 加速球', self)
        else:
            action = QAction('显示 加速球', self)

        return action

    def on_trigger_wake_up(self, target = None):
        print('func triggered')
        if target is not None:
            print(target)
            getattr(self.parent, target).click()

            if target == 'btn_toggle_AppStore':
                return None
        self.parent.show()

        # print(self.parent.isVisible())
        # # if not self.parent.isVisible():
        # #     self.parent.show()
        # self.parent.show()
        #
        # if target is not None:
        #     getattr(self.parent, target).click()

    def on_trigger_msg_gen(self, target_msg):
        message_title = '蓝狐 - 终端助手'
        message_content = target_msg
        subprocess.Popen(['notify-send', message_title, message_content])

    def on_triggered_cm1(self):
        self.on_trigger_wake_up('btn_toggle_Main')
        self.on_trigger_msg_gen('蓝狐又和主人见面啦，真开心呢。💖')
        pass

    def on_triggered_cm2(self):
        self.on_trigger_wake_up('btn_toggle_ProcManager')
        self.on_trigger_msg_gen('呼呼，进程管理页面已经打开啦。')

    def on_triggered_cm3(self):
        self.on_trigger_wake_up('btn_toggle_CleanerTool_stack')
        self.on_trigger_msg_gen('呼呼，全面清理页面已经打开啦。')

    def on_triggered_cm4(self):
        self.on_trigger_wake_up('btn_toggle_PerfMonitor')
        self.on_trigger_msg_gen('呼呼，性能监控页面已经打开啦。')

    def on_triggered_cm5(self):
        self.on_trigger_wake_up('btn_toggle_Utilities')
        self.on_trigger_msg_gen('呼呼，实用工具页面已经打开啦。')

    def on_triggered_cm6(self):
        self.on_trigger_wake_up('btn_toggle_AppStore')
        self.on_trigger_msg_gen('呼呼，应用中心页面已经打开啦。')

    def on_triggered_cm_theme(self):
        if not hasattr(self, 'theme_picker'):
            self.theme_picker = SysTray_Theme(self.parent)
        self.theme_picker.show()

    def on_trigger_cm_repo(self):
        if not hasattr(self, 'report_sub_window'):
            self.report_sub_window = SysTray_RP(self.parent)
        self.report_sub_window.show()
        self.on_trigger_msg_gen('遇到了问题呢？请不要担心，我们全力为您提供帮助！')
        pass

    def on_trigger_cm_about(self):
        if not hasattr(self, 'about_page'):
            self.about_page = SysTray_About()
        self.about_page.show()
        pass

    def on_tiggered_cm_end(self):
        if not hasattr(self, 'double_check_on_exit'):
            self.double_check_on_exit = SysTray_DCE(self.parent)
        self.double_check_on_exit.show()
        # self.on_trigger_msg_gen('主人，你不要我了吗嘤嘤QAQ')

        # self.parent.on_trigger_quit()
        # # QCoreApplication.quit()
        # # sys.exit()
        pass
