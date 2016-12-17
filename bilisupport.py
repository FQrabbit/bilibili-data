'''API列表'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

DATABASE = MongoClient('mongodb://127.0.0.1:27017/', connect=False)
AVIDLIST = DATABASE['bilibili-data']['SubmitVideos']
DANMAKULIST = DATABASE['bilibili-data']['DanmakuData']
REPLYLIST = DATABASE['bilibili-data']['CommentData']
ACCOUNTLIST = DATABASE['bilibili-data']['SpaceInfo']
ERRORLIST = DATABASE['bilibili-data']['Errorlist']

# APPKEY = '12737ff7776f1ade'
APPKEY = '8e9fc618fbd41e28'

# CID_DANMAKU.format(cid)
CID_DANMAKU = 'http://comment.bilibili.com/{0}.xml'
# {'aid': aid}
API_PAGELIST = 'http://www.bilibili.com/widget/getPageList?'
# {'mid': mid, 'pagesize': pagesize, 'tid': tid, 'page': page}
API_SUBMITVIDEOS = 'http://space.bilibili.com/ajax/member/getSubmitVideos?'
# {'type': 'json', 'appkey': APPKEY, 'id': aid} & cookies needed
API_VIDEOSTATUS = 'http://api.bilibili.com/view?'
# {'mid': mid} {'Referer': 'http://space.bilibili.com/{mid}/'}
API_SPACE = 'http://space.bilibili.com/ajax/member/GetInfo'

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
