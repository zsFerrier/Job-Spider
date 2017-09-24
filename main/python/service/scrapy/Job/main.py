# -*- coding: utf-8 -*-

__author__ = 'liuyang'

'''
scrapy爬虫启动文件，负责全部scrapy爬虫的执行
'''

from scrapy import cmdline

class StartScrapySpider(object):

    def __init__(self):
        pass

    def start(self,name):

        '''
        接收爬虫名，依次执行各爬虫
        :param name: 可以是字符串或者列表 
        '''

        if isinstance(name,str):
            cmdline.execute(("scrapy crawl " + name).split())
        else:
            print "ScrapyError：爬虫执行失败"


if __name__ == "__main__":
    startScrapySpider = StartScrapySpider()
    '''
    爬虫名          任务
    UNDPjoblinks    爬取UNDP连接
    UNDPjob         爬取UNDP岗位
    UNDPleaders     爬取UNDP领导人
    
    OECDleaders     爬取OECD领导人
    WIPOleaders     爬取WIPO领导人

    ESCIjobs        爬取escience岗位
    '''
    # startScrapySpider.start("OECDleaders")
    startScrapySpider.start("ESCIjobs -o ESCIjobs.csv")
    # startScrapySpider.start('UNDPleaders')
    # startScrapySpider.start("UNDPjob -o UNDP.csv")


