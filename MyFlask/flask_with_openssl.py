#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MyFlask.app import app

app.debug = True
#app.run('0.0.0.0', debug=True, port=8100, ssl_context="adhoc")
app.run(host='0.0.0.0', debug=True, port=8080)