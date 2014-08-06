#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wenzhiquan'

from User_based_CF import *
from datetime import *

if __name__ == "__main__":
    startTime = datetime.now()
    print "Start time is %s" % startTime
    print "Program starting..."
    item_recommend = UserBasedCF()
    #Fisrt launch
    # item_recommend.user_similarity_cosine()
    # item_recommend.item_similarity_whole()
    # rank = item_recommend.recommend()

    #To find KNN
    # item_sim_knn = item_recommend.item_sim_knn_settler()
    # rank = item_recommend.recommend(item_sim_knn)

    #Launch with knn
    # item_recommend.user_sim_data_read(r"files/user_sim_knn.dict")
    # rank = item_recommend.recommend()

    #Rank read
    item_recommend.rank_read()

    # Recommendation evaluation matrics
    print "%3s%20s%20s%20s%20s" % ('K', "recall", 'precision', 'coverage', 'popularity')
    recall_and_precision = item_recommend.recall_and_precision()
    recall = recall_and_precision[0]
    precision = recall_and_precision[1]
    coverage = item_recommend.coverage()
    popularity = item_recommend.popularity()
    print "%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (10, recall * 100, precision * 100, coverage * 100, popularity)

    finishTime = datetime.now()
    print "The whole time algorithm spends is:"
    print(finishTime-startTime)