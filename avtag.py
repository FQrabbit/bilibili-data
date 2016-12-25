'''遍历稿件tag'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import TAGLIST, ERRORLIST, API_TAG
import requests


def gettag(aid):
    '''获取稿件tag'''
    if not aid:
        return 404
    aid = int(aid)
    aidparams = {
        'aid': aid,
        'jsonp': 'jsonp'
    }
    info = requests.get(url=API_TAG, params=aidparams).json()
    if info.get('code') == 0:
        tags = [{
            'aid': aid,
            'tag': x.get('tag_id')
            } for x in info.get('data')]
        TAGLIST.insert_many(tags)
        print(aid)
    else:
        ERRORLIST.insert_one(info)


if __name__ == '__main__':
    MULTIPOOL = ThreadPool(8)
    for avid in open('videoaid.csv', 'r'):
        MULTIPOOL.apply_async(gettag, (avid,))
    MULTIPOOL.close()
    MULTIPOOL.join()
