#!/usr/bin/env python
# -*- coding:utf-8 -*-
from functools import wraps
import config as cf
# Create decorators
#decorators 
def is_hp_empty(view_func):
    @wraps(view_func)
    def wrapper(messageReceive,userkey,inventorykey,marketkey,r):
        if  int(r.hgetall(userkey)['hp_now']) <= 0:
            pipeline = r.pipeline()
            pipeline.delete(userkey)
            pipeline.delete(inventorykey)
            pipeline.delete(marketkey)
            pipeline.execute()
            return cf.DEAD_STR
        else:
            return view_func(messageReceive,userkey,r)
    return wrapper