#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, logging, time

#创建日志对象
def createLogger(name="", path="logs", level=logging.WARNING):
    #
    if not os.path.exists(path):
        os.makedirs(path)

    #
    logger = logging.getLogger(name)

    #文件名称
    filename = time.strftime("%Y%m%d%H%M%S.log", time.localtime())

    #设置handler
    file_handler = logging.FileHandler(os.path.join(path, filename))
    stream_handler = logging.StreamHandler()

    #设置级别
    file_handler.setLevel(level)
    stream_handler.setLevel(level)

    #设置format
    logging_format = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s (%(filename)s at line %(lineno)s)')
    file_handler.setFormatter(logging_format)
    stream_handler.setFormatter(logging_format)

    return logger