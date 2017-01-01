'''AID对应MID'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import API_VIDEOSTATUS, AID2MID, APPKEY, HEADERS
import requests


def getdata(avid):
    '''获取数据'''
    params = {
        'type': 'json',
        'appkey': APPKEY,
        'id': avid
    }
    try:
        rawdata = requests.get(url=API_VIDEOSTATUS, params=params, headers=HEADERS).json()
    except TimeoutError:
        pass
    postdata = {
        'aid': avid,
        'mid': rawdata.get('mid')
    }
    AID2MID.insert(postdata)


if __name__ == '__main__':
    MULTIPOOL = ThreadPool(8)
    for aid in range(1, 7454282):
        if AID2MID.find_one({"aid": aid}) is None:
            print(aid)
            MULTIPOOL.apply_async(getdata, (aid,))
    MULTIPOOL.close()
    MULTIPOOL.join()
