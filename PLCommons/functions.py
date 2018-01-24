#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

#去除文件名(目录名)中的无效字符
def makeVaildPath(filename):
    temp = filename
    temp = temp.strip()
    INVALID_CHARS = '\\/:*?"<>|,'
    for c in INVALID_CHARS:
        temp = temp.replace(c, "")
    return temp
	
#64位的uuid
def uuid64():
    return uuid.uuid1().hex + uuid.uuid1().hex

def uuid32():
    return uuid.uuid1().hex

#print(uuid64())