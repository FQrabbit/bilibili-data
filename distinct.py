'''数据库去重'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from pymongo import MongoClient

DATABASE = MongoClient('mongodb://127.0.0.1:27017/', connect=False)
TAGLIST = DATABASE['bilibili-data']['TagData']


def check(tid):
    '''去重'''
    if TAGLIST.find({"tag_id": tid}).count() > 1:
        TAGLIST.delete_one({"tag_id": tid})


if __name__ == '__main__':
    MULTIPOOL = ThreadPool(16)
    for i in range(1, 1773900):
        MULTIPOOL.apply_async(check, (i,))
    MULTIPOOL.close()
    MULTIPOOL.join()
