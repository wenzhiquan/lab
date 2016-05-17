#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: config.py
@time: 16/1/5 17:48
@description: null
"""
from os import path
from sys import argv
from ConfigParser import ConfigParser

conf = ConfigParser()
conf.read('config/config.ini')


# 文件各项之间的分隔符
separator = conf.get('mainconf', 'separator')
subSeparator = conf.get('mainconf', 'subseparator')

# meta file为元数据文件存放的位置
metaRatingFile = path.join(path.dirname(argv[0]), conf.get('fileconf', 'metaRatingFile'))
metaMovieFile = path.join(path.dirname(argv[0]), conf.get('fileconf', 'metaMovieFile'))

# 训练集和测试集
trainFile = path.join(path.dirname(argv[0]), r'result/trainRatings.txt')
testFile = path.join(path.dirname(argv[0]), r'result/testRatings.txt')
uiDictFile = path.join(path.dirname(argv[0]), r'result/uiDict.dict')
iuDictFile = path.join(path.dirname(argv[0]), r'result/iuDict.dict')
# sorted file为将元数据按照时间先后顺序排列的文件
sortedRatingFile = path.join(path.dirname(argv[0]), r'result/sortedRatings.txt')

# label file为将排序后的文件后面接上对应电影的label生成的文件
ratingWithLabelFile = path.join(path.dirname(argv[0]), r'result/ratingWithLabels.txt')

# user prefer file为存放计算出的用户偏好的文件
userPreferFile = path.join(path.dirname(argv[0]), r'result/userPrefer.txt')

# 用于存放与用户最相似的n个用户的文件
n = 100
listLength = 50  # 推荐列表长度
userSimMatrix = path.join(path.dirname(argv[0]), r'result/userSimMatrix.dict')
CFUUserSimMatrix = path.join(path.dirname(argv[0]), r'result/CFUUserSimMatrix.dict')
combineSimMatrix = path.join(path.dirname(argv[0]), r'result/combineSimMatrix.dict')
CFUItemSimMatrix = path.join(path.dirname(argv[0]), r'result/CFUItemSimMatrix.dict')
promoteCFUUserSimMatrix = path.join(path.dirname(argv[0]), r'result/promoteCFUUserSimMatrix.dict')
recommendDict = path.join(path.dirname(argv[0]), r'result/recommend.dict')
timeIntercalDict = path.join(path.dirname(argv[0]), r'result/timeInterval.dict')

# 用于存放推荐列表的文件
recommendListFile = path.join(path.dirname(argv[0]), r'result/recommendGradeList.txt')

needDivideTrainAndTest = False  # 是否需要划分测试集和训练集
needPreSettle = False  # 是否需要预处理数据
needCFU = False  # 是否需要运行CFU
needUHCF = True  # 是否需要进行UHCF的运算
needCombine = False  # 是否需要合并CFU和UHCF用户矩阵
needEvaluate = True  # 是否需要进行评价


# UHCF计算时的time hot算法的参数
G = 1.3  # G为time hot算法的衰减参数,越大衰减越厉害,时间越近的值权重越大
delta = 500  # delta 为移动坐标轴的参数

percentage = 0.05  # 运行时每次显示的完成百分比

# label dictionary 为所有电影的类型及其编号
labelDict = {
    'unknown': 0,
    'Action': 1,
    'Adventure': 2,
    'Animation': 3,
    "Children's": 4,
    'Comedy': 5,
    'Crime': 6,
    'Documentary': 7,
    'Drama': 8,
    'Fantasy': 9,
    'Film-Noir': 10,
    'Horror': 11,
    'Musical': 12,
    'Mystery': 13,
    'Romance': 14,
    'Sci-Fi': 15,
    'Thriller': 16,
    'War': 17,
    'Western': 18,
    # 'IMAX': 19
}
labelLength = len(labelDict)
