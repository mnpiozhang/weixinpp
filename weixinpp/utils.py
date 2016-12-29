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


############工具方法or参数###############
helpStr = '''hello this is my toy.
host info input 1
memory info input 2
user info input 3
cpu info input 4
playplay game input 5
help info input ? or help'''

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
            return helpStr
        else:
            return "hehe"
    


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

def startPlay(messageReceive,userkey,r):
    attr_dict = { 
                 "money":1000,
                 "score":0,
                 "process":0,
                 "hp":10,
                 }
    r.hmset(userkey, attr_dict)  
    return '''start games.please chose
    1.get a weapon
    2.go to hit dog
    '''
    #return "我还没想好...."

@is_hp_empty
def goOnGames(messageReceive,userkey,r):
    userInfo = r.hgetall(userkey)  
    if messageReceive.Content == "1":
        userInfo["money"] = userInfo["money"] -100
        r.hmset(userkey, userInfo)
        return "you buy a weapon,go on"
    elif messageReceive.Content == "2":
        userInfo["hp"] = userInfo["hp"] -1
        r.hmset(userkey, userInfo)
        return "you hit a dog,go on"
        