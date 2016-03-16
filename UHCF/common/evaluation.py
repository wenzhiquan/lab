#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: evaluation.py
@time: 16/1/6 17:23
@description: null
"""
from config import config
import math

class Evaluation(object):
    def __init__(self, filename=None):
        resultFile = filename or config.recommandListFile
        result = open(resultFile).readlines()
        test = open(config.testFile).readlines()
        self.resultData = {}
        self.testData = {}
        for i in result:
            tmp = i[:-1].split(config.separator)
            userId = tmp[0]
            recommandList = tmp[1].split(config.subSeparator)
            self.resultData.setdefault(userId, recommandList)
        for i in test:
            tmp = i[:-1].split(config.separator)
            userId = tmp[0]
            movieId = tmp[1]
            self.testData.setdefault(userId, [])
            self.testData[userId].append(movieId)


    def recall_and_precision(self):
        """
        Get the recall and precision
        """
        result = self.resultData
        test = self.testData
        hit = 0
        recall = 0
        precision = 0
        for user in result.keys():
            tu = test.get(user, {})
            for item in result[user]:
                if item in tu:
                    hit += 1
            recall += len(tu)
            precision += config.listLength

        recall = hit * 100 / (recall * 1.0)
        precision = hit * 100 / (precision * 1.0)
        if recall != 0 and precision != 0:
            return [recall, precision]
        else:
            return [0, 0]

    def fvalue(self, rap=None):  # rap意思是recall and precision
        if rap[0] == 0 and rap[1] == 0:
            return 0
        return rap[0] * rap[1] * 2 / (rap[0] + rap[1])

    def coverage(self, train=None, test=None):
        train = train or self.train_data
        test = test or self.test_data
        recommend_items = set()
        all_items = set()
        for user in train.keys():
            for item in train[user].keys():
                all_items.add(item)
            rank = self.rank[user]
                   # or self.recommend(user, k=k, n_item=n_item)
            for item, w in rank.items():
                recommend_items.add(item)
        if len(all_items) != 0:
            cov = len(recommend_items) / (len(all_items) * 1.0)
            return cov
        else:
            return 0

    def popularity(self, train=None, test=None):
        """
        Get the popularity
        """
        train = train or self.train_data
        item_popularity = dict()
        for user, items in train.items():
            for item in items.keys():
                item_popularity.setdefault(item, 0)
                item_popularity[item] += 1
        ret = 0
        n = 0
        for user in train.keys():
            rank = self.rank[user]
                   # or self.recommend(user, k=k, n_item=n_item)
            for item, w in rank.items():
                ret += math.log(1+item_popularity.get(item, 0))
                n += 1

        if n != 0:
            result = ret / (n * 1.0)
            return result
        else:
            return 0

    def diversity(self, train=None, test=None, item_sim=None):
        """
        Get the diversity
        """
        train = train or self.train_data
        test = test or self.test_data
        item_sim = item_sim or self.item_sim
        item_diversity = 0

        for user in train.keys():
            tmp_numerator = 0
            rank = self.rank[user]
                   # or self.recommend(user, k=k, n_item=n_item)
            for item_i, wi in rank.items():
                for item_j, wj in rank.items():
                    if item_i == item_j:
                        continue
                    tmp_numerator += item_sim[item_i][item_j]
            item_diversity += 1 - tmp_numerator / (len(rank) * (len(rank) - 1) * 1.0)
        if len(train) != 0:
            item_diversity /= len(train)

        return item_diversity


if __name__ == '__main__':
    evaluate = Evaluation()
    evaluate.recall_and_precision()