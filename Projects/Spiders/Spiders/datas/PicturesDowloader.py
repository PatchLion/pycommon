#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import threading, time
import requests, os
from MyCommons import *
from Projects.Spiders.Spiders.datas.PicturesSession import allImageFromDB

IMAGE_DIR = os.path.split(__file__)[0] + "/../images"

class Downloader(object):
    def __init__(self):
        super(Downloader, self).__init__()
        if not os.path.exists(IMAGE_DIR):
            os.mkdir(IMAGE_DIR)
        self._semaphore = threading.Semaphore(4)
        self._started = False
        self._threads = None

    def start(self, infos):
        if self._started:
            print("Downloader started!")
            return
        self._threads = [threading.Thread(target=self.downloadFun, args=[page_url, info]).start() for page_url, info in infos.items()]
        self._started = True

    def stop(self):
        self._started = False

    def downloadFun(self, page_url, info):
        #print(page_url, info)
        self._semaphore.acquire()

        path = IMAGE_DIR + "/" + checkFileName(info[0])
        if not os.path.exists(path):
            os.mkdir(path)

        for url in info[1:]:
            filename = os.path.split(url)[1]
            filepath = path + "/" + filename
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
                except ex as e:
                    print(e)

            else:
                print("{0} Existed!".format(filepath))
        self._semaphore.release()

if "__main__" == __name__:
    allImages = allImageFromDB()
    downloader = Downloader()
    downloader.start(allImages)
    loop = asyncio.get_event_loop()
    loop.run_forever()
