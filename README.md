weixinpp
===========
基于微信公众号开发的文字游戏（还没做完= =）。我取名叫<<打狗传>>，后台是用的flask和redis。

说明
===========
* 需要先申请个微信公众号来调用该接口应用。
* 后台应用端口用的是flask默认5000端口，url为"/weixin"
* 使用redis存储数据，需要事先部署redis，默认连本机的6379端口

试试看
===========
<<打狗传>>的微信公众号为 "在家随便玩一玩" 

依赖
===========

    pip install flask
    pip install redis
    
启动 
===========
直接启动

    nohup python -u hello.py &

考究点可以前面加上nginx做反向代理和gunicorn
