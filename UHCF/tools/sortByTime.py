#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: sortByTime.py
@time: 15/12/7 14:28
"""
from config import config


def sortByTime():
    print 'sorting meta data by time......'
    filename = config.trainFile
    read = open(filename, 'r')
    data = read.readlines()
    read.close()

    sorted_lines = sorted(data, key=lambda l: float(l.split('::')[3]), reverse=False)

    outfile = config.sortedRatingFile
    out = open(outfile, 'w')
    out.write(''.join(sorted_lines))
    out.close()

