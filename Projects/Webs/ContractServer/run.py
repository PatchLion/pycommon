#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Projects.Webs.ContractServer.app import app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)