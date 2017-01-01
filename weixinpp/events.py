#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import random
from werkzeug.contrib.profiler import available


#####工具方法
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

#####################事件类
class RandomEvent:
    def __init__(self,userkey,inventorykey,userInfo,inventoryInfo,r):
        self.userkey = userkey
        self.inventorykey = inventorykey
        self.userInfo = userInfo
        self.inventoryInfo = inventoryInfo
        self.r = r
        
class SmallDogHit(RandomEvent):
    def work(self):
        reduce_hp = random.randint(1, 2)
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
    
class DaBaoJian(RandomEvent):
    def work(self):
        increase_hp_limit = random.randint(2, 4)
        resultdict = {
                      "increase_hp_limit":increase_hp_limit
                      }
        newhp = int(self.userInfo['hp_limit']) + increase_hp_limit
        pipeline = self.r.pipeline()
        pipeline.hincrby(self.userkey,"hp_limit",increase_hp_limit)
        pipeline.hset(self.userkey,"hp_now",newhp)
        pipeline.hset(self.userkey,"money",0)
        pipeline.hset(self.userkey,"place",2)
        pipeline.execute()
        outStr = '''不知不觉间你来到了东莞楼，决定大保健一发，然后花天酒地花光了所有钱。HP上限提高了{increase_hp_limit} 并且恢复了所有体力。
请选择:
1.确认
'''
        return outStr.format(**resultdict)
    
class BaiGuDaoRen(RandomEvent):
    def work(self):
        if self.userInfo.has_key('baigudaoren'):
            if self.userInfo["baigudaoren"] == "1":
                self.r.hset(self.userkey,"place",2)
                self.r.hset(self.userkey,"baigudaoren",2)
                outStr = '''自从上次遇到白骨道人后，你久久不能忘怀她的身影。你再一次来到了白骨洞。但是没有见到她。
请选择:
1.确认
'''
                return outStr
            elif self.userInfo["baigudaoren"] == "2":
                reduce_hp = random.randint(4, 5)
                available_items = ["化功大法","万骨魔剑"]
                add_items = random.choice(available_items)
                resultdict = {
                              "reduce_hp":reduce_hp,
                              "add_items":add_items
                              }
                pipeline = self.r.pipeline()
                pipeline.hincrby(self.userkey,"hp_now",-reduce_hp)
                pipeline.zincrby(self.inventorykey,add_items,1)
                pipeline.hset(self.userkey,"place",2)
                pipeline.hset(self.userkey,"baigudaoren",3)
                pipeline.execute()
                outStr = '''你还是不死心，决定最后再去见一次白骨道人。在离白骨洞很远的地方就听到了厮杀声。你上前一看有人正围攻白骨洞，你立即前去助阵。在身负重伤的情况下帮助白骨道人击败敌人。
白骨道人最后还是死了，临死前她告诉你之前的敌人是驼峰山庄的人，并留给了你她的一样宝物。
损失hp{reduce_hp},道具:{add_items}
请选择:
1.确认
'''
                return outStr.format(**resultdict)
        else:
            boneNum = is_item_exist(self.inventoryInfo,"骨头")
            if boneNum >= 2:
                pipeline = self.r.pipeline()
                pipeline.hset(self.userkey,"place",2)
                pipeline.zincrby(self.inventorykey,"骨头",-2)
                pipeline.hset(self.userkey,"baigudaoren",1)
                pipeline.execute()
                outStr = '''忽然阴风阵阵，让你觉的毛骨悚然，原来你误闯白骨洞。只见一名白衣女子出现在你面前。自称自己是白骨道人，你打扰了她练功，除非交出2根骨头，不然就要你好看。
你一摸口袋，发现之前打狗得到了很多狗骨头，你交出了2根给白骨道人后离开了。
请选择:
1.确认
'''
                return outStr
            else:
                self.r.hset(self.userkey,"baigudaoren",1)
                self.r.hset(self.userkey,"place",2)
                outStr = '''忽然阴风阵阵，让你觉的毛骨悚然，原来你误闯白骨洞。只见一名白衣女子出现在你面前。自称自己是白骨道人，你打扰了她练功，除非交出2根骨头，不然就要你好看。
由于你没有足够的骨头，只能上前应战。大战三百回合后，第二天一早你离开了白骨洞。
请选择:
1.确认
'''
                return outStr