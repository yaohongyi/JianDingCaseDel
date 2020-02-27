#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import sys
import os
import base64
from PyQt5 import QtWidgets, QtGui, QtCore
from icon import icon

with open('temp.ico', 'wb') as file:
    file.write(base64.b64decode(icon.img))


class Client(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(350, 240)
        self.setWindowTitle('鉴定系统案件清理器_20200227')
        self.setWindowIcon(QtGui.QIcon('temp.ico'))
        os.remove('temp.ico')
        # 创建窗口元素
        ip_label = QtWidgets.QLabel('* IP地址：')
        ip_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        ip_input = QtWidgets.QLineEdit()
        port_label = QtWidgets.QLabel('* 端口：')
        port_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        port_input = QtWidgets.QLineEdit()
        user_label = QtWidgets.QLabel('* 用户名：')
        user_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        user_input = QtWidgets.QLineEdit()
        password_label = QtWidgets.QLabel('* 密码：')
        password_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        password_input = QtWidgets.QLineEdit()
        # 案件匹配规则
        rule_label = QtWidgets.QLabel('* 搜索规则：')
        rule_label.setToolTip('案件名称搜索规则')
        rule_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        full_rb = QtWidgets.QRadioButton('全文搜索')
        full_rb.setToolTip('搜索包含关键字XXX的案件名称')
        start_rb = QtWidgets.QRadioButton('特定开头')
        start_rb.setToolTip('搜索以关键字XXX开头的案件名称')
        end_rb = QtWidgets.QRadioButton('特定结尾')
        end_rb.setToolTip('搜索以关键字XXX结尾的案件名称')
        rule_bg = QtWidgets.QButtonGroup()
        rule_bg.addButton(full_rb, 1)
        rule_bg.addButton(start_rb, 1)
        rule_bg.addButton(end_rb, 1)
        keyword_label = QtWidgets.QLabel('关键字：')
        keyword_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)
        keyword_input = QtWidgets.QLineEdit()
        keyword_input.setPlaceholderText('请输入案件名称关键字')
        # 案件删除范围
        scope_label = QtWidgets.QLabel('* 执行范围：')
        all_rb = QtWidgets.QRadioButton('全部')
        case_list_rb = QtWidgets.QRadioButton('案件列表')
        case_recycle_rb = QtWidgets.QRadioButton('案件回收站')
        scope_bg = QtWidgets.QButtonGroup()
        scope_bg.addButton(all_rb, 2)
        scope_bg.addButton(case_list_rb, 2)
        scope_bg.addButton(case_recycle_rb, 2)
        # 【执行】按钮
        execute_button = QtWidgets.QPushButton('开始执行(F10)')
        # 页面元素布局
        client_grid = QtWidgets.QGridLayout(self)
        client_grid.addWidget(ip_label, 0, 1, 1, 1)
        client_grid.addWidget(ip_input, 0, 2, 1, 1)
        client_grid.addWidget(port_label, 0, 3, 1, 1)
        client_grid.addWidget(port_input, 0, 4, 1, 1)
        client_grid.addWidget(user_label, 1, 1, 1, 1)
        client_grid.addWidget(user_input, 1, 2, 1, 1)
        client_grid.addWidget(password_label, 1, 3, 1, 1)
        client_grid.addWidget(password_input, 1, 4, 1, 1)
        client_grid.addWidget(rule_label, 2, 1, 1, 1)
        client_grid.addWidget(full_rb, 2, 2, 1, 1)
        client_grid.addWidget(start_rb, 2, 3, 1, 1)
        client_grid.addWidget(end_rb, 2, 4, 1, 1)
        client_grid.addWidget(keyword_label, 3, 1, 1, 1)
        client_grid.addWidget(keyword_input, 3, 2, 1, 3)
        client_grid.addWidget(scope_label, 4, 1, 1, 1)
        client_grid.addWidget(all_rb, 4, 2, 1, 1)
        client_grid.addWidget(case_list_rb, 4, 3, 1, 1)
        client_grid.addWidget(case_recycle_rb, 4, 4, 1, 1)
        client_grid.addWidget(execute_button, 5, 1, 1, 4)



def main():
    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
