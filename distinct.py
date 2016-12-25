'''数据库去重'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from bilisupport import AVIDLIST

for aid in open('videoaid.csv', 'r'):
    aid = int(aid.strip('\n').strip('\r'))
    while AVIDLIST.find({"aid": aid}).count() > 1:
        print('found', aid)
        AVIDLIST.delete_one({"aid": aid})
