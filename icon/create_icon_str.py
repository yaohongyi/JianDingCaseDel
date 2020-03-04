#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import base64
import os

save_file = 'icon.py'

os.remove(save_file)

with open(save_file, "a") as f:
    f.write("img='")
with open("./icon.ico", "rb") as i:
    b64str = base64.b64encode(i.read())
    with open(save_file, "ab+") as f:
        f.write(b64str)
with open(save_file, "a") as f:
    f.write("'")
