#!/usr/bin/env python
#_*_ coding:utf-8 _*_

###########redis database connect
REDIS_SERVER="127.0.0.1"
REDIS_PORT=6379

###########init info
INIT_STATE={ 
            "money":1000,
            "score":0,
            "process":0,
            "hp_now":10,
            "hp_limit":10,
            }

START_STR = '''hello this is my toy.
start game input 1
if you need help，
input ? or help'''

HELP_STR = '''这是一款文字冒险游戏
'''

DEAD_STR = '''you are dead
restart game input 1
if you need help，
input ? or help'''

#############game process info

START_GAME='''开始游戏了，你扮演的是初出茅庐的少侠胡二虎。
你来到了新手村桃花镇，你有{money}块钱。现在你的选择是：
1.去客栈休息
2.去商店
3.去打狗
c.查看状态'''

ROLE_STATE='''你是少侠胡二虎
HP:{hp_now}/{hp_limit}
money:{money}
道具:{items}
'''


###初始阶段住宿
STAY_HOTEL='''你在客栈花了100块睡了一晚，觉的很舒服。
体力恢复到了满状态。你走出了客栈，现在你的选择：
1.再去客栈休息一晚
2.去商店
3.去打狗
c.查看状态'''

NOMONEY_STAY_HOTEL='''你想在客栈睡一晚，但是没有足够的钱。
你被客栈赶了出来，现在你的选择：
1.再去客栈休息一晚
2.去商店
3.去打狗
c.查看状态'''
###

###初始阶段买东西
SHOP_BEGIN='''你来到了商店，看到琳琅满目的商品，
准备买东西了，现在你的选择是：
1.木剑 200
2.铁剑 500
0.退出商店
c.查看状态'''

SHOP_BEGIN_NOMONEY='''你没有足够的钱买东西，现在你的选择是：
1.木剑 200
2.铁剑 500
0.退出商店
c.查看状态'''

SHOP_BEGIN_BUYOK='''你买好了东西，你还有{money}块
现在你的选择是：
1.木剑 200
2.铁剑 500
0.退出商店
c.查看状态'''

OUT_SHOP='''你走出了商店，现在你的选择是：
1.去客栈休息
2.去商店
3.去打狗
c.查看状态'''
###





BUY_WEAPON='''you buy a weapon,go on
HP:{hp}
money:{money}
score:{score}'''

HIT_DOG='''you hit a dog,go on'''