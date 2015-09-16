#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wenzhiquan
# created time: 2015-09-15 18:17:52

filename = r"result/channel.txt"

read = open(filename, 'r')

data = read.readlines()

read.close()

sorted_lines = sorted(data, key=lambda l: float(l.split('\t')[1]), reverse = True)

print sorted_lines

outfile = r"result/sortedChannel.txt"

out = open(outfile, 'w')

out.write(''.join(sorted_lines))
