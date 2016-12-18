'''用户空间信息爬虫'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from bilisupport import ACCOUNTLIST, API_SPACE, ERRORLIST, HEADERS
import requests


def getspaceinfo(headers, form):
    '''json解码完写数据'''
    try:
        jsondata = requests.post(url=API_SPACE, headers=headers, data=form)
    except TimeoutError:
        ERRORLIST.insert(form)
    if jsondata.status_code != 200:
        ERRORLIST.insert(form)
        print(u"API 返回 403")
        return 0
    data = jsondata.json().get('data')
    if data == "服务器遇到了一些问题":
        print(u"服务器遇到了一些问题")
        ERRORLIST.insert(form)
        return 0
    ACCOUNTLIST.update(form, {'$set': data}, upsert=True)
    print(form)
    return 1


if __name__ == '__main__':
    for mid in range(12977, 60631040):
        spaceurl = 'http://space.bilibili.com/{mid}/'.format(mid=mid)
        HEADERS['Referer'] = spaceurl
        postheaders = {'Referer': spaceurl}
        postdata = {'mid':"{0}".format(mid)}
        if getspaceinfo(HEADERS, postdata):
            pass
        else:
            print(u"屏蔽判定，暂停1分钟")
            time.sleep(61)
            mid -= 1
