#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import time

#返回消息xml信息
class BaseReplyMsg:
    def __init__(self):
        pass
    def send(self):
        return "success"

class TextReplyMsg(BaseReplyMsg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)
    
    
#接收到的消息xml信息
class BaseMsg:
    def __init__(self,xmlReceive):
        self.ToUserName = xmlReceive.find('ToUserName').text
        self.FromUserName = xmlReceive.find('FromUserName').text
        self.CreateTime = xmlReceive.find('CreateTime').text
        self.MsgType = xmlReceive.find('MsgType').text
        self.MsgId = xmlReceive.find('MsgId').text
        
class TextMsg(BaseMsg):
    def __init__(self, xmlReceive):
        BaseMsg.__init__(self, xmlReceive)
        self.Content = xmlReceive.find('Content').text.encode("utf-8")
        
        
#接收到的事件xml信息
class BaseEvent:
    def __init__(self,xmlReceive):
        self.ToUserName = xmlReceive.find('ToUserName').text
        self.FromUserName = xmlReceive.find('FromUserName').text
        self.CreateTime = xmlReceive.find('CreateTime').text
        self.MsgType = xmlReceive.find('MsgType').text
        self.Event = xmlReceive.find('Event').text