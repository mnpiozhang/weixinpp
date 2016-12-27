#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from flask import Flask
from flask import request
import hashlib
from common import solve_request
from utils import resp_content,helpStr
from xmlobjs import TextMsg,TextReplyMsg,BaseEvent



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
            #print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except:
            return "Hello World!"
    else:
        messageReceive = solve_request(request)
        #print messageReceive.MsgType 
        #print  messageReceive.Event 
        if isinstance(messageReceive, TextMsg) and messageReceive.MsgType == 'text':
            toUser = messageReceive.FromUserName
            fromUser = messageReceive.ToUserName
            content = resp_content(messageReceive)
            replyMsg = TextReplyMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif isinstance(messageReceive, BaseEvent) and messageReceive.MsgType == 'event' and messageReceive.Event == 'subscribe':
            toUser = messageReceive.FromUserName
            fromUser = messageReceive.ToUserName
            content = helpStr
            replyMsg = TextReplyMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            return "success"
            
            

        
        
        
if __name__ == "__main__":
    app.run()