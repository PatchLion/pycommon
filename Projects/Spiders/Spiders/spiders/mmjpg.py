# -*- coding: utf-8 -*-
from .PicturesSpiderBase import PicturesSpiderBase

class MmjpgSpider(PicturesSpiderBase):
    name = 'mmjpg'
    allowed_domains = ['mmjpg.com']
    start_urls = ['http://www.mmjpg.com/']

    #pages
    def pages(self, sel):
        return sel.xpath("//div[@class='pic']/ul/li/span/a")

    #page_url, title
    def pageUrlAndTitle(self, sel):
        title = sel.xpath("string(.)").extract()[0]
        url = sel.xpath("@href").extract()[0]

        return url, title

    #next_page_url#
    def nextPageUrl(self, sel):
        nextUrl = sel.xpath("//div[@class='page']/a")
        for next in nextUrl:
            if next.xpath("text()").extract()[0] == "下一页":
                temp = next.xpath("@href").extract()[0]
                return 'http://www.mmjpg.com' + temp

        return ""


    #parent_page_url
    def parentPageUrl(self, url):
        page_url = ""
        if len(res) == 5:
            page_url = os.path.split(url)[0]
        elif len(res) == 4:
            page_url = url
        return page_url

    #images
    def images(self, sel):
        return sel.xpath("//div[@class='article']/div[@class='content']/a")

    #image_url
    def imageUrl(self, sel):
        return sel.xpath("img/@src").extract()[0]

    #next_image_page_url
    def nextImagePageUrl(self, sel):
        nextPageNode = sel.xpath("//div[@class='page']/a")
        for node in nextPageNode:
            span_text = node.xpath("string(.)").extract()[0]
            url = node.xpath("string(.)").extract()[0]
            if "下一张" == span_text:
                next_url = 'http://www.mmjpg.com'+node.xpath("@href").extract()[0]
                return next_url
            else:
                return ""
