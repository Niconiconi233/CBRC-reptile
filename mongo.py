import pymongo

class MongoClient:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client["CBRC"]
        self.col = self.db["CBRC-DATA"]
    
    def insertOne(self, oneData):
        x = self.db.insert_one(oneData)
        return x
    
    def insertMany(self, datas):
        x = self.db.insert_many(datas)
        return x
        