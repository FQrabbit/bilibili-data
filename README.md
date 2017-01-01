bilibili-data
===
## 哔哩哔哩弹幕网数据爬虫


基于Python3，需要以下库支持:  
> sudo -H pip install requests pymongo multiprocessing BeautifulSoup4  

默认使用了Mongodb存储数据，SQL是坏文明。

> BeautifulSoup 用了 lxml 来解析网页，你可能需要安装 lxml 库：  
> sudo -H pip install lxml  
但是 pip 安装 lxml 速度奇慢而且很可能报错，如果你是 Ubuntu 或者 Debian，推荐：  
> sudo apt-get install python-lxml

如果你是 Windows 用户，请去 [这里](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml) 下载对应版本的whl来安装

## 脚本分类

| 文件 | 用途 |
 - | - |
| aid2uid.py | AV号与UP主对应关系 |
| alluid.py | 全站UP主投稿遍历 |
| avdesc.py | 全站AV号基础数据补足 |
| avtag.py | 全站AV号TAG数据对应 |
| bilisupport.py | 使用到的API和常量列表 |
| comment.py | 全站视频评论遍历 |
| danmaku.py | 全站视频弹幕遍历 |
| space.py | 全站用户空间信息遍历 |
| tag.py | 全站TAG数据遍历 |

## 稿件数据结构为：

```code
{
    "aid" : AV号,
    "title" : 标题,
    "subtitle" : 备注,
    "typeid" : 分区,
    "description" : 视频简介,
    "created" : 投稿时间,
    "mid" : UP主id,
    "author" : UP主昵称,
    "copyright" : 原创/搬运,
    "pic" : 封面图,
    "length" : 视频时长,
    "play" : 播放数,
    "review" : 弹幕数,
    "coins" : 硬币数,
    "favorites" : 收藏数,
    "comment" : 评论数,
    "video_review" : 评论数
}
```

| aid | title | typeid | mid | author | created | copyright | length |
 - | - | - | - | - | - | - | - |
| INT | CHAR | INT | INT | CHAR | CHAR | CHAR | INT |
| - | - | 24:'MAD·AMV' | - | - | - | Copy | - |
| - | - | 25:'MMD·3D' | - | - | - | Original | - |
| - | - | 47:'短片·手书·配音' | - | - | - | Unknow | - |
| - | - | 27:'综合' | - | - | - | - | - |
| - | - | 33:'连载动画' | - | - | - | - | - |
| - | - | 32:'完结动画' | - | - | - | - | - |
| - | - | 153:'国产动画' | - | - | - | - | - |
| - | - | 51:'番剧资讯' | - | - | - | - | - |
| - | - | 152:'官方延伸' | - | - | - | - | - |
| - | - | 28:'原创音乐' | - | - | - | - | - |
| - | - | 31:'翻唱' | - | - | - | - | - |
| - | - | 30:'VOCALOID·UTAU' | - | - | - | - | - |
| - | - | 59:'演奏' | - | - | - | - | - |
| - | - | 29:'三次元音乐' | - | - | - | - | - |
| - | - | 54:'OP/ED/OST' | - | - | - | - | - |
| - | - | 130:'音乐选集' | - | - | - | - | - |
| - | - | 20:'宅舞' | - | - | - | - | - |
| - | - | 154:'三次元舞蹈' | - | - | - | - | - |
| - | - | 156:'舞蹈教程' | - | - | - | - | - |
| - | - | 17:'单机联机' | - | - | - | - | - |
| - | - | 65:'网游·电竞' | - | - | - | - | - |
| - | - | 136:'音游' | - | - | - | - | - |
| - | - | 19:'Mugen' | - | - | - | - | - |
| - | - | 121:'GMV' | - | - | - | - | - |
| - | - | 37:'纪录片' | - | - | - | - | - |
| - | - | 124:'趣味科普人文' | - | - | - | - | - |
| - | - | 122:'野生技术协会' | - | - | - | - | - |
| - | - | 39:'演讲•公开课' | - | - | - | - | - |
| - | - | 96:'星海' | - | - | - | - | - |
| - | - | 95:'数码' | - | - | - | - | - |
| - | - | 98:'机械' | - | - | - | - | - |
| - | - | 138:'搞笑' | - | - | - | - | - |
| - | - | 21:'日常' | - | - | - | - | - |
| - | - | 76:'美食圈' | - | - | - | - | - |
| - | - | 75:'动物圈' | - | - | - | - | - |
| - | - | 161:'手工' | - | - | - | - | - |
| - | - | 162:'绘画' | - | - | - | - | - |
| - | - | 163:'运动' | - | - | - | - | - |
| - | - | 22:'鬼畜调教' | - | - | - | - | - |
| - | - | 26:'音MAD' | - | - | - | - | - |
| - | - | 126:'人力VOCALOID' | - | - | - | - | - |
| - | - | 127:'教程演示' | - | - | - | - | - |
| - | - | 157:'美妆' | - | - | - | - | - |
| - | - | 158:'服饰' | - | - | - | - | - |
| - | - | 164:'健身' | - | - | - | - | - |
| - | - | 159:'时尚资讯' | - | - | - | - | - |
| - | - | 166:'广告' | - | - | - | - | - |
| - | - | 71:'综艺' | - | - | - | - | - |
| - | - | 137:'明星' | - | - | - | - | - |
| - | - | 131:'Korea相关' | - | - | - | - | - |
| - | - | 82:'电影相关' | - | - | - | - | - |
| - | - | 85:'短片' | - | - | - | - | - |
| - | - | 145:'欧美电影' | - | - | - | - | - |
| - | - | 146:'日本电影' | - | - | - | - | - |
| - | - | 147:'国产电影' | - | - | - | - | - |
| - | - | 83:'其他国家' | - | - | - | - | - |
| - | - | 15:'连载剧集' | - | - | - | - | - |
| - | - | 34:'完结剧集' | - | - | - | - | - |
| - | - | 86:'特摄·布袋' | - | - | - | - | - |
| - | - | 129:'电视剧相关' | - | - | - | - | - |

* 由于分区变动原因实际获取到的 typeid 并不只有上表所列的范围。
* Unknow 状态的稿件随机测试的结果应该是搬运状态，有待确认。

## 评论数据结构为：

```code
{
    "root_str" : "0",
    "content" : {
        "device" : 设备,
        "message" : 评论正文,
        "plat" : 平台,
        "members" : []
    },
    "parent_str" : 评论父楼层,
    "parent" : 评论父楼层,
    "mid" : 用户uid,
    "root" : 0,
    "member" : {
        "uname" : 用户昵称,
        "rank" : "10000",
        "vip" : {……}, vip/大会员相关
        "sign" : 用户签名,
        "sex" : 用户性别,
        "avatar" : 用户头像,
        "DisplayRank" : "0",
        "mid" : 用户uid,
        "level_info" : {
            "current_min" : 1500,
            "current_level" : 现在等级,
            "next_exp" : 距离下一级经验值,
            "current_exp" : 现在经验值
        },
        "nameplate" : {……},
        "pendant" : {……},
        "official_verify" : {……}
    },
    "type" : 1,
    "like" : 点赞数,
    "rpid" : 评论ID,
    "count" : 0,
    "rpid_str" : 评论ID,
    "ctime" : 评论时间,
    "action" : 0,
    "oid" : 评论所属视频,
    "replies" : [],
    "floor" : 评论楼层,
    "rcount" : 0,
    "state" : 0
}
```

| oid | floor | parent | mid | ctime | content.message | plat | rpid |
 - | - | - | - | - | - | - | - |
| INT | INT | INT | INT | INT | CHAR | CHAR | INT |
| - | - | 0: 主楼 | - | - | - | 1: 网页 | - |
| - | - | 9: 楼中楼 | - | - | - | 2: 安卓 | - |
| - | - | - | - | - | - | 3: iOS | - |
| - | - | - | - | - | - | 4: Windows Phone | - |
| - | - | - | - | - | - | 5: 安卓? | - |

* 设备信息具体对应不确定，仅作参考

## 弹幕数据结构为：

```code
{
    "aid" : 视频av号, # 并不包含在弹幕文件中
    "cid" : 视频cid, # 并不包含在弹幕文件中
    "time" : 弹幕时间点,
    "mode" : 弹幕模式，
    "font" : 字号大小,
    "color" : 弹幕颜色,
    "date" : 弹幕发送日期,
    "pool" : 弹幕池,
    "hash" : 用户uid的HASH,
    "id" : 弹幕id,
    "text" : 弹幕内容
}
```

| aid | cid | time | mode | font | color | date | pool | hash | id | text |
 - | - | - | - | - | - | - | - | - | - | - |
| INT | INT | CHAR | INT | INT | CHAR | CHAR | INT | CHAR | INT | CHAR |
| - | - | - | 1~3: 普通弹幕 | - | - | #FFFFFF | - | - | - | - |
| - | - | - | 4: 底部弹幕 | - | - | - | - | - | - | - |
| - | - | - | 5: 顶部弹幕 | - | - | - | - | - | - | - |
| - | - | - | 6: 逆向弹幕 | - | - | - | - | - | - | - |
| - | - | - | 7~8: 高级弹幕 | - | - | - | - | - | - | - |

* 未确认其他类型弹幕的具体对应关系

## 用户空间数据结构为：

```code
{
    "mid" : 用户uid,
    "place" : 地区,
    "playNum" : 投稿播放总数,
    "sex" : 用户性别,
    "coins" : 硬币数,
    "spacesta" : 0,
    "DisplayRank" : "1001",
    "attentions" : [……], 关注列表
    "theme_preview" : "",
    "friend" : 0,
    "official_verify" : {……},
    "toutu" : 空间头图,
    "sign" : 签名,
    "description" : 签名,
    "toutuId" : 1,
    "im9_sign" : 兴趣圈,
    "name" : 用户昵称,
    "level_info" : {……}, 用户等级相关
    "nameplate" : {……}, 勋章相关
    "approve" : false,
    "face" : 用户头像,
    "birthday" : 生日,
    "article" : 0,
    "theme" : 空间使用主题,
    "rank" : "10000",
    "fans" : 粉丝数,
    "pendant" : {……}, 挂件相关
    "attention" : 关注数,
    "regtime" : 注册时间
}
```

| mid | name | sex | regtime | fans | attention | description |
 - | - | - | - | - | - | - |
| INT | CHAR | CHAR | INT | INT | INT | CHAR |
| - | - | - | - | - | - | - |

* description 待确认

## TAG数据结构为：

```code
{
    "tag_id" : 标签id,
    "subscribe_count" : 订阅数,
    "cover" : 封面,
    "name" : 标签名,
    "visit_count" : 访问数,
    "subscribed" : 0
}
```

| tag_id | name | subscribe_count | visit_count | cover | subscribed |
 - | - | - | - | - | - |
| INT | CHAR | INT | INT |CHAR | INT |
| - | - | - | - | - | 0 |

* 未确认subscribed的作用