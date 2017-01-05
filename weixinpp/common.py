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
#本来用于转换服务器内存等单位用的，现在用不到了    
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

############工具方法or参数###############

#ex[('a',1),('b',2)] ==> aX1 bX2
#返回道具数量和数量 结果为字符串
def itemslist_to_str(inventoryInfo):
    itemsOut=""
    for k,v in inventoryInfo:
        strOut = k + 'X' + str(v)
        itemsOut = itemsOut + " " + strOut
    return itemsOut

#返回主人公功力值
def role_force(forceInfo):
    a = dict(forceInfo)
    return a["胡二虎"]

#将dmi信息切分成段落，现专门搞游戏了已不用
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

#返回天梯排行的结果,返回结果为字符串
def wulin_rank(forceInfo):
    outStr="武林天梯排名\n"
    a = 1
    for k,v in forceInfo:
        outLine = "第%s:%s 功力:%s\n" %(str(a),k,str(v))
        outStr = outStr + outLine
        a = a + 1
    return outStr


def is_item_exist(inventoryInfo,itemname):
    '''
    inventoryInfo 主人公背包列表ex: [('a','1'),('b','2')]
    itemname 道具名
    return 如果道具有就返回道具数量，没有就返回0
    '''
    a = dict(inventoryInfo)
    if a.has_key(itemname):
        return int(a[itemname])
    else:
        return 0
