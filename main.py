import sys
import platform
from time import time, sleep, strftime
import subprocess
import signal

## import components from PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *

## import resources and layout
from UI.ui_main import Ui_MainWindow

## import utilities
## please note that the modules that can be imported must use _ instead of -
from Utils.Constant_Repo import draft_comm_sender_daemon

## import functions defining logic
from Logic import Process_Manager
from Logic import Netconnect_Manager
from Logic import Performance_Monitor
from Logic import Home_Logic
from Logic import Gen_Cleaner_Main
from Logic import Utilities
from Logic import AppStore_Caller
from Logic import Proc_Netconnect_Main
from Logic import System_Tray
from Logic import Side_Button_Setter

# ## import a dedicated function
# ## so that the assets can be wrapped in the package
# from Assets import Assets_Loader

## import visual assets
import qtawesome as qta


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        ## set the behavior when the app is launched.
        self.Visual()
        self.Logic()
        self.InitWorkflow()

    def Visual(self):

        ## setting the currently used taskbar name and icon

        self.setWindowIcon(QIcon(":/images/Home_Page/CyanFox_Icon.png"))
        # self.setWindowIcon(QIcon(":/images/Home_Page/CyanFox_Icon_64px_Aqua.svg"))
        # self.setWindowIcon(qta.icon('fa5b.firefox', color = 'skyblue'))
        # self.setWindowIcon(qta.icon('mdi.sticker-outline'))
        self.setWindowTitle('蓝狐 - 竭诚服务')
        self.label_credits.setText('内部评估版本。此拷贝不允许二次分发。')
        self.label_version.setText('2021 - 0.7.05gv α')

        self.frame_extra_menus.setVisible(False)

        # ## make the window top on the desktop
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        ## shadow effect
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)
        self.effect_shadow.setBlurRadius(30)
        self.effect_shadow.setColor(Qt.gray)
        self.centralwidget.setGraphicsEffect(self.effect_shadow)
        # self.centralwidget.setGraphicsEffect(self.effect_shadow)

        ## blur effect
        self.blur_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        self.blur_effect.setOffset(0, 0)
        self.blur_effect.setBlurRadius(25)
        self.blur_effect.setColor(QColor(239, 237, 255))

        ## make the window to the center of the screen
        ## get the geometry of the screen
        screen_geo = QDesktopWidget().screenGeometry()
        ## get the geometry of the current window
        window_geo = self.geometry()
        ## this line is dedicated for the main window,
        ## since the interactive area is on the right of the main window
        target_left_point = int((screen_geo.width() - window_geo.width()) / 2 - 100)
        target_top_point = int((screen_geo.height() - window_geo.height()) / 2)
        ## move the window
        self.move(target_left_point, target_top_point)

        ## setting icons for the side bat
        ## this setting can implement the target design

        ## setting the stylesheet of the buttons
        Side_Button_Setter.side_button_style(self)

        ## the app icon placeholder
        self.btn_App_Name_Container.setText(' 蓝狐')
        self.btn_App_Name_Container.setFlat(True)
        self.btn_App_Name_Container.setDisabled(False)
        self.btn_App_Name_Container.setIcon(QIcon(":/images/Home_Page/CyanFox_Icon_64px_Aqua.svg"))
        self.btn_App_Name_Container.setIconSize(QtCore.QSize(65, 65))
        self.btn_App_Name_Container.setStyleSheet("QPushButton {\n"
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

    def Logic(self):
        self.stackedWidget.setCurrentWidget(self.page_home)
        # print(self.stackedWidget.styleSheet())

        # self.label_top_insp_info.setText(self.btn_toggle_Main.text())

        ## an automatic manner
        for key, value in self.__dict__.items():
            if key.startswith('btn_toggle'):
                getattr(self, key).clicked.connect(self.Button)
                getattr(self, key).setCheckable(True)
                getattr(self, key).setIconSize(QtCore.QSize(20, 20))

        self.btn_toggle_Main.setChecked(True)
        self.btn_toggle_AppStore.setCheckable(False)
        # self.btn_toggle_Main.setDown(True)

        pass

    def Button(self):
        # fetch the signal.
        btnWidget = self.sender()

        ## setting the function to remain the pressed situation of a button
        def button_pressed_visual(btn_name):
            for key, value in self.__dict__.items():
                if key.startswith('btn_toggle'):
                    ## setDown -> setChecked
                    getattr(self, key).setChecked(False)
                    # getattr(self, key).setDown(False)
            getattr(self, btn_name).setChecked(True)
            # getattr(self, btn_name).setDown(True)

        ## setting the mapping relationship between the button and the stacked item
        if btnWidget.objectName() == "btn_toggle_Main":
            self.stackedWidget.setCurrentWidget(self.page_home)
            button_text = getattr(self, btnWidget.objectName()).text()
            # self.label_top_insp_info.setText(button_text)
            button_pressed_visual(btnWidget.objectName())
            ## the following way can cause problem
            # Home_Logic.home_page_caller(self)
            Home_Logic.content_refresh_helper(self)

        if btnWidget.objectName() == "btn_toggle_ProcManager":
            self.stackedWidget.setCurrentWidget(self.page_process_manager)
            button_text = getattr(self, btnWidget.objectName()).text()
            # self.label_top_insp_info.setText(button_text)
            button_pressed_visual(btnWidget.objectName())
            # Process_Manager.processtable(self, mainp)
            # Netconnect_Manager.Nettable(self, mainp)
            Proc_Netconnect_Main.Porc_NetConnect_Call(self)
            # print(self.process_mng_refresh_delay.text())

        if btnWidget.objectName() == 'btn_toggle_CleanerTool_stack':
            self.stackedWidget.setCurrentWidget(self.page_cleaner_tools)
            button_text = getattr(self, btnWidget.objectName()).text()
            # self.label_top_insp_info.setText(button_text)
            button_pressed_visual(btnWidget.objectName())
            # Cleaner_Tool.stacked_cleaner_tool_page_caller(self)
            Gen_Cleaner_Main.cleaner_page_caller(self)

        if btnWidget.objectName() == "btn_toggle_PerfMonitor":
            self.stackedWidget.setCurrentWidget(self.page_perf_monitor)
            button_text = getattr(self, btnWidget.objectName()).text()
            # self.label_top_insp_info.setText(button_text)
            button_pressed_visual(btnWidget.objectName())
            Performance_Monitor.perf_mon_page_caller(self)

        if btnWidget.objectName() == "btn_toggle_Utilities":
            self.stackedWidget.setCurrentWidget(self.page_utilities)
            button_text = getattr(self, btnWidget.objectName()).text()
            # self.label_top_insp_info.setText(button_text)
            button_pressed_visual(btnWidget.objectName())
            Utilities.utilities_page_caller(self)

        if btnWidget.objectName() == "btn_toggle_AppStore":
            # self.stackedWidget.setCurrentWidget(self.page_app_store)
            button_text = getattr(self, btnWidget.objectName()).text()
            # self.label_top_insp_info.setText(button_text)
            # button_pressed_visual(btnWidget.objectName())
            AppStore_Caller.app_store_init(self)

    def InitWorkflow(self):
        # ## a prompt to involve the assets folder here
        # Assets_Loader.assets_load_status()

        ## insert the workflow for cs communication, configuration distribution and
        ## necessary utilities to be booted up while lauching the app

        ## communication to server side

        ## updating local configuration

        ## constant report
        self.cons_repo = draft_comm_sender_daemon.SystemInspect(ins_freq = 7000)
        self.cons_repo.daemon = True
        self.cons_repo.ins_flag = False
        self.cons_repo.start()

        ## logic for home
        ## to deal with the problem of home logic not functioning if that button is not pressed
        ## call the relevant function here
        ## if this line is above the constant repo, the thread callback will not work
        Home_Logic.home_page_caller(self)
        pass

    def closeEvent(self, event) -> None:
        ## rewrite the close event to cooperate with the system tray
        event.ignore()
        print('main window hidden. ')
        self.hide()
        ## so as to ensure that there will be no additional resource consumption.
        self.stackedWidget.setCurrentWidget(self.page_home)

        message_title = '蓝狐 - 终端助手'
        message_content = '蓝狐已经藏到系统托盘里啦，有需要可以随时叫醒我呢啾咪。💖'
        subprocess.Popen(['notify-send', message_title, message_content])

    def on_trigger_quit(self):
        print('main class triggered quit. ')

        ## first, we need to make sure that all the threading has been stopped
        signal.raise_signal(signal.SIGKILL)

        ## then call native functions to stop it

        # QCoreApplication.quit()
        # sys.exit()
        # app.quit()
        # self.hide()
        # app.quit()
        pass


if __name__ == "__main__":
    ## this line is a fixed configuration
    ## use QApplication to make an instance of app
    app = QApplication(sys.argv)
    ## so that the image assets will be loaded in a higher resolution
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    mainp = MyWindow()
    ## this argument can be adjusted to delay the demonstration of the pop-up of this window
    ## can use this time for the pre-render of the home page
    ## and the execution of subsequent functions in the background
    # QApplication.processEvents()
    # sleep(1)
    QApplication.processEvents()
    mainp.show()

    ## add some argument for the system tray function here.
    sys_tray = System_Tray.CyanFoxTray(mainp)
    sys_tray.show()

    # ## if the mainp is closed, then the application should be terminated here
    # QtCore.QTimer.singleShot(0, mainp.close)
    sys.exit(app.exec_())
