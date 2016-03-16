#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: combineById.py
@time: 15/12/7 15:06
@description: null
"""
from tools import sortByTime
from config import config


def combineById():
    print 'combining data with labels......'
    filename = config.sortedRatingFile
    read = open(filename, 'r')
    data = read.readlines()
    read.close()

    filename = config.metaMovieFile
    read = open(filename, 'r')
    movies = read.readlines()
    read.close()

    movieDict = {}

    for i in movies:
        labelArr = []
        for m in range(19):
            labelArr.append('0')
        tmp = i.split(config.separator)
        movieId = tmp[0]
        labels = tmp[2][:-1].split(config.subSeparator)
        for j in labels:
            labelArr[config.labelDict[j]] = '1'
        movieDict.setdefault(movieId, config.subSeparator.join(labelArr))

    outfile = config.ratingWithLabelFile
    out = open(outfile, 'w')

    for i in data:
        tmp = i.split(config.separator)
        movieId = tmp[1]
        tmp[3] = tmp[3][:-1]
        tmp.append(movieDict[movieId])
        out.write(config.separator.join(tmp) + '\n')

    out.close()
