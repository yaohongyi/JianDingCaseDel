#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
from PyQt5 import QtCore
from public_methon import request_post


class JianDingAPI:
    def __init__(self, url_prefix, username, password):
        self.url = url_prefix
        self.session_id = self.login(username, password)

    def login(self, username, password):
        url = f"{self.url}/call?id=experts.login&v="
        data = {
            'nickname': username,
            'passwd': password
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
                  first_case_classify_id: str = "", second_case_classify_id: str = ""):
        """
        获取案件列表
        :param offset: 偏移
        :param limit: 数量
        :param key_word: 关键字
        :param remove_type: 0-案件列表，10-案件回收站
        :param case_type: 1-我的案件，2-分发案件，16-所有案件，128-共享案件
        :param first_case_classify_id: 一级案件分类id
        :param second_case_classify_id: 二级案件分类id
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
            "secondLevel": second_case_classify_id
        }
        res = request_post(url, data)
        return res

    def list_case_list_data(self):
        """获取案件列表的案件"""
        res = self.list_case()
        return res

    def list_case_recycle_data(self, remove_type=10):
        """获取案件回收站的案件"""
        res = self.list_case(remove_type=remove_type)
        return res

    def search_case_list(self, search_rule, keyword) -> tuple:
        """从案件列表筛选出目标案件"""
        case_list_res = self.list_case_list_data()
        # 获取案件列表接口中的caseList
        has_error = case_list_res.get('hasError')
        case_id_list = []
        case_name_list = []
        if has_error is False:
            case_list = case_list_res.get('data').get('caseList')
            if case_list is False:
                return case_id_list, case_name_list
            else:
                # 将目标案件id添加到列表中
                for case in case_list:
                    case_name = case.get('caseName')
                    # 全文搜索
                    if search_rule == 0:
                        match_result = case_name.find(keyword)
                        if match_result != -1:
                            case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            case_id_list.append(case_id)
                    # 开头搜索
                    elif search_rule == 1:
                        match_result = case_name.startswith(keyword)
                        if match_result:
                            case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            case_id_list.append(case_id)
                    # 结尾搜索
                    else:
                        match_result = case_name.endswith(keyword)
                        if match_result:
                            case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            case_id_list.append(case_id)
        return case_id_list, case_name_list

    def search_recycle_case_list(self, search_rule, keyword) -> tuple:
        """从案件回收站筛选出目标案件"""
        case_list_res = self.list_case_recycle_data()
        has_error = case_list_res.get('hasError')
        recycle_case_id_list = []
        recycle_case_name_list = []
        if has_error is False:
            case_list = case_list_res.get('data').get('caseList')
            if case_list:
                for case in case_list:
                    case_name = case.get('caseName')
                    # 全文搜索
                    if search_rule == 0:
                        match_result = case_name.find(keyword)
                        if match_result != -1:
                            recycle_case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            recycle_case_id_list.append(case_id)
                    # 开头搜索
                    elif search_rule == 1:
                        match_result = case_name.startswith(keyword)
                        if match_result:
                            recycle_case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            recycle_case_id_list.append(case_id)
                    # 结尾搜索
                    else:
                        match_result = case_name.endswith(keyword)
                        if match_result:
                            recycle_case_name_list.append(case_name)
                            case_id = case.get('criminalCaseId')
                            recycle_case_id_list.append(case_id)
        return recycle_case_id_list, recycle_case_name_list

    def search_target_case(self, execute_scope, search_rule, keyword):
        if execute_scope == 0:
            case_id_list, case_name_list = self.search_case_list(search_rule, keyword)
            recycle_case_id_list, recycle_case_name_list = self.search_recycle_case_list(search_rule, keyword)
            return case_id_list, case_name_list, recycle_case_id_list, recycle_case_name_list
        elif execute_scope == 1:
            case_id_list, case_name_list = self.search_case_list(search_rule, keyword)
            return case_id_list, case_name_list
        else:
            recycle_case_id_list, recycle_case_name_list = self.search_recycle_case_list(search_rule, keyword)
            return recycle_case_id_list, recycle_case_name_list

    def remove_case(self, case_id, remove_type):
        """
        删除案件
        :param case_id: 案件id
        :param remove_type: 删除类型，案件列表删除10，回收站删除20
        :return: 接口响应
        """
        url = f'{self.url}/call?id=experts.removeCriminalCase&v=&timeout=120000'
        data = {
            'criminalCaseId': case_id,
            'removeType': remove_type,
            'sessionId': self.session_id
        }
        res = request_post(url, data)
        return res

    def remove_case_list_data(self, case_id, remove_type=10):
        """从案件列表删除数据"""
        self.remove_case(case_id, remove_type)

    def remove_case_recycle_data(self, case_id, remove_type=20):
        """从案件回收站删除数据"""
        self.remove_case(case_id, remove_type)

    def remove_target_case(self, execute_scope, search_rule, keyword):
        search_result = self.search_target_case(execute_scope, search_rule, keyword)
        """删除筛选出来的目标案件"""
        if execute_scope == 0:
            case_id_list = search_result[0]
            recycle_case_id_list = search_result[2]
            for case_id in case_id_list:
                self.remove_case_list_data(case_id)
                recycle_case_id_list.append(case_id)
            for recycle_case_id in recycle_case_id_list:
                self.remove_case_recycle_data(recycle_case_id)
        elif execute_scope == 1:
            case_id_list = search_result[0]
            for case_id in case_id_list:
                self.remove_case_list_data(case_id)
        else:
            recycle_case_id_list = search_result[0]
            for recycle_case_id in recycle_case_id_list:
                self.remove_case_recycle_data(recycle_case_id)


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
        self.search_rule = kwargs.get('search_rule')
        self.execute_scope = kwargs.get('execute_scope')
        self.jd_api = JianDingAPI(url_prefix, self.username, self.password)

    def do_search(self):
        session_id = self.jd_api.login(self.username, self.password)
        if session_id != 1:
            search_result = self.jd_api.search_target_case(self.execute_scope, self.search_rule, self.keyword)
            # 如果执行范围为全部清理，则查询案件列表及案件回收站，将查询到的结果发送信号
            if self.execute_scope == 0:
                # 将案件列表查询到的案件进行信号发送
                case_name_list = search_result[1]
                if len(case_name_list) == 0:
                    self.search_info.emit(f'案件列表未搜索到匹配关键字【{self.keyword}】的案件！')
                    self.search_info.emit('')
                else:
                    self.search_info.emit(f'案件列表搜索到匹配关键字【{self.keyword}】的案件有：')
                    for case_name in case_name_list:
                        self.search_info.emit(case_name)
                    self.search_info.emit('')
                # 将案件回收站查询到的案件进行信号发送
                recycle_case_name_list = search_result[3]
                if len(recycle_case_name_list) == 0:
                    self.search_info.emit(f'案件回收站未搜索到匹配关键字【{self.keyword}】的案件！')
                    self.search_info.emit('')
                else:
                    self.search_info.emit(f'案件回收站搜索到匹配关键字【{self.keyword}】的案件有：')
                    for recycle_case_name in recycle_case_name_list:
                        self.search_info.emit(recycle_case_name)
                    self.search_info.emit('')
            elif self.execute_scope == 1:
                # 将案件列表查询到的案件进行信号发送
                case_name_list = search_result[1]
                if len(case_name_list) == 0:
                    self.search_info.emit(f'案件列表未搜索到匹配关键字【{self.keyword}】的案件！')
                    self.search_info.emit('')
                else:
                    self.search_info.emit(f'案件列表搜索到匹配关键字【{self.keyword}】的案件有：')
                    for case_name in case_name_list:
                        self.search_info.emit(case_name)
                    self.search_info.emit('')
            else:
                recycle_case_name_list = search_result[1]
                if len(recycle_case_name_list) == 0:
                    self.search_info.emit(f'案件回收站未搜索到匹配关键字【{self.keyword}】的案件！')
                    self.search_info.emit('')
                else:
                    self.search_info.emit(f'案件回收站搜索到匹配关键字【{self.keyword}】的案件有：')
                    for recycle_case_name in recycle_case_name_list:
                        self.search_info.emit(recycle_case_name)
                    self.search_info.emit('')
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
        self.search_rule = kwargs.get('search_rule')
        self.execute_scope = kwargs.get('execute_scope')
        self.jd_api = JianDingAPI(url_prefix, self.username, self.password)

    def do_remove(self):
        self.jd_api.remove_target_case(self.execute_scope, self.search_rule, self.keyword)
        self.remove_info.emit('案件已经全部删除！')

    def run(self):
        self.do_remove()


if __name__ == "__main__":
    a = {'ip': '192.168.0.75', 'port': '20000', 'username': 'lily', 'password': '123456', 'keyword': '',
         'search_rule': 0, 'execute_scope': 2}
    search_case = SearchCase(**a)
    print(search_case.do_search())
