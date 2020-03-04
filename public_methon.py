#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import json
import requests
import logging
import os

import urllib3


def get_file_path(project_name='JianDingCaseDel', file_name='catalina.log'):
    """获得日志文件保存路径"""
    sep = str(os.sep)
    current_file_path = os.path.split(os.path.abspath(__file__))[0]
    path_split = current_file_path.split(sep)
    project_index = path_split.index(project_name)
    need_path = path_split[:project_index + 1]
    need_path.append(file_name)
    finally_path = sep.join(need_path)
    return finally_path


def log_config():
    log_path = get_file_path()
    root_logger = logging.getLogger()
    root_logger.setLevel('WARN')
    basic_format = "%(asctime)s [%(levelname)s] %(message)s"
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(basic_format, date_format)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    fh = logging.FileHandler(log_path)
    fh.setFormatter(formatter)
    root_logger.addHandler(sh)
    root_logger.addHandler(fh)


log_config()


def dict_format(dict_object):
    format_object = json.dumps(dict_object, indent=4, ensure_ascii=False, separators=(',', ':'))
    return format_object


def request_post(method_name, url, req):
    headers = {
        "Content-Type": "application/json"
    }
    logging.info(f"The {method_name} request data is:\n{dict_format(req)}")
    try:
        res = requests.post(url, data=json.dumps(req), headers=headers).json()
        logging.info(f"The {method_name} response data is:\n{dict_format(res)}")
    except (TimeoutError,
            ConnectionRefusedError,
            urllib3.exceptions.NewConnectionError,
            urllib3.exceptions.MaxRetryError,
            requests.exceptions.ConnectionError):
        res = None
    return res


