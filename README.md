weixinpp
===========
基于微信公众号开发的文字游戏（还没做完= =）。我取名叫<<打狗传>>，后台是用的flask和redis。

试试看
===========
<<打狗传>>的微信公众号为 "在家随便玩一玩".关注即可试玩

说明
===========
* 通过微信公众号后台来调用该接口应用。实现文字信息的交互。
* 通过随机触发某些事件来推动游戏。
* 后台应用端口用的是flask默认5000端口，url为"/weixin"
* 使用redis存储数据，需要事先部署redis，默认连本机的6379端口

依赖
===========

    pip install flask
    pip install redis
    
启动 
===========
直接启动

    nohup python -u hello.py &

考究点可以前面加上nginx做反向代理和gunicorn
