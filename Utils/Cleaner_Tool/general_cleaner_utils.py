## import python dependencies
import os
from glob import glob
import subprocess
# import time
import threading
from threading import Timer
from datetime import datetime
from datetime import timedelta
from time import time, sleep, strftime

## import PyQt5 dependencies
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


def content_scanner(target_dir):
    target_dir = relative_dir_parser(target_dir)

    if not os.path.isfile(target_dir):
        output = subprocess.Popen('du -cbs %s' % target_dir, shell = True,
                                  stdout = subprocess.PIPE).communicate()[0]

        file_size = str(output, 'utf-8').split('\t')[-2].split('\n')[-1]
    else:
        file_size = os.path.getsize(target_dir)

    ## sub-processing code use compare function, thus convert this var to int
    return int(file_size)


def relative_dir_parser(input_dir):
    ## os.environ['HOME'] can cause compatibility problems
    if input_dir.startswith('~/'):
        result_dir = os.path.expanduser(input_dir)
    else:
        result_dir = input_dir
    return result_dir


class CleanerToolUtils(QThread):
    ## the progress of scanning
    redundancy_det_progress = QtCore.pyqtSignal(int)

    ## the sum size of the scanned files here
    # redundancy_size = QtCore.pyqtSignal(int)
    ## int can cause overflow error
    redundancy_size = QtCore.pyqtSignal(float)

    def __init__(self):
        super().__init__()

        ## setting up the variables here.
        self.size_threshold = 4194304  # 4MiB
        ## the above setting is mainly because du -chs for a folder will return 4096
        self.dump_size = 0

        ## define the target directory of the huge file scanning
        # self.target_dir = '~/Project/dup_test'
        # self.target_dir = '~/Downloads'
        self.target_dir = '~/'

        ## this following vars are now determined from the user input
        ## these values can be overwritten by the caller function

        self.huge_file_size_threshold = 52428800  ## 50MiB

        self.outd_file_size_threshold = 10485760  ## 10MiB
        self.outd_file_time_threshold = 10

        self.test_run = True

        ## define the flag for determining how old should be categorized as "outdated".

        # pass

    ## the tasks to be initiated when the .start function is called.
    def run(self) -> None:
        ## the measurements to ensure a fresh start.
        self.dump_size = 0
        self.redundancy_det_progress.emit(0)

        ## the block of redundancy
        ## 25% prgs
        self.thumbnails_scan()
        if not self.test_run:
            sleep(3)
        ## TODO(Leon): in later implementations, can use a random.random call
        ## to dynamically change the sleep time here.
        self.cache_dir_scan()
        if not self.test_run:
            sleep(3)
        self.recycle_bin_scan()
        if not self.test_run:
            sleep(1)

        ## the block of privacy
        self.recently_used_record_scan()
        self.bash_history_scan()
        self.browser_file_scan()
        if not self.test_run:
            sleep(2)

        ## the block of huge files
        self.huge_file_scanner()
        if not self.test_run:
            sleep(3)

        ## the block of outdated files
        self.outd_file_scanner()

    def thumbnails_scan(self):
        dir_for_scan = r'~/.cache/thumbnails/'
        try:
            file_size = content_scanner(dir_for_scan)
        except:
            file_size = 0

        ## 单位为Byte 此处为阈值判断
        ## 预留后期打开某些子项的flag placeholder
        if file_size > self.size_threshold:
            self.thumbnails_size = file_size
            self.dump_size += file_size
        else:
            self.thumbnails_size = float(0)

        self.redundancy_det_progress.emit(6)
        self.redundancy_size.emit(self.dump_size)

    def cache_dir_scan(self):
        dir_for_scan = r'~/.cache/'
        file_size = content_scanner(dir_for_scan)

        if file_size > self.size_threshold:
            self.cache_size = file_size
            self.dump_size += file_size
        else:
            self.cache_size = float(0)

        self.redundancy_det_progress.emit(17)
        self.redundancy_size.emit(self.dump_size)

    def recycle_bin_scan(self):
        dir_for_scan = r'~/.local/share/Trash/files'

        file_size = content_scanner(dir_for_scan)

        if file_size > self.size_threshold:
            self.recycle_bin_size = file_size
            self.dump_size += file_size
        else:
            self.recycle_bin_size = float(0)

        self.redundancy_det_progress.emit(25)
        self.redundancy_size.emit(self.dump_size)

    def recently_used_record_scan(self):
        dir_for_scan = r'~/.local/share/recently-used.xbel'
        target_dir = relative_dir_parser(dir_for_scan)
        if os.path.isfile(target_dir):
            self.recently_used_record_flag = True
        else:
            self.recently_used_record_flag = False
        self.redundancy_det_progress.emit(33)
        pass

    def bash_history_scan(self):
        dir_for_scan = r'~/.bash_history'
        target_dir = relative_dir_parser(dir_for_scan)
        if os.path.exists(target_dir):
            self.bash_history_flag = True
        else:
            self.bash_history_flag = False
        self.redundancy_det_progress.emit(41)
        pass

    def browser_file_scan(self):
        ## mozilla firefox
        dir = '~/.mozilla/firefox/'
        dir = relative_dir_parser(dir)
        result = glob(dir + '*.default*')

        det_agg_list = []

        ## examining the sqlite files used to store history information, etc.
        for each_profile in result:
            record_det = glob(each_profile + '/*.sqlite')
            # print(record_det)
            ## aggregate the results under different folders.
            det_agg_list += record_det

        if len(det_agg_list) > 0:
            self.firefox_flag = True
        else:
            self.firefox_flag = False

        ## chrome
        dir = '~/.config/google-chrome/Default/'
        dir = relative_dir_parser(dir)
        result = glob(dir + '*')

        if len(result) > 0:
            self.chrome_flag = True
        else:
            self.chrome_flag = False

        ## chromium
        dir = '~/.config/chromium/Default/'
        dir = relative_dir_parser(dir)
        result = glob(dir + '*')

        if len(result) > 0:
            self.chromium_flag = True
        else:
            self.chromium_flag = False

        if ((self.firefox_flag == True) or (self.chrome_flag == True) or (self.chromium_flag == True)):
            self.browser_flag = True
        else:
            self.browser_flag = False

        self.redundancy_det_progress.emit(50)
        pass

    # def apt_pac_scan(self):
    #     flag1 = os.path.exists('/var/cache/apt/archives')
    #     self.redundancy_det_progress.emit(80)
    #     flag2 = os.path.exists('/var/lib/apt/lists/partial')
    #     self.redundancy_det_progress.emit(85)
    #     flag3 = os.path.exists('/var/cache/apt/pkgcache.bin')
    #     self.redundancy_det_progress.emit(90)
    #     flag4 = os.path.exists('/var/cache/apt/srcpkgcache.bin')
    #     self.redundancy_det_progress.emit(95)
    #
    #     ## /var/tmp/
    #     flag5 = True if len(glob('/var/tmp/*')) > 0 else False
    #
    #     ## scan for its content
    #     dir_for_scan = r'/var/cache/apt/'
    #     file_size = content_scanner(dir_for_scan)
    #     dump_size = file_size
    #
    #     dir_for_scan = r'/var/lib/apt/'
    #     file_size = content_scanner(dir_for_scan)
    #     dump_size += file_size
    #
    #     self.dump_size += dump_size
    #
    #     self.redundancy_det_progress.emit(100)
    #     self.redundancy_size.emit(self.dump_size)
    #
    #     apt_flag = flag1 or flag2 or flag3 or flag4 or flag5
    #
    #     if apt_flag:
    #         print('pos')
    #     else:
    #         print('neg')

    def thumbnails_clear(self):
        # os.system('sh ./sh/thumbnails_clean.sh')
        os.system('rm -rf ~/.cache/thumbnails/')

    def bash_history_clear(self):
        os.system('cat /dev/null > ~/.bash_history && history -c')
        pass

    def recently_used_clear(self):
        os.system('rm -rf ~/.local/share/recently-used.xbel')

    def cache_dir_clear(self):
        os.system('rm -rf ~/.cache/')

    def recycle_bin_clear(self):
        os.system('rm -rf ~/.local/share/Trash/files')

    def apt_pac_clear(self):
        ## here called some sudo commands
        os.system('sudo apt-get -y clean')
        os.system('sudo apt-get -y autoclean')
        os.system('sudo rm -r /var/tmp/')

    def browser_related_clean(self):
        os.system('rm -rf ~/.mozilla/firefox/*.default*/cookies.*')
        os.system('rm -rf ~/.mozilla/firefox/*.default*/sessionstore.*')
        os.system('rm -rf ~/.mozilla/firefox/*.default*/sessionstore-backups')
        os.system('rm -rf ~/.mozilla/firefox/*.default*/minidump')
        os.system('rm -rf ~/.mozilla/firefox/*.default*/crashes')
        os.system('rm -rf ~/.mozilla/firefox/*.default*/*.sqlite')

        os.system('rm -rf ~/.config/google-chrome/Default/Autofill*')
        os.system('rm -rf ~/.config/google-chrome/Default/blob*')
        os.system('rm -rf ~/.config/google-chrome/Default/Cookies*')
        os.system('rm -rf ~/.config/google-chrome/Default/Favi*')
        os.system('rm -rf ~/.config/google-chrome/Default/GPUCache*')
        os.system('rm -rf ~/.config/google-chrome/Default/Hist*')
        os.system('rm -rf ~/.config/google-chrome/Default/Login*')
        os.system('rm -rf ~/.config/google-chrome/Default/LOG*')
        os.system('rm -rf ~/.config/google-chrome/Default/Safe*')
        os.system('rm -rf ~/.config/google-chrome/Default/Session*')
        os.system('rm -rf ~/.config/google-chrome/Default/Site*')
        os.system('rm -rf ~/.config/google-chrome/Default/Top*')
        os.system('rm -rf ~/.config/google-chrome/Default/Visited*')

        os.system('rm -rf ~/.config/chromium/Default/Autofill*')
        os.system('rm -rf ~/.config/chromium/Default/blob*')
        os.system('rm -rf ~/.config/chromium/Default/Cookies*')
        os.system('rm -rf ~/.config/chromium/Default/Favi*')
        os.system('rm -rf ~/.config/chromium/Default/GPUCache*')
        os.system('rm -rf ~/.config/chromium/Default/Hist*')
        os.system('rm -rf ~/.config/chromium/Default/Login*')
        os.system('rm -rf ~/.config/chromium/Default/LOG*')
        os.system('rm -rf ~/.config/chromium/Default/Safe*')
        os.system('rm -rf ~/.config/chromium/Default/Session*')
        os.system('rm -rf ~/.config/chromium/Default/Site*')
        os.system('rm -rf ~/.config/chromium/Default/Top*')
        os.system('rm -rf ~/.config/chromium/Default/Visited*')
        pass

    def huge_file_scanner(self):
        ## update the progress bar
        self.redundancy_det_progress.emit(52)

        self.target_dir = relative_dir_parser(self.target_dir)
        print(self.target_dir)

        ## huge file stores the information of the detected huge files under the target dir
        huge_file = []

        ## huge file size records the sum size of detected huge files
        huge_file_size = 0

        # a1_time = time()

        ## if we simply use the os.walk function, there can be some performance issues here
        sub_folders_list = [name for name in os.listdir(self.target_dir)
                            if os.path.isdir(os.path.join(self.target_dir, name))]
        for sub_folder_iter in sub_folders_list:
            if (sub_folder_iter.startswith('.')) or (sub_folder_iter.startswith('Pub')):
                continue
            for parent, dirnames, filenames in os.walk(os.path.join(self.target_dir, sub_folder_iter)):

                for filename in filenames:
                    full_path = os.path.join(parent, filename)
                    print(full_path)
                    # huge_file.append(full_path)
                    top_parent_folder = full_path.split('/')[3]
                    if top_parent_folder.startswith('.'):
                        continue
                    bottom_parent_folder = full_path.split('/')[-2]
                    if bottom_parent_folder.startswith('.'):
                        continue

                    try:
                        size = os.path.getsize(full_path)
                        # self.size = size
                    except FileNotFoundError:
                        print('this file cannot be accessed. ', full_path)
                        continue

                    last_access = str(datetime.fromtimestamp(os.path.getatime(full_path))).split('.')[0]
                    last_modify = str(datetime.fromtimestamp(os.path.getmtime(full_path))).split('.')[0]

                    if size >= self.huge_file_size_threshold:
                        # print('the full name of the file is %s' % full_path)
                        huge_file.append([full_path, size, last_access, last_modify])
                        huge_file_size += size
                        self.dump_size += size
                        # if self.dump_size < 0:
                        #     print('full_path')
                        #     raise ValueError
                        # print('debug line', self.dump_size, size)
                        self.redundancy_size.emit(self.dump_size)
                        # sleep(1)

        # a2_time = time()
        # print('elapsed time', a2_time - a1_time)
        self.huge_file_size = huge_file_size
        # self.dump_size += huge_file_size

        self.redundancy_det_progress.emit(75)
        # self.redundancy_size.emit(self.dump_size)

        self.huge_file = sorted(huge_file, key = lambda d: d[1], reverse = True)

        pass

    def huge_file_selective_clear(self):
        pass

    def outd_file_scanner(self):
        self.redundancy_det_progress.emit(76)

        self.target_dir = relative_dir_parser(self.target_dir)

        ## outd file stores the information of the detected outd files under the target dir
        outd_file = []

        ## outd file size records the sum size of detected outd files
        outd_file_size = 0
        print('outd start')

        ## if we simply use the os.walk function, there can be some performance issues here
        sub_folders_list = [name for name in os.listdir(self.target_dir)
                            if os.path.isdir(os.path.join(self.target_dir, name))]
        for sub_folder_iter in sub_folders_list:
            if (sub_folder_iter.startswith('.')) or (sub_folder_iter.startswith('Pub')):
                continue
            for parent, dirnames, filenames in os.walk(os.path.join(self.target_dir, sub_folder_iter)):

                for filename in filenames:
                    full_path = os.path.join(parent, filename)
                    # print('the full name of the file is %s' % full_path)
                    try:
                        size = os.path.getsize(full_path)
                    except FileNotFoundError:
                        # print('this file cannot be accessed. ')
                        continue
                    last_access = str(datetime.fromtimestamp(os.path.getatime(full_path))).split('.')[0]
                    last_modify = str(datetime.fromtimestamp(os.path.getmtime(full_path))).split('.')[0]

                    if size >= self.outd_file_size_threshold:
                        current_time = datetime.fromtimestamp(time())
                        last_access_time = datetime.fromtimestamp(os.path.getatime(full_path))
                        day_lapse = (current_time - last_access_time).days
                        # print(day_lapse)
                        if day_lapse >= self.outd_file_time_threshold:
                            outd_file.append([full_path, size, last_access, last_modify])
                            outd_file_size += size
                            self.dump_size += size
                            self.redundancy_size.emit(self.dump_size)
                            # print(full_path)

        self.outd_file_size = outd_file_size
        # self.dump_size += outd_file_size
        print('outd end')

        self.redundancy_det_progress.emit(100)
        # self.redundancy_size.emit(self.dump_size)

        self.outd_file = sorted(outd_file, key = lambda d: d[1], reverse = True)

        # print('the length of the outdated file list ', len(self.outd_file))
        pass

    def outd_file_selective_clear(self):
        pass

    def remove_designated_file(self, target, dry_run = False):
        if not dry_run:
            output = subprocess.Popen('rm -rf %s' % target, shell = True,
                                      stdout = subprocess.PIPE).communicate()[0]
        else:
            print('dry run for cleaning %s' % target)
        pass
