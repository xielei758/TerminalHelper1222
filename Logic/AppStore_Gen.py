import sys
import platform
import time
import json

## import components from PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent, pyqtSignal)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

## import some other components here.
from functools import partial
import subprocess
import threading
from threading import Thread
from time import sleep

import qtawesome as qta

## import utilities here
## the following line caused some top-level import error

sys.path.append('..')

## import the ui layout of sub pages
from UI.sub_pages.ui_app_store_gen import Ui_AppStoreGen

## import resources files here
from UI import ui_image_assets


class AppStore_Gen(QMainWindow, Ui_AppStoreGen):
    def __init__(self, parent = None):
        super().__init__()
        # super(AppStore_Sep, self).__init__(parent)
        self.setupUi(self)

        self.parent = parent

        self.sub_window_visual()

        self.fetch_info()

        self.app_store_init_visual()
        self.app_store_init_logic()

        ## this line needs to be formatted when all the elements are initiated here.
        self.sub_window_element_setter()

    def sub_window_visual(self):
        self.setWindowTitle('蓝狐 - 应用中心')
        self.setWindowIcon(QIcon(":/images/Home_Page/CyanFox_Icon_64px_White.svg"))

        ## to address the bug that search bat cannot work with Chinese characters
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.Dialog)

        self.activateWindow()

        # ## make the window top on the desktop
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        ## shadow effect
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)
        self.effect_shadow.setBlurRadius(30)
        self.effect_shadow.setColor(Qt.gray)
        # self.setGraphicsEffect(self.effect_shadow)
        # self.centralwidget.setGraphicsEffect(self.effect_shadow)
        # self.centralwidget.setStyleSheet('background-color: rgb(240, 250, 254); \n')

        ## make the window to the center of the screen
        ## get the geometry of the screen
        screen_geo = QDesktopWidget().screenGeometry()
        ## get the geometry of the current window
        window_geo = self.geometry()
        target_left_point = int((screen_geo.width() - window_geo.width()) / 2 - 100)
        target_top_point = int((screen_geo.height() - window_geo.height()) / 2)
        ## move the window
        self.move(target_left_point, target_top_point)

        self.frame_extra_menus.setVisible(False)

        ## to fill the placeholders on the main page.
        self.placeholder_visual_set()

        ## to change the element stylesheet on the app detail page.
        self.appstore_detail_page_visual()

        pass

    def sub_window_element_setter(self):
        ## define the elements on the page
        ## e.g. the buttons, the lines, etc.

        ## the app icon
        ## the app icon placeholder
        self.btn_App_Name_Container.setText('')
        self.btn_App_Name_Container.setFlat(True)
        self.btn_App_Name_Container.setDisabled(False)
        self.btn_App_Name_Container.setIcon(QIcon(":/images/Home_Page/CyanFox_Icon_64px_White.svg"))
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

        self.btn_App_Name_Container_title.setText('应用中心')
        self.btn_App_Name_Container_title.setFlat(True)
        self.btn_App_Name_Container_title.setDisabled(True)
        # self.btn_App_Name_Container_title.setIcon(QIcon(":/images/Home_Page/CyanFox_Icon_64px_White.svg"))
        # self.btn_App_Name_Container_title.setIconSize(QtCore.QSize(55, 55))
        self.btn_App_Name_Container_title.setStyleSheet("QPushButton {\n"
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

        ## controls the bottom line
        # self.frame_grip.setVisible(False)
        version_mark = str('0.1.05 α')
        self.label_credits.setText(f'蓝狐应用商店 {version_mark}')
        self.label_version.setText(f'应用目录最近更新于 {time.strftime("%Y-%m-%d %H:%M", time.localtime())}')

        ## setting the stylesheet of the buttons and qlineedit
        ## this part should be defined under the definition of such elements there.
        pass

    def app_store_init_visual(self):

        ## making sure that the placeholder in the QLineEdit can shift its color
        ## then the placeholder text will be dimmed

        self.search_bar_empty_sheet = 'QLineEdit{ \n' \
                                      'border: 3px solid rgba(255, 255, 255, 180); \n' \
                                      'border-radius: 8px; \n' \
                                      'background: transparent; \n' \
                                      'font: 12pt "Noto Mono"; \n' \
                                      'color: rgba(255, 255, 255, 110); \n' \
                                      '}'

        self.search_bar_filled_sheet = 'QLineEdit{ \n' \
                                       'border: 3px solid rgba(255, 255, 255, 180); \n' \
                                       'border-radius: 8px; \n' \
                                       'background: transparent; \n' \
                                       'font: 12pt "Noto Mono"; \n' \
                                       'color: rgba(255, 255, 255, 190); \n' \
                                       '}'

        self.search_bar_edit.setAttribute(Qt.WA_InputMethodEnabled, True)
        self.search_bar_edit.setAttribute(Qt.WA_InputMethodTransparent, False)

        # self.search_bar_edit.textChanged.connect(self.search_bar_reset_stylesheet)

        pass

    def app_store_init_logic(self):

        ## banner logic here
        self.bind_banner_prev_logic()
        self.banner_cycle_logic_caller()

        ## set the default placeholder text for the search bar
        self.search_bar_edit.setPlaceholderText('呼呼，在这里输入想要搜索的内容')

        ## hide the return button here
        self.search_bar_return_btn.setVisible(False)

        ## bind the logic of the side buttons here.
        self.side_button_logic()

        ## bind the logic of the search button
        self.search_bar_trigger_btn.clicked.connect(self.on_click_search_btn)

        ## bind the logic of the return button
        self.search_bar_return_btn.clicked.connect(self.on_click_return_btn)

        ## bind the button for app detail page
        self.page_home_app_detail.clicked.connect(self.on_entering_app_detail_page)
        pass

    def bind_banner_prev_logic(self):
        for key, value in self.__dict__.items():
            if key.startswith('page_home_banner_prev'):
                getattr(self, key).clicked.connect(self.banner_action)
        pass

    def banner_cycle_logic_caller(self):
        self.banner_cycle_daemon = threading.Thread(target = self.banner_cycle_logic)
        self.banner_cycle_daemon.start()
        pass

    def banner_cycle_logic(self):
        self.current_prev = 0
        self.prev_banner_count = int(self.page_home_banner_main_ver.count()) - 1

        while True:
            sleep(6)
            self.banner_cycle_executor()
        pass

    def banner_cycle_executor(self):
        self.current_prev = self.current_prev + 1 if self.current_prev <= self.prev_banner_count else 1
        exec('self.page_home_banner_prev_%d.click()' % self.current_prev)
        pass

    def banner_action(self):
        btnWidget = self.sender()

        clicked_prev_button_id = btnWidget.objectName().split('_')[-1]
        self.current_prev = int(clicked_prev_button_id)
        # print('current prev changed. ')

        current_stylesheet = getattr(self, btnWidget.objectName()).styleSheet()

        current_stylesheet_array = current_stylesheet.split('\n')

        ## initiate this var here.
        current_border_image = None

        for cont in current_stylesheet_array:
            if cont.startswith('border-image'):
                current_border_image = cont.split('image:')[-1][:-2]

        target_stylesheet = ('QPushButton \n'
                             '{font-size:16pt; \n'
                             'color: rgb(0, 0, 0); \n'
                             'border-image: %s; \n'
                             'border-radius: 6px; \n}' % current_border_image)

        self.page_home_banner_main_content.setStyleSheet(target_stylesheet)

        pass

    def appstore_detail_page_visual(self):
        ## this function controls the elements on the detail page of an App.

        self.app_detail_icon_placeholder.setText('')
        self.app_detail_icon_placeholder.setFlat(True)
        self.app_detail_icon_placeholder.setDisabled(False)
        self.app_detail_icon_placeholder.setIcon(QIcon(":/images/Home_Page/CyanFox_Icon_64px_Aqua.svg"))
        self.app_detail_icon_placeholder.setIconSize(QtCore.QSize(105, 105))
        self.app_detail_icon_placeholder.setStyleSheet("QPushButton {\n"
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

        self.app_detail_promo_pic_placeholder_1.setStyleSheet('QPushButton \n'
                                                              '{font-size:16pt; \n'
                                                              'color: rgb(0, 0, 0); \n'
                                                              'border-image: url(":/images/App_Store/placeholder.png"); \n'
                                                              'border-radius: 6px; \n}')
        self.app_detail_promo_pic_placeholder_2.setStyleSheet('QPushButton \n'
                                                              '{font-size:16pt; \n'
                                                              'color: rgb(0, 0, 0); \n'
                                                              'border-image: url(":/images/App_Store/placeholder.png"); \n'
                                                              'border-radius: 6px; \n}')

        pass

    def on_entering_app_detail_page(self):
        self.search_bar_return_btn.setVisible(True)

        ## prepare for the content on this page
        ## for example, app name, etc.
        app_name = None

        par_on_click_app_detail_install_button = partial(self.on_click_app_install, app_name)
        self.app_detail_install_button.clicked.connect(par_on_click_app_detail_install_button)

        ## change the subpage
        self.AppStore_stackedWidget.setCurrentWidget(self.page_app_detail)
        pass

    def on_click_app_install(self, app_name):
        ## this function is for the purpose of executing the app installation
        print('now installing', app_name)
        pass

    def fetch_info(self):
        pass

    def side_button_logic(self):
        for key, value in self.__dict__.items():
            if key.startswith('btn_toggle'):
                getattr(self, key).clicked.connect(self.Button)
                getattr(self, key).setCheckable(True)
                getattr(self, key).setIconSize(QtCore.QSize(26, 26))

        self.btn_toggle_Main.setChecked(True)
        self.btn_toggle_Main.click()
        self.side_button_icon_setter()

        # self.AppStore_stackedWidget.setCurrentWidget(self.page_app_detail)

        ## current logic of filling the subpages is that,
        ## this action will only happen once, when the AppStore is called.
        self.content_filler()
        pass

    def Button(self):
        btnWidget = self.sender()

        def button_pressed_visual(btn_name):
            for key, value in self.__dict__.items():
                if key.startswith('btn_toggle'):
                    ## setDown -> setChecked
                    getattr(self, key).setChecked(False)
                    # getattr(self, key).setDown(False)
            getattr(self, btn_name).setChecked(True)

        self.search_bar_return_btn.setVisible(False)

        if btnWidget.objectName() == "btn_toggle_Main":
            self.AppStore_stackedWidget.setCurrentWidget(self.page_home)
            button_pressed_visual(btnWidget.objectName())
            ## related to the banner recycle logic
            self.banner_recycle = True

        if btnWidget.objectName() == "btn_toggle_All":
            self.AppStore_stackedWidget.setCurrentWidget(self.page_all_apps)
            button_pressed_visual(btnWidget.objectName())

        if btnWidget.objectName() == "btn_toggle_Update":
            self.AppStore_stackedWidget.setCurrentWidget(self.page_update)
            button_pressed_visual(btnWidget.objectName())

        if btnWidget.objectName() == "btn_toggle_Uninstall":
            self.AppStore_stackedWidget.setCurrentWidget(self.page_uninstall)
            button_pressed_visual(btnWidget.objectName())

        pass

    def side_button_icon_setter(self):
        self.btn_toggle_Main.setIcon(qta.icon('mdi.home-outline', color = 'white'))
        self.btn_toggle_All.setIcon(qta.icon('mdi.select-all', color = 'white'))
        self.btn_toggle_Update.setIcon(qta.icon('mdi.update', color = 'white'))
        # mdi.timeline-check-outline
        self.btn_toggle_Uninstall.setIcon(qta.icon('mdi.recycle-variant', color = 'white'))
        pass

    def closeEvent(self, event) -> None:
        ## rewrite the close event to cooperate with the system tray
        event.ignore()
        # print('AppStore hidden. ')
        self.hide()

    def on_click_search_btn(self):
        target_text = self.search_bar_edit.text()

        print('the search btn is activated. ', target_text)
        if len(target_text) != 0:
            self.search_bar_return_btn.setVisible(True)
            self.AppStore_stackedWidget.setCurrentWidget(self.page_search)
        else:
            QMessageBox.question(self, "信号接收不到", "现在还没有输入要搜索的内容，执行不了搜索指令呢。", QMessageBox.Yes)
        pass

    def search_bar_reset_stylesheet(self):
        if not self.search_bar_edit.text():
            self.search_bar_edit.setStyleSheet(self.search_bar_empty_sheet)
        else:
            self.search_bar_edit.setStyleSheet(self.search_bar_filled_sheet)
        pass

    def on_click_return_btn(self):
        self.btn_toggle_Main.click()

        self.search_bar_return_btn.setVisible(False)
        pass

    def placeholder_visual_set(self):
        ## the main banner
        self.page_home_banner_main_content.setStyleSheet('QPushButton \n'
                                                         '{font-size:16pt; \n'
                                                         'color: rgb(0, 0, 0); \n'
                                                         'border-image: url(":/images/App_Store/placeholder_CPC.jpg"); \n'
                                                         'border-radius: 6px; \n}')
        self.page_home_banner_main_content.setText(' ')
        self.page_home_banner_main_content.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        ## side banners
        self.page_home_banner_prev_1.setStyleSheet('QPushButton \n'
                                                   '{font-size:16pt; \n'
                                                   'color: rgb(0, 0, 0); \n'
                                                   'border-image: url(":/images/App_Store/placeholder_side_1.jpg"); \n'
                                                   'border-radius: 6px; \n}')
        self.page_home_banner_prev_1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.page_home_banner_prev_2.setStyleSheet('QPushButton \n'
                                                   '{font-size:16pt; \n'
                                                   'color: rgb(0, 0, 0); \n'
                                                   'border-image: url(":/images/App_Store/placeholder_side_2.jpg"); \n'
                                                   'border-radius: 6px; \n}')
        self.page_home_banner_prev_2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.page_home_banner_prev_3.setStyleSheet('QPushButton \n'
                                                   '{font-size:16pt; \n'
                                                   'color: rgb(0, 0, 0); \n'
                                                   'border-image: url(":/images/App_Store/placeholder_side_3.jpg"); \n'
                                                   'border-radius: 6px; \n}')
        self.page_home_banner_prev_3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.page_home_banner_prev_4.setStyleSheet('QPushButton \n'
                                                   '{font-size:16pt; \n'
                                                   'color: rgb(0, 0, 0); \n'
                                                   'border-image: url(":/images/App_Store/placeholder_side_4.jpg"); \n'
                                                   'border-radius: 6px; \n}')
        self.page_home_banner_prev_4.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        pass

    def content_filler(self):
        self.on_init_all_apps_all_tab()
        self.on_init_all_apps_browser()
        self.on_init_all_apps_work()
        self.on_init_all_apps_entertainment()
        pass

    def page_controller(self, signal):
        table_widget = signal[2]
        total_page = table_widget.showTotalPage()
        if "home" == signal[0]:
            table_widget.curPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "翻不动了唔", "当前已经是首页了哦。", QMessageBox.Yes)
                return
            table_widget.curPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(self, "翻不动了唔", "现在已经是最后一页啦。", QMessageBox.Yes)
                return
            table_widget.curPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            table_widget.curPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if len(signal[1]) != 0:
                if total_page < int(signal[1]) or int(signal[1]) < 0:
                    QMessageBox.critical(self, "你输入的页码不太对的亚子", "输入的这个页码超出范围了哦。", QMessageBox.Yes)
                    return
            else:
                QMessageBox.critical(self, "页码框现在是空着的哦", "没办法跳到一个空着的页码哈。", QMessageBox.Yes)
                return
            table_widget.curPage.setText(signal[1])

        self.changeTableContent(table_widget)  # 改变表格内容

    def changeTableContent(self, table_widget: QTableWidget):
        """根据当前页改变表格的内容"""
        cur_page = table_widget.curPage.text()
        print(cur_page)
        # 改变表格内容
        create_table(self, table_widget.table, table_widget.Package_info, cur_page, table_widget.Total_pages)
        pass

    def on_init_all_apps_all_tab(self):
        self.recommandapp_table = TableWidget()
        self.recommandapp_table.setPageController(self.recommandapp_table.Total_pages, self.recommandapp_table,
                                                  self.all_apps_vbox_all_tab, self.all_apps_vbox_navi_tab)
        self.recommandapp_table.control_signal.connect(self.page_controller)
        pass

    def on_init_all_apps_browser(self):
        pass

    def on_init_all_apps_work(self):
        pass

    def on_init_all_apps_entertainment(self):
        pass

class TableWidget(QWidget):
    control_signal = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        self.__init_ui()

    def __init_ui(self):
        self.table = QTableWidget()  # 3 行 5 列的表格
        Init_table(self, self.table)
        # 获取Package信息，导入表格
        self.Package_info, self.Package_len = get_app_jsoninfo(self)

        # 假定一页是30个app，根据package_len确定总页数
        if self.Package_len % 30 == 0:
            self.Total_pages = int(self.Package_len / 30)
        else:
            self.Total_pages = int(self.Package_len / 30) + 1
        create_table(self, self.table, self.Package_info, 1, self.Total_pages)  # 初始创立第一页

        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应宽度

    def setPageController(self, page, table: object, layout: QVBoxLayout, layout_navi: QVBoxLayout):

        ## first determine if the target layout is empty
        target_layout_count = layout.count()

        ## if the target count is not zero, then clean the contents in that layout
        if target_layout_count != 0:
            print('init')
            for i in reversed(range(layout.count())):
                try:
                    layout.itemAt(i).widget().setParent(None)
                except AttributeError as err_msg:
                    print('AppStore: cannot delete elements in the target layout', err_msg)

        """自定义页码控制器"""
        control_layout = QHBoxLayout()
        homePage = QPushButton("首页")
        homePage.setStyleSheet("QPushButton {\n"
                               "    font-size:12pt; color: rgb(255, 255, 255);\n"
                               "    background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(56,81,111), stop:1 rgb(97,96,137));\n"
                               # "    border: none; \n"
                               # "    background-color: rgb(130, 109, 159);\n"
                               "}\n"
                               "QPushButton:hover {\n"
                               "    background-color: rgb(169, 135, 207);\n"
                               "}\n"
                               "QPushButton:pressed {    \n"
                               "    background-color: rgb(104, 87, 127);\n"
                               "}")

        prePage = QPushButton("<上一页")
        prePage.setStyleSheet("QPushButton {\n"
                              "    font-size:12pt; color: rgb(255, 255, 255);\n"
                              "    background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(56,81,111), stop:1 rgb(97,96,137));\n"
                              # "    border: none; \n"
                              # "    background-color: rgb(130, 109, 159);\n"
                              "}\n"
                              "QPushButton:hover {\n"
                              "    background-color: rgb(169, 135, 207);\n"
                              "}\n"
                              "QPushButton:pressed {    \n"
                              "    background-color: rgb(104, 87, 127);\n"
                              "}")

        self.curPage_prompt = QLabel("当前页")
        self.curPage_prompt.setStyleSheet('font: 12pt; \n')

        self.curPage = QLabel("1")
        nextPage = QPushButton("下一页>")
        nextPage.setStyleSheet("QPushButton {\n"
                               "    font-size:12pt; color: rgb(255, 255, 255);\n"
                               "    background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(56,81,111), stop:1 rgb(97,96,137));\n"
                               # "    border: none; \n"
                               # "    background-color: rgb(130, 109, 159);\n"
                               "}\n"
                               "QPushButton:hover {\n"
                               "    background-color: rgb(169, 135, 207);\n"
                               "}\n"
                               "QPushButton:pressed {    \n"
                               "    background-color: rgb(104, 87, 127);\n"
                               "}")

        finalPage = QPushButton("尾页")
        finalPage.setStyleSheet("QPushButton {\n"
                                "    font-size:12pt; color: rgb(255, 255, 255);\n"
                                "    background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(56,81,111), stop:1 rgb(97,96,137));\n"
                                # "    border: none; \n"
                                # "    background-color: rgb(130, 109, 159);\n"
                                "}\n"
                                "QPushButton:hover {\n"
                                "    background-color: rgb(169, 135, 207);\n"
                                "}\n"
                                "QPushButton:pressed {    \n"
                                "    background-color: rgb(104, 87, 127);\n"
                                "}")
        self.totalPage = QLabel("共" + str(page) + "页")
        self.totalPage.setStyleSheet('font: 12pt; \n')

        skipLable_0 = QLabel("跳到")
        skipLable_0.setStyleSheet('font: 12pt; \n')

        self.skipPage = QLineEdit()
        self.skipPage.setMaxLength(3)
        self.skipPage.setMaximumWidth(50)
        num_regx = QtCore.QRegExp("[0-9]")
        cust_validator = QtGui.QRegExpValidator(self)
        cust_validator.setRegExp(num_regx)
        self.skipPage.setValidator(cust_validator)
        self.skipPage.setStyleSheet("QLineEdit{\n"
                                    "    /* background-color: rgba(255, 255, 255, 200);\n"
                                    "    color: rgb(0, 0, 0);  */\n"
                                    "    border: 3px solid rgba(255, 255, 255, 180);\n"
                                    "    border-radius: 8px;\n"
                                    "    background: transparent;\n"
                                    "    font: 12pt \"Noto Mono\";\n"
                                    "    color: rgba(255, 255, 255, 180); \n"
                                    "    font-weight: bold;  \n"
                                    "}")

        skipLabel_1 = QLabel("页")
        skipLabel_1.setStyleSheet('font: 12pt; \n')

        confirmSkip = QPushButton("确定")
        confirmSkip.setStyleSheet("QPushButton {\n"
                                  "    font-size:12pt; color: rgb(255, 255, 255);\n"
                                  "    background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(56,81,111), stop:1 rgb(97,96,137));\n"
                                  # "    border: none; \n"
                                  # "    background-color: rgb(130, 109, 159);\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "    background-color: rgb(169, 135, 207);\n"
                                  "}\n"
                                  "QPushButton:pressed {    \n"
                                  "    background-color: rgb(104, 87, 127);\n"
                                  "}")

        homePage.clicked.connect(lambda: self.__home_page(table))
        prePage.clicked.connect(lambda: self.__pre_page(table))
        nextPage.clicked.connect(lambda: self.__next_page(table))
        finalPage.clicked.connect(lambda: self.__final_page(table))
        confirmSkip.clicked.connect(lambda: self.__confirm_skip(table))
        control_layout.addStretch(1)
        control_layout.addWidget(homePage)
        control_layout.addWidget(prePage)
        control_layout.addWidget(self.curPage_prompt)
        control_layout.addWidget(self.curPage)
        control_layout.addWidget(nextPage)
        control_layout.addWidget(finalPage)
        control_layout.addWidget(self.totalPage)
        control_layout.addWidget(skipLable_0)
        control_layout.addWidget(self.skipPage)
        control_layout.addWidget(skipLabel_1)
        control_layout.addWidget(confirmSkip)
        control_layout.addStretch(1)

        ## the following line adds the table to the target layout
        layout.addWidget(self.table)
        # layout_app.addWidget(self.table)
        # self.setLayout(layout)
        layout_navi.addLayout(control_layout)

    def __home_page(self, table: object):
        """点击首页信号"""
        self.control_signal.emit(["home", self.curPage.text(), table])

    def __pre_page(self, table: object):
        """点击上一页信号"""
        self.control_signal.emit(["pre", self.curPage.text(), table])

    def __next_page(self, table: object):
        """点击下一页信号"""
        self.control_signal.emit(["next", self.curPage.text(), table])

    def __final_page(self, table: object):
        """尾页点击信号"""
        self.control_signal.emit(["final", self.curPage.text(), table])

    def __confirm_skip(self, table: object):
        """跳转页码确定"""
        self.control_signal.emit(["confirm", self.skipPage.text(), table])

    def showTotalPage(self):
        """返回当前总页数"""
        return int(self.totalPage.text()[1:-1])

class AppDetail_Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super(AppDetail_Button, self).__init__(*args, **kwargs)
        self.detail_button = QPushButton()
        self.button_init()

    def button_init(self):
        # self.detail_button.setIconSize(QSize(35, 35))
        self.detail_button.setMinimumSize(155, 50)
        self.detail_button.setMaximumSize(155, 50)
        self.detail_button.setObjectName('AppInstall_Button')

        self.detail_button.setDefault(False)
        # self.detail_button.setCheckable(True)
        # self.detail_button.setChecked(True)
        self.detail_button.setStyleSheet('QPushButton \n'
                                         '{font-size:14pt; \n'
                                         'color: rgba(250, 250, 250, 230); \n'
                                         'background-color: rgb(129, 129, 183); \n'
                                         'border: none; \n'
                                         # 'border: 1px solid rgb(250, 250, 250); \n'
                                         '} \n'
                                         'QPushButton:hover \n'
                                         '{background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(56,81,111), stop:1 rgb(97,96,137)); \n'
                                         '} \n'
                                         'QPushButton:pressed \n'
                                         '{background-color: rgb(22, 62, 110); \n'
                                         '} ')

class Install_Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super(Install_Button, self).__init__(*args, **kwargs)
        self.install_button = QPushButton('一键安装', self)
        self.button_init()

    def button_init(self):
        self.install_button.setDefault(False)
        self.install_button.setMinimumSize(155, 25)
        self.install_button.setMaximumSize(155, 25)
        self.install_button.setStyleSheet('QPushButton \n'
                                          '{font-size:14pt; \n'
                                          'color: rgba(50, 50, 50, 200); \n'
                                          'background-color: rgb(230, 230, 230); \n'
                                          # 'border: 2px solid rgb(40, 40, 40); \n'
                                          '} \n'
                                          'QPushButton:hover \n'
                                          '{background-color: rgb(255, 255, 255); \n'
                                          '} \n'
                                          'QPushButton:checked \n'
                                          '{background-color: rgb(179, 179, 179); \n'
                                          '} ')

class MyprogressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(MyprogressBar, self).__init__(*args, **kwargs)
        self.Myprocbar = QProgressBar()
        self.Init()

    def Init(self):
        self.Myprocbar.setFormat(str("正在安装...%p%"))
        self.Myprocbar.setTextVisible(True)
        self.Myprocbar.setAlignment(Qt.AlignCenter)
        # self.Myprocbar.setRange(0,100)
        self.Myprocbar.setMaximum(0)
        self.Myprocbar.setMinimum(0)
        self.Myprocbar.setStyleSheet("QProgressBar{\n"
                                      "    border: 1px solid grey;\n"
                                      "    border-radius: 8px;\n"
                                      "    text-align: center\n"
                                      "}\n"
                                      "\n"
                                      "QProgressBar::chunk {\n"
                                      "    background-color: qlineargradient(y1: 0, y2: 1, stop: 0 rgb(229,152,155), stop: 1 rgb(170,141,171));\n"
                                      "    width: 7px;\n"
                                      "    margin: 1px;\n"
                                      "}")

class Install_UI(QWidget):
    def __init__(self, progress,button,parent=None):
        super(Install_UI, self).__init__()
        self.button = button
        self.progress = progress
        self.Init()

    def Init(self):
        self.process = QtCore.QProcess(self)
        self.process.finished.connect(self.finished)

    def finished(self):
        print(self.process.state())
        self.button.setText('已安装')
        self.button.setVisible(True)
        self.progress.setVisible(False)
        self.process = None

def Init_table(self, table: QTableWidget):
    table.setColumnCount(5)
    table.setSelectionMode(QAbstractItemView.NoSelection)
    table.setFocusPolicy(Qt.NoFocus)
    # 隐藏表头和网格线
    table.horizontalHeader().setVisible(False)
    table.verticalHeader().setVisible(False)
    table.setShowGrid(False)
    pass

def create_table(self, table: QTableWidget, Packages, page, totalpage):
    table.clear()
    row = 0
    column = 0
    App_count = []
    # 如果渲染的不是最后一页,需要渲染30个app
    if int(page) != int(totalpage):
        for i in range(30):
            item = (int(page) - 1) * 30 + i
            App_count.append(item)
    else:  # 如果渲染的是最后一页,
        # 计算最后一页App数量
        count_last = len(Packages) - (totalpage - 1) * 30
        for i in range(count_last):
            item = (int(page) - 1) * 30 + i
            App_count.append(item)
    for Package in App_count:
        table.setRowCount(row + 1)
        table.setRowHeight(row, 90)
        table.setColumnWidth(column, 165)
        widget = QWidget()
        app_name = "软件名" + str(Package)

        Detail_Button = AppDetail_Button()
        Detail_Button.detail_button.setText(app_name)
        Detail_Button.detail_button.setIcon(QIcon(':/images/Cleaner/u880.png'))
        Detail_Button.detail_button.setIconSize(QtCore.QSize(35, 35))
        Detail_Button.detail_button.setProperty('Package', Packages[Package]['Package'])
        Detail_Button.detail_button.clicked.connect(lambda: app_detail(self, app_name))


        Install = Install_Button()
        Install.install_button.setProperty('Package', Packages[Package]['Package'])
        Install.install_button.clicked.connect(lambda: Install_app(self, app_name, table))

        Install_Bar = MyprogressBar()
        Install_Bar.Myprocbar.setVisible(False)
        vBox = QVBoxLayout()
        vBox.addStretch(0)
        vBox.addWidget(Detail_Button.detail_button)
        vBox.addWidget(Install.install_button)
        vBox.addWidget(Install_Bar.Myprocbar)
        vBox.addStretch(0)
        vBox.setSpacing(0)
        widget.setLayout(vBox)
        table.setCellWidget(row, column, widget)
        if column == 4:
            row += 1
            column = 0
        else:
            column += 1
    pass

def get_app_jsoninfo(self):
    Package_file = open('AppPackage.json', 'r', encoding = 'utf-8')
    Package_info = json.load(Package_file)
    Package_len = len(Package_info)
    return Package_info, Package_len

def app_detail(self, name):
    info = self.sender()
    Package_name = info.property('Package')
    print(name, Package_name)
    pass

def Install_app(self, name, table:QTableWidget):
    button = self.sender()
    row = table.indexAt(button.parent().pos()).row()
    column = table.indexAt(button.parent().pos()).column()
    button.setText("正在安装...")
    button.setEnabled(False)
    button.setVisible(False)
    # 动态跑马灯展示安装
    bar = button.parent().findChild(QProgressBar)

    InstallPackage_name = "firefox"
    # subprocess.Popen('pkexec sudo -S apt-get install %s' % (InstallPackage_name), shell=True, stdout=subprocess.PIPE).communicate()[0]
    try:
        self.install_page_call = Install_UI(bar, button)
        self.install_page_call.process.start('pkexec sudo DEBIAN_FRONTEND=noninteractive apt-get install -y %s' % (InstallPackage_name))
        bar.setVisible(True)
    except Exception as err_msg:
        print("安装出错", err_msg)
    pass
