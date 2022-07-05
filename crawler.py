import requests
import json
import logging
import time
from config import HEADER, URL


class Crawler:
    def __init__(self, start = 1, end = 1, place = "yunnan"):
        self.start = start
        self.end = end
        self.header = HEADER
        self.url = URL[place]
        self.array = []
        self.count = 0

    def starts(self):
        self.__preStart()
        for i in range(self.start, self.end):
            self.array.append(self.__download(i))
        self.__postStart()
        return self.array

    def __preStart(self):
        self.count = self.__getPageCount()
        logging.info("---------start----------")

    def __postStart(self):
        totalCount = (self.end - self.start)
        if len(self.array) == totalCount:
            logging.info("--------------end-------------")
        else:
            logging.warning("----------warn----------")
            logging.warning("total count:" + str(totalCount) + " but download count:" + str(len(self.array)))

    def __getPageCount(self):
        obj = self.__download(1)
        if obj is not None:
            logging.info(obj["data"]["total"])
        else:
            logging.error("error to get count")

    def __download(self, page):
        url = self.url.format(page)
        html = requests.get(url, self.header)
        if html.status_code == 200:
            jsonObj = json.loads(html.content)
            return jsonObj
        else:
            logging.error(html.status_code)


