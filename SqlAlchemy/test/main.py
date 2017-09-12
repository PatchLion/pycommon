#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import *
from SqlAlchemy.test.tables import *
from SqlAlchemy.test.settings import *
from SqlAlchemy.DBOperator import *
import os

session = createEngine("sqlite:///" + DB_FILE_PATH, not os.path.exists(DB_FILE_PATH))

new_user = User(id="1", name="lucky")

new_users = [new_user, User(id="2", name="patchlion")]

addOrRecord(session, new_users)
print(isRecordExist(session, User, User.id == new_user.id))
'''removeRecords(session, User, User.id.in_(("1", "2")))
print(isRecordExist(session, User, User.id == new_user.id))'''
print(records(session, User))
print(recordsCount(session, User))