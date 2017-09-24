# -*- coding:utf-8 -*-
__author__ = 'LiuYang'
import logging.config

from src.main.python.util.io.FileUtil import FileUtil
import json,requests
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger("ahu")

class SendReq(object):

    def __init__(self,url,headers):

        self.url = url
        self.headers = headers

    def post(self,post_data):
        '''
        post请求
        :param post_data: 请求参数
        :return: json格式post响应结果
        '''
        response = requests.post(self.url, data=post_data, headers=self.headers)
        return json.loads(response.text)