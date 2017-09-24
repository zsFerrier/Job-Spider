# -*- coding: utf-8 -*-
__author__ = 'liuyang'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import re
import time
from scrapy.http import Request
from selenium import webdriver
from scrapy.http import HtmlResponse
from ..allitems.jobitems import UNDPJobDataItem,UNDPJobDataItem2
from src.main.python.util.common.strUtil import StrUtil
import logging.config
from src.main.python.util.io.FileUtil import FileUtil
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu') 
path = FileUtil().getResoursePath() + "/links/UNDPjobLinks.txt"

class UNDPjobSpider(scrapy.Spider):

    name = "UNDPjob"

    def __init__(self):

        self.noidziduan = ['Location :','Application Deadline :','Additional  Category :',
                       'Type of Contract :','Post Level :','Languages Required :','Duration of Initial Contract :',
                       'Expected Duration of Assignment :']

        self.ITE = ['Location','ApplicationDeadline','TypeofContract','PostLevel','LanguagesRequired',
                    'DurationofInitialContract','ExpectedDurationofAssignment','AdditionalCategory']

        self.textnfo_noid = ['Background','Duties and Responsibilities','Competencies','Required Skills and Experience']

        # 用来存储第二种页面信息的容器
        self.items = []

        # self.driver = webdriver.Chrome()
        # self.driver.maximize_window()

    def start_requests(self):

        '''
        读取连接，进行数据抽取
        '''

        f = open(path)
        allUNDPlinks = f.read().split('\n')

        for links in allUNDPlinks:
            link =  links.split('\t')
            # 连接以“id=2”结尾
            if link[0].endswith('id=2'):
                pass
                # self.crawlhaveid(link)

            # 连接不以“id=2”结尾
            else:
                print link[0]
                yield Request(url=link[0],
                                callback=self._UNDPprase,
                                meta={"describe":link[1],
                                        "suoshu":link[2],
                                        "work":link[3],
                                        "applytime":link[4],
                                        "linkman":link[5]}
                                  )

    def _UNDPprase(self, response):
        '''
       使用scrapy框架解析岗位信息（第一种页面形式）
       '''
        logger.debug('crawl')
        work_or_PostLevel = response.meta["work"]

        job = scrapy.Selector(response)
        item = self._setitem_noid(response)

        if response.url.endswith('id=2'):
            pass
        else:
            try:
                self._crawlnoid(job,item,work_or_PostLevel)
            except:
                logger.warning("未能爬取到页面%s的相关数据"%response.url)
            yield item

    def _crawlnoid(self,job,item,work_or_PostLevel):

        '''
        对第一种形式页面进行字段解析
        '''

        item["work"] = work_or_PostLevel

        #TODO  提取基本信息
        trs = job.xpath('//div[@id="content-main"]/table[1]/tr')

        for tr in trs:
            ziduanming = tr.xpath('td[1]/strong/text()').extract()
            if ziduanming:
                if ziduanming[0] in self.noidziduan:
                    context = tr.xpath('td[2]/text()').extract()
                    if context:
                        if StrUtil.delWhite(ziduanming[0].strip(':')) == "LanguagesRequired":
                            item[StrUtil.delWhite(ziduanming[0].strip(':'))] = re.sub('\W',' ',StrUtil.delWhite(context[0]))
                        else:
                            item[StrUtil.delWhite(ziduanming[0].strip(':'))] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(context[0]))


        # TODO  提取技能经历等数据
        skilldatas = job.xpath('//div[@id="content-main"]/table[2]/tr')

        for i in range(0,len(skilldatas),1):
            name = skilldatas[i].xpath('td[@class="field"]/h5/text()').extract()
            if name:
                if name[0] in self.textnfo_noid:
                    data = skilldatas[i+1].xpath('td[@class="text"]')
                    info = data.xpath('string(.)').extract()
                    item[StrUtil.delWhite(name[0])] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(info[0]))


    def crawlhaveid(self, link):

        '''
        打开第二种形式页面并进行页面提取
        '''
        item = self.setitem_haveid(link)
        retrynum = 0
        self.driver.get(link[0])
        time.sleep(2)

        self.driver.implicitly_wait(30)

        # 判断页面是否加载成功
        if "Job" in self.driver.page_source:
            try:
                # 进行页面解析
                self.crawlinfohaveid(item,self.driver.page_source)
            except:
                pass
        else:
            retrynum += 1
            time.sleep(5)
            if retrynum < 10:
                self.driver.refresh()
                self.crawlhaveid(link)
            else:
                logger.error("重试10次仍不能正常显示：  " + link[0])


    def crawlinfohaveid(self,item,page_sourse):

        '''
        对第二种页面进行字段提取
        '''
        pass

    def setitem_haveid(self,link):
        '''
        初始化第二种页面全部字段
        '''
        item = UNDPJobDataItem2()
        item["englishname"] = "UNDP"
        item["chinesename"] = "联合国开发计划署"
        item["incontinent"] = "北美洲"
        item["incountry"] = "美国"
        item["type"] = "科学研究"
        item["url"] = "http://www.undp.org/"
        item["alljoburl"] = "https://jobs.undp.org/cj_view_jobs.cfm"
        item["joburl"] = link[0]
        item["describe"] = link[1]
        item["suoshu"] = link[2]
        item["applytime"] = link[4]
        item["linkman"] = link[5]
        return item

    def _setitem_noid(self,response):
        '''
        初始化第一种页面全部字段
        '''
        item = UNDPJobDataItem()
        item["work"] = ""
        item["englishname"] = "UNDP"
        item["chinesename"] = "联合国开发计划署"
        item["incontinent"] = "北美洲"
        item["incountry"] = "美国"
        item["type"] = "科学研究"
        item["url"] = "http://www.undp.org/"
        item["alljoburl"] = "https://jobs.undp.org/cj_view_jobs.cfm"
        item["joburl"] = response.url
        item["describe"] = response.meta["describe"]
        item["suoshu"] = response.meta["suoshu"]
        item["applytime"] = response.meta["applytime"]
        item["linkman"] = response.meta["linkman"]
        for ite in self.ITE:
            item[ite] = ""
        return item