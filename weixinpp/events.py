#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import random
from common import is_item_exist
import inspect
import sys 

#####################事件类
class RandomEvent:
    def __init__(self,userkey,inventorykey,forcekey,userInfo,inventoryInfo,forceInfo,r):
        self.userkey = userkey
        self.inventorykey = inventorykey
        self.forcekey = forcekey
        self.userInfo = userInfo
        self.inventoryInfo = inventoryInfo
        self.forceInfo = forceInfo
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

class BigDogHit(RandomEvent):
    def work(self):
        reduce_hp = random.randint(3, 5)
        add_money = random.randint(100, 130)
        available_items = ["狗肉","骨头","九阳神功"]
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
        outStr = '''你遇到一条凶猛的狼狗向你袭来，你击杀了它，损失hp{reduce_hp},你获得了金钱:{add_money}，道具:{add_items}
请选择:
1.确认
'''
        return outStr.format(**resultdict)


class GetManyMoney(RandomEvent):
    def work(self):
        reduce_hp = random.randint(1, 2)
        add_money = random.randint(200, 500)
        resultdict = {
                      "reduce_hp":reduce_hp,
                      "add_money":add_money
                      }
        pipeline = self.r.pipeline()
        pipeline.hincrby(self.userkey,"hp_now",-reduce_hp)
        pipeline.hincrby(self.userkey,"money",add_money)
        pipeline.hset(self.userkey,"place",2)
        pipeline.execute()
        outStr = '''你看到有人欺压百姓，作为正义的伙伴，不能坐视不理，教训完恶霸后，狠狠敲了一笔然后离开了，你损失hp{reduce_hp},你获得了金钱:{add_money}
请选择:
1.确认
'''
        return outStr.format(**resultdict)

class DaoMuBiJi(RandomEvent):
    def work(self):
        pipeline = self.r.pipeline()
        pipeline.hset(self.userkey,"place",3)
        pipeline.execute()
        outStr = '''你遇到了江湖赫赫有名的盗墓王张起灵，他说刚干了一票正准备上交国家，并示意你给点好处可以让你挑两件。
你看了看他的东西，现在选择是：
1.混元功 2000
2.紫气朝阳决 3000
3.橡皮剑 3000
4.塑料剑 5000
5.不可名状的小册子 6666
0.啥也不选上交国家
c.查看状态'''
        return outStr


class DaBaoJian(RandomEvent):
    def work(self):
        if self.userInfo.has_key('dongwan'):
            if self.userInfo['dongwan'] == '10':
                increase_hp_limit = random.randint(2, 4)
                resultdict = {
                              "increase_hp_limit":increase_hp_limit
                              }
                newhp = int(self.userInfo['hp_limit']) + increase_hp_limit
                pipeline = self.r.pipeline()
                pipeline.hincrby(self.userkey,"hp_limit",increase_hp_limit)
                pipeline.hset(self.userkey,"hp_now",newhp)
                if self.userInfo['money'] >= 1000:
                    pipeline.hincrby(self.userkey,"money",-1000)
                else:
                    pipeline.hset(self.userkey,"money",0)
                pipeline.hset(self.userkey,"place",2)
                pipeline.hincrby(self.userkey,"dongwan",1)
                pipeline.zincrby(self.forcekey,"胡二虎",20)
                pipeline.zincrby(self.inventorykey,"伟哥大法",1)
                pipeline.execute()
                outStr = '''不知不觉间你来到了东莞楼，决定大保健一发，然后花天酒地花了一大笔钱。HP上限提高了{increase_hp_limit} 并且恢复了所有体力。因为一直大保健的缘故，你领悟到了伟哥大法。
获得道具伟哥大法
功力提升20点
请选择:
1.确认
'''
                return outStr.format(**resultdict)
            else:
                increase_hp_limit = random.randint(2, 4)
                resultdict = {
                              "increase_hp_limit":increase_hp_limit
                              }
                newhp = int(self.userInfo['hp_limit']) + increase_hp_limit
                pipeline = self.r.pipeline()
                pipeline.hincrby(self.userkey,"hp_limit",increase_hp_limit)
                pipeline.hset(self.userkey,"hp_now",newhp)
                if self.userInfo['money'] >= 1000:
                    pipeline.hincrby(self.userkey,"money",-1000)
                else:
                    pipeline.hset(self.userkey,"money",0)
                pipeline.hset(self.userkey,"place",2)
                pipeline.hincrby(self.userkey,"dongwan",1)
                pipeline.zincrby(self.forcekey,"胡二虎",2)
                pipeline.execute()
                outStr = '''不知不觉间你来到了东莞楼，决定大保健一发，然后花天酒地花了一大笔钱。HP上限提高了{increase_hp_limit} 并且恢复了所有体力。
功力提升2点
请选择:
1.确认
'''
                return outStr.format(**resultdict)
        else:
            increase_hp_limit = random.randint(2, 4)
            resultdict = {
                          "increase_hp_limit":increase_hp_limit
                          }
            newhp = int(self.userInfo['hp_limit']) + increase_hp_limit
            pipeline = self.r.pipeline()
            pipeline.hincrby(self.userkey,"hp_limit",increase_hp_limit)
            pipeline.hset(self.userkey,"hp_now",newhp)
            if self.userInfo['money'] >= 1000:
                pipeline.hincrby(self.userkey,"money",-1000)
            else:
                pipeline.hset(self.userkey,"money",0)
            pipeline.hset(self.userkey,"place",2)
            pipeline.hincrby(self.userkey,"dongwan",1)
            pipeline.zincrby(self.forcekey,"胡二虎",2)
            pipeline.execute()
            outStr = '''不知不觉间你来到了东莞楼，决定大保健一发，然后花天酒地花了一大笔钱。HP上限提高了{increase_hp_limit} 并且恢复了所有体力。
功力提升2点
请选择:
1.确认
'''
            return outStr.format(**resultdict)

class ManySwords(RandomEvent):
    def work(self):
        if is_item_exist(self.inventoryInfo,"万骨魔剑") and is_item_exist(self.inventoryInfo,"木剑") and is_item_exist(self.inventoryInfo,"铁剑") and is_item_exist(self.inventoryInfo,"塑料剑") and is_item_exist(self.inventoryInfo,"橡皮剑"):
            pipeline = self.r.pipeline()
            pipeline.hset(self.userkey,"place",2)
            pipeline.zincrby(self.inventorykey,"万剑归宗",1)
            pipeline.zincrby(self.forcekey,"胡二虎",50)
            pipeline.hset(self.userkey,"manyswords",1)
            pipeline.zrem(self.inventorykey,"万骨魔剑","木剑","铁剑","塑料剑","橡皮剑")
            pipeline.execute()
            outStr = '''你遇到一个样貌落魄的男人,声称只要找到万骨魔剑,塑料剑,橡皮剑,铁剑,木剑,他就传授你绝学万剑归宗.
你恰好有他要的东西。你抱着试试看的心态把东西交给了他。一瞬间脑海里面就浮现出了很多玄妙的招式。当你醒过来的时候感觉菊花有点痒，那个男人已经离开了，你学会了万剑归宗。
功力提升50点
请选择:
1.确认
'''
            return outStr
        else:
            self.r.hset(self.userkey,"place",2)
            outStr = '''你遇到一个样貌落魄的男人,声称只要找到万骨魔剑,塑料剑,橡皮剑,铁剑,木剑,他就传授你绝学万剑归宗.
你心想一定是遇到了疯子,而且你也没有他要的东西。你就离开了。
请选择:
1.确认
'''
            return outStr

class FiveAir(RandomEvent):
    def work(self):
        if is_item_exist(self.inventoryInfo,"化功大法") and is_item_exist(self.inventoryInfo,"九阳神功") and is_item_exist(self.inventoryInfo,"混元功") and is_item_exist(self.inventoryInfo,"伟哥大法") and is_item_exist(self.inventoryInfo,"紫气朝阳决"):
            pipeline = self.r.pipeline()
            pipeline.hset(self.userkey,"place",2)
            pipeline.zincrby(self.inventorykey,"五气朝元",1)
            pipeline.zincrby(self.forcekey,"胡二虎",50)
            pipeline.hset(self.userkey,"fiveair",1)
            pipeline.zrem(self.inventorykey,"化功大法","九阳神功","紫气朝阳决","混元功","伟哥大法")
            pipeline.execute()
            outStr = '''你遇到一个仙风道骨的人正在打坐.向你讨要化功大法,九阳神功,紫气朝阳决,混元功,伟哥大法。
你觉的此人样貌不凡,定是奇人,就将身上的5本秘籍交给了他。他则给你输了一道真气，你学会了道家上乘功夫五气朝元。
功力提升50点
请选择:
1.确认
'''
            return outStr
        else:
            self.r.hset(self.userkey,"place",2)
            outStr = '''你遇到一个仙风道骨的人正在打坐.向你讨要化功大法,九阳神功,紫气朝阳决,混元功,伟哥大法。
你觉的此人样貌不凡,定是奇人,但你没有他要的东西。你就离开了。
请选择:
1.确认
'''
            return outStr


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
                pipeline.zincrby(self.forcekey,"胡二虎",10)
                pipeline.zadd(self.forcekey,"白骨道人",40)
                pipeline.execute()
                outStr = '''你还是不死心，决定最后再去见一次白骨道人。在离白骨洞很远的地方就听到了厮杀声。你上前一看有人正围攻白骨洞，你立即前去助阵。在身负重伤的情况下帮助白骨道人击败敌人。
白骨道人最后还是死了，临死前她告诉你之前的敌人是蜀山剑派的人，并留给了你她的一样宝物。
损失hp{reduce_hp},获得道具:{add_items}，功力提升10
请选择:
1.确认
'''
                return outStr.format(**resultdict)
            elif self.userInfo["baigudaoren"] == "3":
                reduce_hp = random.randint(4, 5)
                #available_items = ["紫气朝阳决"]
                #add_items = random.choice(available_items)
                resultdict = {
                              "reduce_hp":reduce_hp
                              }
                pipeline = self.r.pipeline()
                pipeline.hincrby(self.userkey,"hp_now",-reduce_hp)
                #pipeline.zincrby(self.inventorykey,add_items,1)
                pipeline.hset(self.userkey,"place",2)
                pipeline.hset(self.userkey,"baigudaoren",4)
                pipeline.zincrby(self.forcekey,"胡二虎",10)
                pipeline.zadd(self.forcekey,"白骨道人",400)
                pipeline.zadd(self.forcekey,"李逍遥",150)
                pipeline.execute()
                outStr = '''你来到蜀山，为报之前白骨道人的仇与蜀山剑派的弟子大打出手，最后蜀山掌门李逍遥出动将你教训了一顿。突然有人从背后偷袭了李逍遥，原来是白骨道人，她并没有死，她当年被李逍遥调戏怀恨在心，所以利用了拥有绝世神功的你。你见势不妙，只能选择正义的撤退。。。
损失hp{reduce_hp},功力提升10
白骨道人重出江湖
李逍遥被偷袭，功力大损
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
                pipeline.zadd(self.forcekey,"白骨道人",25)
                pipeline.execute()
                outStr = '''忽然阴风阵阵，让你觉的毛骨悚然，原来你误闯白骨洞。只见一名白衣女子出现在你面前。自称自己是白骨道人，你打扰了她练功，除非交出2根骨头，不然就要你好看。
你一摸口袋，发现之前打狗得到了很多狗骨头，你交出了2根给白骨道人后离开了。
请选择:
1.确认
'''
                return outStr
            else:
                pipeline = self.r.pipeline()
                pipeline.hset(self.userkey,"baigudaoren",1)
                pipeline.hset(self.userkey,"place",2)
                pipeline.zincrby(self.forcekey,"胡二虎",3)
                pipeline.zadd(self.forcekey,"白骨道人",25)
                pipeline.execute()
                outStr = '''忽然阴风阵阵，让你觉的毛骨悚然，原来你误闯白骨洞。只见一名白衣女子出现在你面前。自称自己是白骨道人，你打扰了她练功，除非交出2根骨头，不然就要你好看。
由于你没有足够的骨头，只能上前应战。大战三百回合后，第二天一早你离开了白骨洞。
功力提升3点
请选择:
1.确认
'''
                return outStr

###################返回所有事件类，不包含父类RandomEvent    
def all_events_class():
    allClassIncludeSuper = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    return [ x for x in allClassIncludeSuper if not x[0] == "RandomEvent"]

#print all_events_class()
