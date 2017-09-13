# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy import Request
from Projects.Spiders.Spiders.datas.PicturesTables import *
from Projects.Spiders.Spiders.datas.PicturesSession import session
import MySqlAlchemy

class PicturesSpiderBase(scrapy.Spider):
    #pages
    def pages(self, sel):
        return None

    #page_url, title
    def pageUrlAndTitle(self, sel):
        return "", ""

    #next_page_url#
    def nextPageUrl(self, sel):
        return ""

    #parent_page_url
    def parentPageUrl(self, url):
        return ""

    #images
    def images(self, sel):
        return None

    #image_url
    def imageUrl(self, sel):
        return ""

    #next_image_page_url
    def nextImagePageUrl(self, sel):
        return ""

    def parse(self, response):
        sel = Selector(response)
        pages = self.pages(sel)

        if pages is None or len(pages) == 0:
            print("Pages is invaild!")
            return

        results = []
        for page in pages:
            #print("Page Sel -->", page.extract())
            page_url, title = self.pageUrlAndTitle(page)
            if (page_url is not None and len(page_url) > 0)\
                and (title is not None and len(title) > 0):
                if not MySqlAlchemy.isRecordExist(session, Pages, Pages.page_url == page_url):
                    print("Title PageUrl:", title, page_url)
                    results.append(Pages(page_url=page_url, title=title))
                    yield Request(page_url, callback=self.parseImage)
            else:
                print("Invaild URL when page parsed! Image url = {0} Page url = {1}".format(title, page_url))

        if len(results) > 0:
            MySqlAlchemy.addOrRecord(session, results)

        next_page = self.nextPageUrl(sel)
        if next_page is not None and len(next_page) > 0:
            print("Next Page:", next_page)
            yield Request(next_page)

    def parseImage(self, response):
        sel = Selector(response)
        images = self.images(sel)

        if images is None or len(images) == 0:
            print("Images is invaild!")
            return

        results = []
        for image in images:
            image_url = self.imageUrl(image)
            page_url = self.parentPageUrl(response.url)
            if (image_url is not None and len(image_url) > 0)\
                and (page_url is not None and len(page_url) > 0):
                if not MySqlAlchemy.isRecordExist(session, ImageUrls, ImageUrls.image_url == image_url):
                    results.append(ImageUrls(page_url=page_url, image_url=image_url))
            else:
                print("Invaild URL when image parsed! Image url = {0} Page url = {1}".format(image_url, page_url))

        if len(results) > 0:
            MySqlAlchemy.addOrRecord(session, results)

        nextImageUrl = self.nextImagePageUrl(sel)
        if nextImageUrl is not None and len(nextImageUrl) > 0:
            yield Request(nextImageUrl, callback=self.parseImage)
