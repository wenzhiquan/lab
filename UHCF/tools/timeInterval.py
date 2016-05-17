#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: timeInterval.py
@time: 16/5/17 下午3:01
@description: null
"""
from config import config
from datetime import datetime
from lib import stdLib

def timeInterval():
    print 'calculating time interval......'
    filename = config.trainFile
    read = open(filename, 'r')
    data = read.readlines()
    read.close()

    userDict = dict()
    now = datetime(2016, 5, 17)
    maxTime = datetime.utcfromtimestamp(0)
    resultDict = dict()

    for i in data:
        tmp = i[:-1].split(config.separator)
        userId = tmp[0]
        time = datetime.utcfromtimestamp(float(tmp[3]))
        userDict.setdefault(userId, maxTime)
        if time > userDict[userId]:
            userDict[userId] = time

    for userId in userDict:
        userDict[userId] = now - userDict[userId]

    outfile = config.timeIntercalDict
    stdLib.dumpData(userDict, outfile)
