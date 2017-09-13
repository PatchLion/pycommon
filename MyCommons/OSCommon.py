#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

INVALID_CHARS = '\\/:*?"<>|，'

def checkFileName(filename):
    temp = filename
    temp = temp.strip()
    for c in INVALID_CHARS:
        temp = temp.replace(c, "")
    return temp

def spliturl(url):
    res = []
    temp = os.path.split(url)
    while len(temp[0]) != 0:
        res.append(temp[1])
        temp = os.path.split(temp[0])
    res.append(temp[1])
    return res