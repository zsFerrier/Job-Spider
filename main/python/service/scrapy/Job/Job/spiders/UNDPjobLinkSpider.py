# -*- coding: utf-8 -*-
__author__ = 'liuyang'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('/home/robin/Workspace/pycode/venv/JobSpider/ahu.ailab/')
import scrapy
from scrapy.http import Request
import logging.config
from src.main.python.util.io.FileUtil import FileUtil

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

path = FileUtil().getResoursePath() + "/links/UNDPjobLinks.txt"

class UNDPjobLinkSpider(scrapy.Spider):
    name = "UNDPjoblinks"

    def __init__(self):
       self.preurl = "https://jobs.undp.org/"

    def start_requests(self):
        # URL容器
        urls = []
        urls.append("https://jobs.undp.org/cj_view_jobs.cfm")
        for everurl in urls:
            yield Request(url=everurl, callback=self.jobParse)

    # 解析函数
    def jobParse(self, response):
        if response.url == "https://jobs.undp.org/cj_view_jobs.cfm":
            self.UNDP(response)

    def UNDP(self,response):
        '''
        解析联合国开发计划蜀
        '''
        f = open(path, 'w')
        selector = scrapy.Selector(response)
        logger.debug("开始解析UNDP(联合国开发计划蜀)的连接信息")
        table = selector.xpath('//div[@id="content-main"]/table[@class="table-sortable"]')
        for evertable in table:
            tbody = evertable.xpath('tr')
            for everlink in tbody[:-1]:
                #提取具体岗位连接
                link = everlink.xpath('td[1]/a/@href').extract()

                #提取岗位描述信息
                describe = everlink.xpath('td[1]/a/text()').extract()
                DESERIBE = describe[0] if len(describe) else ""

                #提取所属系统(第二列)
                suoshu = everlink.xpath('td[2]/text()').extract()
                SUOSHU = suoshu[0] if len(suoshu) else ""

                #提取岗位名称
                work = everlink.xpath('td[3]/text()').extract()
                WORK = work[0].strip() if len(work) else ""

                #提取岗位申请时间
                applytime = everlink.xpath('td[4]/text()').extract()
                APPLYTIME = applytime[1] if len(applytime) else ""

                #提取岗位联系人
                linkman = everlink.xpath('td[5]/text()').extract()
                LINKMAN = linkman[0] if len(linkman) else ""

                if len(link):
                    if link[0].startswith('c'):
                        URL = self.preurl + link[0]
                        f.write('\t'.join([URL,DESERIBE,SUOSHU,WORK,APPLYTIME,LINKMAN]))
                        f.write('\n')
                    else:
                        f.writelines('\t'.join([link[0], DESERIBE, SUOSHU, WORK, APPLYTIME, LINKMAN]))
                        f.write('\n')
                else:
                    pass
        logger.debug("保存UNDP岗位连接成功")
        f.close()