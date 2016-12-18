'''遍历全站评论'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import REPLYLIST, ERRORLIST, API_REPLY
import requests


def getcomment(oid):
    '''获取视频评论内容'''
    oid = int(oid)
    page = 1
    params = {
        'jsonp': 'jsonp',
        'type': 1,
        'sort': 0,
        'oid': oid,
        'pn': page,
        'nohot': 1
    }
    temp = requests.get(url=API_REPLY, params=params).json()
    if temp.get('code') != 0:
        errdict = {
            'oid': oid,
            'code': temp.get('code'),
            'message': temp.get('message')
        }
        ERRORLIST.insert_one(errdict)
        print(oid, temp.get('code'), temp.get('message'))
    else:
        # 循环
        while temp['data'].get('replies'):
            replylst = temp['data'].get('replies')
            REPLYLIST.insert_many(replylst)
            print(oid, params['pn'])
            params['pn'] = temp['data']['page']['num'] + 1
            temp = requests.get(url=API_REPLY, params=params).json()


if __name__ == '__main__':
    MULTIPOOL = ThreadPool(16)
    for avid in open('videoaid2.csv', 'r'):
        MULTIPOOL.apply_async(getcomment, (avid,))
    MULTIPOOL.close()
    MULTIPOOL.join()
