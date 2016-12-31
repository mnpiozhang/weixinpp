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

############工具方法or参数###############

#ex[('a',1),('b',2)] ==> aX1 bX2
def itemslist_to_str(inventoryInfo):
    itemsOut=""
    for k,v in inventoryInfo:
        strOut = k + 'X' + str(v)
        itemsOut = itemsOut + " " + strOut
    return itemsOut

    
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


########################################################
#具体处理逻辑
def resp_content(messageReceive):
    r = redisConnect()
    userkey = "users:%s" %(hashlib.md5(messageReceive.FromUserName).hexdigest())
    inventorykey = "inventory:%s" %(hashlib.md5(messageReceive.FromUserName).hexdigest())
    marketkey = "marketkey:%s" %(hashlib.md5(messageReceive.FromUserName).hexdigest())
    if r.exists(userkey):
        return goOnGames(messageReceive,userkey,inventorykey,marketkey,r) 
    else:
        if messageReceive.Content == "1":
            return startPlay(messageReceive,userkey,inventorykey,marketkey,r)
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
def startPlay(messageReceive,userkey,inventorykey,marketkey,r):
    '''
    messageReceive-------接收到的微信xml信息
    userkey--------------用户信息key
    inventorykey---------包裹信息key
    marketkey------------能买道具信息key
    r--------------------Redis链接对象
    '''
    attr_dict = cf.INIT_STATE
    r.hmset(userkey, attr_dict)
    #r.sadd(inventorykey,"绝世神功")
    r.zadd(inventorykey,"绝世神功",1)
    r.zadd(marketkey,"木剑",200,"铁剑",500)
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

@is_hp_empty
def goOnGames(messageReceive,userkey,inventorykey,marketkey,r):
    userInfo = r.hgetall(userkey)
    inventoryInfo = r.zrange(inventorykey,0,-1,withscores=True,score_cast_func=intern)
    marketInfo = r.zrange(marketkey,0,-1,withscores=True,score_cast_func=intern)
    #marketInfo = r.
    #流程为0在新手村
    if userInfo["process"] == "0":
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
            userInfo["process"] = 1
            r.hmset(userkey, userInfo)
            return cf.SHOP_BEGIN
        elif messageReceive.Content == "3":
            #userInfo["hp_now"] = int(userInfo["hp_now"]) -1
            #r.hmset(userkey, userInfo)
            r.hincrby(userkey,"hp_now",-1)
            return cf.HIT_DOG.format(**userInfo)
        #选择c 看状态
        elif messageReceive.Content == "c":
            #将两个字典合并起来
            return cf.ROLE_STATE.format(**dict({"items":itemslist_to_str(inventoryInfo)},**userInfo))
        else:
            return "hehe,请做一个选择"
    #流程1 在商店
    elif userInfo["process"] == "1":
        #选择木剑 价格200
        if messageReceive.Content == "1":
            return buySomething("木剑",200,userkey,inventorykey,userInfo,r)
        #选择铁剑 价格500
        elif messageReceive.Content == "2":
            return buySomething("铁剑",500,userkey,inventorykey,userInfo,r)
        elif messageReceive.Content == "0":
            userInfo["process"] = 0
            r.hmset(userkey, userInfo)
            return cf.OUT_SHOP
        elif messageReceive.Content == "c":
            #将两个字典合并起来
            return cf.ROLE_STATE.format(**dict({"items":itemslist_to_str(inventoryInfo)},**userInfo))
        else:
            return "hehe,请做一个选择"
        #r.hincrby('16d3bf1e764582efffcb2255d025cf15','money',100)