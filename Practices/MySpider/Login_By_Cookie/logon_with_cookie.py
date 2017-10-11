#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request, urllib.parse, urllib.error
import http.cookiejar
from Commons import randomUserAgent

LOGIN_URL = 'http://acm.hit.edu.cn/hoj/system/login'
values = {'user': '******', 'password': '******'} # , 'submit' : 'Login'
postdata = urllib.parse.urlencode(values).encode()
user_agent = randomUserAgent()
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(LOGIN_URL, postdata, headers)
try:
    response = opener.open(request)
    page = response.read().decode()
    # print(page)
except urllib.error.URLError as e:
    print(e.code, ':', e.reason)

cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
print(cookie)
for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)

get_url = 'http://acm.hit.edu.cn/hoj/problem/solution/?problem=1'  # 利用cookie请求访问另一个网址
get_request = urllib.request.Request(get_url, headers=headers)
get_response = opener.open(get_request)
print(get_response.read().decode())
# print('You have not solved this problem' in get_response.read().decode())