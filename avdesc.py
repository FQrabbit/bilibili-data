'''遍历全站AID'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import API_VIDEOSTATUS, HEADERS, APPKEY, AVIDLIST
import requests


def getinfo(aid):
    '''获取aid信息'''
    if not aid:
        return 404
    else:
        aid = int(aid)
    paramsinfo = {'type': 'json', 'appkey': APPKEY, 'id': aid}
    gsvres = requests.get(url=API_VIDEOSTATUS, params=paramsinfo, headers=HEADERS).json()
    if gsvres.get('code') is None:
        postdata = {
            'comment': int(gsvres.get('video_review')),
            'video_review': int(gsvres.get('video_review')),
            'coins': int(gsvres.get('coins')),
            'favorites': int(gsvres.get('favorites'))
        }
        if gsvres.get('play') != "--":
            postdata['play'] = gsvres.get('play')
        AVIDLIST.update({'aid': aid}, {'$set': postdata})
    else:
        print(aid, gsvres.get('code'), gsvres.get('error'))
        return 404


if __name__ == '__main__':
    # getinfo(2053)
    MULTIPOOL = ThreadPool(16)
    for avid in open('videoaid.csv', 'r'):
        MULTIPOOL.apply_async(getinfo, (avid, ))
    MULTIPOOL.close()
    MULTIPOOL.join()
