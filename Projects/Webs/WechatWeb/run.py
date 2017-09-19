#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from app import wechat

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

wechat.create_menu(menu)

app.run(host='0.0.0.0', debug=True, port=80)