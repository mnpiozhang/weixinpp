#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from datetime import  datetime
import multiprocessing
import os
import platform
import socket
import hashlib
import psutil

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
    if messageReceive.Content == "1":
        return "hostname: " + socket.gethostname() +"\nos: " + "-".join(platform.dist())
    elif messageReceive.Content == "2":
        return getMem()
    elif messageReceive.Content == "3":
        return getOnlineUser()
    elif messageReceive.Content == "4":
        return getCpu()
    elif messageReceive.Content == "5":
        return playplay(messageReceive)
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

def playplay(messageReceive):
    r = redisConnect()
    userkey = hashlib.md5(messageReceive.FromUserName).hexdigest()
    if r.exists(userkey):
        return "go on"
    else:
        return "start"
    #return "我还没想好...."