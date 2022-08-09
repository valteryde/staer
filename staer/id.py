
from random import randint
import os


nums = {}
def getid(key:str='') -> str:

    if key not in nums.keys():
        nums[key] = -1

    #token = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(24))
    nums[key] += 1

    return str(nums[key])


def getFilename(path:str or os.PathLike) -> str:
    
    files = [i.split('.')[0] for i in os.listdir(path)]

    filename = getid(path)
    while filename in files:
        filename = getid(path)

    return str(filename)
