#!/usr/bin/env python
# -*- coding:utf-8 -*-
from functools import wraps
import config as cf
# Create decorators
#decorators 
def is_hp_empty(view_func):
    @wraps(view_func)
    def wrapper(messageReceive,userkey,r):
        if  int(r.hgetall(userkey)['hp_now']) <= 0:
            r.delete(userkey)
            return cf.DEAD_STR
        else:
            return view_func(messageReceive,userkey,r)
    return wrapper