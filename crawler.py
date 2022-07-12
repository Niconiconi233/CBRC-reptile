from tkinter.messagebox import NO
import requests
import json
import logging
from config import HEADER, URL, proxies, RETRY
from func import random_sleep


class Crawler:
    def __init__(self, start = 1, end = 1, place = "yunnan"):
        self.start = start
        self.end = end
        self.header = HEADER
        self.url = URL[place]
        self.array = []
        self.errorurl = []
        self.count = 0
        self.retry = 0
        logging.basicConfig(level=logging.INFO)
        if self.start == self.end:
            self.end += 1

    #[start, end)
    def starts(self):
        self.__preStart()
        for i in range(self.start, self.end):
            res = self.__downloadi(i)
            if res != None:
                self.array.append(res)
            random_sleep()
                
        self.__postStart()
        return self.array

    def __trydownloaderror(self):
        urls = self.errorurl
        self.errorurl = []
        for i in urls:
            res = self.__downloadu(i)
            random_sleep(10, 5)
        self.retry += 1


    def __preStart(self):
#        self.count = self.__getPageCount()
        logging.info("---------start----------")

    def __postStart(self):
        totalCount = (self.end - self.start)
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
        html = requests.get(url, self.header, proxies=proxies)
        if html.status_code == 200:
            jsonObj = json.loads(html.content)
            return jsonObj
        else:
            logging.error(html.status_code)
            self.errorurl.append(url)
            return None

    def __downloadu(self, url):
        html = requests.get(url, self.header, proxies=proxies)
        if html.status_code == 200:
            jsonObj = json.loads(html.content)
            return jsonObj
        else:
            logging.error(html.status_code)
            self.errorurl.append(url)
            return None

