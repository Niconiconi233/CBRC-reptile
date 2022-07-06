from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
import math
import queue


class MyThreadPool:
    def __init__(self, taskCount, taskList, workerCount=cpu_count()):
        self.taskCount = taskCount
        self.workerCount = workerCount
        self.loopCount = int(math.ceil(self.taskCount / self.workerCount))
        self.taskList = taskList
        self.res = []


    def __runner(self, func):
        resList = []
        while not self.taskList.empty():
            res = func(self.taskList.get())
            resList.append(res)
        return resList


    def starts(self, func):
        with ThreadPoolExecutor(max_workers=self.workerCount) as executor:
            task_list = []
            for i in range(self.workerCount):
                job = executor.submit(self.__runner, func)
                print(job)
                task_list.append(job)

            for future in as_completed(task_list):
                if future.result():
                    self.res.append(future.result())

    def getResult(self):
        return self.res
