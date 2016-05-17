#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: UHCF.py
@time: 15/12/7 15:16
@description: null
"""
from datetime import datetime
from config import config
from math import sqrt
from lib import stdLib

class UHCF(object):
    def __init__(self):
        self.userDict = dict()  # 用于存放用户及其偏好的dictionary
        self.userPreferRateDict = dict()  # 用于存放用户及其各个标签偏好比率的dictionary
        self.timeIntervalDict = dict()
        self.now = datetime(2016, 5, 17)  # datetime.utcnow()
        self.timeInterval()

    # 生成用户偏好的函数
    def generaUserPrefer(self):
        print 'UHCF starting...'
        ratings = open(config.ratingWithLabelFile)
        data = ratings.readlines()
        length = len(data)
        ratings.close()

        count = 0.0
        for i in data:
            count += 1
            self.labelPreferCal(i)
            if count % int(length * config.percentage) == 0:
                print '%f%%' % (count * 100 / (length))
        # self.labelPreferRate()
        # self.userDict = dict()
        # for i in data:
        #     count += 1
        #     self.labelPreferCal(i, False)
        #     if count % int(length * config.percentage) == 0:
        #         print '%f%%' % (count * 100 / (length * 2))
        # 对用户标签偏好进行归一化
        for i in self.userDict:
            maxV = minV = self.userDict[i][0]
            for j in range(1, config.labelLength):
                if self.userDict[i][j] > maxV:
                    maxV = self.userDict[i][j]
                if self.userDict[i][j] < minV:
                    minV = self.userDict[i][j]
            for j in range(config.labelLength):
                self.userDict[i][j] = (self.userDict[i][j] - minV) / (maxV - minV)


        outfile = config.userPreferFile
        out = open(outfile, 'w')
        for i in self.userDict:
            result = ""
            for j in range(config.labelLength):
                if j in self.userDict[i]:
                    result += str(self.userDict[i][j]) + config.subSeparator
                else:
                    result += '0|'
            out.write(i + config.separator + result[:-1] + '\n')
        out.close()

        print 'finished...'
        return 0

    def labelPreferCal(self, line, isFirst = True):
        tmp = line[:-1].split(config.separator)
        userId = tmp[0]
        # movieId = tmp[1]
        grade = float(tmp[2])
        rateTime = datetime.utcfromtimestamp(float(tmp[3]))
        T = (self.now - rateTime - self.timeIntervalDict[userId]).days + 1  # 将打分时间距今的时间转换为天数
        if T <= 0:
            print "T: %d, id: %s" % (T, userId)
        labels = tmp[4]
        labelArr = labels.split(config.subSeparator)
        labelLen = 0  # 电影所含的标签数量
        for i in labelArr:
            if i == '1':
                labelLen += 1

        if isFirst is True:  # 是否为第一次进行训练,是否需要基于偏好进行在训练
            aGrade = grade / labelLen  # 每个标签的平均得分 TODO:按照用户以前生成的偏好对不同标签进行偏置

        self.userDict.setdefault(userId, {})

        # 对每个标签进行time hot算法的计算,得出每个标签的得分
        for j in range(config.labelLength):
            self.userDict[userId].setdefault(j, 0)
            if labelArr[j] == '1':
                if isFirst is False:
                    aGrade = grade * self.userPreferRateDict[userId][j]
                self.userDict[userId][j] += aGrade / pow(T, config.G)

    # 在训练时为每个标签计算评分
    def labelPreferRate(self):
        allRate = 0.0
        for user in self.userDict:
            for j in range(config.labelLength):
                    allRate += self.userDict[user][j]
            for j in range(config.labelLength):
                self.userPreferRateDict.setdefault(user, {})
                self.userPreferRateDict[user].setdefault(j, 0.0)
                self.userPreferRateDict[user][j] = self.userDict[user][j] / allRate

    def simCalculate(self):
        read = open(config.userPreferFile, 'r')
        data = read.readlines()
        length = len(data)
        print 'user amount %d' % length
        userMatrix = {}
        print 'similarity calculating......'
        count = 0.0
        # 根据用户偏好计算用户之间的相似度
        for i in data:
            count += 1
            tmp_i = i[:-1].split(config.separator)
            userIID = tmp_i[0]
            iLabelArr = tmp_i[1].split(config.subSeparator)
            userMatrix.setdefault(userIID, [])
            calculateDict = {}  # 存放计算出的相似度结果的dictionary
            for j in data:
                tmp_j = j[:-1].split(config.separator)
                userJID = tmp_j[0]
                if userJID == userIID:
                    continue
                else:
                    jLabelArr = tmp_j[1].split(config.subSeparator)
                    average_i = 0  # 存放用户i的评分均值
                    average_j = 0  # 存放用户j的评分均值
                    for m in range(config.labelLength):
                        average_i += float(iLabelArr[m])
                        average_j += float(jLabelArr[m])
                    average_i /= config.labelLength
                    average_j /= config.labelLength
                    fractions = 0
                    numerator_x = 0
                    numerator_y = 0
                    # 根据皮尔森算法公式进行相似度计算
                    for m in range(config.labelLength):
                        x = float(iLabelArr[m])
                        y = float(jLabelArr[m])
                        fractions += (x - average_i) * (y - average_j)
                        numerator_x += (x - average_i) ** 2
                        numerator_y += (y - average_j) ** 2
                    result = fractions / sqrt(numerator_x * numerator_y)
                    calculateDict.setdefault(userJID, result)
            # 将所有的相似度进行降序排列
            sortedSimGrade = sorted(calculateDict.iteritems(), key=lambda d: d[1], reverse=True)
            for m in range(config.n):
                userMatrix[userIID].append(sortedSimGrade[m])
            if count % int(length * config.percentage) == 0:
                print '%.3f%%' % (count * 100 / length)
        outfile = config.userSimMatrix
        stdLib.dumpData(userMatrix, outfile)

        print 'finished......'

    def timeInterval(self):
        print 'calculating time interval......'
        filename = config.ratingWithLabelFile
        read = open(filename, 'r')
        data = read.readlines()
        read.close()

        initTime = datetime.utcfromtimestamp(0)

        for i in data:
            tmp = i[:-1].split(config.separator)
            userId = tmp[0]
            time = datetime.utcfromtimestamp(float(tmp[3]))
            self.timeIntervalDict.setdefault(userId, initTime)
            if time > self.timeIntervalDict[userId]:
                self.timeIntervalDict[userId] = time

        for userId in self.timeIntervalDict:
            self.timeIntervalDict[userId] = self.now - self.timeIntervalDict[userId]

