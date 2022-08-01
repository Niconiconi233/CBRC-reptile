import pymongo
import logging
from bloomFilter import  BloomFilter

class MongoClient:
    def __init__(self, place):
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client["CBRC"]
        self.colPlace = "CBRC-DATA-" + place 
        self.col = self.db[self.colPlace]
        self.bloomFilter = BloomFilter(1000000, 0.01, self.colPlace)
    
    def insertOne(self, oneData):
        x = self.col.insert_one(oneData)
        self.bloomFilter.put(oneData["docId"])
        return x
    
    def insertMany(self, datas):
        x = self.col.insert_many(datas)
        for i in datas:
            self.bloomFilter.put(i["docId"])
        return x

    def getColCount(self):
        return self.col.count()

    def findAndInsert(self, data):
        self.__createFilter()
        if self.bloomFilter.contains(data["docId"]):
            logging.info("-------数据存在 skip---------")
        else:
            self.col.insert_one(data)
            self.bloomFilter.put(data["docId"])

    def getOne(self, query):
        self.col.find(query)
        return self.col.find(query)

    def getAll(self):
        doc = self.col.find(None)
        return doc


    def __createFilter(self):
        if not self.bloomFilter.fileCached():
            logging.info("-------init mongo filter-----------")
            cols = self.getAll()
            cols = [doc for doc in cols]
            for i in cols:
                self.bloomFilter.put(cols["docId"])
            logging.info("---------mongo filter created---------")


