#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Projects.Spiders.meizitu.meizitu.settings import *
from Projects.Spiders.meizitu.datas.tables import *
from MySqlAlchemy import *
import os
meizituSession = createEngine("sqlite:///" + os.path.split(__file__)[0] + "/" + DBFILE, not os.path.exists(DBFILE))


#所有页面信息
def allPageFromDB():
    res = {}
    pages = records(meizituSession, Pages)
    for page in pages:
        res[page.page_url] = page.title
    return res

#所有图片URL
def allImageFromDB():
    res = {}
    pages = allPageFromDB()
    imageUrls = records(meizituSession, ImageUrls)
    for imageurl in imageUrls:
        if imageurl.page_url not in res.keys():
            res[imageurl.page_url] = [pages[imageurl.page_url]]
        res[imageurl.page_url].append(imageurl.image_url)
    return res
