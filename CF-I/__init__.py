#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wenzhiquan'

from Item_based_CF import *
from datetime import *

if __name__ == "__main__":
    startTime = datetime.now()
    print "Start time is %s" % startTime
    print "Program starting..."
    item_recommend = ItemBasedCF()
    #Fisrt launch
    # item_recommend.correlation_based_sim()
    # item_recommend.item_similarity_whole()
    # rank = item_recommend.recommend()

    #To find KNN
    # item_sim_knn = item_recommend.item_sim_knn_settler()
    # rank = item_recommend.recommend(item_sim_knn)

    #Launch with knn
    item_recommend.item_sim_data_read(r"files/item_sim_cb.dict")
    # rank = item_recommend.recommend()

    #Rank read
    item_recommend.rank_read()

    # Recommendation evaluation matrics
    print "%3s%20s%20s%20s%20s%20s" % ('K', "recall", 'precision', 'coverage', 'popularity', 'diversity')
    for k in [5, 10, 20, 40, 80, 160]:
        recall_and_precision = item_recommend.recall_and_precision(k=k)
        recall = recall_and_precision[0]
        precision = recall_and_precision[1]
        coverage = item_recommend.coverage(k=k)
        popularity = item_recommend.popularity(k=k)
        diversity = item_recommend.diversity(k=k)
        print "%3d%19.3f%%%19.3f%%%19.3f%%%20.3f%19.3f%%" \
              % (k, recall * 100, precision * 100, coverage * 100, popularity, diversity * 100)

    finishTime = datetime.now()
    print "The whole time algorithm spends is:"
    print(finishTime-startTime)