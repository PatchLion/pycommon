# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy import Request
from Projects.Spiders.Spiders.datas.PicturesTables import *
from Projects.Spiders.Spiders.datas.PicturesSession import session
import MySqlAlchemy
import os

class MzituPagesSpider(scrapy.Spider):
    name = 'mzitu'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://www.mzitu.com']

    def parse(self, response):
        sel = Selector(response)
        pages = sel.xpath("//ul[@id='pins']/li/span/a")

        results = []
        for page in pages:
            title = page.xpath("string(.)").extract()[0]
            url = page.xpath("@href").extract()[0]

            if not MySqlAlchemy.isRecordExist(session, Pages, Pages.page_url == url):
                results.append(Pages(page_url=url, title=title))
                print(title, url)
            yield Request(url, callback=self.page)
        if len(results) > 0:
            MySqlAlchemy.addOrRecord(session, results)

        nextPageNode =sel.xpath("//a[@class='next page-numbers']/@href").extract()
        if len(nextPageNode) > 0:
            nextPage = nextPageNode[0]
            yield Request(nextPage)

    @staticmethod
    def spliturl(url):
        res = []
        temp = os.path.split(url)
        while len(temp[0]) != 0:
            res.append(temp[1])
            temp = os.path.split(temp[0])
        res.append(temp[1])
        return res


    def page(self, response):
        res = MzituPagesSpider.spliturl(response.url)

        page_url = ""
        if len(res) == 4:
            page_url = os.path.split(response.url)[0]
        elif len(res) == 3:
            page_url = response.url

        print(res, page_url)
        sel = Selector(response)
        image_url = sel.xpath("//div[@class='main-image']/p/a/img/@src").extract()[0]
        print(image_url)
        if not MySqlAlchemy.isRecordExist(session, ImageUrls, ImageUrls.image_url == image_url):
            MySqlAlchemy.addOrRecord(session, ImageUrls(page_url=page_url, image_url=image_url))

        nextPageNode = sel.xpath("//div[@class='pagenavi']/a")

        for node in nextPageNode:
            span_text = node.xpath("span/text()").extract()[0]

            if "下一页»" == span_text:
                next_url = node.xpath("@href").extract()[0]
                yield Request(url=next_url, callback=self.page)