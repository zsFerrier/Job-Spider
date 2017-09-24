# -*- coding: utf-8 -*-
__author__ = 'Liuyang'

from src.main.python.dao.jobDao.CsvCao import SaveToCsv
from src.main.python.util.io.FileUtil import FileUtil
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import logging.config
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')
WHOLinksPath = FileUtil().getResoursePath() + "/links/WHOjobLinks.txt"
WHOJobsPath = u"WHO.csv"

class WHOJobsSpider(object):

    def __init__(self):
        self.preurl = "https://tl-ex.vcdp.who.int/careersection/ex/jobdetail.ftl?job="
        self.ITE = ["Contractduration", "PrimaryLocation", "Organization", "Schedule"]
        self.driver = webdriver.Chrome()

    def start(self):

        items = []
        f = open(WHOLinksPath)
        allUNDPlinks = f.read().split('\n')
        logger.debug("WHO全部待爬岗位：" + str(allUNDPlinks.__len__()))
        # 遍历每个连接进行数据抽取
        for links in allUNDPlinks[:-1]:
            link = links.split('\t')
            item = self.crawljobs(link)
            items.append(item)

        # TODO 保存爬取的数据
            saveToCsv = SaveToCsv()
            saveToCsv.saveWHOjobs(WHOJobsPath,items)

    def crawljobs(self,link):
        '''
        遍历所有的连接进行数据爬取 
        '''
        retrynum = 0
        self.driver.get(self.preurl+link[1])
        time.sleep(3)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)

        # 判断页面是否加载成功
        if "Job" in self.driver.page_source:
            item = self.handlejichuinfo(link,self.driver.page_source)
            return item
        else:
            retrynum += 1
            time.sleep(5)
            if retrynum < 10:
                self.driver.refresh()
                self.crawljobs(link)
            else:
                logger.error("重试10次仍不能正常显示：  " + self.preurl+link[1])

    def handlejichuinfo(self,link,page_sourse):
        '''
        爬取基础信息
        '''
        item = {}
        item["englishname"] = "WHO"
        item["chinesename"] = "世界卫生组织"
        item["incontinent"] = "欧洲"
        item["incountry"] = "瑞士"
        item["type"] = "卫生"
        item["url"] = "http://www.who.int/en/"
        item["alljoburl"] = "https://tl-ex.vcdp.who.int/careersection/ex/jobsearch.ftl#"
        item["joburl"] = self.preurl+link[1]
        item["work"] = link[0]
        item["Location"] = link[2]
        item["PostLevel"] = link[3]
        item["ContractualArrangement"] = link[4]
        item["ClosingDate"] = link[5]

        response = HtmlResponse(url="my HTML string", body=page_sourse, encoding="utf-8")

        # 爬取合同期限
        ContractdurationXpath = '//div[@class="editablesection"]/div[@id="requisitionDescriptionInterface.ID1489.row1"]/' \
                                'span[@id="requisitionDescriptionInterface.ID1522.row1"]/text()'
        Contractduration = response.xpath(ContractdurationXpath).extract()
        item["Contractduration"] = Contractduration[0] if Contractduration else ""

        # 爬取主要地点
        PrimaryLocationXpath  = '//div[@class="editablesection"]/div[@id="requisitionDescriptionInterface.ID1653.row1"]/' \
                                'span[@id="requisitionDescriptionInterface.ID1696.row1"]/text()'
        PrimaryLocation = response.xpath(PrimaryLocationXpath).extract()
        item["PrimaryLocation"] = PrimaryLocation[0] if Contractduration else ""

        # 爬取工作公告
        JobPostingXpath       = '//div[@class="editablesection"]/div[@id="requisitionDescriptionInterface.ID1549.row1"]/' \
                                'span[@id="requisitionDescriptionInterface.reqPostingDate.row1"]/text()'
        JobPosting = response.xpath(JobPostingXpath).extract()
        item["JobPosting"] = JobPosting[0] if JobPosting else ""

        # 爬取所在组织
        OrganizationXpath     = '//div[@class="editablesection"]/div[@id="requisitionDescriptionInterface.ID1753.row1"]/' \
                                'span[@id="requisitionDescriptionInterface.ID1796.row1"]/text()'
        Organization = response.xpath(OrganizationXpath).extract()
        item["Organization"] = Organization[0] if Organization else ""

        # 爬取是否要求全职
        ScheduleXpath         = '//div[@class="editablesection"]/div[@id="requisitionDescriptionInterface.ID1803.row1"]/' \
                                'span[@id="requisitionDescriptionInterface.ID1846.row1"]/text()'
        Schedule = response.xpath(ScheduleXpath).extract()
        item["Schedule"] = Schedule[0] if Schedule else ""
        return item

    def depose(self):
        self.driver.close()

if __name__ == "__main__":

    wHOJobsSpider = WHOJobsSpider()
    wHOJobsSpider.start()
    wHOJobsSpider.depose()