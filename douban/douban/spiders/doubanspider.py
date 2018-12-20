# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest,Request
from scrapy.selector import Selector
from  PIL import Image
from io import BytesIO
import re
class DoubanspiderSpider(scrapy.Spider):
    name = 'doubanspider'
    start_urls = ['http://douban.com/']
    login_url='https://accounts.douban.com/login'
    def start_requests(self):
        yield Request('https://accounts.douban.com/login',callback=self.login)
   
    #下载验证码和模拟登陆
    def login(self,response):
        
        login_pic_url=response.xpath('//*[@id="captcha_image"]/@src').extract_first()                    
        print('获取验证码url中')
        print(login_pic_url)     
        data={'captcha-solution':input('输入验证码：'),
        'form_email':'1004210191@qq.com','form_password':'********'}
        yield FormRequest.from_response(response,formdata=data,callback=self.parsepage)

    def parsepage(self, response):
        with open('D:/豆瓣.html','wb') as f:
            f.write(response.body)

   
    
