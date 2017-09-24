# -*- coding:utf-8 -*-

__author__ = 'LiuYang'
import json
import logging.config
from src.main.python.service.api.job.sendreq import SendReq
from src.main.python.util.io.FileUtil import FileUtil
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger("ahu")

class WHOjobLinkSpider(object):
    def __init__(self):
        self.path = FileUtil().getResoursePath() + "/links/WHOjobLinks.txt"
        self.url = 'https://tl-ex.vcdp.who.int/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233'
        self.headers = {
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "Content-Length":"946",
            "Content-Type":"application/json",
            "Cookie":"locale=en",
            "Host":"tl-ex.vcdp.who.int",
            "Origin":"https://tl-ex.vcdp.who.int",
            "Referer":"https://tl-ex.vcdp.who.int/careersection/ex/jobsearch.ftl",
            "tz":"GMT+08:00",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }
        self.data = json.loads('{"multilineEnabled":true,"sortingSelection":\
        {"sortBySelectionParam":"3","ascendingSortingOrder":"false"},\
        "fieldData":{"fields":{"KEYWORD":"","LOCATION":""},\
        "valid":true},"filterSelectionParam":{"searchFilterSelections":[{"id":"POSTING_DATE","selectedValues":[]},\
        {"id":"LOCATION","selectedValues":[]},\
        {"id":"JOB_FIELD","selectedValues":[]},\
        {"id":"JOB_TYPE","selectedValues":[]},\
        {"id":"JOB_SCHEDULE","selectedValues":[]},\
        {"id":"JOB_LEVEL","selectedValues":[]},\
        {"id":"EMPLOYEE_STATUS","selectedValues":[]}]},\
        "advancedSearchFiltersSelectionParam":{"searchFilterSelections":[{"id":"ORGANIZATION","selectedValues":[]},\
        {"id":"LOCATION","selectedValues":[]},\
        {"id":"JOB_FIELD","selectedValues":[]},\
        {"id":"JOB_NUMBER","selectedValues":[]},\
        {"id":"URGENT_JOB","selectedValues":[]},\
        {"id":"EMPLOYEE_STATUS","selectedValues":[]},\
        {"id":"JOB_SCHEDULE","selectedValues":[]},\
        {"id":"JOB_TYPE","selectedValues":[]},\
        {"id":"JOB_LEVEL","selectedValues":[]}]},"pageNo":2}')
        self.sendReq = SendReq(self.url,self.headers)
    def getlinks(self, page_num):
        self.data["pageNo"] = page_num
        self.post_data = json.dumps(self.data)
        response = self.sendReq.post(self.post_data)
        return response

if __name__ == "__main__":
    wHOjobLinkSpider = WHOjobLinkSpider()
    f = open(wHOjobLinkSpider.path, 'w')
    for i in range(1,6,1):
        data = wHOjobLinkSpider.getlinks(i)
        for everydata in data["requisitionList"]:
            work = everydata["column"][0]
            num = everydata["column"][1]
            Location = everydata["column"][2].strip('[').strip(']').strip('"')
            PostLevel = everydata["column"][3]
            ContractualArrangement = everydata["column"][4]
            ClosingDate = everydata["column"][5]
            try:
                f.write('\t'.join([work, num, Location, PostLevel, ContractualArrangement, ClosingDate]))
                f.write('\n')
            except:
                logger.error('\t'.join([work, num, Location, PostLevel, ContractualArrangement, ClosingDate]))
    f.close()