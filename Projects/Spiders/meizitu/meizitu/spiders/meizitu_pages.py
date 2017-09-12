# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy import Request

class MeizituPagesSpider(scrapy.Spider):
    name = 'meizitu_pages'
    allowed_domains = ['meizitu.com']
    start_urls = ['http://www.meizitu.com/a/more_1.html']

    def parse(self, response):
        sel = Selector(response)
        pages = sel.xpath("//ul[@class='wp-list clearfix']/li/div/h3[@class='tit']")
        list_page = []

        page_urls = MeizituSpider.dboperator.allPageUrls()

        for page in pages:
            url = page.xpath('a/@href').extract()[0].lower().strip()

            if url not in page_urls:
                p = Pages()
                p.url = url
                if len(page.xpath('a/text()').extract())>0:
                    p.title = page.xpath('a/text()').extract()[0].lower().strip()
                else:
                    p.title = page.xpath('a/b/text()').extract()[0].lower().strip()

                print(p.title, p.url)
                list_page.append(p)

        MeizituSpider.dboperator.addOrUpdatePages(list_page)

        nexthtml = sel.xpath("//div[@id='wp_page_numbers']/ul/li/a[text()='下一页']/@href").extract()
        if len(nexthtml) > 0:
            nexturl = 'http://www.meizitu.com/a/' + nexthtml[0]
            return Request(nexturl)