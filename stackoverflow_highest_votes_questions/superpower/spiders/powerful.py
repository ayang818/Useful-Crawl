# -*- coding: utf-8 -*-
import re

import scrapy
# from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.selector import Selector

from ..items import SuperpowerItem


class PowerfulSpider(scrapy.Spider):
    name = 'powerful'
    # allowed_domains = ['baidu.com']
    def start_requests(self):
        start_url = "https://stackoverflow.com/questions?sort=votes"
        yield Request(start_url, callback = self.parse,)

    def parse(self, response):
        #在产生response对象的时候自动创建了Selector对象,源码。
        # @property        
        # def selector(self):            
        #     from scrapy.selector import Selector            
        #     if self._cached_selector is None:                
        #         self._cached_selector = Selector(self)            
        #         return self._cached_selector 

        # selector = Selector(text= response.text)
        questions = response.xpath('//*[@class="question-summary"]/div[2]/h3/a//text()').extract()
        votes = response.xpath('//*[@class="question-summary"]/div[1]/div[1]/div[1]/div/span/strong//text()').extract()
        for question, vote in zip(questions, votes):
            sut = SuperpowerItem()
            sut['questions'] = question
            sut['votes'] = vote
            yield sut


