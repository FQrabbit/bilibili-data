'''用户空间信息爬虫'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

import multiprocessing

import requests
from pymongo import MongoClient

DATABASE = MongoClient('mongodb://127.0.0.1:27017/', connect=False)
DATABASE = DATABASE['bilibili-data']['SpaceInfo']
API = 'http://space.bilibili.com/ajax/member/GetInfo'

def writedata(headers, form):
    '''json解码完写数据'''
    jsondata = requests.post(url=API, headers=headers, data=form)
    data = jsondata.json()
    DATABASE.insert(data)
    DATABASE.close()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    POOL = multiprocessing.Pool(processes=2)
    for mid in range(1, 60631040):
        spaceurl = 'http://space.bilibili.com/{mid}/'.format(mid=mid)
        postheaders = {'Referer': spaceurl}
        postdata = {'mid':"{0}".format(mid)}
        print(mid)
        POOL.apply_async(writedata, (postheaders, postdata, ))
    POOL.close()
    POOL.join()
