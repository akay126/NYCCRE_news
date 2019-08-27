from scrapy import Spider, Request
from commob.items import CommobItem
import pandas as pd
from numpy import repeat,array
import string
import regex as re

class CommobSpider(Spider):
    name = 'commob'
    allowed_urls = ['https://commercialobserver.com']
    start_urls = ['https://commercialobserver.com/']
    def parse (self,response):
        sales_urls = ['https://commercialobserver.com/sales/page/{}/'.format(i) for i in range(1,94)]
        finance_urls = ['https://commercialobserver.com/finance/page/{}/'.format(i) for i in range(1,148)]
        leases_urls = ['https://commercialobserver.com/leases/page/{}/'.format(i) for i in range(1,329)]
        design_urls = ['https://commercialobserver.com/design-construction/page/{}/'.format(i) for i in range(1,78)]
        request_urls = sales_urls + finance_urls + leases_urls + design_urls
        for url in request_urls:
            yield Request(url=url,callback=self.parse_indv)
    def parse_indv (self,response):
        article_urls_1 = response.xpath('//*[@class = "large-card card"]/a/@href').extract()
        article_urls_2 = response.xpath('//*[@class = "medium-card card"]/a/@href').extract()
        article_urls = article_urls_1 + article_urls_2
        for url in article_urls:
            yield Request(url= url,callback=self.parse_article)

    def parse_article(self,response):
        regex = re.compile(r'[\n\r\t]')

        title = response.xpath('//*[@class = "entry-header"]/h1/text()').extract_first().replace('\xa0',' ')
        title = regex.sub('',title).strip()

        date_published = response.xpath('//*[@class = "date"]/text()').extract_first().replace('\xa0',' ')
        date_published = regex.sub('',date_published).strip()

        content = ''.join(response.xpath('//*[@class = "content  "]/p/text() | //p/a/text()').extract()[2:-2])
        tags = response.xpath('//*[@class = "story-keywords-container"]/a/text()').extract()

        item = CommobItem()

        item['title'] = title
        item['date_published'] = date_published
        item['content'] = content 
        item['tags'] = tags
        yield item