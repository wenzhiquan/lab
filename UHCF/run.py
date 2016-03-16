#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: run.py
@time: 16/1/5 21:43
@description: null
"""
from datetime import datetime
from tools.sortByTime import sortByTime
from tools.combineById import combineById
from tools.divideTrainAndTest import divideTrainAndTest
from CFU.CFU import CFU
from core.UHCF import UHCF
from common.evaluation import Evaluation
from common.recommandation import generaRecommandList
from common.combineCFUAndTHCCF import combine
from common.movieAttr import MovieAttr
from config import config

if __name__ == '__main__':
    startTime = datetime.now()

    print 'program start......'
    print 'start time :'
    print startTime
    movieAttr = MovieAttr()
    movieAttr.commonLabel()
    if config.needDivideTrainAndTest is True:
        divideTrainAndTest()
    if config.needPreSettle is True:
        sortByTime()
        combineById()
    if config.needUHCF is True:
        uhcf = UHCF()
        uhcf.generaUserPrefer()
        uhcf.simCalculate()
        generaRecommandList(config.userSimMatrix)
    if config.needCFU is True:
        cfu = CFU()
        cfu.matrix()
        generaRecommandList()
    if config.needCombine is True:
        combine()
        generaRecommandList(config.combineSimMatrix)
    if config.needEvaluate is True:
        evaluate = Evaluation()
        rap = evaluate.recall_and_precision()
        print "recall: %5.5f%%" % rap[0]
        print "precision: %5.5f%%" % rap[1]
        fvalue = evaluate.fvalue(rap)
        print "F value: %5.5f%%" % fvalue
        outfile = r'result/evaluationResult.txt'
        out = open(outfile, 'a')
        out.write('n = ' + str(config.n) + ', listLength = ' + str(config.listLength) +
                  ', G = ' + str(config.G) + ', delta = ' + str(config.delta) +
                  '::precision = ' + str(rap[0])[:7] + '%, recall = ' + str(rap[1])[:7] +
                  '%, F value = ' + str(fvalue)[:7] + '%\n')
        out.close()
    endTime = datetime.now()
    print 'program finished......'
    print 'finish time :'
    print endTime
    print 'total run time :'
    print endTime - startTime
