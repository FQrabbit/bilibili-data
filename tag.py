'''遍历tag'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import TAGLIST, ERRORLIST, API_TAGINFO
import requests


def taginfo(tid):
    '''获取tag信息'''
    if not tid:
        return 404
    tid = int(tid)
    tagparams = {
        'id': tid,
        'jsonp': 'jsonp'
    }
    info = requests.get(url=API_TAGINFO, params=tagparams).json()
    if info.get('code') == 0:
        print(info.get('result'))
        TAGLIST.update({'tag_id': tid}, {'$set': info.get('result')}, upsert=True)
    else:
        ERRORLIST.insert_one({'tag_id': tid})


if __name__ == '__main__':
    # taginfo(2053)
    MULTIPOOL = ThreadPool(16)
    for i in range(1, 1773900):
        MULTIPOOL.apply_async(taginfo, (i,))
    MULTIPOOL.close()
    MULTIPOOL.join()
