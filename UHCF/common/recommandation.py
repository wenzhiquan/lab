#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: recommandation.py
@time: 16/1/18 14:27
@description: null
"""
from config import config
from lib import stdLib
from math import pi

def generaRecommandList(simMatrix = None):
    filename = simMatrix or config.CFUUserSimMatrix
    data = stdLib.loadData(filename)
    length = len(data)

    ratingDict = stdLib.loadData(config.uiDictFile)

    recommandDict = dict()
    count = 0
    print 'generating recommand list......'
    for userId in data:
        count += 1
        recommandDict.setdefault(userId, dict())
        for j in data[userId]:
            tmpUser = j[0]
            grade = j[1]
            for movie in ratingDict[tmpUser]:
                if movie in ratingDict[userId]:
                    continue
                recommandDict[userId].setdefault(movie, 0)
                recommandDict[userId][movie] += float(pi) * float(grade)
        recommandDict[userId] = dict(sorted(recommandDict[userId].items(),
                                            key=lambda x: x[1], reverse=True)[0:config.listLength])

        if count % int(length * config.percentage) == 0:
            print '%.3f%%' % (count * 100 / length)
    print 'writing data......'
    outfile = config.recommandListFile
    out = open(outfile, 'w')
    for i in recommandDict:
        out.write(i + config.separator + config.subSeparator.join(recommandDict[i]) + '\n')
    out.close()
