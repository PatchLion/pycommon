#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Projects.Spiders.Spiders.settings import *
from Projects.Spiders.Spiders.datas.PicturesTables import *
from MySqlAlchemy import *

session = createEngine("sqlite:///" + os.path.split(__file__)[0] + "/" + PICTURE_DBFILE_NAME, not os.path.exists(PICTURE_DBFILE_NAME))


#所有页面信息
def allPageFromDB():
    res = {}
    pages = records(session, Pages)
    for page in pages:
        res[page.page_url] = page.title
    return res


#所有图片URL
def allImageFromDB():
    res = {}
    pages = allPageFromDB()
    imageUrls = records(session, ImageUrls)
    for imageurl in imageUrls:
        if imageurl.page_url not in res.keys():
            res[imageurl.page_url] = [pages[imageurl.page_url]]
        res[imageurl.page_url].append(imageurl.image_url)
    return res
