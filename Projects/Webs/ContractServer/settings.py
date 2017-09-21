#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# 数据库连接字符串示例
# oracle: oracle://apps:apps@10.0.0.100:1522/VID
# mysql: mysql://root:root@localhost:3306/new_db?charset=utf8
# sqlite: sqlite:///test.db
DB_STRING = 'sqlite:///' + os.path.split(__file__)[0] + "/database/contracts.db"

#文件存储根目录
FILE_RESTORE_ROOT_DIR = "Contract-Files"