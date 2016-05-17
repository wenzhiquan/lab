#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: recommendation.py
@time: 16/1/18 14:27
@description: null
"""
from config import config
from lib import stdLib
from math import pi

def generaRecommendList(simMatrix = None, isScored = True):
    filename = simMatrix or config.CFUUserSimMatrix
    simUsers = stdLib.loadData(filename)
    length = len(simUsers)

    uiDict = stdLib.loadData(config.uiDictFile)
    recommendDict = dict()
    count = 0
    print 'generating recommend list......'
    for user in simUsers:
        count += 1
        if user not in uiDict:
            continue
        history = uiDict[user]
        simSum = 0
        avgU = sum(uiDict[user].values()) / float(len(uiDict[user]))
        recommendDict.setdefault(user, dict())
        for simUser in simUsers[user]:  # simUsers是用户相似度矩阵,candidate是与userId相似的用户及其相似度
            tmpUser = simUser[0]
            similarity = simUser[1]
            simSum += similarity
            if tmpUser in uiDict:
                candidate = uiDict[tmpUser]
                # avg = sum(candidate.values()) / float(len(candidate))
                for item in candidate:
                    if item in history:
                        continue
                    rating = candidate[item]  # - avg
                    recommendDict[user].setdefault(item, 0)
                    recommendDict[user][item] += float(similarity) * rating
        for item in recommendDict[user]:
            if simSum != 0:
                recommendDict[user][item] /= simSum
                recommendDict[user][item] += avgU
        recommendDict[user] = dict(sorted(recommendDict[user].items(),
                                            key=lambda x: x[1], reverse=True)[0:config.listLength])
        # print recommendDict[userId]
        if count % int(length * config.percentage) == 0:
            print '%.3f%%' % (count * 100 / length)
    print 'writing data......'
    outfile = config.recommendListFile
    out = open(outfile, 'w')
    for i in recommendDict:
        out.write(i + config.separator + config.subSeparator.join(recommendDict[i]) + '\n')
    out.close()
    outfile = config.recommendDict
    stdLib.dumpData(recommendDict, outfile)
