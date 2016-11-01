bilibili-data
===
哔哩哔哩弹幕网数据爬虫
---

基于Python3，使用了gevent进行携程，需要以下库支持:  
> sudo -H pip install BeautifulSoup4 requests gevent pymongo  

默认使用了SQLite存储数据，你也可以用mongodb，将代码中的WriteData替换为MongoData即可

BeautifulSoup 用了 lxml 来解析网页，你可能需要安装 lxml 库：  
> sudo -H pip install lxml  

但是 pip 安装 lxml 速度奇慢而且很可能报错，如果你是 Ubuntu 或者 Debian，推荐：  
> sudo apt-get install python-lxml

如果你是 Windows 用户，请去 [这里](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml) 下载对应版本的whl来安装

使用方法
---

> python Avid.py

That's all.

P.S.
---
目前抓取的数据为：

| 视频AV号 | 视频标题 | UP主mid | UP主昵称 | 投稿时间 | 投稿分区 | 视频封面图(缩略图) | 稿件状态 |
 ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| INT | CHAR | INT | CHAR | CHAR | CHAR | CHAR | INT |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | 200（正常稿件） |
| ----- | 跳转地址 | 0 | bilibili | NULL | NULL | NULL | 301（撞车跳转） |
| ----- | 不能访问 | 0 | bilibili | NULL | NULL | NULL | 404（不能访问） |
| ----- | 页面不存在 | 0 | bilibili | NULL | NULL | NULL | 404（不能访问） |

* 锁定稿件、删除稿件、会员稿件的状态都是404，之后会考虑识别会员状态。
* 「页面不存在」可能是因为稿件尚在审核中。
* 用户投稿数可通过目前数据倒推，其他数据目前没有计划。
* 因为没有使用API，理论上不会被限制？暴力抓取被封IP请自行负责。
* 目前的数据量是1.15GB，不会有网盘下载的，放弃吧。