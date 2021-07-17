import math
import time
import random

def generateId():
    # Return XV + n  len(n)=22  total_len=24
    return "XV"+str(int(math.floor(time.time()*1000000000000)+random.randint(0,1000000000))%10000000000000000000000)