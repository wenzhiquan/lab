#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: combineCFUAndTHCCF.py
@time: 16/1/18 17:30
@description: null
"""
from config import config
from lib import stdLib

def combine():
    CFUData = stdLib.loadData(config.CFUUserSimMatrix)
    simData = stdLib.loadData(config.userSimMatrix)
    print 'start combining CFU and sim......'
    a = 0.28
    CFUDict = {}
    simDict = {}
    resultDict = {}
    for user in CFUData:
        CFUDict.setdefault(user, {})
        for tuples in CFUData[user]:
            CFUDict[user].setdefault(tuples[0], tuples[1])
        simDict.setdefault(user, {})
        for tuples in simData[user]:
            simDict[user].setdefault(tuples[0], tuples[1])

    for user in CFUDict:
        for simUser in CFUDict[user]:
            if simUser in simDict[user]:
                CFUDict[user][simUser] = CFUDict[user][simUser] * a + simDict[user][simUser] * (1 - a)
            else:
                CFUDict[user][simUser] *= a
        for simUser in simDict[user]:
            CFUDict[user].setdefault(simUser, simDict[user][simUser] * (1 - a))

    # for user in CFUData:
    #     i, j = 0, 0
    #     resultDict.setdefault(user, [])
    #     while i < len(CFUData[user]) and j < len(simData[user]):
    #         if CFUData[user][i][1] > simData[user][j][1]:
    #             resultDict[user].append(CFUData[user][i])
    #             i += 1
    #         else:
    #             resultDict[user].append(simData[user][j])
    #             j += 1
    #     while i < len(CFUData[user]):
    #         resultDict[user].append(CFUData[user][i])
    #         i += 1
    #     while j < len(simData[user]):
    #         resultDict[user].append(simData[user][j])
    #         j += 1
        sortedRecommand = sorted(CFUDict[user].iteritems(), key=lambda d: d[1], reverse=True)
        resultDict.setdefault(user, [])
        for i in sortedRecommand:
            resultDict[user].append(i)

    stdLib.dumpData(resultDict, config.combineSimMatrix)
    print 'combine finished......'