'''遍历全站弹幕'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import DANMAKULIST, API_PAGELIST, CID_DANMAKU
import requests
from bs4 import BeautifulSoup


def getdanmaku(aid, cid):
    '''通过CID获取弹幕'''
    if not cid:
        return 404
    else:
        aid = int(aid)
        cid = int(cid)
    print(aid, cid)
    link = CID_DANMAKU.format(cid)
    response = requests.get(url=link, timeout=300)
    content = BeautifulSoup(response.text, "xml")
    # <d p="190.56399536133,5,25,15138834,1465868252,0,61dba469,1957402211">弹幕字幕</d>
    danmaku_raw = [x for x in content.select('i')[0].select('d')]
    danmaku_data = [{
        'aid': aid,
        'cid': cid,
        'time': float(x.attrs['p'].split(',')[0]),
        'mode': int(x.attrs['p'].split(',')[1]),
        'font': int(x.attrs['p'].split(',')[2]),
        'color': ("#%06x" % int(x.attrs['p'].split(',')[3], 10)).upper(),
        'date': float(x.attrs['p'].split(',')[4]),
        'pool': int(x.attrs['p'].split(',')[5]),
        'hash': x.attrs['p'].split(',')[6],
        'id': int(x.attrs['p'].split(',')[7]),
        'text': x.string
        } for x in danmaku_raw]
    DANMAKULIST.insert_many(danmaku_data)


if __name__ == '__main__':
    MULTIPOOL = ThreadPool(16)
    for avid in open('videoaid.csv', 'r'): #1096797
        params = {'aid': avid}
        try:
            resp = requests.get(url=API_PAGELIST, params=params, timeout=300)
        except TimeoutError:
            resp = requests.get(url=API_PAGELIST, params=params)
        if resp.status_code == 200:
            pages = resp.json()
            #result = [getdanmaku(avid, page['cid']) for page in pages]
            for page in pages:
                MULTIPOOL.apply_async(getdanmaku, (avid, page['cid']))
    MULTIPOOL.close()
    MULTIPOOL.join()
    #getdanmaku(807478, 1172133)
