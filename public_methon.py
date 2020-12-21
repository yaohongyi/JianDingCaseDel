#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import json
import requests
import urllib3


def dict_format(dict_object):
    format_object = json.dumps(dict_object, indent=4, ensure_ascii=False, separators=(',', ':'))
    return format_object


def request_post(url, req):
    headers = {
        "Content-Type": "application/json",
        "Client-Version": '2.9.6'
    }
    try:
        res = requests.post(url, data=json.dumps(req), headers=headers).json()
    except (TimeoutError,
            ConnectionRefusedError,
            urllib3.exceptions.NewConnectionError,
            urllib3.exceptions.MaxRetryError,
            requests.exceptions.ConnectionError):
        res = None
    return res


