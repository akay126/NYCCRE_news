from scrapy import Spider, Request
from real_deal.items import RealDealItem
import csv
import re
# from pandas import DataFrame,read_csv
import pandas as pd
from numpy import repeat,array


class RealDealSpider(Spider):
    name = 'real_deal'
    allowed_urls = ['https://therealdeal.com/']
    start_urls = ['https://therealdeal.com/category/development/page/1/']
    def parse (self,response):
        resi_urls = ['https://therealdeal.com/category/residential-real-estate/page/{}/'.format(i) for i in range(1,270)]
        comm_urls = ['https://therealdeal.com/category/commercial-real-estate//page/{}/'.format(i) for i in range(1,344)]
        dev_urls = ['https://therealdeal.com/category/development/page/{}/'.format(i) for i in range(1,87)]
        design_urls = ['https://therealdeal.com/category/architecture-and-design/page/{}/'.format(i) for i in range(1,23)]
        request_urls = resi_urls + comm_urls + dev_urls + design_urls
        for url in request_urls:
            yield Request(url=url,callback=self.parse_indv)

    def parse_indv(self,response):

        article_urls = response.xpath('//*[@class="entry-title entry-summary"]/a[1]/@href').extract()



        for url in article_urls:
            yield Request(url= url,callback=self.parse_article)

    def parse_article(self,response):

        title = response.xpath('//*[@class="single-title-full"]/text()').extract_first()
        second_headline = response.xpath('//*[@class="secondary-headline"]/text()').extract_first()
        date_published  = response.xpath('//*[@class="date updated published"]/text()').extract_first()
        content =''.join(response.xpath('//*[@class="post-content-box"]/p/text() | //p/a/text()').extract())
        tags = response.xpath('//*[@class="post-tags-list"]/a/text()').extract()

        item = RealDealItem()
        item ['title'] = title
        item ['second_headline'] = second_headline  
        item ['date_published']  = date_published
        item ['content'] = content 
        item ['tags'] = tags
        yield item