from scrapy import Spider, Request
from post.items import PostItem
import pandas as pd
from numpy import repeat,array
import string
import regex as re

class PostSpider(Spider):
    name = 'post'
    allowed_urls = ['https://nypost.com']
    start_urls = ['https://nypost.com/']
    def parse (self,response):
        request_urls = ['https://nypost.com/real-estate/page/{}/'.format(i) for i in range(1,779)] #1967
        for url in request_urls:
            yield Request(url=url,callback=self.parse_indv)
    def parse_indv (self,response):

        article_urls = response.xpath('//*[@class="entry-heading"]/a/@href').extract()

        for url in article_urls:
            yield Request(url= url,callback=self.parse_article)

    def parse_article(self,response):
        regex = re.compile(r'[\n\r\t]')

        title = ''.join(response.xpath('//*[@class = "article-header"]/h1/text()').extract())
        title = title.str.replace('\t','')
        title = title.str.replace('\n',' ')

        date_published = response.xpath('//*[@class = "byline-date"]/text()').extract()[:2]
        date_published = ("{} {}").format(regex.sub('',date_published[0]).strip(),regex.sub('',date_published[1]).strip())

        content = ''.join(response.xpath('//*[@class = "entry-content entry-content-read-more"]/p/text() | //p/a/text()').extract()[:-7])
        tags = response.xpath('//*[@class = "tag-list"]/a/text()').extract()

        item = PostItem()

        item['title'] = title
        item['date_published'] = date_published
        item['content'] = content 
        item['tags'] = tags
        yield item