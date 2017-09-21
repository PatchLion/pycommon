#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
sys.path.insert(0, os.path.split(os.path.realpath(__file__))[0] + "/../../..")


from Projects.Webs.ContractServer.app import app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)