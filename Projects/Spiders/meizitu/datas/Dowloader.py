#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Projects.Spiders.meizitu.datas.MeizituSession import allImageFromDB
import requests, os
from MyCommons.UserAgentStrings import *

allImages = allImageFromDB()

INVALID_CHARS = '\\/:*?"<>|，'
IMAGE_DIR = os.path.split(__file__)[0] + "/../images"

def checkFileName(filename):
    temp = filename
    temp = temp.strip()
    for c in INVALID_CHARS:
        temp = temp.replace(c, "")
    return temp

#print(IMAGE_DIR)
for pageurl, imageurls in allImages.items():
    #print(imageurl, images)
    if not os.path.exists(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)
    path = IMAGE_DIR + "/" + checkFileName(imageurls[0])
    if not os.path.exists(path):
        os.mkdir(path)

    for url in imageurls[1:]:
        filename = os.path.split(url)[1]
        filepath = path + "/" + filename
        if not os.path.exists(filepath):
            headers = {'User-Agent':randomUserAgent()}
            req = requests.get(url, headers=headers)
            #print(req.status_code)
            if req.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(req.content)
                    print("Write to:", filepath)