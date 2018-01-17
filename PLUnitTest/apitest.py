#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, unittest, urllib


class ApiTest(unittest.TestCase):
    HOST_URL = "http://127.0.0.1:5000"
    ECHOCOLOR_ENABEL = False

    def __init__(self, *args, **kwargs):
        self.reset()
        unittest.TestCase.__init__(self, *args, **kwargs)

    # 重置成功失败个数
    def reset(self):
        self._success = 0
        self._failed = 0

    # 打印报告 自动重置成功失败个数
    def printReport(self):
        print("--------------测试结果---------------")
        print(self.passString("成功: %d" % self._success), "      ", self.warningString("失败: %d" % self._failed))
        self.reset()
        print("------------------------------------")

    def get(self, api, compares, testfunc=None, param=None):
        url = urllib.request.urljoin(ApiTest.HOST_URL, api)
        if param is not None:
            print("GET", url, "With", param)
            res = requests.get(url=url, params=param)
            return self._resolve_response(res, testfunc, compares, "GET", str(param))
        else:
            print("GET", url)
            res = requests.get(url=url)
            return self._resolve_response(res, testfunc, compares, "GET", "")

    def post(self, api, compares, testfunc=None, param=None):
        url = urllib.request.urljoin(ApiTest.HOST_URL, api)
        if param is not None:
            data = json.dumps(param, ensure_ascii=False)
            print("POST", url, "With", data)
            res = requests.post(url=url, data=data.encode("utf-8"))
            return self._resolve_response(res, testfunc, compares, "POST", str(param))
        else:
            print("POST", url)
            res = requests.post(url=url)
            return self._resolve_response(res, testfunc, compares, "POST", "")

    def _resolve_response(self, res, testfunc, compares, method, param):
        if testfunc is None:
            testfunc = self.assertEquals
        ret = None
        if 200 != res.status_code:
            ret = res.status_code, -1, res.reason, None
        else:
            content = res.content.decode(encoding='utf-8')
            if isinstance(content, str) and len(content) > 0:
                # print("cccc" , type(content))
                data = json.loads(content)
                ret = res.status_code, data["code"], data["msg"], data.get("data", None)
            else:
                ret = 200, -1, "无效的返回格式", None

        print("--------------------Api test result-----------------------")
        print(ApiTest.titleString(" Api.url:") + " %s" % res.url)
        print(ApiTest.titleString(" Api.method:") + " %s" % method)
        print(ApiTest.titleString(" Api.param:") + " %s" % param)
        print(ApiTest.titleString(" Network.code:") + " %d" % ret[0])
        print(ApiTest.titleString(" Response.code:") + " %d" % ret[1])
        print(ApiTest.titleString(" Response.msg:") + " %s" % ret[2])
        data_string = str(ret[3])
        if len(data_string) > 10:
            data_string = data_string[:30] + " ..."
        print(ApiTest.titleString(" Response.data:") + " %s" % data_string)
        print("----------------------------------------------------------")

        try:
            if len(compares) >= 1:
                testfunc(ret[0], compares[0])  # 网络code
            if len(compares) >= 2:
                testfunc(ret[1], compares[1])  # 自定义api code
            print(ApiTest.passString("[Info] Pass"))
            self._success = self._success+1
        except Exception as e:
            print(ApiTest.warningString("[Warning] Not Pass: %s" % e))
            self._failed = self._failed+1
        print("\n")

    @classmethod
    def warningString(cls, string):
        if cls.ECHOCOLOR_ENABEL:
            return "\033[1;31m" + string + "\033[0m"
        else:
            return string

    @classmethod
    def titleString(cls, string):
        if cls.ECHOCOLOR_ENABEL:
            return "\033[1;34m" + string + "\033[0m"
        else:
            return string

    @classmethod
    def passString(cls, string):
        if cls.ECHOCOLOR_ENABEL:
            return "\033[1;32m" + string + "\033[0m"
        else:
            return string


if "__main__" == __name__:
    ApiTest.HOST_URL = "http://www.patchlion.cn:5000"
    ApiTest.ECHOCOLOR_ENABEL = True

    apitest = ApiTest()
    apitest.post(api="/classifies", compares=[200, 0])
    apitest.post(api="/cacheversion", testfunc=apitest.assertEquals, compares=[200, 0])
    apitest.post(api="/cacheversion", param={"test": "test"}, testfunc=apitest.assertEquals, compares=[200, 0])
    apitest.printReport()
