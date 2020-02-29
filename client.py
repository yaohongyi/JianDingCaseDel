#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import sys
import os
import base64
from PyQt5 import QtWidgets, QtGui, QtCore
from icon import icon
from public_methon import dict_format


# 生成icon
with open('temp.ico', 'wb') as file:
    file.write(base64.b64decode(icon.img))


class Client(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(500, 600)
        self.setWindowTitle('鉴定系统案件清理器_20200228')
        self.setWindowIcon(QtGui.QIcon('temp.ico'))
        os.remove('temp.ico')
        client_grid = QtWidgets.QGridLayout(self)
        '''创建窗口元素'''
        ip_label = QtWidgets.QLabel('* IP地址：')
        ip_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        self.ip_input = QtWidgets.QLineEdit()
        self.ip_input.setText('192.168.0.75')
        port_label = QtWidgets.QLabel('* 端口：')
        self.port_input = QtWidgets.QLineEdit()
        self.port_input.setText('20000')
        user_label = QtWidgets.QLabel('* 用户名：')
        user_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        self.user_input = QtWidgets.QLineEdit()
        password_label = QtWidgets.QLabel('* 密码：')
        self.password_input = QtWidgets.QLineEdit()
        # 案件匹配规则
        rule_label = QtWidgets.QLabel('* 搜索规则：')
        rule_label.setToolTip('案件名称搜索规则')
        rule_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        self.full_rb = QtWidgets.QRadioButton('全文搜索')
        self.full_rb.setChecked(True)
        self.full_rb.setToolTip('搜索包含关键字XXX的案件名称')
        self.start_rb = QtWidgets.QRadioButton('特定开头')
        self.start_rb.setToolTip('搜索以关键字XXX开头的案件名称')
        self.end_rb = QtWidgets.QRadioButton('特定结尾')
        self.end_rb.setToolTip('搜索以关键字XXX结尾的案件名称')
        rule_bg = QtWidgets.QButtonGroup(self)
        rule_bg.addButton(self.full_rb)
        rule_bg.addButton(self.start_rb)
        rule_bg.addButton(self.end_rb)
        keyword_label = QtWidgets.QLabel('关键字：')
        keyword_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        self.keyword_input = QtWidgets.QLineEdit()
        self.keyword_input.setPlaceholderText('请输入案件名称关键字')
        # 案件删除范围
        scope_label = QtWidgets.QLabel('* 执行范围：')
        self.all_rb = QtWidgets.QRadioButton('全部清理')
        self.all_rb.setChecked(True)
        self.case_list_rb = QtWidgets.QRadioButton('清理案件列表')
        self.case_recycle_rb = QtWidgets.QRadioButton('清理案件回收站')
        scope_bg = QtWidgets.QButtonGroup(self)
        scope_bg.addButton(self.all_rb)
        scope_bg.addButton(self.case_list_rb)
        scope_bg.addButton(self.case_recycle_rb)
        # 【开始执行】按钮
        execute_button = QtWidgets.QPushButton('开始执行(F10)')
        execute_button.setShortcut('F10')
        execute_button.clicked.connect(self.execute)
        # 【清理日志】按钮
        clear_button = QtWidgets.QPushButton('清理日志(Ctrl+L)')
        clear_button.setShortcut('Ctrl+L')
        clear_button.clicked.connect(self.clear_log)
        # 日志打印显示
        self.log_browser = QtWidgets.QTextBrowser()
        # 【填写信息】组布局
        top_gb = QtWidgets.QGroupBox('【填写信息】')
        client_grid.addWidget(top_gb, 0, 1, 1, 1)
        top_grid = QtWidgets.QGridLayout(top_gb)
        top_grid.addWidget(ip_label, 0, 1, 1, 1)
        top_grid.addWidget(self.ip_input, 0, 2, 1, 2)
        top_grid.addWidget(port_label, 0, 4, 1, 1)
        top_grid.addWidget(self.port_input, 0, 5, 1, 2)
        top_grid.addWidget(user_label, 1, 1, 1, 1)
        top_grid.addWidget(self.user_input, 1, 2, 1, 2)
        top_grid.addWidget(password_label, 1, 4, 1, 1)
        top_grid.addWidget(self.password_input, 1, 5, 1, 2)
        top_grid.addWidget(rule_label, 2, 1, 1, 1)
        top_grid.addWidget(self.full_rb, 2, 2, 1, 1)
        top_grid.addWidget(self.start_rb, 2, 3, 1, 1)
        top_grid.addWidget(self.end_rb, 2, 4, 1, 2)
        top_grid.addWidget(keyword_label, 3, 1, 1, 1)
        top_grid.addWidget(self.keyword_input, 3, 2, 1, 5)
        top_grid.addWidget(scope_label, 4, 1, 1, 1)
        top_grid.addWidget(self.all_rb, 4, 2, 1, 1)
        top_grid.addWidget(self.case_list_rb, 4, 3, 1, 1)
        top_grid.addWidget(self.case_recycle_rb, 4, 4, 1, 2)
        top_grid.addWidget(execute_button, 5, 1, 1, 3)
        top_grid.addWidget(clear_button, 5, 4, 1, 3)
        # 【日志打印】组布局
        bottom_gb = QtWidgets.QGroupBox('【日志打印】')
        client_grid.addWidget(bottom_gb, 1, 1, 2, 1)
        bottom_grid = QtWidgets.QGridLayout(bottom_gb)
        bottom_grid.addWidget(self.log_browser)

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
        self.print_log(dict_format(value))
        return value

    def execute(self):
        value = self.get_value()

    def print_log(self, text):
        self.log_browser.append(text)

    def clear_log(self):
        self.log_browser.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
