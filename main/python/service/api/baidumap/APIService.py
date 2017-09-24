# -*- coding:utf-8 -*-

import logging

from src.main.python.util.http.UniversalSDK import APIClient

logger = logging.getLogger('ugc')


class BaiduMapAPIService(object):
    def __init__(self, ak):

        self.baiduClient = APIClient("http://api.map.baidu.com")
        self.__ak = ak

    def doGeocoding(self, addressText):
        '''
        正向地理编码geocoding
        地址：http://api.map.baidu.com/geocoder/v2/
        类型：get
        '''
        data = self.baiduClient.geocoder.v2.addtrail("/").get(ak=self.__ak, output="json", address=addressText)
        return data