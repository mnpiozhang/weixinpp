#!/usr/bin/env python
#_*_ coding:utf-8 _*_


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