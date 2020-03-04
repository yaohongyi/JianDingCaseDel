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


# 生成运行时图标
with open('temp.ico', 'wb') as file:
    file.write(base64.b64decode(img))


class Client(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(500, 500)
        self.setWindowTitle('鉴定系统案件清理器_20200304')
        self.setWindowIcon(QtGui.QIcon('temp.ico'))
        os.remove('temp.ico')
        self.client_grid = QtWidgets.QGridLayout(self)
        '''创建窗口元素'''
        self.ip_label = QtWidgets.QLabel('* IP地址：')
        self.ip_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.ip_input = QtWidgets.QLineEdit()
        self.ip_input.setText('192.168.0.75')
        self.port_label = QtWidgets.QLabel('* 端口：')
        self.port_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.port_input = QtWidgets.QLineEdit()
        self.port_input.setText('20000')
        self.user_label = QtWidgets.QLabel('* 用户名：')
        self.user_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.user_input = QtWidgets.QLineEdit()
        self.user_input.setText('lily')
        self.password_label = QtWidgets.QLabel('* 密码：')
        self.password_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setText('123456')
        # 案件匹配规则
        self.rule_label = QtWidgets.QLabel('* 搜索规则：')
        self.rule_label.setToolTip('案件名称搜索规则')
        self.rule_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.full_rb = QtWidgets.QRadioButton('全文搜索')
        self.full_rb.setChecked(True)
        self.full_rb.setToolTip('搜索包含关键字XXX的案件名称')
        self.full_rb.clicked.connect(self.keyword_interaction)
        self.start_rb = QtWidgets.QRadioButton('特定开头')
        self.start_rb.setToolTip('搜索以关键字XXX开头的案件名称')
        self.start_rb.clicked.connect(self.keyword_interaction)
        self.end_rb = QtWidgets.QRadioButton('特定结尾')
        self.end_rb.setToolTip('搜索以关键字XXX结尾的案件名称')
        self.end_rb.clicked.connect(self.keyword_interaction)
        self.rule_bg = QtWidgets.QButtonGroup(self)
        self.rule_bg.addButton(self.full_rb)
        self.rule_bg.addButton(self.start_rb)
        self.rule_bg.addButton(self.end_rb)
        self.keyword_label = QtWidgets.QLabel('关键字：')
        self.keyword_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.keyword_input = QtWidgets.QLineEdit()
        self.keyword_input.setPlaceholderText('请输入案件名称关键字，为空则匹配所有案件')
        # 案件删除范围
        self.scope_label = QtWidgets.QLabel('* 执行范围：')
        self.all_rb = QtWidgets.QRadioButton('全部清理')
        self.all_rb.setChecked(True)
        self.case_list_rb = QtWidgets.QRadioButton('清理案件列表')
        self.case_recycle_rb = QtWidgets.QRadioButton('清理案件回收站')
        self.scope_bg = QtWidgets.QButtonGroup(self)
        self.scope_bg.addButton(self.all_rb)
        self.scope_bg.addButton(self.case_list_rb)
        self.scope_bg.addButton(self.case_recycle_rb)
        # 【查询案件】按钮
        self.search_button = QtWidgets.QPushButton('查询案件(F9)')
        self.search_button.setShortcut('F9')
        self.search_button.clicked.connect(self.search)
        # 【开始执行】按钮
        self.execute_button = QtWidgets.QPushButton('执行删除(F10)')
        self.execute_button.setToolTip('先查询出案件再执行删除！')
        self.execute_button.setShortcut('F10')
        self.execute_button.setEnabled(False)
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
        self.top_grid.addWidget(self.scope_label, 2, 1, 1, 1)
        self.top_grid.addWidget(self.all_rb, 2, 2, 1, 1)
        self.top_grid.addWidget(self.case_list_rb, 2, 3, 1, 1)
        self.top_grid.addWidget(self.case_recycle_rb, 2, 4, 1, 2)
        self.top_grid.addWidget(self.rule_label, 3, 1, 1, 1)
        self.top_grid.addWidget(self.full_rb, 3, 2, 1, 1)
        self.top_grid.addWidget(self.start_rb, 3, 3, 1, 1)
        self.top_grid.addWidget(self.end_rb, 3, 4, 1, 2)
        self.top_grid.addWidget(self.keyword_label, 4, 1, 1, 1)
        self.top_grid.addWidget(self.keyword_input, 4, 2, 1, 5)
        self.top_grid.addWidget(self.search_button, 5, 1, 1, 2)
        self.top_grid.addWidget(self.execute_button, 5, 3, 1, 2)
        self.top_grid.addWidget(self.clear_button, 5, 5, 1, 2)
        # 【日志打印】组布局
        self.bottom_gb = QtWidgets.QGroupBox('【信息打印】')
        self.client_grid.addWidget(self.bottom_gb, 1, 1, 2, 1)
        self.bottom_grid = QtWidgets.QGridLayout(self.bottom_gb)
        self.bottom_grid.addWidget(self.log_browser)
        # 【开始执行】按钮不可点击
        self.ip_input.textChanged.connect(self.set_execute_button)
        self.port_input.textChanged.connect(self.set_execute_button)
        self.user_input.textChanged.connect(self.set_execute_button)
        self.password_input.textChanged.connect(self.set_execute_button)
        self.rule_bg.buttonClicked.connect(self.set_execute_button)
        self.keyword_input.textChanged.connect(self.set_execute_button)
        self.scope_bg.buttonClicked.connect(self.set_execute_button)

    def keyword_interaction(self):
        if self.full_rb.isChecked():
            self.keyword_label.setText('关键字：')
            self.keyword_input.setPlaceholderText('请输入案件名称关键字，为空则匹配所有案件')
        else:
            self.keyword_label.setText('* 关键字：')
            self.keyword_input.setPlaceholderText('请输入关键字，不允许为空')
        self.keyword_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)

    # 为空检验
    def null_check(self, value):
        ip = value.get('ip')
        port = value.get('port')
        username = value.get('username')
        password = value.get('password')
        keyword = value.get('keyword')
        null_field_list = []
        ip_zh = 'IP地址'
        port_zh = '端口'
        username_zh = '用户名'
        password_zh = '密码'
        keyword_zh = '关键字'
        if ip == '':
            null_field_list.append(ip_zh)
        if port == '':
            null_field_list.append(port_zh)
        if username == '':
            null_field_list.append(username_zh)
        if password == '':
            null_field_list.append(password_zh)
        if self.start_rb.isChecked() and keyword == '':
            null_field_list.append(keyword_zh)
        if self.end_rb.isChecked() and keyword == '':
            null_field_list.append(keyword_zh)
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
        # 获取匹配规则单选按钮值
        if self.full_rb.isChecked():
            search_rule = 0
        elif self.start_rb.isChecked():
            search_rule = 1
        else:
            search_rule = 2
        # 获取执行范围单选按钮值
        if self.all_rb.isChecked():
            execute_scope = 0
        elif self.case_list_rb.isChecked():
            execute_scope = 1
        else:
            execute_scope = 2
        value = {
            'ip': ip,
            'port': port,
            'username': username,
            'password': password,
            'keyword': keyword,
            'search_rule': search_rule,
            'execute_scope': execute_scope
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
