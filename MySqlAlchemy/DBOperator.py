from sqlalchemy import *
from MySqlAlchemy.EngineCreator import *

'''查询记录'''
def records(session, type, cond = None):
    if cond is None or cond is "":
        rs = session.query(type).all()
    else:
        rs = session.query(type).filter(cond).all()
    return rs

'''联合查询'''
def unionRecords(session, src_type, dest_type, cond):
    return session.query(src_type, dest_type).filter(cond).all()

'''记录数量'''
def recordsCount(session, type, cond = None):
    return len(records(session, type, cond))

'''记录是否存在'''
def isRecordExist(session, type, cond):
    return (0 != recordsCount(session, type, cond))

'''添加或更新记录'''
def addOrRecord(session, records):
    size = 0
    if isinstance(records, list):
        for record in records:
            session.merge(record)
        size = len(records)
    else:
        session.merge(records)
        size = 1
    print("Total {0} record added or updated!".format(size))
    session.commit()
    return size

'''删除纪录'''
def removeRecords(session, t, conds = None):
    size = 0
    if conds is None:
        size = session.query(t).delete(synchronize_session=False)
    else:
        size = session.query(t).filter(conds).delete(synchronize_session=False)
    session.commit()
    print("Total {0} record removed! [{1}]".format(size, type(t)))
    return  size