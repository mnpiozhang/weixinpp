#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import psutil
import socket
from common import bytes2human
from datetime import  datetime

#具体处理逻辑
def resp_content(messageReceive):
    if messageReceive.Content == "1":
        return socket.gethostname()
    elif messageReceive.Content == "2":
        return getMem()
    elif messageReceive.Content == "3":
        return getOnlineUser
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
        resp = resp + "User:%sFrom:%sTime:%s\n" %(i[0],i[1],i[2])
    return resp