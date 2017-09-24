# -*- coding: utf-8 -*-
__author__ = 'Robin'

import sys
sys.path.append('/home/robin/Workspace/pycode/venv/JobSpider/ahu.ailab')
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy.http import Request
from scrapy.http import HtmlResponse
from time import sleep
from src.main.python.util.common.strUtil import StrUtil
from src.main.python.util.io.FileUtil import FileUtil
from ..allitems.jobitems import ITERjobDataItem
import logging.config
import random
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class ITERJobSpider(scrapy.Spider):
    
    name = 'ITERjob'

    start_urls = ['http://www.iter.org/jobs']

    def __init__(self):
        logger.debug('start crawl ITER job page')

    def parse(self, response):
        
        '''
        读取job页，获取详情链接
        '''
        
        item = self._inititem()
        selector = scrapy.Selector(response)
        logger.info('open ITER job page successfully!')
        self.joblink = selector.xpath("//table[@class='table']/tr/td[1]/a/@href").extract()
        i = 0
        for url in self.joblink:
            # print 'this url is ' + url
            # url = random.choice(self.joblink)
            i += 1
            yield Request(url=url, callback=self._parseJobDetail, headers={
                'Cookie': 'ASP.NET_SessionId=rpk1v3202gzb5fjp5tymxa30',
                'Referer': 'http://www.iter.org/jobs'
            }, meta={
                'JobDetailUrl': url,
                'id': i
            })
            logger.debug('已爬取第%d个岗位' % i)
        logger.debug('共爬取%d个岗位' % i)


    def _parseJobDetail(self, response):
        selector = scrapy.Selector(response)
        logger.info(response.meta['id'])
        # path = './' + response.meta['id'] + '.html'
        # print 'path is %d' % path
        with open('./1.html', 'w') as f:
            f.write(response.text)
        item = self._inititem()
        yield item


    def _inititem(self):
        '''
        初始化字段
        '''
        item = ITERjobDataItem()
        item['JobTitle'] = ''
        item['JobDetailUrl'] = ''
        logger.info('intalized ok!')
        return item