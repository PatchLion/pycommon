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