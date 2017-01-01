'''API列表'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

DATABASE = MongoClient('mongodb://127.0.0.1:27017/', connect=False)
AID2MID = DATABASE['bilibili-data']['AID2MID']
AVIDLIST = DATABASE['bilibili-data']['SubmitVideos']
DANMAKULIST = DATABASE['bilibili-data']['DanmakuData']
REPLYLIST = DATABASE['bilibili-data']['CommentData']
ACCOUNTLIST = DATABASE['bilibili-data']['SpaceInfo']
TAGLIST = DATABASE['bilibili-data']['TagData']
AVTAGLIST = DATABASE['bilibili-data']['AVTagData']
ERRORLIST = DATABASE['bilibili-data']['Errorlist']

# APPKEY = '12737ff7776f1ade'
APPKEY = '8e9fc618fbd41e28'

# CID_DANMAKU.format(cid)
CID_DANMAKU = 'http://comment.bilibili.com/{0}.xml'
# CID_DANMAKU_HIS.format(cid)
CID_DANMAKU_HIS = 'http://comment.bilibili.com/rolldate,{0}'
# CID_HISDANMAKU.format(timestamp, cid)
CID_HISDANMAKU = 'http://comment.bilibili.com/dmroll,{0},{1}'

# {'aid': aid}
API_PAGELIST = 'http://www.bilibili.com/widget/getPageList?'

# {'mid': mid, 'pagesize': pagesize, 'tid': tid, 'page': page}
API_SUBMITVIDEOS = 'http://space.bilibili.com/ajax/member/getSubmitVideos?'

# {'type': 'json', 'appkey': APPKEY, 'id': aid} & cookies needed
API_VIDEOSTATUS = 'http://api.bilibili.com/view?'

# {'mid': mid} {'Referer': 'http://space.bilibili.com/{mid}/'} POST method
API_SPACE = 'http://space.bilibili.com/ajax/member/GetInfo'

# {'jsonp': jsonp, 'type': 1, 'sort': 0, 'oid': oid, 'pn': page, 'nohot': 1}
API_REPLY = 'http://api.bilibili.com/x/v2/reply?'

# {'aid': aid, 'jsonp': 'jsonp'}
API_TAG = 'http://api.bilibili.com/x/tag/archive/tags?'
# {'id': tid, 'jsonp': 'jsonp'}
API_TAGINFO = 'http://api.bilibili.com/tags/info_description?'
# {'aid': aid, 'tag_id': tagid, 'jsonp': 'jsonp'} POST method & cookies needed
API_TAGDEL = 'http://api.bilibili.com/x/tag/archive/del'
# {'aid': aid, 'tag_name': tagname, 'jsonp': 'jsonp'} POST method & cookies needed
API_TAGADD = 'http://api.bilibili.com/x/tag/archive/add'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Cookie': 'SESSDATA=; \
    LIVE_BUVID=; \
    LIVE_BUVID__ckMd5=; \
    DedeUserID=; \
    DedeUserID__ckMd5='
    }

PROXIES = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
