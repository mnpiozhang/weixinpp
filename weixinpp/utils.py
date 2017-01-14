#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from datetime import  datetime
import hashlib
from decorators import is_hp_empty
from common import bytes2human, redisConnect,itemslist_to_str,role_force,wulin_rank,strip_and_lower
import config as cf
from events import all_events_class
import random
from redis.utils import pipeline



########################################################
#接收用户发送的消息
def resp_content(messageReceive):
    r = redisConnect()
    userkey = "users:%s" %(hashlib.md5(messageReceive.FromUserName).hexdigest())
    inventorykey = "inventory:%s" %(hashlib.md5(messageReceive.FromUserName).hexdigest())
    forcekey = "force:%s" %(hashlib.md5(messageReceive.FromUserName).hexdigest())
    userinputcontent = strip_and_lower(messageReceive.Content)
    if r.exists(userkey):
        return goOnGames(messageReceive,userkey,inventorykey,forcekey,r) 
    else:
        if userinputcontent == "1":
            return startPlay(messageReceive,userkey,inventorykey,forcekey,r)
        elif userinputcontent in ["?","？","help"] :
            return cf.HELP_STR
        else:
            return "hehe,please input 1 or ?"


##############################
#游戏处理逻辑
def startPlay(messageReceive,userkey,inventorykey,forcekey,r):
    '''
    messageReceive-------接收到的微信xml信息
    userkey--------------用户信息key
    inventorykey---------包裹信息key
    marketkey------------能买道具信息key
    r--------------------Redis链接对象
    '''
    attr_dict = cf.INIT_STATE
    pipeline = r.pipeline()
    pipeline.hmset(userkey, attr_dict)
    #r.sadd(inventorykey,"绝世神功")
    pipeline.zadd(inventorykey,"绝世神功",1)
    for k,v in cf.FORCE_RANK.iteritems():
        pipeline.zadd(forcekey,k,v)
    pipeline.execute()
    return cf.START_GAME.format(**attr_dict)
    #return "我还没想好...."

def buySomething(itemname,price,userkey,inventorykey,userInfo,r):
    if  int(userInfo["money"]) - price >= 0:
        pipeline = r.pipeline()
        pipeline.hincrby(userkey,"money",-price)
        pipeline.zincrby(inventorykey,itemname,1)
        pipeline.execute()
        #地点1 商店
        if userInfo["place"] == "1":
            return cf.SHOP_BEGIN_BUYOK.format(**r.hgetall(userkey))
        #地点3 盗墓
        elif userInfo["place"] == "3":
            return cf.DAOMU_BEGIN_BUYOK.format(**r.hgetall(userkey))
    else:
        if userInfo["place"] == "1":
            return cf.SHOP_BEGIN_NOMONEY
        elif userInfo["place"] == "3":
            return cf.DAOMU_BEGIN_NOMONEY

def hitDogEvent(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r):
    eventDict = {}
    for className,eventClass in all_events_class():
        eventDict[className] = eventClass(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r)
    '''
    eventDict = {
            'smalldoghit':events.SmallDogHit(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r),
            'nomaldoghit':events.NomalDogHit(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r),
            'dabaojian':events.DaBaoJian(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r),
            'baigudaoren':events.BaiGuDaoRen(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r),
            'manyswords':events.ManySwords(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r)
            }
    '''
    if userInfo.has_key('baigudaoren'):
        #判断有key叫baigudaoren且value为3时，白骨道人事件已触发并且流程结束。不再出现。
        if userInfo['baigudaoren'] == "4":
            eventDict.pop('BaiGuDaoRen')
    #判断有key叫manyswords，则万剑归宗事件已经结束。不再出现
    elif userInfo.has_key('manyswords'):
        eventDict.pop('ManySwords')
    #判断有key叫fiveair，则五气朝元事件结束。不再出现
    elif userInfo.has_key('fiveair'):
        eventDict.pop('FiveAir')
    #print eventDict
    randomEvent = random.choice(eventDict.keys())
    return eventDict[randomEvent].work()

@is_hp_empty
def goOnGames(messageReceive,userkey,inventorykey,forcekey,r):
    userInfo = r.hgetall(userkey)
    inventoryInfo = r.zrange(inventorykey,0,-1,withscores=True,score_cast_func=intern)
    forceInfo = r.zrevrange(forcekey,0,-1,withscores=True,score_cast_func=intern)
    inputInfo = strip_and_lower(messageReceive.Content)
    #地点为0在新手村
    if userInfo["place"] == "0":
        #选择1 进客栈
        if inputInfo == "1":
            #redis里面取出来的字典的值都变为str了
            if int(userInfo["money"]) -100 >= 0:
                userInfo["money"] = int(userInfo["money"]) -100
                userInfo["hp_now"] = int(userInfo["hp_limit"])
                r.hmset(userkey, userInfo)
                return cf.STAY_HOTEL.format(**userInfo)
            else:
                return cf.NOMONEY_STAY_HOTEL.format(**userInfo)
        #选择2 去商店--初始化的时候
        elif inputInfo == "2":
            userInfo["place"] = 1
            r.hmset(userkey, userInfo)
            return cf.SHOP_BEGIN
        elif inputInfo == "3":
            return hitDogEvent(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r)
        #选择c 看状态
        elif inputInfo == "c":
            #将两个字典合并起来
            return cf.ROLE_STATE.format(**dict({"items":itemslist_to_str(inventoryInfo),"force":role_force(forceInfo)},**userInfo))
        elif inputInfo == "r":
            #将两个字典合并起来
            return wulin_rank(forceInfo)
        elif inputInfo in ["?","？","help"] :
            return cf.HELP_STR
        else:
            return "hehe,请做一个选择"
    #地点1 在商店
    elif userInfo["place"] == "1":
        #选择木剑 价格200
        if inputInfo == "1":
            return buySomething("木剑",200,userkey,inventorykey,userInfo,r)
        #选择铁剑 价格500
        elif inputInfo == "2":
            return buySomething("铁剑",500,userkey,inventorykey,userInfo,r)
        elif inputInfo == "0":
            userInfo["place"] = 0
            r.hmset(userkey, userInfo)
            return cf.OUT_SHOP
        elif inputInfo == "c":
            #将两个字典合并起来
            return cf.ROLE_STATE.format(**dict({"items":itemslist_to_str(inventoryInfo),"force":role_force(forceInfo)},**userInfo))
        elif inputInfo == "r":
            #将两个字典合并起来
            return wulin_rank(forceInfo)
        elif inputInfo in ["?","？","help"] :
            return cf.HELP_STR
        else:
            return "hehe,请做一个选择"
    #地点2 打狗事件结束
    elif userInfo["place"] == "2":
        #选择1确认信息，能进入以下逻辑说明HP大于0,然后地点改为0
        if inputInfo == "1":
            r.hset(userkey,"place",0)
            return cf.COMEBACK_BEGIN
        elif inputInfo in ["?","？","help"] :
            return cf.HELP_STR
        else:
            return "hehe,请做一个选择"
    #地点3 盗墓事件
    elif userInfo["place"] == "3":
        if inputInfo == "1":
            return buySomething("混元功",2000,userkey,inventorykey,userInfo,r)
        elif inputInfo == "2":
            return buySomething("紫气朝阳决",3000,userkey,inventorykey,userInfo,r)
        elif inputInfo == "3":
            return buySomething("橡皮剑",3000,userkey,inventorykey,userInfo,r)
        elif inputInfo == "4":
            return buySomething("塑料剑",5000,userkey,inventorykey,userInfo,r)
        elif inputInfo == "5":
            return buySomething("不可名状的小册子",6666,userkey,inventorykey,userInfo,r)
        elif inputInfo == "0":
            userInfo["place"] = 0
            r.hmset(userkey, userInfo)
            return cf.COMEBACK_BEGIN
        elif inputInfo == "c":
            #将两个字典合并起来
            return cf.ROLE_STATE.format(**dict({"items":itemslist_to_str(inventoryInfo),"force":role_force(forceInfo)},**userInfo))
        else:
            return "hehe,请做一个选择"