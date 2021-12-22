from functools import partial
import threading

from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtGui import QStandardItemModel

from .Netconnect_Manager import Nettable_Call
from .Process_Manager import Processtable_Call


def Porc_NetConnect_Call(self):
    self.proc_manager_terminate = False

    ## specify the default subpage
    self.ProcessManager_tab.setCurrentIndex(0)

    ## to refresh the information here.
    self.cons_repo.process_check()
    self.cons_repo.network_comm_check()

    # 调用process表和nettable表
    Processtable_Call(self)
    Nettable_Call(self)

    # 防止一开始未调用
    index = self.process_mng_table_view.model().index(0, 1)
    check_id = self.process_mng_table_view.model().data(index)
    if check_id == None:
        Processtable_Call(self)
        Nettable_Call(self)

    # 一个临时model()
    self.temp_model = QStandardItemModel()

    # 离开进程界面
    leave_threading(self)
    pass


def leave_threading(self):
    par_on_going_leave_page = partial(on_going_leave_page, self)
    self.stackedWidget.currentChanged.connect(par_on_going_leave_page)
    # self.page_process_manager.currentChanged.connect(par_on_going_leave_page)


def on_going_leave_page(self):
    try:
        self.process_mng_table_view.setModel(self.temp_model)
        self.net_table_view.setModel(self.temp_model)

        ## set the terminate flag to True
        self.proc_manager_terminate = True

        ## delete unnecessary elements here
        purge_elements(self)

    except Exception as err_msg:
        print("error msg:", err_msg)

    pass


def purge_elements(self):
    # try:
    #     del self.proc_data_model, self.sortermodel, self.process_mng_table_view
    #     del self.process_mng_table_view, self.Detail_window, self.proc_data_model
    #     del self.net_table_view, self.net_table_view, self.Net_data_model
    # except Exception:
    #     pass
    print('test', hasattr(self, 'proc_table_refresh_thread'))
    pass
