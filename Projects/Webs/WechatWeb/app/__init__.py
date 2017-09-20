#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic

conf = WechatConf(appid='wx2c21f552e41d70e3', token="diornext", appsecret="f8dc86b8b03aff989311a8650a1f81e1", encrypt_mode='normal')
wechat = WechatBasic(conf=conf)

app = Flask(__name__)

from app import views