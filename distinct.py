'''数据库去重'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

DATABASE = MongoClient('mongodb://127.0.0.1:27017/', connect=False)
AVIDLIST = DATABASE['bilibili-data']['SubmitVideos']

for aid in open('videoaid.csv', 'r'):
    aid = int(aid.strip('\n').strip('\r'))
    while AVIDLIST.find({"aid": aid}).count() > 1:
        print('found', aid)
        AVIDLIST.delete_one({"aid": aid})
