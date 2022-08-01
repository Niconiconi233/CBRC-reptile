from tkinter.messagebox import NO
import requests
import json
import logging
from config import HEADER, proxies, RETRY
from func import random_sleep


class Crawler:
    def __init__(self, url):
        self.header = HEADER
        self.url = url
        self.array = []
        self.errorurl = []
        self.count = 0
        self.retry = 0
        logging.basicConfig(level=logging.INFO)


    #针对范围下载
    #[start, end)
    def downloadByRange(self, start, end):
        self.__preStart()
        if start == end:
            end += 1
        for i in range(start, end):
            res = self.__downloadi(i)
            if res != None:
                self.array.append(res)
            random_sleep()        
        self.__postStart(start, end)
        return self.array

    #根据docid下载
    def downloadByIndex(self, indexs):
        self.__preStart()
        for i in indexs:
            url = self.url.format(i["docId"])
            res = self.__downloadu(url)
            if res != None:
                self.array.append(res)
                random_sleep()
        return self.array


    def __trydownloaderror(self):
        urls = self.errorurl
        self.errorurl = []
        for i in urls:
            res = self.__downloadu(i)
            random_sleep(10, 5)
        self.retry += 1


    def __preStart(self):
        logging.info("---------start----------")

    def __postStart(self, start, end):
        totalCount = (end - start)
        if len(self.array) == totalCount:
            logging.info("--------------end-------------")
        else:
            while  self.retry < RETRY and len(self.errorurl) > 0:
                logging.warn("------------try download error-----------")
                self.__trydownloaderror()

    def getPageCount(self):
        return self.__getPageCount()

    def __getPageCount(self):
        obj = self.__downloadi(1)
        if obj is not None:
            count = obj["data"]["total"]
            return count
        else:
            logging.error("error to get count")

    def __downloadi(self, page):
        url = self.url.format(page)
        content = self.__download(url)
        if content != None:
            jsonObj = json.loads(content)
            return jsonObj
        else:
            return None

    def __downloadu(self, url):
        content = self.__download(url)
        if content != None:
            jsonObj = json.loads(content)
            return jsonObj
        else:
            return None

    def __download(self, url):
        html = requests.get(url, self.header, proxies=proxies)
        if html.status_code == 200:
            return html.content
        else:
            logging.error(html.status_code)
            self.errorurl.append(url)
            return None
