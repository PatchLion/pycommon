#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Projects.Spiders.mzitu.datas.MzituSession import allImageFromDB
import requests, os
from MyCommons import *

allImages = allImageFromDB()

IMAGE_DIR = os.path.split(__file__)[0] + "/../images"

#print(IMAGE_DIR)
def process():
    index = 1
    for pageurl, imageurls in allImages.items():
        print(str(index) + " / " + str(len(allImages)))
        if not os.path.exists(IMAGE_DIR):
            os.mkdir(IMAGE_DIR)
        path = IMAGE_DIR + "/" + checkFileName(imageurls[0])
        if not os.path.exists(path):
            os.mkdir(path)

        for url in imageurls[1:]:
            filename = os.path.split(url)[1]
            filepath = path + "/" + filename
            if not os.path.exists(filepath):
                headers = {'User-Agent':randomUserAgent(), "Referer": "http://www.mzitu.com"}
                try:
                    req = requests.get(url, headers=headers)
                    #print(req.status_code)
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

        index = index + 1

if "__main__" == __name__:
    process()