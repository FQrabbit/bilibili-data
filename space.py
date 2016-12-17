'''用户空间信息爬虫'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import ACCOUNTLIST, ERRORLIST, API_SPACE
import requests


def getspaceinfo(headers, form):
    '''json解码完写数据'''
    try:
        jsondata = requests.post(url=API_SPACE, headers=headers, data=form)
    except TimeoutError:
        ERRORLIST.insert(form)
    data = jsondata.json().get('data')
    ACCOUNTLIST.update(form, {'$set': data}, upsert=True)


if __name__ == '__main__':
    MULTIPOOL = ThreadPool(2)
    for mid in range(1, 60631040):
        spaceurl = 'http://space.bilibili.com/{mid}/'.format(mid=mid)
        postheaders = {'Referer': spaceurl}
        postdata = {'mid':"{0}".format(mid)}
        print(mid)
        MULTIPOOL.apply_async(getspaceinfo, (postheaders, postdata, ))
    MULTIPOOL.close()
    MULTIPOOL.join()
