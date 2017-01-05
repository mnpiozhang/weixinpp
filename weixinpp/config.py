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
            "place":0,
            "hp_now":10,
            "hp_limit":10,
            }

START_STR = '''hello这是一款文字类的冒险游戏<<打狗传>>
是我闲的蛋疼基于微信公众号后端开发的
游戏流程通过选择去打狗来开展
主人公HP小于等于0时，游戏结束
游戏过程中可以选择c来查看状态
start game input 1
if you need help，
input ? or help'''

HELP_STR = '''hello,this is my toy
游戏名称，<<打狗传>>
主人公，胡二虎
主人公HP小于等于0时，游戏结束
通过去客栈休息来恢复体力
去商店购买道具
去打狗开展游戏流程
游戏过程中可以选择c来查看状态
游戏过程中可以选择r来查看武林天梯
游戏过程中可以输入?或help来查看此帮助信息
'''

DEAD_STR = '''你由于失血过多快跪了，你从包里取出绝世神功使出了保命绝技。小命虽然保住了但是你功力全失，只能黯然退隐江湖。
restart game input 1
if you need help，
input ? or help'''

FORCE_RANK = {
              "胡二虎":10,
              "成昆":50,
              "张三丰":500,
              "楚留香":260,
              "张起灵":160,
              "胡一刀":200,
              "石达开":120,
              "宁不凡":499,
              "赛特":450,
              "宇文拓":460,
              }

#############game process info

START_GAME='''开始游戏了，你扮演的是初出茅庐的少侠胡二虎。
你来到了新手村桃花镇，你有{money}块钱。现在你的选择是：
1.去客栈休息
2.去商店
3.去打狗
c.查看状态
r.武林天梯'''

ROLE_STATE='''你是少侠胡二虎
HP:{hp_now}/{hp_limit}
money:{money}
功力值:{force}
道具:{items}
'''


###初始阶段住宿和回城
STAY_HOTEL='''你在客栈花了100块睡了一晚，觉的很舒服。
体力恢复到了满状态。你走出了客栈，现在你的选择：
1.再去客栈休息一晚
2.去商店
3.去打狗
c.查看状态
r.武林天梯'''

NOMONEY_STAY_HOTEL='''你想在客栈睡一晚，但是没有足够的钱。
你被客栈小二赶了出来，现在你的选择：
1.再去客栈休息一晚
2.去商店
3.去打狗
c.查看状态
r.武林天梯'''

COMEBACK_BEGIN='''你回到了村庄，你的选择是：
1.去客栈休息
2.去商店
3.去打狗
c.查看状态
r.武林天梯'''
###

###初始阶段买东西
SHOP_BEGIN='''你来到了商店，看到琳琅满目的商品，
准备买东西了，现在你的选择是：
1.木剑 200
2.铁剑 500
0.退出商店
c.查看状态
r.武林天梯'''

SHOP_BEGIN_NOMONEY='''你没有足够的钱买东西，现在你的选择是：
1.木剑 200
2.铁剑 500
0.退出商店
c.查看状态
r.武林天梯'''

SHOP_BEGIN_BUYOK='''你买好了东西，你还有{money}块
现在你的选择是：
1.木剑 200
2.铁剑 500
0.退出商店
c.查看状态
r.武林天梯'''

OUT_SHOP='''你走出了商店，现在你的选择是：
1.去客栈休息
2.去商店
3.去打狗
c.查看状态
r.武林天梯'''
###





BUY_WEAPON='''you buy a weapon,go on
HP:{hp}
money:{money}
score:{score}'''

HIT_DOG='''you hit a dog,go on'''