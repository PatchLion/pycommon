#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, unittest, urllib

class ApiTest(unittest.TestCase):
    HOST_URL = "http://127.0.0.1:5000"

    def get(self, api,  compares, testfunc=None, param=None):
        if testfunc is None:
            testfunc = self.assertEquals
        url = urllib.request.urljoin(ApiTest.HOST_URL, api)
        if param is not None:
            print("GET", url, "With", param)
            res = requests.get(url=url, params=param)
        else:
            print("GET", url)
            res = requests.get(url=url)
        return ApiTest._resolve_response(res, testfunc, compares, "GET")

    def post(self, api, compares, testfunc=None, param=None):
        if testfunc is None:
            testfunc = self.assertEquals
        url = urllib.request.urljoin(ApiTest.HOST_URL, api)
        if param is not None:
            data = json.dumps(param, ensure_ascii=False)
            print("POST", url, "With", data)
            res = requests.post(url=url, data=data.encode("utf-8"))
        else:
            print("POST", url)
            res = requests.post(url=url)
        return self._resolve_response(res, testfunc, compares, "POST")

    def _resolve_response(self, res, testfunc, compares, method):
        ret = None
        if 200 != res.status_code:
            ret = res.status_code, -1, res.reason, None
        else:
            content = res.content.decode(encoding='utf-8')
            if isinstance(content, str) and len(content) > 0:
                #print("cccc" , type(content))
                data = json.loads(content)
                ret = res.status_code, data["code"], data["msg"], data.get("data", None)
            else:
                ret = 200, -1, "无效的返回格式", None

        print('''
--------------------Api test result-----------------------
\033[1;34m Api.url:\033[0m %s
\033[1;34m Api.method:\033[0m %s
\033[1;34m Network.code:\033[0m %d
\033[1;34m Response.code:\033[0m %d
\033[1;34m Response.msg:\033[0m %s
\033[1;34m Response.data:\033[0m %s
----------------------------------------------------------
        ''' % (res.url, method, ret[0], ret[1], ret[2], ret[3]))

        try:
            if len(compares) >= 1:
                testfunc(ret[0], compares[0]) #网络code
            if len(compares) >= 2:
                testfunc(ret[1], compares[1]) #自定义api code
            print("\033[1;32m[Info] Pass\033[0m\n")
        except Exception as e:
            print("\033[1;31m[Warning] Not Pass:", e, "\033[0m\n")



'''
if "__main__" == __name__:
    ApiTest.HOST_URL = "http://www.patchlion.cn:5000"

    apitest = ApiTest()
    apitest.post(api="/classifies", compares=[200, 0])
    apitest.post(api="/cacheversion", testfunc=apitest.assertEquals, compares=[200, 0])
'''
