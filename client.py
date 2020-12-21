#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import sys
import os
import base64
from PyQt5 import QtWidgets, QtGui, QtCore
from icon.icon import img
from api_list import RemoveCase, SearchCase
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']


# 生成LOGO
with open('temp.ico', 'wb') as file:
    file.write(base64.b64decode(img))


class Client(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(500, 500)
        self.setWindowTitle('鉴定系统案件清理器_20201221')
        self.setWindowIcon(QtGui.QIcon('temp.ico'))
        os.remove('temp.ico')
        self.client_grid = QtWidgets.QGridLayout(self)
        '''创建窗口元素'''
        self.ip_label = QtWidgets.QLabel('* IP地址：')
        self.ip_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.ip_input = QtWidgets.QLineEdit()
        self.port_label = QtWidgets.QLabel('* 端口：')
        self.port_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.port_input = QtWidgets.QLineEdit()
        self.user_label = QtWidgets.QLabel('* 用户名：')
        self.user_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.user_input = QtWidgets.QLineEdit()
        self.password_label = QtWidgets.QLabel('* 密码：')
        self.password_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.password_input = QtWidgets.QLineEdit()
        self.keyword_label = QtWidgets.QLabel('关键字：')
        self.keyword_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.keyword_input = QtWidgets.QLineEdit()
        self.keyword_input.setPlaceholderText('请输入案件名称关键字，为空则匹配所有案件')
        # 【查询案件】按钮
        self.search_button = QtWidgets.QPushButton('查询案件(F9)')
        self.search_button.setShortcut('F9')
        self.search_button.clicked.connect(self.search)
        # 【执行删除】按钮
        self.execute_button = QtWidgets.QPushButton('执行删除(F10)')
        self.execute_button.setToolTip('先查询出案件再执行删除！')
        self.execute_button.setShortcut('F10')
        # self.execute_button.setEnabled(False)
        self.execute_button.clicked.connect(self.execute)
        # 【清理日志】按钮
        self.clear_button = QtWidgets.QPushButton('清理日志(Ctrl+L)')
        self.clear_button.setShortcut('Ctrl+L')
        self.clear_button.clicked.connect(self.clear_log)
        # 日志打印显示
        self.log_browser = QtWidgets.QTextBrowser()
        # 【填写信息】组布局
        self.top_gb = QtWidgets.QGroupBox('【填写信息】')
        self.client_grid.addWidget(self.top_gb, 0, 1, 1, 1)
        self.top_grid = QtWidgets.QGridLayout(self.top_gb)
        self.top_grid.addWidget(self.ip_label, 0, 1, 1, 1)
        self.top_grid.addWidget(self.ip_input, 0, 2, 1, 2)
        self.top_grid.addWidget(self.port_label, 0, 4, 1, 1)
        self.top_grid.addWidget(self.port_input, 0, 5, 1, 2)
        self.top_grid.addWidget(self.user_label, 1, 1, 1, 1)
        self.top_grid.addWidget(self.user_input, 1, 2, 1, 2)
        self.top_grid.addWidget(self.password_label, 1, 4, 1, 1)
        self.top_grid.addWidget(self.password_input, 1, 5, 1, 2)
        self.top_grid.addWidget(self.keyword_label, 2, 1, 1, 1)
        self.top_grid.addWidget(self.keyword_input, 2, 2, 1, 5)
        self.top_grid.addWidget(self.search_button, 3, 1, 1, 3)
        self.top_grid.addWidget(self.execute_button, 3, 4, 1, 3)
        self.top_grid.addWidget(self.clear_button, 4, 1, 1, 6)
        # 【日志打印】组布局
        self.bottom_gb = QtWidgets.QGroupBox('【信息打印】')
        self.client_grid.addWidget(self.bottom_gb, 1, 1, 2, 1)
        self.bottom_grid = QtWidgets.QGridLayout(self.bottom_gb)
        self.bottom_grid.addWidget(self.log_browser)
        # 设置默认值
        self.set_default_value()

    def set_default_value(self):
        """"""
        self.ip_input.setText('192.168.0.75')
        self.port_input.setText('20000')
        self.user_input.setText('yaocheng')
        self.password_input.setText('123456')

    # 为空检验
    def null_check(self, value):
        ip = value.get('ip')
        port = value.get('port')
        username = value.get('username')
        password = value.get('password')
        null_field_list = []
        ip_zh = 'IP地址'
        port_zh = '端口'
        username_zh = '用户名'
        password_zh = '密码'
        if ip == '':
            null_field_list.append(ip_zh)
        if port == '':
            null_field_list.append(port_zh)
        if username == '':
            null_field_list.append(username_zh)
        if password == '':
            null_field_list.append(password_zh)
        if null_field_list:
            prompt = '丨'.join(null_field_list)
            self.print_log(f'请输入：{prompt}！')
        return null_field_list

    def get_value(self):
        ip = self.ip_input.text()
        port = self.port_input.text()
        username = self.user_input.text()
        password = self.password_input.text()
        keyword = self.keyword_input.text()
        value = {
            'ip': ip,
            'port': port,
            'username': username,
            'password': password,
            'keyword': keyword
        }
        return value

    def search(self):
        self.clear_log()
        value = self.get_value()
        null_field_check_result = self.null_check(value)
        if null_field_check_result:
            self.set_execute_button()
        else:
            self.search_case = SearchCase(**value)
            self.search_case.search_info.connect(self.print_log)
            self.search_case.start()
            self.execute_button.setEnabled(True)

    def execute(self):
        value = self.get_value()
        null_field_check_result = self.null_check(value)
        if null_field_check_result:
            ...
        else:
            self.remove_case = RemoveCase(**value)
            self.remove_case.remove_info.connect(self.print_log)
            self.remove_case.start()
            self.set_execute_button()

    def set_execute_button(self):
        """设置【执行删除】按钮不可点击"""
        self.execute_button.setEnabled(False)

    def print_log(self, info):
        self.log_browser.append(info)

    def clear_log(self):
        self.log_browser.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
