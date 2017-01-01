'''遍历用户UID'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import API_SUBMITVIDEOS, AVIDLIST, HEADERS
import requests


def getvideos(uid):
    '''获取用户投稿'''
    params = {
        'mid': uid,
        'pagesize': 30,
        'tid': 0,
        'page': 1
    }
    gsvres = requests.get(url=API_SUBMITVIDEOS, headers=HEADERS, params=params).json()
    if not gsvres['status']:
        return 503
    else:
        while params['page'] <= gsvres['data']['pages']:
            videos = gsvres['data']['vlist']
            AVIDLIST.insert_many(videos)
            params['page'] += 1
            gsvres = requests.get(url=API_SUBMITVIDEOS, headers=HEADERS, params=params).json()


if __name__ == '__main__':
    # getvideos(39147112)
    MULTIPOOL = ThreadPool(8)
    for mid in range(1, 60640000):
        print(mid)
        MULTIPOOL.apply_async(getvideos, (mid,))
    MULTIPOOL.close()
    MULTIPOOL.join()
