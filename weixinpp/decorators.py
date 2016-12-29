#!/usr/bin/env python
# -*- coding:utf-8 -*-
from functools import wraps
# Create decorators
#decorators 
def is_hp_empty(view_func):
    @wraps(view_func)
    def wrapper(messageReceive,userkey,r):
        if  int(r.hgetall(userkey)['hp']) <= 0:
            r.delete(userkey)
            return "you are dead"
        else:
            return view_func(messageReceive,userkey,r)
    return wrapper