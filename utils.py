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
        return w()
    else:
        return "hehe"
    


def getMem():
    memInfo = psutil.virtual_memory()
    totalMem = memInfo.total
    availableMem = memInfo.available
    resp = "总内存  %s\n可用内存  %s" %(bytes2human(totalMem),bytes2human(availableMem))
    return resp

def w():
    # TODO user idle time not yet achieve
    user_idle_time = '0.00s'
    ret = []
    for u in psutil.users():
        ret.append([u.name,
                    u.host,
                    datetime.fromtimestamp(u.started).strftime("%H:%M"),
                    user_idle_time
                    ])
    return ret