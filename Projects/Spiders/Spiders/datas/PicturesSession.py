#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Projects.Spiders.Spiders.settings import *
from Projects.Spiders.Spiders.datas.PicturesTables import *
from MySqlAlchemy import *

session = createEngine("sqlite:///" + os.path.split(__file__)[0] + "/" + PICTURE_DBFILE_NAME, not os.path.exists(PICTURE_DBFILE_NAME))


def checkUrl(url):
    new = url.strip()
    return new

#所有页面信息
def allPageFromDB():
    res = {}
    pages = records(session, Pages)
    for page in pages:
        url = checkUrl(page.page_url)
        res[page.page_url] = page.title
    return res


#所有图片URL
def allImageFromDB():
    res = {}
    pages = allPageFromDB()
    imageUrls = records(session, ImageUrls)
    for imageurl in imageUrls:
        url = checkUrl(imageurl.page_url)
        if url in pages.keys():
            if url not in res.keys():
                res[url] = [pages[url]]
            res[url].append(imageurl.image_url)
    return res

#所有图片URL
def allImageListFromDB():

    imageUrls = records(session, ImageUrls)
    res = [info.image_url for info in imageUrls]

    return res