#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import inspect
from PyQt5 import QtCore
from public_methon import request_post


class IdentityAPI(QtCore.QThread):
    text = QtCore.pyqtSignal(str)

    def __init__(self, **kwargs):
        super().__init__()
        ip = kwargs.get('ip')
        port = kwargs.get('port')
        self.url_prefix = f"http://{ip}:{port}"
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.keyword = kwargs.get('keyword')
        self.search_rule = kwargs.get('search_rule')
        self.execute_scope = kwargs.get('execute_scope')

    def login(self):
        url = f"{self.url_prefix}/call?id=experts.login&v="
        data = {
            'nickname': self.username,
            'passwd': self.password
        }
        method_name = inspect.stack()[0][3]
        res = request_post(method_name, url, data)
        session_id = None
        if res:
            has_error = res.get('hasError')
            if has_error is False:
                session_id = res.get('data').get('sessionId')
            elif has_error is True:
                session_id = 0  # 账号密码错误
        else:
            session_id = 1  # 服务器无法连接
        return session_id

    def list_case(self, session_id, offset=0, limit=99999, remove_type=0, case_type=1):
        """
        获取案件列表
        :param session_id: 用户登录后获取的session_id
        :param offset: 位移量
        :param limit: 获取量
        :param remove_type: 案件列表为0，案件回收站为10
        :param case_type: 案件列表和案件回收站都填1
        :return: 接口响应
        """
        url = f"{self.url_prefix}/call?id=experts.listCriminalCase&v="
        data = {
            "sessionid": session_id,
            "offset": offset,
            "limit": limit,
            "removeType": remove_type,
            "key_word": [self.keyword],
            "type": case_type
        }
        method_name = inspect.stack()[0][3]
        res = request_post(method_name, url, data)
        return res

    def list_case_list_data(self, session_id):
        """获取案件列表的案件"""
        res = self.list_case(session_id)
        return res

    def list_case_recycle_data(self, session_id, remove_type=10):
        """获取案件回收站的案件"""
        res = self.list_case(session_id, remove_type=remove_type)
        return res

    def remove_case(self, session_id, case_id, remove_type):
        """
        删除案件
        :param session_id: 用户登录后获取的session_id
        :param case_id: 案件id
        :param remove_type: 删除类型，案件列表删除10，回收站删除20
        :return: 接口响应
        """
        url = f'{self.url_prefix}/call?id=experts.removeCriminalCase&v=&timeout=120000'
        data = {
            'criminalCaseId': case_id,
            'removeType': remove_type,
            'sessionId': session_id
        }
        method_name = inspect.stack()[0][3]
        res = request_post(method_name, url, data)
        return res

    def remove_case_list_data(self, session_id, case_id, remove_type=10):
        """从案件列表删除数据"""
        self.remove_case(session_id, case_id, remove_type)

    def remove_case_recycle_data(self, session_id, case_id, remove_type=20):
        """从案件回收站删除数据"""
        self.remove_case(session_id, case_id, remove_type)

    def search_case_list(self, session_id):
        case_list_res = self.list_case_list_data(session_id)
        # 获取案件列表接口中的caseList
        has_error = case_list_res.get('hasError')
        if has_error is False:
            case_list = case_list_res.get('data').get('caseList')
        else:
            case_list = []
        # 将目标案件id添加到列表中
        case_id_list = []
        if case_list is False:
            return case_id_list
        else:
            for case in case_list:
                case_name = case.get('caseName')
                # 全文搜索
                if self.search_rule == 0:
                    match_result = case_name.find(self.keyword)
                    if match_result != -1:
                        case_id = case.get('caseName')
                        case_id_list.append(case_id)
                # 开头搜索
                elif self.search_rule == 1:
                    match_result = case_name.startswith(self.keyword)
                    if match_result:
                        case_id = case.get('caseName')
                        case_id_list.append(case_id)
                # 结尾搜索
                else:
                    match_result = case_name.endswith(self.keyword)
                    if match_result:
                        case_id = case.get('caseName')
                        case_id_list.append(case_id)
            return case_id_list

    def to_do(self):
        session_id = self.login()
        if session_id != 1:
            ...
        elif session_id == 0:
            self.text.emit('用户名密码错误！')
        else:
            self.text.emit('服务器无法连接，请检查IP和端口！')

    def run(self):
        self.to_do()


if __name__ == "__main__":
    info = {
        "ip": "192.168.0.75",
        "port": "20000",
        "username": "yaocheng",
        "password": "123456",
        "keyword": "",
        "search_rule": 0,
        "execute_scope": 0
    }
    jd_api = IdentityAPI(**info)
    session = jd_api.login()
