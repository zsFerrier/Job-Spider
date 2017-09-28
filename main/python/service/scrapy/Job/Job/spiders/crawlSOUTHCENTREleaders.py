# -*- coding: utf-8 -*-
__author__ = 'zhaosheng'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy.http import Request
from ..allitems.leaderitems import SOUTHCENTRELeadersItem
from src.main.python.util.common.strUtil import StrUtil
from src.main.python.util.io.FileUtil import FileUtil
import logging.config

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class SOUTHCENTREleadersSpider(scrapy.Spider):
    name = "SOUTHCENTREleaders"

    start_urls = ["https://www.southcentre.int/board-members/"]

    def __init__(self):
        logger.debug("开始爬取SOUTHCENTRE领导人信息")
        self.preurl = 'http://www.southcentre.int'

    def parse(self, response):
        selector = scrapy.Selector(response)
        item = self._inititem()

        '''
        //*[@id="inside_content"]/h4[2]/span/font/font
        //*[@id="inside_content"]/h4[3]/span/font/font
        '''
        a = 0
        i = 0
        RootPaths = selector.xpath('//div[@id="inside_content"]/table')
        for RootPath in RootPaths[:2:]:
            if a == 0:
                item["work"] = ''.join(selector.xpath('//div[@id="inside_content"]/h4[2]/span/text()').extract())
                a = a + 1
            else:
                item["work"] = ''.join(selector.xpath('//div[@id="inside_content"]/h4[3]/span/text()').extract())
            LeadPaths = RootPath.xpath('tbody/tr')
            for LeadPath in LeadPaths:
                item["duration"] = ''.join(LeadPath.xpath('td[1]/text()').extract())
                item["nation"] = ''.join(LeadPath.xpath('td[3]/text()').extract())
                item["name"] = ''.join(LeadPath.xpath('td[2]/a/text()').extract())
                item["url"] = ''.join(LeadPath.xpath('td[2]/a/@href').extract())
                print item["url"]
                if item["url"]:
                    yield Request(url=item["url"], \
                                  callback=self.leaderParse, \
                                  meta={"Duration": item["duration"], "Work": item["work"], "Name": item["name"], "Nation": item["nation"], "Url": item["url"]})
                    i = i + 1
                    logger.debug('已爬取第%d位领导人' % i)
        logger.debug('爬取South Centre领导人结束，共爬取%d位领导人' % i)


    def leaderParse(self, response):
        item = self._inititem()
        item["duration"] = response.meta["Duration"]
        item["work"] = response.meta["Work"]
        item["name"] = response.meta["Name"]
        item["nation"] = response.meta["Nation"]
        item["url"] = response.meta["Url"]
        selector = scrapy.Selector(response)
        LeaderResumes = selector.xpath('//div[@id="inside_content"]/p')
        Resumes = []
        for LeaderResume in LeaderResumes:
            Resume = ''.join(LeaderResume.xpath('text()').extract())

            if Resume:
                Resumes.append(str(Resume))
        item["resume"] = ';'.join(Resumes)
        yield item

    def _inititem(self):
        '''
        duration = scrapy.Field()     #在职时间
        work = scrapy.Field()         #职位
        name = scrapy.Field()         #姓名
        nation = scrapy.Field()       #国家
        resume = scrapy.Field()       #简历
        englishname = scrapy.Field()  # 组织英文缩写
        url = scrapy.Field()  # 领导人连接
        :return: item
        '''
        item = SOUTHCENTRELeadersItem()
        item["duration"] = ""
        item["work"] = ""
        item["name"] = ""
        item["nation"] = ""
        item["resume"] = ""
        item["englishname"] = "South Centre"
        item["url"] = ""
        logger.info("初始化SouthCentre领导人item成功")
        return item
