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
        has_error = res.get('hasError')
        if has_error is False:
            session_id = res.get('data').get('sessionId')
        else:
            session_id = None
        return session_id

    def list_case(self, session_id, offset=0, limit=999, removeType=0, type=1):
        url = f"{self.url_prefix}/call?id=experts.listCriminalCase&v="
        data = {
            "sessionid": session_id,
            "offset": offset,
            "limit": limit,
            "removeType": removeType,
            "key_word": [self.keyword],
            "type": type
        }
        method_name = inspect.stack()[0][3]
        res = request_post(method_name, url, data)
        return res

    def to_do(self):
        session_id = self.login()
        if session_id:
            ...
        else:
            self.text.emit('用户名密码错误！')

    def run(self):
        self.to_do()


if __name__ == "__main__":
    info = {
        "ip": "47.107.34.83",
        "port": "20000",
        "username": "yaocheng",
        "password": "123456",
        "keyword": "",
        "search_rule": 0,
        "execute_scope": 0
    }
    jd_api = IdentityAPI(**info)
    session = jd_api.login()
    jd_api.list_case(session)
