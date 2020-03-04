#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import inspect
import logging
from PyQt5 import QtCore
from public_methon import request_post, log_config


class SearchCase(QtCore.QThread):
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

    def search_case_list(self, session_id) -> list:
        """从案件列表筛选出目标案件"""
        case_list_res = self.list_case_list_data(session_id)
        # 获取案件列表接口中的caseList
        has_error = case_list_res.get('hasError')
        case_id_list = []
        case_name_list = []
        if has_error is False:
            case_list = case_list_res.get('data').get('caseList')
            if case_list is False:
                return case_id_list
            else:
                # 将目标案件id添加到列表中
                for case in case_list:
                    case_name = case.get('caseName')
                    # 全文搜索
                    if self.search_rule == 0:
                        match_result = case_name.find(self.keyword)
                        if match_result != -1:
                            case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            case_id_list.append(case_id)
                    # 开头搜索
                    elif self.search_rule == 1:
                        match_result = case_name.startswith(self.keyword)
                        if match_result:
                            case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            case_id_list.append(case_id)
                    # 结尾搜索
                    else:
                        match_result = case_name.endswith(self.keyword)
                        if match_result:
                            case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            case_id_list.append(case_id)
        else:
            case_id_list = []
        logging.info(f'在案件列表找到的目标案件有:{case_name_list}')
        logging.info(f'在案件列表找到的目标案件id有:{case_id_list}')
        if case_name_list:
            self.text.emit(f'在案件列表找到与关键字“{self.keyword}”匹配的案件有：')
            for case_name in case_name_list:
                self.text.emit(case_name)
        else:
            self.text.emit(f'在案件列表没有找到与关键字“{self.keyword}”匹配的案件！')
        self.text.emit('')
        return case_id_list

    def search_recycle_case_list(self, session_id) -> list:
        """从案件回收站筛选出目标案件"""
        case_list_res = self.list_case_recycle_data(session_id)
        has_error = case_list_res.get('hasError')
        recycle_case_id_list = []
        case_name_list = []
        if has_error is False:
            case_list = case_list_res.get('data').get('caseList')
            if case_list:
                for case in case_list:
                    case_name = case.get('caseName')
                    # 全文搜索
                    if self.search_rule == 0:
                        match_result = case_name.find(self.keyword)
                        if match_result != -1:
                            case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            recycle_case_id_list.append(case_id)
                    # 开头搜索
                    elif self.search_rule == 1:
                        match_result = case_name.startswith(self.keyword)
                        if match_result:
                            case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            recycle_case_id_list.append(case_id)
                    # 结尾搜索
                    else:
                        match_result = case_name.endswith(self.keyword)
                        if match_result:
                            case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            recycle_case_id_list.append(case_id)
            else:
                recycle_case_id_list = []
        else:
            recycle_case_id_list = []
        logging.info(f'在案件回收站找到的目标案件有:{case_name_list}')
        logging.info(f'在案件回收站找到的目标案件id有:{recycle_case_id_list}')
        if case_name_list:
            self.text.emit(f'在案件回收站找到与关键字“{self.keyword}”匹配的案件有：')
            for case_name in case_name_list:
                self.text.emit(case_name)
        else:
            self.text.emit(f'在案件回收站没有找到与关键字“{self.keyword}”匹配的案件！')
        self.text.emit('')
        return recycle_case_id_list

    def search_target_case(self, session_id):
        if self.execute_scope == 0:
            case_id_list = self.search_case_list(session_id)
            recycle_case_id_list = self.search_recycle_case_list(session_id)
            return session_id, case_id_list, recycle_case_id_list
        elif self.execute_scope == 1:
            case_id_list = self.search_case_list(session_id)
            return session_id, case_id_list
        else:
            recycle_case_id_list = self.search_recycle_case_list(session_id)
            return session_id, recycle_case_id_list

    def do_search(self):
        session_id = self.login()
        result = None
        if session_id != 1:
            result = self.search_target_case(session_id)
        elif session_id == 0:
            self.text.emit('用户名密码错误！')
        else:
            self.text.emit('服务器无法连接，请检查IP和端口！')
        return result

    def run(self):
        self.do_search()


class RemoveCase(QtCore.QThread):
    text = QtCore.pyqtSignal(str)

    def __init__(self, search_result, **kwargs):
        super().__init__()
        self.search_result = search_result
        self.session_id = self.search_result[0]
        ip = kwargs.get('ip')
        port = kwargs.get('port')
        self.url_prefix = f"http://{ip}:{port}"
        self.execute_scope = kwargs.get('execute_scope')

    def remove_case(self, case_id, remove_type):
        """
        删除案件
        :param case_id: 案件id
        :param remove_type: 删除类型，案件列表删除10，回收站删除20
        :return: 接口响应
        """
        url = f'{self.url_prefix}/call?id=experts.removeCriminalCase&v=&timeout=120000'
        data = {
            'criminalCaseId': case_id,
            'removeType': remove_type,
            'sessionId': self.session_id
        }
        method_name = inspect.stack()[0][3]
        res = request_post(method_name, url, data)
        return res

    def remove_case_list_data(self, case_id, remove_type=10):
        """从案件列表删除数据"""
        self.remove_case(case_id, remove_type)

    def remove_case_recycle_data(self, case_id, remove_type=20):
        """从案件回收站删除数据"""
        self.remove_case(case_id, remove_type)

    def remove_target_case(self):
        """删除筛选出来的目标案件"""
        if self.execute_scope == 0:
            case_id_list = self.search_result[1]
            recycle_case_id_list = self.search_result[2]
            for case_id in case_id_list:
                self.remove_case_list_data(case_id)
                recycle_case_id_list.append(case_id)
            for recycle_case_id in recycle_case_id_list:
                self.remove_case_recycle_data(recycle_case_id)
        elif self.execute_scope == 1:
            case_id_list = self.search_result[1]
            for case_id in case_id_list:
                self.remove_case_list_data(case_id)
        else:
            recycle_case_id_list = self.search_result[1]
            for recycle_case_id in recycle_case_id_list:
                self.remove_case_recycle_data(recycle_case_id)
        self.text.emit('已完成案件删除！')

    def run(self):
        self.remove_target_case()


if __name__ == "__main__":
    a = {'ip': '192.168.0.75', 'port': '20000', 'username': 'lily', 'password': '123456', 'keyword': '',
         'search_rule': 0, 'execute_scope': 2}
    search_case = SearchCase(**a)
    print(search_case.do_search())
