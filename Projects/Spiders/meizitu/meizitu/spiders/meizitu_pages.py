# -*- coding: utf-8 -*-
import scrapy


class MeizituPagesSpider(scrapy.Spider):
    name = 'meizitu_pages'
    allowed_domains = ['meizitu.com']
    start_urls = ['http://meizitu.com/']

    def parse(self, response):
        pass
