from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Icd9Spider(CrawlSpider):
    name = 'icd9__'
    start_urls = ['http://www.icd9data.com']
    num = 1
    rules = (
        # 定位到指定的url
        Rule(LinkExtractor(restrict_xpaths='.//div[@class="homePageLeftColumn"]/ul[1]/li[1]/a[1]'),
             callback='parse_', follow=True),
        # 跟进后筛选的url
        Rule(LinkExtractor(restrict_css='.definitionList li'), callback='parse_', follow=True),
    )

    def parse_(self, response):
        item = {}
        lis = response.css('.definitionList li')
        lis_ = response.css('.codeHierarchyUL').xpath('./li[position()>1]')
        string = response.url.split('http://www.icd9data.com/2015/Volume1')[-1]
        num = string.count('/')
        if lis:
            for li in lis:
                item['code'] = li.xpath('.//text()').get()
                item['depth'] = num
                item['href'] = 'http://www.icd9data.com' + li.xpath('.//a/@href').get()
                item['descr'] = li.xpath('.//text()').extract()[-1]
                yield item
        elif lis_:
            for li in lis_:
                item['code'] = li.xpath('./span/a[1]/text()').get()
                item['depth'] = num
                item['href'] = 'http://www.icd9data.com' + li.xpath('./span/a[1]/@href').get()
                item['descr'] = li.xpath('./span/span/text()').get()
                yield item
