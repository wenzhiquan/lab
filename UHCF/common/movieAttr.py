#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: movieAttr.py
@time: 16/3/6 11:19
@description: null
"""
from config import config
from lib import stdLib


class MovieAttr():
    def __init__(self):
        pass

    def hotMovie(self):
        read = open(config.trainFile, 'r')
        data = read.readlines()
        read.close()
        length = len(data)

        hotMovieDict = dict()

        for i in data:
            tmp = i[:-1].split(config.separator)
            movieId = tmp[1]
            hotMovieDict.setdefault(movieId, 0)
            hotMovieDict[movieId] += 1

        hotMovieList = sorted(hotMovieDict.items(), key=lambda x: x[1], reverse=True)
        outFile = r'result/hotMovie.list'
        stdLib.dumpData(hotMovieList, outFile)

    def goodMovie(self):
        read = open(config.trainFile, 'r')
        data = read.readlines()
        read.close()
        length = len(data)

        goodMovieDict = dict()
        gradeCountDict = dict()

        for i in data:
            tmp = i[:-1].split(config.separator)
            movieId = tmp[1]
            grade = tmp[2]
            goodMovieDict.setdefault(movieId, 0)
            gradeCountDict.setdefault(movieId, 0)
            goodMovieDict[movieId] += float(tmp[2])
            gradeCountDict[movieId] += 1

        for i in goodMovieDict:
            goodMovieDict[i] = goodMovieDict[i] / gradeCountDict[i]

        goodMovieList = sorted(goodMovieDict.items(), key=lambda x: x[1], reverse=True)
        print goodMovieList
        outFile = r'result/goodMovie.list'
        stdLib.dumpData(goodMovieList, outFile)

    def commonLabel(self):
        read = open(config.ratingWithLabelFile, 'r')
        data = read.readlines()
        read.close()
        length = len(data)

        labelDict = dict()
        for j in range(config.labelLength):
            labelDict.setdefault(j, 0)
        for i in data:
            tmp = i[:-1].split(config.separator)
            labels = tmp[4].split(config.subSeparator)
            for j in range(config.labelLength):
                if labels[j] == '1':
                    labelDict[j] += 1

        labelList = sorted(labelDict.items(), key=lambda x: x[1], reverse=True)
        print labelList
        outFile = r'result/commonLabel.list'
        stdLib.dumpData(labelList, outFile)