# -*- coding: utf-8 -*-
from .PicturesSpiderBase import PicturesSpiderBase

class MeizituPagesSpider(PicturesSpiderBase):
    name = 'meizitu'
    allowed_domains = ['meizitu.com']
    start_urls = ['http://www.meizitu.com/a/more_1.html']

    #pages
    def pages(self, sel):
        return sel.xpath("//ul[@class='wp-list clearfix']/li/div/h3[@class='tit']")

    #page_url, title
    def pageUrlAndTitle(self, sel):
        page_url = sel.xpath('a/@href').extract()[0]

        title = ""
        if len(sel.xpath('a/text()').extract()) > 0:
            title = sel.xpath('a/text()').extract()[0]
        else:
            title = sel.xpath('a/b/text()').extract()[0]
        return page_url, title

    #next_page_url#
    def nextPageUrl(self, sel):
        nexthtml = sel.xpath("//div[@id='wp_page_numbers']/ul/li/a[text()='下一页']/@href").extract()
        if len(nexthtml) > 0:
            nexturl = 'http://www.meizitu.com/a/' + nexthtml[0]
            return nexturl
        else:
            return ""

    #parent_page_url
    def parentPageUrl(self, url):
        return url.strip().lower()

    #images
    def images(self, sel):
        res = sel.xpath("//div[@id='picture']/p/img")
        if len(res) == 0:
            res = sel.xpath("//div[@class='postContent']/p/img")
        return res

    #image_url
    def imageUrl(self, sel):
        return sel.xpath('@src').extract()[0]
