# -*- coding: utf-8 -*-

__author__ = 'Robin'

import sys
sys.path.append('/home/robin/Workspace/pycode/venv/JobSpider/ahu.ailab')
from src.main.python.util.io.FileUtil import FileUtil
from src.main.python.dao.jobDao.CsvCao import SaveToCsv
from src.main.python.util.common.strUtil import StrUtil
from selenium import webdriver
from scrapy.http import HtmlResponse
import requests
from bs4 import BeautifulSoup
import time
import re
import logging.config
logger = logging.getLogger('ahu')
ITERJobsPath = u"ITER.csv"

class ITERJobSpider():

    def __init__(self):
        # self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver = webdriver.PhantomJS()
        print 'open PhantomJS OK!'

    def crawlJobPage(self):
        JobUrl = 'http://www.iter.org/jobs'
        self.driver.get(JobUrl)
        print 'start crawl'
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        linktag = soup.find('table', class_='table').find_all('a')
        jobslink = []
        for link in linktag:
            jobslink.append(link['href'])
        jobslink = list(set(jobslink))
        # print jobslink
        i = 0
        items = []
        for link in jobslink:
            i += 1
            self.driver.get(link)
            item = self.crawlJobDetailPage(self.driver.page_source, i)
            items.append(item)
            print '爬取岗位%s完成' % item['Main job']
            # print 'title is ' + self.driver.title
        print '共爬取%d个岗位' % i
        saveToCsv = SaveToCsv()
        saveToCsv.saveITERjobs(ITERJobsPath, items)

    def crawlJobDetailPage(self, res, id):
        # file = './%d.html' % id
        # with open(file, 'w') as f:
            # f.write(res.encode('utf-8'))
        soup = BeautifulSoup(res, 'html.parser')
        tr = soup.find('div', id='subform').find('table').find('tbody').find_all('tr')
        # print tr[0].find('td').find('h3').find('span').text
        item = {}
        item['Division'] = ""
        item['Diploma'] = ""
        item['Others'] = ""
        item['Jobtitle'] = tr[0].find('td').find('h3').find('span').text
        trs = tr[1].find('td').find('table').find('tbody').find_all('tr')
        for t in trs:
            try:
                td = t.find_all('td')
                # print td[0].find('span').text
                key = td[0].find('div').find('span').text
                value = td[1].find('span').text
                item[key] = value
            except:
                pass
        
        # for k,v in item.items():
            # print k, ':', v
        return item


    def closeDriver(self):
        self.driver.close()


def main():
    spider = ITERJobSpider()
    spider.crawlJobPage()
    spider.closeDriver()
        
if __name__ == '__main__':
    main()