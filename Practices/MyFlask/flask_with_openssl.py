#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import *

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', debug=True, port=8001)
