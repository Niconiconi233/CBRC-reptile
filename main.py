import math
import queue
import logging
from threadpool import MyThreadPool
from crawler import Crawler
from mongo import MongoClient

count = 0
page = 0
cpuCount = 3
task = queue.Queue()


def calc():
    global page
    global task
    if count <= 0:
        logging.warning("------data count <= 0------------")
        exit(-1)
    page = math.ceil(count / 18)
    size = math.ceil(page / cpuCount)
    starts = 1
    ends = size
    for i in range(1, cpuCount + 1):
        if i != 1 and starts >= page:
            break
        #修正
        if i == cpuCount:
            ends = page + 1
        task.put((starts, ends))
        starts = ends
        ends = ends + size

#保存数据到mongo，适用于增量更新
def updateToMongo(data):
    mongo = MongoClient()
    for i in data:
        for j in i["data"]["rows"]:
            mongo.findAndInsert(j)
    logging.info("------------updated to mongo-------------")

#大批量数据更新
def saveToMongo(data):
    mongo = MongoClient()
    for i in data:
        mongo.insertMany(i["data"]["rows"])
    logging.info("------------save to mongo-------------")


#判断本地数据是否等于远端数据，相符跳过，否则更新
def judgeToDownload():
    global count
    mongo = MongoClient()
    dbcount = mongo.getColCount()
    count = Crawler().getPageCount()
    if dbcount == count:
        logging.info("本地数据与远端数据一致，跳过")
    else:
        calc()
        t = MyThreadPool(cpuCount, task, cpuCount)
        t.starts(func)
        r = t.getResult()

        res_array = r[0][0]
        for i in range(1, len(r)):
            res_array.extend(r[i][0])

        #判断是增量还是全量
        if count - dbcount > 18:
            logging.info("---------save to mongo---------")
            saveToMongo(res_array)
        else:
            logging.info("---------update to mongo----------")
            updateToMongo(res_array)


def func(tuple):
    c = Crawler(tuple[0], tuple[1])
    return c.starts()



def main():
    judgeToDownload()





if __name__ == '__main__':
    main()
