import json
import math
import queue
import logging
from threadpool import MyThreadPool
from crawler import Crawler
from mongo import MongoClient
from config import LIST_URL, PAGE_URL

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
    mongo = MongoClient("beijing")
    for i in data:
        for j in i["data"]["rows"]:
            mongo.findAndInsert(j)
    logging.info("------------updated to mongo-------------")

#大批量数据更新
def saveToMongo(data):
    mongo = MongoClient("beijing")
    for i in data:
        mongo.insertMany(i["data"]["rows"])
    logging.info("------------save to mongo-------------")


#判断本地数据是否等于远端数据，相符跳过，否则更新
def judgeToDownload():
    global count
    mongo = MongoClient("beijing")
    dbcount = mongo.getColCount()
    count = Crawler(LIST_URL["beijing"]).getPageCount()
    if dbcount == count:
        logging.info("本地数据与远端数据一致，跳过")
    else:
        logging.info("dbcount" + str(dbcount) + "pageCount:" + str(count))
        count = count - dbcount
        calc()
        t = MyThreadPool(cpuCount, task, cpuCount)
        t.starts(func)
        r = t.getResult()

        res_array = r[0][0]
        for i in range(1, len(r)):
            res_array.extend(r[i][0])

        if dbcount == 0:
            saveToMongo(res_array)
        else:
            updateToMongo(res_array)

def func(tuple):
    c = Crawler(LIST_URL["beijing"])
    return c.downloadByRange(tuple[0], tuple[1])

def funcc(index):
    c = Crawler(PAGE_URL)
    return c.downloadByIndex(index)


def getListInfo():
    m = MongoClient("beijing")
    a = m.getAll()
    return a


def downloadAndSaveInfo():
    indexs = getListInfo()
    piceCount = math.ceil(indexs.count() / cpuCount)
    indexs = [doc for doc in indexs]
    start = 0
    end = piceCount - 1
    for i in range(1, cpuCount + 1):
        if i != 1 and start > end:
            break
        if end > len(indexs):
            end = len(indexs)
        task.put(indexs[start:end])
        start = end
        end = end + piceCount
    
    t = MyThreadPool(cpuCount, task, cpuCount)
    t.starts(funcc)
    r = t.getResult()

    res_array = r[0][0]
    for i in range(1, len(r)):
        res_array.extend(r[i][0])

    a = json.loads(res_array[0])
    print("1")


    



def main():
    judgeToDownload()
#    downloadAndSaveInfo()





if __name__ == '__main__':
    main()
