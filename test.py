#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from flask import Flask
from flask import request
import hashlib
import  xml.etree.ElementTree as xmlee
from xmlanalysis import TextMsg
import reply

app = Flask(__name__)

@app.route("/weixin", methods=['GET','POST'])
def hello():
    if request.method == 'GET':
        try:
            signature = request.values.get('signature')
            timestamp = request.values.get('timestamp')
            nonce = request.values.get('nonce')
            echostr = request.values.get('echostr')
            token = "helloworld"
            tmplist = [token, timestamp, nonce]
            tmplist.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, tmplist)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except:
            return "Hello World!"
    else:
        messageReceive = solve_request(request)
        if isinstance(messageReceive, TextMsg) and messageReceive.MsgType == 'text':
                toUser = messageReceive.FromUserName
                fromUser = messageReceive.ToUserName
                content = "test"
                replyMsg = reply.TextReplyMsg(toUser, fromUser, content)
                return replyMsg.send()
            
            
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
        
        
        
if __name__ == "__main__":
    app.run()