#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import threading, time
import requests, os
from Commons import *
from Projects.Spiders.Spiders.datas.PicturesSession import allImageFromDB

IMAGE_DIR = os.path.split(__file__)[0] + "/../images"

class Downloader(object):
    def __init__(self):
        super(Downloader, self).__init__()
        if not os.path.exists(IMAGE_DIR):
            os.mkdir(IMAGE_DIR)
        self._semaphore = threading.Semaphore(10)
        self._started = False
        self._threads = None
        self._timer = threading.Timer(1, self.checkState)

    def start(self, infos):
        if self._started:
            print("Downloader started!")
            return
        self._threads = [threading.Thread(target=self.downloadFun, args=[page_url, info]) for page_url, info in infos.items()]
        for thread in self._threads:
            thread.start()
        self._started = True
        self._timer.start()

    def stop(self):
        self._started = False
        self._timer.cancel()

    @classmethod
    def filePath(cls, url, parentdir):
        path = IMAGE_DIR + "/" + checkDirName(parentdir)
        if not os.path.exists(path):
            os.mkdir(path)
        filename = os.path.split(url)[1]
        filepath = path + "/" + filename
        return filepath

    def checkState(self):
        print("Checking......")
        if self.allThreadFinished():
            print("All thread finished!!")
            self._timer.cancel()
        else:
            self._timer = threading.Timer(1, self.checkState)
            self._timer.start()


    def allThreadFinished(self):
        states = [thread.is_alive() for thread in self._threads]
        return not (True in states)

    def downloadFun(self, page_url, info):
        #print(page_url, info)
        self._semaphore.acquire()

        for url in info[1:]:
            filepath = Downloader.filePath(url, info[0])
            if not os.path.exists(filepath):
                headers = {'User-Agent': randomUserAgent(), "Referer": url}
                try:
                    req = requests.get(url, headers=headers)
                    # print(req.status_code)
                    if req.status_code == 200:
                        with open(filepath, 'wb') as f:
                            f.write(req.content)
                            print("Write to:", filepath)
                    else:
                        print("Request error code [{0}]! {1}".format(req.status_code, filepath))
                except Exception as e:
                    print(e)

        self._semaphore.release()

if "__main__" == __name__:
    allImages = allImageFromDB()

    print("------->", len(allImages))

    if len(allImages) > 0:
        downloader = Downloader()
        downloader.start(allImages)

    loop = asyncio.get_event_loop()
    loop.run_forever()
