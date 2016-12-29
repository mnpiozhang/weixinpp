#!/usr/bin/env python
#_*_ coding:utf-8 _*_

REDIS_SERVER="127.0.0.1"
REDIS_PORT=6379

HELP_STR = '''hello this is my toy.
host info input 1
memory info input 2
user info input 3
cpu info input 4
playplay game input 5
help info input ? or help'''

START_GAME='''开始游戏，请选择
1.get a weapon
2.go to hit dog
HP:{hp}
money:{money}
score:{score}'''

BUY_WEAPON='''you buy a weapon,go on
HP:{hp}
money:{money}
score:{score}'''

HIT_DOG='''you hit a dog,go on
HP:{hp}
money:{money}
score:{score}'''