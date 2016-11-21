#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import json
import time
from time import strftime

import sqlite3
import pymongo
from pymongo import MongoClient

import gevent
from gevent.pool import Pool
from gevent import monkey
monkey.patch_socket()


def MongoData(oid=None, data=None):
    try:
        oid = int(oid)
        if not data:
            return None
    except TypeError:
        return None
    rfloor, floor, mid, ctime, rtime, msg, device, rpid = data
    post = {"Oid" : oid,
            "Floor" : rfloor,
            "Flor" : floor,
            "Mid" : mid,
            "Ctime" : ctime,
            "Rtime" : rtime,
            "Msg" : msg,
            "Device" : device,
            "Rpid": rpid}
    try:
        if collection.find_one({"Rpid": rpid}) is None:
            collection.insert(post)
        else:
            pass
    except pymongo.errors.ServerSelectionTimeoutError:
        print('mongo error')


def WriteData(oid=None, data=None):
    try:
        oid = int(oid)
        if not data:
            return None
    except TypeError:
        return None
    try:
        database = sqlite3.connect('comment.db')
        curs = database.cursor()
        curs.execute('''CREATE TABLE IF NOT EXISTS commentlist 
            (Oid INT, Floor INT, Flor INT, Mid INT, 
            Ctime INT, Rtime CHAR(20), Msg CHAR(1000), Device CHAR(20), Rpid INT PRIMARY KEY)''')
        ins = 'INSERT OR REPLACE INTO commentlist VALUES({oid}, ?, ?, ?, ?, ?, ?, ?, ?)'.format(oid=oid)
        curs.execute(ins, data)
        database.commit()
        curs.close()
        database.close()
    except:
        print('sql error')


def CountPage(oid=None):
    try:
        oid = int(oid)
    except TypeError:
        return None
    url = 'http://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&sort=0&oid={oid}&pn=1&nohot=1'.format(oid=oid)
    temp = requests.get(url=url)
    try:
        response = json.loads(temp.text)
    except json.JSONDecodeError:
        print('jsondecode')
    if response['code'] == -404: # 未知
        return None
    elif response['code'] == 12002: # 锁定稿件/审核中稿件
        return None
    elif response['code'] == 0: # 正常/用户删除稿件
         count = response['data']['page']['count'] 
         size = response['data']['page']['size']
         # 评论页数计算
         pages = count // size if count % size == 0 else count // size + 1
         print(pages)
    else:
        return None
    return pages


def CommentGet(oid=None, pages=None):
    try:
        oid = int(oid)
        pages = int(pages)
    except TypeError:
        print('typeerror')
    for page in range(1, pages+1):
        url = 'http://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&sort=0&oid={oid}&pn={page}&nohot=1'.format(oid=oid, page=page)
        try:
            temp = requests.get(url=url, timeout=300)
        except requests.exceptions.ConnectionError:
            pass
        print(page)
        try:
            response = json.loads(temp.text)
        except json.JSONDecodeError:
            print('jsonerror')
        replies = response['data']['replies']
        for i in range(len(replies)):
            rpid = replies[i]['rpid']
            rfloor = replies[i]['floor']
            floor = 0
            mid = replies[i]['mid']
            ctime = replies[i]['ctime']
            rtime = strftime("%Y-%m-%d %H:%M", time.localtime(ctime))
            msg = replies[i]['content']['message']
            device = replies[i]['content']['plat']
            data = (rfloor, floor, mid, ctime, rtime, msg, device, rpid)
            MongoData(oid, data)
            # 楼中楼
            if replies[i].get('replies') != []:
                inreplies = replies[i]['replies']
                for j in range(len(inreplies)):
                    inrpid = inreplies[j]['rpid']
                    inrfloor = rfloor
                    infloor = inreplies[j]['floor']
                    inmid = inreplies[j]['mid']
                    inctime = inreplies[j]['ctime']
                    inrtime = strftime("%Y-%m-%d %H:%M", time.localtime(ctime))
                    inmsg = inreplies[j]['content']['message']
                    indevice = inreplies[j]['content']['plat']
                    data = (inrfloor, infloor, inmid, inctime, inrtime, inmsg, indevice, inrpid)
                    MongoData(oid, data)


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017/', connect=False)
    db = client['bilibili-data']
    collection = db['comments']
    database = sqlite3.connect('database.db')
    curs = database.cursor()
    curs.execute('''SELECT DISTINCT Avid FROM avlist WHERE Status = 200 ORDER BY Avid''')
    rows = curs.fetchall()
    for row in rows:
        print(row)
        if row != (None,):
            avid, = row
            CommentGet(avid,CountPage(avid))
    #CommentGet(6976624,CountPage(6976624))