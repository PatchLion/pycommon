# -*- coding: utf-8 -*-
from .PicturesSpiderBase import PicturesSpiderBase

class AitaotuSpider(PicturesSpiderBase):
    name = 'aitaotu'
    allowed_domains = ['aitaotu.com']
    start_urls = ['https://www.aitaotu.com/meinv']

    #pages
    def pages(self, sel):
        return sel.xpath("//ul[@class='container lazy-load']/li/div/a")

    # page_url, title
    def pageUrlAndTitle(self, sel):
        page_url = "https://www.aitaotu.com" + sel.xpath("@href").extract()[0]
        title = sel.xpath("string(.)").extract()[0]
        return page_url, title

    # next_page_url#
    def nextPageUrl(self, sel):
        temps = sel.xpath("//div[@class='clearfix article-page']/ul/li/a")
        #print("--->", text)
        if temps is not None and len(temps) > 0:
            for temp in temps:
                text = temp.xpath("string()").extract()[0]
                #print("aaaa->", text)
                if "下一页" == text:
                    return "https://www.aitaotu.com" + temp.xpath("@href").extract()[0]
        else:
            return ""

    # parent_page_url
    def parentPageUrl(self, url):
        temps = url.split('_')
        if len(temps) <= 1:
            return url
        else:
            return temps[0] + ".html"

    # images
    def images(self, sel):
        return sel.xpath("//div[@class='clearfix arcmain']/ul/li/p/a")

    # image_url
    def imageUrl(self, sel):
        return sel.xpath("img/@src").extract()[0]

    # next_image_page_url
    def nextImagePageUrl(self, sel):
        temps = sel.xpath("//div[@class='clearfix article-page']/ul/li/a")
        # print("--->", text)
        if temps is not None and len(temps) > 0:
            for temp in temps:
                text = temp.xpath("string()").extract()[0]
                # print("aaaa->", text)
                if "下一页" == text:
                    return "https://www.aitaotu.com" + temp.xpath("@href").extract()[0]
        else:
            return ""