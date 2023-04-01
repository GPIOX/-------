# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from utils.getbib import get_bib_format

from GUI.mainwindow import Ui_MainWindow
from GUI.config_widget import Ui_Form
from GUI.LedIndicatorWidget import *

from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui

import os
import json
import requests
import threading

class ConfigWidget(QWidget):
    configuration_changes_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(ConfigWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.init_content()

        self.ui.save_config.clicked.connect(self.config_save)
        self.ui.cancel.clicked.connect(lambda: self.close())

    def init_content(self):
        if not os.path.exists(os.path.join(os.path.expanduser("~"), 'getbib')):
            os.mkdir(os.path.join(os.path.expanduser("~"), 'getbib'))

        if not os.path.exists(os.path.join(os.path.expanduser("~"), 'getbib', 'config.json')):
            return # No config file, do nothing
        else:
            with open(os.path.join(os.path.expanduser("~"), 'getbib', 'config.json')) as f:
                config_content = json.load(f)

            self.ui.proxy_input.setText(config_content['proxy_port'])
            self.ui.save_path_input.setText(config_content['save_path'])
            self.ui.browser_select_comboBox.setCurrentText(config_content['browser_select'])
            self.ui.executable_path_input.setText(config_content['executable_path'])


    def config_save(self):
        config_content = {}

        config_content['proxy_port'] = self.ui.proxy_input.text()
        config_content['save_path'] = self.ui.save_path_input.text()
        config_content['browser_select'] = self.ui.browser_select_comboBox.currentText()
        config_content['executable_path'] = self.ui.executable_path_input.text()

        with open(os.path.join(os.path.expanduser("~"), 'getbib', 'config.json'), 'w') as f:
            json.dump(config_content, f)

        self.configuration_changes_signal.emit(config_content)

        self.close()

class MainWindow(QMainWindow):
    bib_form_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config_ui = ConfigWidget()

        self.network_led = LedIndicator(self)
        self.google_scholar_led = LedIndicator(self)

        self.network_led.setDisabled(True)  # Make the led non clickable
        self.google_scholar_led.setDisabled(True)  # Make the led non clickable

        self.ui.network.addWidget(self.network_led)
        self.ui.google_scholar.addWidget(self.google_scholar_led)

        self.ui.action.triggered.connect(self.config_json)
        self.ui.clear_save_bib.triggered.connect(self.clear_bib)
        self.ui.recheck.clicked.connect(self.recheck)
        self.ui.determine.clicked.connect(self.get_bib)
        self.ui.open_save_bib.triggered.connect(self.open_save_bib)

        self.config_ui.configuration_changes_signal.connect(self.config_changes)
        self.bib_form_signal.connect(lambda x: self.ui.bib_form.setText(x))
        
        self.get_configuration_json()
        self.get_network_status()
        self.get_google_scholar_status()

    def get_bib_thread(self):
        paper_name = self.ui.paper_name.toPlainText()
        paper_name = paper_name.replace('\n', ' ')

        former_select = self.ui.comboBox.currentText()

        try:
            bib_text = get_bib_format(self.config_content['executable_path'], paper_name, self.config_content['save_path'], former_select)

            self.bib_form_signal.emit(bib_text)
        except:
            self.bib_form_signal.emit('查找文献失败，请检查网络、IP是否被屏蔽或者文献名是否正确')

    def get_bib(self):
        thread = threading.Thread(target=self.get_bib_thread)
        thread.start()

    def recheck_thread(self):
        self.get_network_status()
        self.get_google_scholar_status()
        self.ui.check_finish.setText("完成")

    def recheck(self):
        self.ui.check_finish.setText("检查中...")

        thread_recheck = threading.Thread(target=self.recheck_thread)
        thread_recheck.start()
        # time.sleep(2)
        # self.ui.check_finish.setText("")


    def get_network_status(self):
        try:
            response = requests.get("http://www.baidu.com")

            if response.status_code == 200:
                self.network_led.setChecked(True)
                self.ui.network_info.setText("Network: OK")
            else:
                self.network_led.setChecked(False)
                self.ui.network_info.setText("Network: Error")
        except:
            self.google_scholar_led.setChecked(False)
            self.ui.google_scholar_info.setText("Connect Google Scholar: Error") 

    def get_google_scholar_status(self):
        try:
            response = requests.get(
                "https://scholar.google.com",
                proxies={
                    'https':
                    f'http://127.0.0.1:{self.config_content["proxy_port"]}'
                })

            if response.status_code == 200:
                self.google_scholar_led.setChecked(True)
                self.ui.google_scholar_info.setText("Connect Google Scholar: OK")
            else:
                self.google_scholar_led.setChecked(False)
                self.ui.google_scholar_info.setText("Connect Google Scholar: Error")
        except:
            self.google_scholar_led.setChecked(False)
            self.ui.google_scholar_info.setText("Connect Google Scholar: Error")      

    def config_changes(self, config_content):
        self.config_content = config_content
        # print(config_content)

    def open_save_bib(self):
        if os.path.exists(self.config_content['save_path']):
            os.system(f'explorer /select, {self.config_content["save_path"]}')

    # 设置self.action的事件
    def config_json(self):
        self.config_ui.show()

    def get_configuration_json(self):
        if not os.path.exists(os.path.join(os.path.expanduser("~"), 'getbib', 'config.json')):
            with open(os.path.join(os.path.expanduser("~"), 'getbib', 'config.json'), 'w') as f:
                self.config_content = None
        else:
            with open(os.path.join(os.path.expanduser("~"), 'getbib', 'config.json'), 'r') as f:
                self.config_content = json.load(f)

    def clear_bib(self):
        if os.path.exists(self.config_content['save_path']):
            os.remove(self.config_content['save_path'])
        else:
            return
            
