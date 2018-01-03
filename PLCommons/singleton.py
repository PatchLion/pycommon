from functools import wraps

def singleton(cls):
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

'''
@singleton
class Demo(object)：
    def __init__(self):
        print("init")
    
d1 = Demo()
d2 = Demo()
'''