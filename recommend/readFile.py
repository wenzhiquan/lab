#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wenzhiquan
# created time: 2015-09-15 18:04:21

filename = "data/gcmob_2015-06-07.txt"
#filename = "result/district.txt"

total = 0
read = open(filename, 'r')
data = read.readlines()
read.close()
