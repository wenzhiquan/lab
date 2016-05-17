#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: run.py
@time: 16/3/25 下午4:29
@description: null
"""
import math
from config import config
import heapq
from lib import stdLib


class PromoteCFU(object):
    def __init__(self):
        iuDict = stdLib.loadData(config.iuDictFile)
        self.iuAverageDict = dict()
        for movie in iuDict:
            avg = sum([iuDict[movie][i] for i in iuDict[movie]]) / float(len(iuDict[movie]))
            self.iuAverageDict.setdefault(movie, avg)
        self.itemSimDict = dict()

    def iuMatrix(self, iuDict = None, knn = 500, filtrate = 5):
        '''
        calaulate the item_similarity matrix, using given simialrity method
        :param uiDict: user-item score table, data type: dict
        :threshold: qualifying the neighbour users,data type: float
        :filtrate: the criteria of filting users, data type: int
        '''
        print 'calculating the item matrix......'
        iuDict = iuDict or stdLib.loadData(config.iuDictFile)
        matrixDict = dict()
        PROCESS = len(iuDict)
        COUNTER = 0.0
        for i in iuDict:
            COUNTER += 1
            vec1 = iuDict[i]
            if len(vec1) < filtrate:
                continue
            for j in iuDict:
                if i == j:
                    continue
                vec2 = iuDict[j]
                if len(vec2) < filtrate:
                    continue
                grade = self.itemSim(vec1, vec2)
                if grade > 0:
                    matrixDict.setdefault(i, list())
                    matrixDict[i].append((j, grade))
            if i in matrixDict:
                matrixDict[i] = heapq.nlargest(knn, matrixDict[i], key=lambda x: x[1])
            if COUNTER % int(PROCESS * config.percentage) == 0:
                print '\r%.1f%%' % (100 * COUNTER / PROCESS)
        outfile = config.CFUItemSimMatrix
        stdLib.dumpData(matrixDict, outfile)

    def itemSim(self, vec1, vec2):
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

    def matrix(self, uiDict = None, knn = 200, filtrate = 5):
        '''
        calaulate the item_similarity matrix, using given simialrity method
        :param uiDict: user-item score table, data type: dict
        :threshold: qualifying the neighbour users,data type: float
        :filtrate: the criteria of filting users, data type: int
        '''
        print 'calculating the user matrix......'
        uiDict = uiDict or stdLib.loadData(config.uiDictFile)
        self.itemSimDict = stdLib.loadData(config.CFUItemSimMatrix)
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
                grade = self.fillMatrixAndCal(vec1, vec2)
                if grade > 0:
                    matrixDict.setdefault(i, list())
                    matrixDict[i].append((j, grade))
            if i in matrixDict:
                matrixDict[i] = heapq.nlargest(knn, matrixDict[i], key=lambda x: x[1])
                print matrixDict
            if COUNTER % int(PROCESS * config.percentage) == 0:
                print '\r%.1f%%' % (100 * COUNTER / PROCESS)
        outfile = config.promoteCFUUserSimMatrix
        stdLib.dumpData(matrixDict, outfile)

    def fillMatrixAndCal(self, vec1, vec2):
        su = 0.0
        l1 = 0.0
        l2 = 0.0
        upSum, downSum = 0.0, 0.0
        avg1 = sum([vec1[i] for i in vec1]) / float(len(vec1))
        avg2 = sum([vec2[i] for i in vec2]) / float(len(vec2))
        union = list(set(vec1).union(set(vec2)))
        for i in union:
            if i not in vec1 and i in self.itemSimDict:
                for data in self.itemSimDict[i]:
                    if data[0] in vec1:
                        upSum += data[1] * (vec1[data[0]] - self.iuAverageDict[data[0]])
                    else:
                        upSum += data[1] * (0 - self.iuAverageDict[data[0]])
                    downSum += data[1]
                predict = upSum / downSum
                predictGrade = self.iuAverageDict[i] + predict
                vec1.setdefault(i, predictGrade)
            if i not in vec2 and i in self.itemSimDict:
                for data in self.itemSimDict[i]:
                    if data[0] in vec1:
                        upSum += data[1] * (vec1[data[0]] - self.iuAverageDict[data[0]])
                    else:
                        upSum += data[1] * (-self.iuAverageDict[data[0]])
                    downSum += data[1]
                predict = upSum / downSum
                predictGrade = self.iuAverageDict[i] + predict
                vec2.setdefault(i, predictGrade)
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