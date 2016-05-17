#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: CFU.py
@time: 16/1/8 16:07
@description: null
"""
import math
import heapq
from lib import stdLib
from config import config


class CFU():
    def __init__(self):
        self.r = 0.145380973896
        iuDict = stdLib.loadData(config.iuDictFile)
        self.iuAverageDict = dict()
        for movie in iuDict:
            avg = sum([iuDict[movie][i] for i in iuDict[movie]]) / float(len(iuDict[movie]))
            self.iuAverageDict.setdefault(movie, avg)

    def matrix(self, uiDict = None, knn = 200, filtrate = 5):
        '''
        calaulate the item_similarity matrix, using given simialrity method
        :param uiDict: user-item score table, data type: dict
        :threshold: qualifying the neighbour users,data type: float
        :filtrate: the criteria of filting users, data type: int
        '''
        print 'calculating the user matrix......'
        uiDict = uiDict or stdLib.loadData(config.uiDictFile)
        matrixDict = dict()
        PROCESS = len(uiDict)
        COUNTER = 0.0
        for i in uiDict:
            COUNTER += 1
            vec1 = uiDict[i]
            if len(vec1) < filtrate:
                continue
            for j in uiDict:
                if i == j:
                    continue
                vec2 = uiDict[j]
                if len(vec2) < filtrate:
                    continue
                similarity = self.cosine_scored(vec1, vec2)
                if similarity > 0:
                    matrixDict.setdefault(i, list())
                    matrixDict[i].append((j, similarity))
            if i in matrixDict:
                matrixDict[i] = heapq.nlargest(knn, matrixDict[i], key=lambda x: x[1])
            if COUNTER % int(PROCESS * config.percentage) == 0:
                print '\r%.1f%%' % (100 * COUNTER / PROCESS)
        outfile = config.CFUUserSimMatrix
        stdLib.dumpData(matrixDict, outfile)

    def adjustedCosine(self, vec1, vec2):
        su = 0.0
        l1 = 0.0
        l2 = 0.0
        avg1 = sum([vec1[i] for i in vec1]) / float(len(vec1))
        avg2 = sum([vec2[i] for i in vec2]) / float(len(vec2))
        for i in vec1:
            if i in vec2:
                su += (vec1[i] - avg1) * (vec2[i] - avg2)
                l1 += math.pow((vec1[i] - avg1), 2)
                l2 += math.pow((vec2[i] - avg2), 2)
        temp = l1 * l2
        if temp != 0:
            similarity = su / math.sqrt(temp)
        else:
            similarity = 0
        return similarity

    def dualDecentCorre(self, vec1, vec2):
        su = 0.0
        l1 = 0.0
        l2 = 0.0
        avg1 = sum([vec1[i] for i in vec1]) / float(len(vec1))
        avg2 = sum([vec2[i] for i in vec2]) / float(len(vec2))
        for i in vec1:
            if i in vec2:
                su += (vec1[i] - avg1 - self.iuAverageDict[i] + self.r) \
                      * (vec2[i] - avg2 - self.iuAverageDict[i] + self.r)
                l1 += math.pow((vec1[i] - avg1 - self.iuAverageDict[i] + self.r), 2)
                l2 += math.pow((vec2[i] - avg2 - self.iuAverageDict[i] + self.r), 2)
        temp = l1 * l2
        if temp != 0:
            similarity = su / math.sqrt(temp)
        else:
            similarity = 0
        return similarity

    def cosine_scored(self, vec1, vec2):
        su = 0.0
        l1 = 0.0
        l2 = 0.0
        for i in vec1:
            if i in vec2:
                su += vec1[i] * vec2[i]
                l1 += math.pow(vec1[i],2)
                l2 += math.pow(vec2[i],2)
        temp = l1 * l2
        if temp != 0:
            similarity = su / math.sqrt(temp)
        else:
            similarity = 0
        return similarity


if __name__ == '__main__':
    cfu = CFU()
    cfu.matrix()
