# -*- coding: utf-8 -*-
from .PicturesSpiderBase import PicturesSpiderBase

class MzituPagesSpider(PicturesSpiderBase):
    name = 'mzitu'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://www.mzitu.com']

    #pages
    def pages(self, sel):
        return sel.xpath("//ul[@id='pins']/li/span/a")

    #page_url, title
    def pageUrlAndTitle(self, sel):
        title = sel.xpath("string(.)").extract()[0]
        url = sel.xpath("@href").extract()[0]
        return url, title

    #next_page_url#
    def nextPageUrl(self, sel):
        nextPageNode = sel.xpath("//a[@class='next page-numbers']/@href").extract()
        if len(nextPageNode) > 0:
            nextPage = nextPageNode[0]
            return nextPage
        else:
            return ""

    #parent_page_url
    def parentPageUrl(self, url):
        page_url = ""
        res = os.path.split(url)
        if len(res) == 4:
            page_url = os.path.split(url)[0]
        elif len(res) == 3:
            page_url = url
        return page_url

    #images
    def images(self, sel):
        return sel.xpath("//div[@class='main-image']/p/a")

    #image_url
    def imageUrl(self, sel):
        return sel.xpath("img/@src").extract()[0]

    #next_image_page_url
    def nextImagePageUrl(self, sel):
        nextPageNode = sel.xpath("//div[@class='pagenavi']/a")
        for node in nextPageNode:
            span_text = node.xpath("span/text()").extract()[0]
            if "下一页»" == span_text:
                next_url = node.xpath("@href").extract()[0]
                return next_url
        return ""

