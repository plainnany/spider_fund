# -*- coding: utf-8 -*-
import scrapy
from fund.items import FundItem
from scrapy_selenium import SeleniumRequest
from scrapy_splash import SplashRequest
from fund.codes import getCodeList 


class EastmoneySpider(scrapy.Spider):
    name = 'eastmoney'
    allowed_domains = ['fund.eastmoney.com']
    start_urls = ['http://fund.eastmoney.com/allfund.html']
    
    def parse(self, response):
        code_list = getCodeList()
        for code in code_list: 
            real_url = response.urljoin('http://fundf10.eastmoney.com/jdzf_' + code + '.html')
            yield SplashRequest(real_url,callback=lambda response, typeid=code: self.parse_info(response,typeid), dont_filter=True)

    def parse_info(self, response, code): 
        item = FundItem()
        try:
            item['code'] = code
        except:
            item['code'] = response.xpath('//*[@class="fundDetail-tit"]/div/span[2]/text()').extract()[0]
        item['name'] = response.xpath('//*[@class="bs_jz"]/div[1]/h4[1]/a/text()').extract()[0]     # 基金名称
        try:
            item['recent1Week'] = response.xpath('//*[@class="jdzfnew"]/ul[3]/li[2]/text()').extract()[0]     # 最近一月
            item['recent1Month'] = response.xpath('//*[@class="jdzfnew"]/ul[4]/li[2]/text()').extract()[0]     # 最近一月
            item['recent3Month'] = response.xpath('//*[@class="jdzfnew"]/ul[5]/li[2]/text()').extract()[0]     # 最近一月
            item['recent6Month'] = response.xpath('//*[@class="jdzfnew"]/ul[6]/li[2]/text()').extract()[0]     # 最近一月
            item['recent1Year'] = response.xpath('//*[@class="jdzfnew"]/ul[7]/li[2]/text()').extract()[0]     # 最近一月
            item['recent2Year'] = response.xpath('//*[@class="jdzfnew"]/ul[8]/li[2]/text()').extract()[0]     # 最近一月
            item['recent3Year'] = response.xpath('//*[@class="jdzfnew"]/ul[9]/li[2]/text()').extract()[0]     
            item['recent5Year'] = response.xpath('//*[@class="jdzfnew"]/ul[10]/li[2]/text()').extract()[0]     
            item['from_Build'] = response.xpath('//*[@class="jdzfnew"]/ul[11]/li[2]/text()').extract()[0]     
        except:
            print('catch error')
        yield item