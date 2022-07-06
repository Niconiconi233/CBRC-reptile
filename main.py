import math
import queue
from threadpool import MyThreadPool
from crawler import Crawler
from mongo import MongoClient

count = 0
page = 0
cpuCount = 2
task = queue.Queue()


def calc():
    global count
    global page
    global task
    count = Crawler().getPageCount()
    page = math.ceil(count / 18)
    size = math.ceil(page / cpuCount)
    starts = 1
    ends = size
    for i in range(1, cpuCount + 1):
        #修正
        if i == cpuCount:
            ends = page
        task.put((starts, ends))
        starts = ends + 1
        ends = ends + size



def func(tuple):
    c = Crawler(tuple[0], tuple[1])
    return c.starts()



def main():
    calc()
    t = MyThreadPool(cpuCount, task, cpuCount)
    t.starts(func)
    r = t.getResult()

    res_array = r[0][0]
    for i in range(1, len(r)):
        res_array.extend(r[i][0])

    mongo = MongoClient()
    mongo.insertMany(res_array)
    print("------------save to mongo-------------")



if __name__ == '__main__':
    main()
