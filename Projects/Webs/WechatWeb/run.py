#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from app import wechat

from wechat_sdk.exceptions import OfficialAPIError

app.run(host='0.0.0.0', debug=True, port=80)