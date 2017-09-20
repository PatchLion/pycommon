#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from app import wechat

from wechat_sdk.exceptions import OfficialAPIError

print(wechat.access_token)
menu = {
     "button":[
     {
          "type":"click",
          "name":"注册",
          "key":"REGEDIT"
      },
     {
          "type":"click",
          "name":"登录",
          "key":"LOGIN"
      }]
}
try:
     wechat.create_menu(menu)
except  OfficialAPIError as e:
     print(e)

app.run(host='0.0.0.0', debug=True, port=80)