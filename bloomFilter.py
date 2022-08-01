import ctypes
import math
import pickle
import os

class BloomFilter():
    def __init__(self, n:int, p:float, name) -> None:
        '''
        n 数据规模
        p 误判率
        '''
        self.path = "./data"
        self.serializationFileName = self.path + "/BloomFilter-" + name + "-" + str(n) + "-" + str(p) + ".bf"
        self.bitSize = int(-n * math.log(p) / math.pow(math.log(2), 2))
        self.hashFuncSize = int(self.bitSize * math.log(2) / n)
        self.noChange = True
        self.cached = False
        if os.path.exists(self.serializationFileName):
            with open(self.serializationFileName, "rb") as f:
                self.bitArray = pickle.load(f)
                self.cached = True
                print("------init bloomfilter from file--------")
        else:
            print("----------init bloomfilter-------------")
            self.bitArray = [0] * (int((self.bitSize + 32 - 1) / 32))
            print("----------create bloomfilter done------------")
    
    def __del__(self):
        if not self.noChange:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            with open(self.serializationFileName, "wb") as f:
                pickle.dump(self.bitArray, f)
                print("--------save bloomfilter to file----------")


    def put(self, value):
        self.valueCheck(value)
        hash1 = value.__hash__()
        hash2 = self.unsigned_right_shift(hash1, 16)
        for i in range(self.hashFuncSize):
            combineHash = hash1 + i * hash2
            if combineHash < 0:
                combineHash = ~combineHash
            combineHash = combineHash % self.bitSize
            index = int(combineHash / 32)
            position = combineHash - index * 32
            self.bitArray[index] = self.bitArray[index] | (1 << position)
        self.noChange = False

    def fileCached(self) -> bool:
        return self.cached

    def contains(self, value) -> bool:
        self.valueCheck(value)
        hash1 = value.__hash__()
        hash2 = self.unsigned_right_shift(hash1, 16)
        for i in range(self.hashFuncSize):
            combineHash = hash1 + i * hash2
            if combineHash < 0:
                combineHash = ~combineHash
            combineHash = combineHash % self.bitSize
            index = int(combineHash / 32)
            position = combineHash - index * 32
            result = self.bitArray[index] & (1 << position)
            if result == 0:
                return False
        return True

    def valueCheck(self, value):
        if value != 0 and not value:
            print("value cant\'t be None")
    
    def int_overflow(sefl, value):
        maxint = 2147483647
        if not -maxint - 1 <= value <=maxint:
            value = (value + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
        return value

    def unsigned_right_shift(self, n, i):
        if n < 0:
            n = ctypes.c_uint32(n).value
        if i < 0:
            return -self.int_overflow(n << abs(i))
        
        return self.int_overflow(n >> i)



if __name__ == '__main__':
    n = 100000000
    p = 0.01
    bf = BloomFilter(n, p)
    total_size = 1000000
    error_count = 0


    for i in range(total_size):
        bf.put(i)

    for i in range(total_size):
        if not bf.contains(i):
            error_count += 1
    
    print("error rate: ", float(error_count / total_size) if error_count > 0 else 0)