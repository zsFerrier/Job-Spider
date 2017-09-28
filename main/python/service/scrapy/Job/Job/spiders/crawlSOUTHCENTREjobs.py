# -*- coding: utf-8 -*-
__author__ = 'zhaosheng'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy.http import Request
from src.main.python.util.io.FileUtil import FileUtil
import logging.config
import urllib
import os

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')


class SOUTHCENTREleadersSpider(scrapy.Spider):
    name = "SOUTHCENTREjobs"

    start_urls = ["https://www.southcentre.int/work-opportunities/"]

    def __init__(self):
        logger.debug("开始爬取SOUTHCENTRE工作机会")
        self.preurl = 'http://www.southcentre.int'

    '''
    //div[@id="inside_content"]/ul/li[1]/a
    '''
    def parse(self, response):
        selector = scrapy.Selector(response)
        JobTitles = selector.xpath('//div[@id="inside_content"]/ul/li')
        for JobTitle in JobTitles:
            job = ''.join(JobTitle.xpath('a/text()').extract())
            joblink = ''.join(JobTitle.xpath('a/@href').extract())
            #工作机会的链接
            #print joblink
            filename = str(job)+r'.pdf'
            #生成文件名
            #print filename
            #若不存在文件夹则新建，为PDF存储的地址
            if not os.path.exists("SouthCentreJobsPDF"):
                os.mkdir("SouthCentreJobsPDF")
            FileLocal = os.getcwd()+'\\'+'SouthCentreJobsPDF'+'\\'+filename
            #文件地址
            #print FileLocal
            #把pdf格式链接下载到本地
            urllib.urlretrieve(joblink, FileLocal)


