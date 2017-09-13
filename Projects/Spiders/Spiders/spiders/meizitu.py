# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy import Request
from Projects.Spiders.Spiders.datas.PicturesTables import *
from Projects.Spiders.Spiders.datas.PicturesSession import session
import MySqlAlchemy

class MeizituPagesSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains = ['meizitu.com']
    start_urls = ['http://www.meizitu.com/a/more_1.html']

    def parse(self, response):
        sel = Selector(response)
        pages = sel.xpath("//ul[@class='wp-list clearfix']/li/div/h3[@class='tit']")

        results = []
        for page in pages:
            page_url = page.xpath('a/@href').extract()[0].lower().strip()

            title = ""
            if len(page.xpath('a/text()').extract())>0:
                title = page.xpath('a/text()').extract()[0].lower().strip()
            else:
                title = page.xpath('a/b/text()').extract()[0].lower().strip()


            if not MySqlAlchemy.isRecordExist(session, Pages, Pages.page_url == page_url):
                results.append(Pages(page_url=page_url, title=title))
                print(title, page_url)
                yield Request(page_url, callback=self.readImage)

        if len(results) > 0:
            MySqlAlchemy.addOrRecord(session, results)

        nexthtml = sel.xpath("//div[@id='wp_page_numbers']/ul/li/a[text()='下一页']/@href").extract()

        if len(nexthtml) > 0:
            nexturl = 'http://www.meizitu.com/a/' + nexthtml[0]
            print("Next Url:", nexturl)
            yield Request(nexturl)

    def readImage(self, response):
        url_string = response.url.strip().lower()
        sel = Selector(response)
        images = sel.xpath("//div[@id='picture']/p/img")
        if len(images) == 0:
            images = sel.xpath("//div[@class='postContent']/p/img")

        if len(images) == 0:
            print("images count == 0!!!!!!!!!!!!!!!!!!!!!!!")

        results = []
        for image in images:
            image_url = image.xpath('@src').extract()[0].lower().strip()
            print(image_url)
            page_url = url_string
            if not MySqlAlchemy.isRecordExist(session, ImageUrls, ImageUrls.image_url == image_url):
                results.append(ImageUrls(page_url=page_url, image_url=image_url))

        if len(results) > 0:
            MySqlAlchemy.addOrRecord(session, results)
