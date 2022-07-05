from crawler import Crawler
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count


count = 0
page = 0
cpuCount = 0
result = []

def calc():
    global count
    global page
    global cpuCount
    count = Crawler().getPageCount()
    page = math.ceil(count / 18)
    cpuCount = int(cpu_count() / 2)


def crawlerfunc():
    calc()
    s = 0
    e = 0
    with ThreadPoolExecutor(max_workers=cpuCount) as executor:
        task_list = []
        for i in range(1, cpuCount + 1):
            s = e + 1
            e = i * 8
            # 修正最后一个任务
            if i == cpuCount:
                e = page
            c = Crawler(start = i,end = i*8)
            job = executor.submit(c.starts)
            task_list.append(job)
        
        for future in as_completed(task_list):
            result.append(future.result)



def main():
    crawlerfunc()
    print(len(result))



if __name__ == '__main__':
    main()


