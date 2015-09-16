#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wenzhiquan
# created time: 2015-09-15 18:17:52

from readFile import data

outfile = "result/lastLogin.txt"

column = 9

out = open(outfile, 'w')

channel = {}
for i in data:
    tmp = i.split("\t")
    channel.setdefault(tmp[column][0:10], 0)
    channel[tmp[column][0:10]] += 1
for i in channel:
    out.write(i + '\t' + str(channel[i]) + '\n')
print channel 
