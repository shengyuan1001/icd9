# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request


class Icd9Spider(scrapy.Spider):
    name = 'icd9_'
    allowed_domains = ['www.icd9data.com']
    start_urls = ['http://www.icd9data.com/2015/Volume1/default.htm']

    def parse(self, response):
        item = {}
        lis = response.css('.definitionList li')
        print(len(lis))
        for li in lis:
            item['code'] = li.xpath('.//text()').get()
            item['depth'] = 1
            item['href'] = 'http://www.icd9data.com' + li.xpath('.//a/@href').get()
            item['descr'] = li.xpath('.//text()').extract()[-1]
            yield item
            yield Request(item['href'],
                          callback=self.parse_info,
                          meta={'item': item},
                          priority=10)

    def parse_info(self, response):
        data = response.meta.get('item')
        print('----------11111---------->', data)
        item = {}
        lis = response.css('.definitionList li')
        for li in lis:
            item['code'] = li.xpath('.//text()').get()
            item['depth'] = 2
            item['href'] = 'http://www.icd9data.com' + li.xpath('.//a/@href').get()
            item['descr'] = li.xpath('.//text()').extract()[-1]
            yield item
            yield Request(item['href'],
                          callback=self.parse_info1,
                          meta={'item': item},
                          priority=10)

    def parse_info1(self, response):
        data = response.meta.get('item')
        print('----------22222---------->', data)
        item = {}
        lis = response.css('.definitionList li')
        for li in lis:
            item['code'] = li.xpath('.//text()').get()
            item['depth'] = 2
            item['href'] = 'http://www.icd9data.com' + li.xpath('.//a/@href').get()
            item['descr'] = li.xpath('.//text()').extract()[-1]
            yield item
            yield Request(item['href'],
                          callback=self.parse_info11,
                          meta={'item': item},
                          priority=10)

    def parse_info11(self, response):
        data = response.meta.get('item')
        print('----------33333--------->', data)
        item = {}
        lis = response.css('.definitionList li')
        for li in lis:
            item['code'] = li.xpath('.//text()').get()
            item['depth'] = 3
            item['href'] = 'http://www.icd9data.com' + li.xpath('.//a/@href').get()
            item['descr'] = li.xpath('.//text()').extract()[-1]
            yield item

