from scrapy import Spider, Request
from yimby.items import YimbyItem
import csv
import re
# from pandas import DataFrame,read_csv
import pandas as pd
from numpy import repeat,array

class YimbySpider(Spider):
    name = 'yimby'
    allowed_urls = ['https://newyorkyimby.com']
    start_urls = ['https://newyorkyimby.com/']
    def parse (self,response):
        request_urls = ['https://newyorkyimby.com/page/{}/'.format(i) for i in range(1,2047)] #1967
        for url in request_urls:
            yield Request(url=url,callback=self.parse_indv)
    def parse_indv (self,response):

        article_urls = response.xpath('//*[@class="button-excerpt-more button"]/@href').extract()

        for url in article_urls:
            yield Request(url= url,callback=self.parse_article)

    def parse_article(self,response):

        title = response.xpath('//*[@class="post-title entry-title p-name"]/text()').extract_first()
        date_published = response.xpath('//*[@class="entry-meta-date updated dt-published"]/text()').extract_first().replace(' on ','') + " " + response.xpath('//*[@class="entry-meta"]/text()').extract()[1].strip()
        content = ''.join(response.xpath('//*[@class="entry-content e-content clearfix"]/p/text() | //p/a/text()').extract()[:-8])
        tags = response.xpath('//*[@class="breadcrumb"]/span/a/text()').extract()

        item = YimbyItem()

        item['title'] = title
        item['date_published'] = date_published
        item['content'] = content 
        item['tags'] = tags
        yield item
