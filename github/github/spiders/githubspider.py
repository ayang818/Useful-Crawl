# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest,Request

class GithubspiderSpider(scrapy.Spider):
    name = 'githubspider'
    
    
    def start_requests(self):
        yield Request('https://github.com/login',callback=self.log)
    
    def log(self,response):
        fd={'login':'1004210191@qq.com','password':'********'}
        yield FormRequest.from_response(response,formdata=fd,callback=self.parsepage)
    
    def parsepage(self,response):
        with open('D:/Mygithub.html','wb') as f:
            f.write(response.body)
