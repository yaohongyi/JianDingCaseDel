#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
from PyQt5 import QtCore
from public_methon import request_post


class JianDingAPI:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.session_id = self.login()

    def login(self):
        url = f"{self.url}/call?id=experts.login&v="
        data = {
            'nickname': self.username,
            'passwd': self.password
        }
        res = request_post(url, data)
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

    def list_case(self, offset=0, limit=99999, key_word: list = None, remove_type: int = 0, case_type=1,
                  first_case_classify_id: str = "", second_case_classify_id: str = "", start_data: str = '',
                  end_data: str = ''):
        """
        获取案件列表
        :param offset: 偏移
        :param limit: 数量
        :param key_word: 关键字
        :param remove_type: 0-案件列表，10-案件回收站
        :param case_type: 1-我的案件，2-分发案件，16-所有案件，128-共享案件
        :param first_case_classify_id: 一级案件分类id
        :param second_case_classify_id: 二级案件分类id
        :param start_data:
        :param end_data:
        :return:
        """
        url = f"{self.url}/call?id=experts.listCriminalCase&v="
        data = {
            "sessionid": self.session_id,
            "offset": offset,
            "limit": limit,
            "removeType": remove_type,
            "key_word": key_word,
            "type": case_type,
            "firstLevel": first_case_classify_id,
            "secondLevel": second_case_classify_id,
            'startDate': start_data,
            'endDate': end_data
        }
        res = request_post(url, data)
        return res

    def list_case_list_data(self, keyword):
        """获取案件列表的案件"""
        key_word = list()
        if keyword:
            key_word.append(keyword)
        res = self.list_case(key_word=key_word)
        return res

    def list_case_recycle_data(self, keyword):
        """获取案件回收站的案件"""
        key_word = list()
        if keyword:
            key_word.append(keyword)
        res = self.list_case(key_word=key_word, remove_type=10)
        return res

    def search_case_list(self, keyword) -> tuple:
        """从案件列表筛选出目标案件"""
        case_list_res = self.list_case_list_data(keyword)
        # 获取案件列表接口中的caseList
        has_error = case_list_res.get('hasError')
        case_id_list = []
        case_name_list = []
        if has_error is False:
            case_list = case_list_res.get('data').get('caseList')
            if case_list:
                for case in case_list:
                    case_id = case.get('criminalCaseId')
                    case_id_list.append(case_id)
                    case_name = case.get('caseName')
                    case_name_list.append(case_name)
        return case_id_list, case_name_list

    def search_recycle_case_list(self, keyword) -> tuple:
        """从案件回收站筛选出目标案件"""
        case_list_res = self.list_case_recycle_data(keyword)
        has_error = case_list_res.get('hasError')
        recycle_case_id_list = []
        recycle_case_name_list = []
        if has_error is False:
            case_list = case_list_res.get('data').get('caseList')
            if case_list:
                for case in case_list:
                    case_id = case.get('criminalCaseId')
                    recycle_case_id_list.append(case_id)
                    case_name = case.get('caseName')
                    recycle_case_name_list.append(case_name)
        return recycle_case_id_list, recycle_case_name_list

    def remove_case(self, case_id, remove_type: int = 10):
        """
        删除案件
        :param case_id: 案件id
        :param remove_type: 删除类型，案件列表删除10，回收站删除20
        :return: 接口响应
        """
        url = f'{self.url}/call?id=experts.removeCriminalCase&v='
        data = {
            'criminalCaseId': case_id,
            'removeType': remove_type,
            'sessionId': self.session_id
        }
        res = request_post(url, data)
        return res

    def remove_case_list_data(self, case_id_list):
        """从案件列表删除数据"""
        if case_id_list:
            for case_id in case_id_list:
                self.remove_case(case_id)

    def remove_case_recycle_data(self, recycle_case_id_list):
        """从案件回收站删除数据"""
        if recycle_case_id_list:
            for recycle_case_id in recycle_case_id_list:
                self.remove_case(recycle_case_id, remove_type=20)


class SearchCase(QtCore.QThread):
    search_info = QtCore.pyqtSignal(str)

    def __init__(self, **kwargs):
        super().__init__()
        ip = kwargs.get('ip')
        port = kwargs.get('port')
        url_prefix = f"http://{ip}:{port}"
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.keyword = kwargs.get('keyword')
        self.jd_api = JianDingAPI(url_prefix, self.username, self.password)

    def do_search(self):
        session_id = self.jd_api.login()
        if session_id != 1:
            _, case_name_list = self.jd_api.search_case_list(self.keyword)
            if case_name_list:
                self.search_info.emit(f'【从案件列表搜索到"{self.keyword}"相关的案件有】：')
                for case_name in case_name_list:
                    self.search_info.emit(case_name)
            else:
                self.search_info.emit(f'从案件列表未搜索到"{self.keyword}"相关的案件！！！')
            _, recycle_case_name_list = self.jd_api.search_recycle_case_list(self.keyword)
            if recycle_case_name_list:
                self.search_info.emit(f'【从回收站搜索到"{self.keyword}"相关的案件有】：')
                for recycle_case_name in recycle_case_name_list:
                    self.search_info.emit(recycle_case_name)
            else:
                self.search_info.emit(f'从回收站未搜索到{self.keyword}相关的案件！！！')
        elif session_id == 0:
            self.search_info.emit('用户名密码错误！')
        else:
            self.search_info.emit('服务器无法连接，请检查IP和端口！')

    def run(self):
        self.do_search()


class RemoveCase(QtCore.QThread):
    remove_info = QtCore.pyqtSignal(str)

    def __init__(self, **kwargs):
        super().__init__()
        ip = kwargs.get('ip')
        port = kwargs.get('port')
        url_prefix = f"http://{ip}:{port}"
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.keyword = kwargs.get('keyword')
        self.jd_api = JianDingAPI(url_prefix, self.username, self.password)

    def do_remove(self):
        case_id_list, _ = self.jd_api.search_case_list(self.keyword)
        self.jd_api.remove_case_list_data(case_id_list)
        recycle_case_id_list, _ = self.jd_api.search_recycle_case_list(self.keyword)
        self.jd_api.remove_case_recycle_data(recycle_case_id_list)
        self.remove_info.emit('案件已经全部删除！')

    def run(self):
        self.do_remove()


if __name__ == "__main__":
    a = {'ip': '192.168.0.75', 'port': '20000', 'username': 'lily', 'password': '123456', 'keyword': '',
         'search_rule': 0, 'execute_scope': 2}
    jd = JianDingAPI('http://192.168.0.75:20000', 'yaocheng', '123456')
    jd.search_case_list('姚诚')
