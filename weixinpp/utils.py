#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from datetime import  datetime
import multiprocessing
import os
import platform
import socket
import hashlib
import psutil
from decorators import is_hp_empty
from common import bytes2human, redisConnect
import config as cf
import events
import random
from redis.utils import pipeline

############工具方法or参数###############

#ex[('a',1),('b',2)] ==> aX1 bX2
def itemslist_to_str(inventoryInfo):
    itemsOut=""
    for k,v in inventoryInfo:
        strOut = k + 'X' + str(v)
        itemsOut = itemsOut + " " + strOut
    return itemsOut

def role_force(forceInfo):
    a = dict(forceInfo)
    return a["胡二虎"]

    
def divide_into_paragraphs(data):
    parsedlist = []
    a = ""
    tmplist = data.splitlines(True)
    for i in tmplist:
        if i.strip():
            a = a + i
        else:
            parsedlist.append(a)
            a=""
    parsedlist.append(a)
    return parsedlist

#返回天梯排行的结果
def wulin_rank(forceInfo):
    outStr="武林天梯排名\n"
    a = 1
    for k,v in forceInfo:
        outLine = "第%s:%s 功力:%s\n" %(str(a),k,str(v))
        outStr = outStr + outLine
        a = a + 1
    return outStr

########################################################
#具体处理逻辑
def resp_content(messageReceive):
    r = redisConnect()
    userkey = "users:%s" %(hashlib.md5(messageReceive.FromUserName).hexdigest())
    inventorykey = "inventory:%s" %(hashlib.md5(messageReceive.FromUserName).hexdigest())
    forcekey = "force:%s" %(hashlib.md5(messageReceive.FromUserName).hexdigest())
    if r.exists(userkey):
        return goOnGames(messageReceive,userkey,inventorykey,forcekey,r) 
    else:
        if messageReceive.Content == "1":
            return startPlay(messageReceive,userkey,inventorykey,forcekey,r)
        elif messageReceive.Content == "?" or messageReceive.Content == "？" or  messageReceive.Content == "help":
            return cf.HELP_STR
        else:
            return "hehe,please input 1 or ?"
'''
#######################本来是想搞搞服务器信息查询的 还是算了，专门写个游戏玩玩
def resp_content(messageReceive):
    r = redisConnect()
    userkey = hashlib.md5(messageReceive.FromUserName).hexdigest()
    if r.exists(userkey):
        return goOnGames(messageReceive,userkey,r) 
    else:
        if messageReceive.Content == "1":
            return "hostname: " + socket.gethostname() +"\nos: " + "-".join(platform.dist())
        elif messageReceive.Content == "2":
            return getMem()
        elif messageReceive.Content == "3":
            return getOnlineUser()
        elif messageReceive.Content == "4":
            return getCpu()
        elif messageReceive.Content == "5":
            return startPlay(messageReceive,userkey,r)
        elif messageReceive.Content == "?" or messageReceive.Content == "？" or  messageReceive.Content == "help":
            return cf.HELP_STR
        else:
            return "hehe"
'''    
'''

#服务器基本信息 
def getMem():
    memInfo = psutil.virtual_memory()
    totalMem = memInfo.total
    availableMem = memInfo.available
    resp = "总内存  %s\n可用内存  %s" %(bytes2human(totalMem),bytes2human(availableMem))
    return resp

def getOnlineUser():
    ret = []
    for u in psutil.users():
        ret.append([u.name,
                    u.host,
                    datetime.fromtimestamp(u.started).strftime("%Y%m%d/%H:%M"),
                    ])
    resp = ""
    for i in  ret:
        if i[1] == "":
            i[1] = 'unknown'
        resp = resp + "User:%s From:%s Time:%s\n" %(i[0],i[1],i[2])
    return resp

def getCpu():
    cpuModel =  os.popen("cat /proc/cpuinfo  |grep 'model name' |sort | uniq |awk -F\: '{print $2}' |sed 's/^[ \t]*//g'").read()
    cpuPhysical = os.popen("cat /proc/cpuinfo  |grep 'physical id'|sort|uniq |wc -l").read()
    cpuCore = os.popen("cat /proc/cpuinfo  |grep 'core id'|sort |uniq|wc -l").read()
    cpuProcess = multiprocessing.cpu_count()
    return "型号:" + cpuModel.strip("\n") +"\n物理个数:" + cpuPhysical.strip("\n")+"\ncore个数:" + cpuCore.strip("\n")+"\n线程个数:" + str(cpuProcess).strip("\n")
'''
'''
def getHardware():
    dmiInfo = os.popen("dmidecode").read()
    dmi = divide_into_paragraphs(dmiInfo)
    for i in dmi:
        if "System Information" in i:
            sysinfo = i.strip().split("\n")
            hostinfodic = dict([a.strip().split(": ") for a in sysinfo if ":" in a])
    #print hostinfo
    return "SN: " + hostinfodic['Serial Number'] + "\nManufacturer: " + hostinfodic['Manufacturer'] +"\nProduct: " + hostinfodic['Product Name']
'''

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
    for k,v in cf.FORCE_RANK:
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
        return cf.SHOP_BEGIN_BUYOK.format(**r.hgetall(userkey))
    else:
        return cf.SHOP_BEGIN_NOMONEY


def hitDogEvent(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r):
    eventDict = {
            'smalldoghit':events.SmallDogHit(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r),
            'nomaldoghit':events.NomalDogHit(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r),
            'dabaojian':events.DaBaoJian(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r),
            'baigudaoren':events.BaiGuDaoRen(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r),
            'manyswords':events.ManySwords(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r)
            }
    if userInfo.has_key('baigudaoren'):
        #判断有key叫baigudaoren并切value为3则，白骨道人事件已触发并且流程结束。不再出现。
        if userInfo['baigudaoren'] == "3":
            eventDict.pop('baigudaoren')
    #判断有key叫manyswords，则万剑归宗事件已经结束。不再出现
    elif userInfo.has_key('manyswords'):
        eventDict.pop('manyswords')
    #print eventDict
    randomEvent = random.choice(eventDict.keys())
    return eventDict[randomEvent].work()

@is_hp_empty
def goOnGames(messageReceive,userkey,inventorykey,forcekey,r):
    userInfo = r.hgetall(userkey)
    inventoryInfo = r.zrange(inventorykey,0,-1,withscores=True,score_cast_func=intern)
    forceInfo = r.zrevrange(forcekey,0,-1,withscores=True,score_cast_func=intern)
    #地点为0在新手村
    if userInfo["place"] == "0":
        #选择1 进客栈
        if messageReceive.Content == "1":
            #redis里面取出来的字典的值都变为str了
            if int(userInfo["money"]) -100 >= 0:
                userInfo["money"] = int(userInfo["money"]) -100
                userInfo["hp_now"] = int(userInfo["hp_limit"])
                r.hmset(userkey, userInfo)
                return cf.STAY_HOTEL.format(**userInfo)
            else:
                return cf.NOMONEY_STAY_HOTEL.format(**userInfo)
        #选择2 去商店--初始化的时候
        elif messageReceive.Content == "2":
            userInfo["place"] = 1
            r.hmset(userkey, userInfo)
            return cf.SHOP_BEGIN
        elif messageReceive.Content == "3":
            return hitDogEvent(userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r)
        #选择c 看状态
        elif messageReceive.Content == "c":
            #将两个字典合并起来
            return cf.ROLE_STATE.format(**dict({"items":itemslist_to_str(inventoryInfo),"force":role_force(forceInfo)},**userInfo))
        elif messageReceive.Content == "r":
            #将两个字典合并起来
            return wulin_rank(forceInfo)
        else:
            return "hehe,请做一个选择"
    #地点1 在商店
    elif userInfo["place"] == "1":
        #选择木剑 价格200
        if messageReceive.Content == "1":
            return buySomething("木剑",200,userkey,inventorykey,userInfo,r)
        #选择铁剑 价格500
        elif messageReceive.Content == "2":
            return buySomething("铁剑",500,userkey,inventorykey,userInfo,r)
        elif messageReceive.Content == "0":
            userInfo["place"] = 0
            r.hmset(userkey, userInfo)
            return cf.OUT_SHOP
        elif messageReceive.Content == "c":
            #将两个字典合并起来
            return cf.ROLE_STATE.format(**dict({"items":itemslist_to_str(inventoryInfo),"force":role_force(forceInfo)},**userInfo))
        elif messageReceive.Content == "r":
            #将两个字典合并起来
            return wulin_rank(forceInfo)
        else:
            return "hehe,请做一个选择"
        #r.hincrby('16d3bf1e764582efffcb2255d025cf15','money',100)
    #地点2 打狗事件结束
    elif userInfo["place"] == "2":
        #选择1确认信息，能进入以下逻辑说明HP大于0,然后地点改为0
        if messageReceive.Content == "1":
            r.hset(userkey,"place",0)
            return cf.COMEBACK_BEGIN
        else:
            return "hehe,请做一个选择"
        #r.hincrby('16d3bf1e764582efffcb2255d025cf15','money',100)