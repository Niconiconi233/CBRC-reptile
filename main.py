from crawler import Crawler
import math
import queue
from threadpool import MyThreadPool

count = 0
page = 0
cpuCount = 3


def calc():
    global count
    global page
    count = Crawler().getPageCount()
    page = math.ceil(count / 18)#97

def func(tuple):
    c = Crawler(tuple[0], tuple[1])
    return c.starts()



def main():
    task = queue.Queue()
    task.put((1,3))
    #task.put((33,64))
    #task.put((65,97))
    t = MyThreadPool(cpuCount, task, cpuCount)
    t.starts(func)
    r = t.getResult()


if __name__ == '__main__':
    main()
