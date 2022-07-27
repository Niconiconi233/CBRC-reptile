import pymongo
import logging

class MongoClient:
    def __init__(self, place):
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client["CBRC"]
        self.colPlace = "CBRC-DATA-" + place 
        self.col = self.db[self.colPlace]
    
    def insertOne(self, oneData):
        x = self.col.insert_one(oneData)
        return x
    
    def insertMany(self, datas):
        x = self.col.insert_many(datas)
        return x

    def getColCount(self):
        return self.col.count()

    def findAndInsert(self, data):
        query = {"docId": data["docId"]}
        doc = self.col.find(query)
        if doc.count() > 0:
            logging.info("-------数据存在 skip---------")
        else:
            self.col.insert_one(data)

    def getOne(self, query):
        self.col.find(query)
        return self.col.find(query)

    def getAll(self):
        doc = self.col.find(None)
        return doc