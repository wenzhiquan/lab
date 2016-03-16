#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: divideTrainAndTest.py
@time: 16/1/6 15:29
@description: null
"""
from config import config
from random import seed
from lib import stdLib


def divideTrainAndTest():
    print 'spliting data......'
    read = open(config.metaRatingFile, 'r')
    data = read.readlines()
    read.close()
    trainData = []
    testData = []
    seed(seed)
    for i in data:
        tmp = i[:-1].split(config.separator)
        userId = tmp[0]
        time = tmp[3]
        if float(time) > 977004787:
            testData.append(i)
        else:
            trainData.append(i)
    print len(trainData)
    print len(testData)

    trainOut = open(config.trainFile, 'w')
    trainOut.write(''.join(trainData))
    trainOut.close()
    testOut = open(config.testFile, 'w')
    testOut.write(''.join(testData))
    testOut.close()

    file = open(config.trainFile, 'r')
    data = file.readlines()
    uiDict = {}
    for i in data:
        tmp = i[:-1].split(config.separator)
        userId = tmp[0]
        movieId = tmp[1]
        rating = int(tmp[2])
        uiDict.setdefault(userId, dict())
        uiDict[userId].setdefault(movieId, rating)
    stdLib.dumpData(uiDict, config.uiDictFile)
    print "Data split finished..."


if __name__ == '__main__':
    divideTrainAndTest()