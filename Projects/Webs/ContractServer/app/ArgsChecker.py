#!/usr/bin/env python
# -*- coding: utf-8 -*-

#解析并校验参数
class ArgsChecker(object):
    def __init__(self, args):
        self.args = args
        self.checklist = [] #校验规则，格式 (参数名称，校验函数，是否必须, 是否可为空，取值范围)
        self.params = {}

    def clearCheckList(self):
        self.checklist.clear()

    def clearParams(self):
        self.params.clear()

    def addStringChecker(self, name, is_req = False, isnullable = False):
        self.checklist.append((name, self.CheckString, is_req, isnullable, None))

    def addNumerChecker(self, name, is_req = False, range = (None, None)):
        self.checklist.append((name, self.CheckNumber, is_req, None, range))

    def addDictChecker(self, name, is_req=False, keys = None):
        self.checklist.append((name, self.CheckDict, is_req, None, keys))

    def addArrayChecker(self, name, is_req=False, value_range = None):
        self.checklist.append((name, self.CheckArray, is_req, None, value_range))

    def check(self):
        report = {}
        for check in self.checklist:
            arg_name = check[0]
            check_func = check[1]
            is_req = check[2]
            isnullable = check[3]
            range = check[4]

            temp = {}

            if arg_name not in self.args.keys():
                if is_req:
                    temp["param"] = arg_name
                    temp["message"] = "没有找到参数"
            else:
                if self.args[arg_name] is None:
                    temp["param"] = arg_name
                    temp["message"] = "参数为None"
                else:
                    ck = check_func(self.args[arg_name], isnullable, range)
                    if ck is not None:
                        temp["param"] = arg_name
                        temp["error"] = ck
            if len(temp.keys()) > 0:
                if "errors" not in report.keys():
                    report["errors"] = []
                report["errors"].append(temp)
        return (len(report.keys()) == 0), report


    # 检测字符串
    @classmethod
    def CheckString(cls, arg, isnullable, range):
        if not isinstance(arg, str):
            return "参数类型不为字符串"

        if (arg is None) or len(arg) == 0 and not isnullable:
            return "参数为空"
        else:
            return None

    # 检测数值
    @classmethod
    def CheckNumber(cls,  arg, isnullable, range):
        if not isinstance(arg, int) and not isinstance(arg, float):
            return "参数类型不为数值"

        if range is None:
            return None
        else:
            start = range[0]
            end = range[1]

            if start is not None:
                if arg < start:
                    return "超出最小值:" + str(start)
            if end is not None:
                if arg > end:
                    return  "超出最大值:" + str(end)
        return None

    # 检测字典
    @classmethod
    def CheckDict(cls, arg, isnullable, keys):
        if not isinstance(arg, dict):
            return "参数类型不为字典"

        if keys is None:
            return None

        not_exist_keys = []
        for key in keys:
            if key not in arg.keys():
                not_exist_keys.append(key)
        if len(not_exist_keys) == 0:
            return None
        else:
            return "字典里不包含必须的Key: " + ", ".join(["\"" +  str(key) + "\"" for key in not_exist_keys])

    # 检测数组
    @classmethod
    def CheckArray(cls, arg, isnullable, value_range):
        if not isinstance(arg, list):
            return "参数类型不为数组"

        if value_range is None:
            return None

        print(arg, value_range)
        check = [False for c in arg if c not in value_range]
        if len(check) == 0:
            return None
        else:
            return "数组" + str(arg) + "超出限制范围: " +  str(value_range)

'''
args = {"name": 1, "height": 100, "nick": "", "dict": {"a": 1, "b": 2}, "array": [1, 2]}

ck = ArgsChecker(args)
ck.addNumerChecker(name="name", is_req=True, range=(1,10))
ck.addNumerChecker(name="age", is_req=True, range=(0,200))
ck.addNumerChecker(name="height", is_req=True, range=(0,200))
ck.addStringChecker(name="nick", is_req=False, isnullable=False)
ck.addDictChecker(name="dict", is_req=False, keys=["a", "b", "c", "d"])
ck.addArrayChecker(name="array", is_req=False, value_range=[3, 4, 5])
result = ck.check()

print(result)
'''

