#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import sqlite3
from bs4 import BeautifulSoup
from pymongo import MongoClient
import gevent
from gevent.pool import Pool
from gevent import monkey
monkey.patch_socket()


def MongoData(avid=None, avdata=None):
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client['bilibili']
    collection = db['avlists']
    if not avid:
        return 404
    elif not avdata:
        aid = int(avid)
        avdata = (avid,"NULL",0,"NULL","NULL","NULL","NULL", 0)
    else:
        aid = int(avid)
        avdata = avdata
    aid, title, mid, nick, uptime, region, cover, status = avdata
    post = {"aid" : aid,
            "title" : title,
            "mid" : mid,
            "nick" : nick,
            "uptime" : uptime,
            "region" : region,
            "cover" : cover,
            "status" : status}
    try:
        if collection.find_one({"aid": aid}) is None:
            collection.insert(post)
        else:
            pass
    except:
        return 404


def WriteData(avid=None, avdata=None):
    if not avid:
        return 404
    elif not avdata:
        avid = int(avid)
        avdata = (avid,"NULL",0,"NULL","NULL","NULL","NULL", 0)
    else:
        avid = int(avid)
        avdata = avdata
    try:
        database = sqlite3.connect('AV-database.db')
        curs = database.cursor()
        curs.execute('''CREATE TABLE IF NOT EXISTS avlist 
            (Avid INT PRIMARY KEY, Title CHAR(100), Mid INT, Nick CHAR(20), 
            Uptime CHAR(20), Region CHAR(20), Cover CHAR(200), Status INT)''')
        ins = 'INSERT OR REPLACE INTO avlist VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
        curs.execute(ins, avdata)
        database.commit()
        curs.close()
        database.close()
    except:
        return 404


def GetMaxID():
    url = 'http://www.bilibili.com/newlist.html'
    tmp = requests.get(url=url)
    html = BeautifulSoup(tmp.text, 'lxml')
    maxid = html.select('li[class=l1]')[0].a.attrs['href'].replace('/video/av','').replace('/','')
    return int(maxid)
    

def GetInfo(avid=None):
    if not avid:
        print('No avid found')
        return 404
    else:
        avid = int(avid)
        url = 'http://www.bilibili.com/mobile/video/av{avid}.html'.format(avid=avid)
    response = requests.get(url=url)
    page = BeautifulSoup(response.text, 'lxml')
    try:
        title = page.select('title')[0].string
        # MEMBER ONLY OR LOCKED
        if "不能访问" in title:
            raw = (avid, "不能访问", 0, "bilibili", "NULL", "NULL", "NULL", 404)
            WriteData(avid, raw)
            return 0
        # CAR ACCIDENT
        elif "bilibili - 提示" in title:
            jump = page.select('script')[0].string
            car = re.findall(r"location=\'\/video\/av(\d+)\/\'", jump)[0]
            raw = (avid, "撞车跳转av{avid}".format(avid=car), 0, "bilibili", "NULL", "NULL", "NULL", 301)
            WriteData(avid, raw)
            return 0
        elif "bilibili.tv" in title:
            raw = (avid, "页面不存在", 0, "bilibili", "NULL", "NULL", "NULL", 404)
            WriteData(avid, raw)
            return 0
        else:
            pass
    except TimeoutError:
        print('{avid} ERROR'.format(avid=avid))
        return 404
    try:
        title = page.select('h1[class=video-title]')[0].string
        mid = page.select('a[class=up-detail]')[0].attrs['href'].replace('http://space.bilibili.com/','').replace('#!/video','')
        mid = int(mid)
        nick = page.select('a[class=up-name]')[0].string.replace('UP主: ','')
        uptime = page.select('span[class=up-time]')[0].string
        region = page.select('a[property=v:title]')[-1].string
        cover = page.select('img[id=share_pic]')[0].attrs['src']
        raw = (avid, title, mid, nick, uptime, region, cover, 200)
        printf = "AV{avid:<10} {mid:<10} {uptime:<20} {region:<10} {nick:>20}".format(avid=avid, title=title, mid=mid, nick=nick, uptime=uptime, region=region)
        print(printf)
        WriteData(avid, raw)
    except IndexError:
        #TBD with bangumi
        print('\n')
        return 404


if __name__ == "__main__":
    try:
        database = sqlite3.connect('AV-database.db')
        curs = database.cursor()
        curs.execute('''CREATE TABLE IF NOT EXISTS avlist 
            (Avid INT PRIMARY KEY, Title CHAR(100), Mid INT, Nick CHAR(20), 
            Uptime CHAR(20), Region CHAR(20), Cover CHAR(200), Status INT)''')
        curs.execute('''SELECT MAX(avid) FROM avlist''')
        rows = curs.fetchall()
        minid, = rows[0] if rows[0] != (None,) else (1,)
    except:
        minid = 1
    pool = Pool(5)
    #GetInfo(326)
    for avid in range(minid, GetMaxID()):
        pool.add(gevent.spawn(GetInfo, avid))
    pool.join()
