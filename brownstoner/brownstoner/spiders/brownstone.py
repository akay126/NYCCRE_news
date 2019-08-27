from scrapy import Spider, Request
from brownstoner.items import BrownstonerItem
import csv
import re
import pandas as pd
from numpy import repeat,array

class BrownstonerSpider(Spider):
    name = 'brownstoner'
    allowed_urls = ['https://www.brownstoner.com']
    start_urls = ['https://www.brownstoner.com/']
    def parse (self,response):
        request_urls = ['https://www.brownstoner.com/page/{}/'.format(i) for i in range(1,4108)] #1967
        for url in request_urls:
            yield Request(url=url,callback=self.parse_indv)
    def parse_indv (self,response):

        article_urls = response.xpath('//*[@class = "more-link-wrap wpb_button more-button"]/a/@href').extract()

        for url in article_urls:
            yield Request(url= url,callback=self.parse_article)

    def parse_article(self,response):

        title = response.xpath('//*[@class = "entry-title"]/text()').extract_first()
        date_published = response.xpath('//*[@itemprop = "datePublished"]/@content').extract_first()
        content = ''.join(response.xpath('//*[@class ="td-post-text-content notsinglepage"]/p/text() | //p/a/text()').extract())
        tags = response.xpath('//*[@class ="td-post-source-tags"]/ul/li/a/text()').extract()

        item = BrownstonerItem()

        item['title'] = title
        item['date_published'] = date_published
        item['content'] = content 
        item['tags'] = tags
        yield item