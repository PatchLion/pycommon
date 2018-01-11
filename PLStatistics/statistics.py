#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading, time

class Statistics(threading.Thread):
    def __init__(self):
        self._stacked = []
        self._thread = None

    def run(self):
        pass

    def stop(self):
        pass

    def _threadFunc(self):
        pass