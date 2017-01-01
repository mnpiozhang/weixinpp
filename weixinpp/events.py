#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import random
from werkzeug.contrib.profiler import available

class RandomEvent:
    def __init__(self,userkey,inventorykey,userInfo,r):
        self.userkey = userkey
        self.inventorykey = inventorykey
        self.userInfo = userInfo
        self.r = r
        
class SmallDogHit(RandomEvent):
    def work(self):
        reduce_hp = random.randint(1, 3)
        add_money = random.randint(20, 50)
        available_items = ["狗肉","骨头"]
        add_items = random.choice(available_items)
        resultdict = {
                      "reduce_hp":reduce_hp,
                      "add_money":add_money,
                      "add_items":add_items
                      }
        pipeline = self.r.pipeline()
        pipeline.hincrby(self.userkey,"hp_now",-reduce_hp)
        pipeline.hincrby(self.userkey,"money",add_money)
        pipeline.zincrby(self.inventorykey,add_items,1)
        pipeline.hset(self.userkey,"place",2)
        pipeline.execute()
        outStr = '''你遇到了一条小狗，它朝你卖萌，但是你狠下心击杀了它，你损失hp{reduce_hp},你获得了金钱:{add_money}，道具:{add_items}
请选择:
1.确认
'''
        return outStr.format(**resultdict)
    
    
class NomalDogHit(RandomEvent):
    def work(self):
        reduce_hp = random.randint(2, 4)
        add_money = random.randint(50, 100)
        available_items = ["狗肉","骨头"]
        add_items = random.choice(available_items)
        resultdict = {
                      "reduce_hp":reduce_hp,
                      "add_money":add_money,
                      "add_items":add_items
                      }
        pipeline = self.r.pipeline()
        pipeline.hincrby(self.userkey,"hp_now",-reduce_hp)
        pipeline.hincrby(self.userkey,"money",add_money)
        pipeline.zincrby(self.inventorykey,add_items,1)
        pipeline.hset(self.userkey,"place",2)
        pipeline.execute()
        outStr = '''你看到一条狗正在打坐，你从后面偷袭击杀了它，损失hp{reduce_hp},你获得了金钱:{add_money}，道具:{add_items}
请选择:
1.确认
'''
        return outStr.format(**resultdict)