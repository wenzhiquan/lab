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

spliter = '::'
G = 1.8
delta = 5

def UHCF(filename):
    ratings = open(filename)
    data = ratings.readlines()
    ratings.close()

    userDict = {}

    for i in data:
        tmp = i[:-1].split(spliter)
        userId = tmp[0]
        movieId = tmp[1]
        grade = int(tmp[2])
        RateTime = datetime.utcfromtimestamp(float(tmp[3]))
        T = (datetime.utcnow() - RateTime).days
        labels = tmp[4]
        labelArr = labels.split('|')
        aGrade = grade / len(labelArr)

        userDict.setdefault(userId, {})
        for j in labelArr:
            userDict[userId].setdefault(j, aGrade / pow(T + delta, G))
            userDict[userId][j] = userDict[userId][j] + aGrade / pow(T + delta, G)

    for i in userDict:
        print userDict[i]

    return 0


if __name__ == '__main__':
    UHCF("result/ratingWithLabel.txt")
