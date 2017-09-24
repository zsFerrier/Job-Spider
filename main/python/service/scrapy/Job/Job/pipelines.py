# -*- coding: utf-8 -*-
__author__ = 'liuyang'
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
class JobPipeline(object):
    # TODO 初始化Mysql
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host='',
                                            db='',
                                            user='',
                                            passwd='',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=False
                                            )
    def process_item(self, item, spider):
        item.setdefault('englishname', '')
        item.setdefault('chinesename', '')
        item.setdefault('incontinent', '')
        item.setdefault('incountry', '')
        item.setdefault('type', '')
        item.setdefault('url', '')
        item.setdefault('alljoburl', '')
        item.setdefault('joburl', '')
        item.setdefault('describe', '')
        item.setdefault('suoshu', '')
        item.setdefault('work', '')
        item.setdefault('applytime', '')
        item.setdefault('linkman', '')
        item.setdefault('Location', '')
        item.setdefault('ApplicationDeadline', '')
        item.setdefault('TypeofContract', '')
        item.setdefault('PostLevel', '')
        item.setdefault('LanguagesRequired', '')
        item.setdefault('DurationofInitialContract', '')
        item.setdefault('ExpectedDurationofAssignment', '')
        item.setdefault('AdditionalCategory', '')
        query = self.dbpool.runInteraction(self.insertjobs, item)
        return item
    def insertjobs(self, tx, item):
        """
        数据持久化
        """
        try:
            pass
        except:
            pass