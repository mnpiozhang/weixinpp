#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import  xml.etree.ElementTree as xmlee
from xmlobjs import TextMsg,BaseEvent
from redispool import pool
import redis

#接受并解析xml信息
def solve_request(request):
        #print request.stream.read()
        #rawStr = request.stream.read()
        receiveRequest = request.data
        if len(receiveRequest) == 0:
            return None
        #print rawStr
        xmlReceive = xmlee.fromstring(receiveRequest)
        #print xml_rec
        msg_type = xmlReceive.find('MsgType').text
        if msg_type == 'text':
            return TextMsg(xmlReceive)
        elif msg_type == 'event':
            return BaseEvent(xmlReceive)
        
#抄来的http://code.activestate.com/recipes/578019/        
def bytes2human(n, format='%(value).1f %(symbol)s', symbols='customary'):
    SYMBOLS = {
        'customary'     : ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'),
        'customary_ext' : ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                           'zetta', 'iotta'),
        'iec'           : ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
        'iec_ext'       : ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                           'zebi', 'yobi'),
    }
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    symbols = SYMBOLS[symbols]
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i+1)*10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)

def redisConnect():
    r = redis.Redis(connection_pool=pool)
    return r