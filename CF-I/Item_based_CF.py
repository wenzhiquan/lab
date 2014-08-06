#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wenzhiquan'

import random
import math
from stdLib import *


class ItemBasedCF():
    def __init__(self):
        self.test_data = dict()
        self.train_data = dict()
        self.item_sim = dict()
        self.data_settled_ui = dict()
        self.data_settled_iu = dict()
        self.rank = dict()

        self.data_settler()
        self.split_data()

    def data_settler(self, filename=r"files/ratings.dat"):
        print "Reading data..."
        file = open(filename, 'r')
        datas = file.readlines()

        for i in range(len(datas)):
            datas[i] = datas[i].split("::")
            if datas[i][0] not in self.data_settled_ui:
                self.data_settled_ui[datas[i][0]] = dict()
                self.data_settled_ui[datas[i][0]][datas[i][1]] = datas[i][2]
            elif datas[i][0] in self.data_settled_ui:
                self.data_settled_ui[datas[i][0]][datas[i][1]] = datas[i][2]

            if datas[i][1] not in self.data_settled_iu:
                self.data_settled_iu[datas[i][1]] = dict()
                self.data_settled_iu[datas[i][1]][datas[i][0]] = datas[i][2]
            elif datas[i][1] in self.data_settled_iu:
                self.data_settled_iu[datas[i][1]][datas[i][0]] = datas[i][2]
        print "Data settled..."

    def item_sim_data_read(self, filename=r"files/item_sim.dict"):
        self.item_sim = loadData(filename)

    def rank_read(self, filename=r"files/user_rank_20.dict"):
        self.rank = loadData(filename)

    def split_data(self, k=4, seed=100, m=10):
        ui_data = self.data_settled_ui
        random.seed(seed)
        for user, items in ui_data.items():
            for item, rating in items.items():
                if random.randint(0, m) == k:
                    self.test_data.setdefault(user, {})
                    self.test_data[user][item] = rating
                else:
                    self.train_data.setdefault(user, {})
                    self.train_data[user][item] = rating
        print "Data split finished..."

    def item_similarity_whole(self):
        print "Computing item similarity...."
        for item_i in self.data_settled_iu.keys():
            for item_j in self.data_settled_iu.keys():
                if item_i == item_j:
                    continue
                self.item_sim.setdefault(item_i, {})
                numerator = len(set(self.data_settled_iu[item_i].keys()) & set(self.data_settled_iu[item_j].keys()))
                denominator = math.sqrt(len(self.data_settled_iu[item_i]) * len(self.data_settled_iu[item_j]) * 1.0)
                self.item_sim[item_i][item_j] = numerator / denominator
        dumpData(self.item_sim, r"files/item_sim.dict")
        print "Compute finished..."

    def correlation_based_sim(self):
        print "Computing item similarity...."

        iu = self.data_settled_iu
        ui = self.data_settled_ui

        average = dict()
        numerator = 0
        denominator = [0, 0, 0]
        for items, users in self.data_settled_iu.items():
            if len(users) != 0:
                for rating in users.values():
                    average.setdefault(items, 0)
                    average[items] += int(rating)
                average[items] /= len(users)
            else:
                average[items] = 0

        for item_i in iu.keys():
            for item_j in iu.keys():
                if item_i == item_j:
                    continue
                for user in set(iu[item_i].keys()) & set(iu[item_j].keys()):
                    numerator += (int(ui[user][item_i]) - average[item_i]) * (int(ui[user][item_j]) - average[item_j]) * 1.0
                    denominator[1] += (int(ui[user][item_i]) - average[item_i]) ** 2
                    denominator[2] += (int(ui[user][item_j]) - average[item_j]) ** 2
                denominator[0] = math.sqrt(denominator[1] * denominator[2] * 1.0)
                if denominator[0] != 0:
                    self.item_sim.setdefault(item_i, {})
                    self.item_sim[item_i].setdefault(item_j, 0)
                    self.item_sim[item_i][item_j] = numerator / denominator[0]
                else:
                    self.item_sim.setdefault(item_i, {})
                    self.item_sim[item_i].setdefault(item_j, 0)
        dumpData(self.item_sim, r"files/item_sim_cb.dict")
        print "Compute finished..."

    def item_sim_knn_settler(self, k=200):
        print "Settling item similarity...."
        self.item_sim_data_read()
        item_sim_knn = self.item_sim
        for item_i, item_j in item_sim_knn.items():
            item_sim_knn[item_i] = dict(sorted(item_j.items(), key=lambda x: x[1], reverse=True)[0:k])
        dumpData(item_sim_knn, r"files/item_sim_knn.dict")
        return item_sim_knn

        print "Settle finished..."

    def recommend(self, train=None, item_sim_in=None, n_item=20):
        item_sim = item_sim_in or self.item_sim
        train = train or self.train_data
        for k in [5, 10, 20, 40, 80, 160]:
            for user in train.keys():
                print "Recommending for user %s" % user, "K value is %d" % k
                ru = train.get(user, {})
                for i, pi in ru.items():
                    for j, wj in item_sim[i].items()[0:k]:
                        if j in ru:
                            continue
                        self.rank.setdefault(k, {})
                        self.rank[k].setdefault(user, {})
                        self.rank[k][user].setdefault(j, 0)
                        self.rank[k][user][j] += float(pi) * float(wj)
                self.rank[k][user] = dict(self.rank[k][user].items()[0:n_item])
        dumpData(self.rank, r"files/user_rank_20_cb.dict")
        return self.rank

    def recall_and_precision(self, train=None, test=None, k=200, n_item=20):
        """
        Get the recall and precision
        """
        train = train or self.train_data
        test = test or self.test_data
        hit = 0
        recall = 0
        precision = 0
        for user in train.keys():
            tu = test.get(user, {})
            rank = self.rank[k][user]
            for item, w in rank.items():
                if item in tu:
                    hit += 1
            recall += len(tu)
            precision += n_item

        if recall != 0 and precision != 0:
            return [hit / (recall * 1.0), hit / (precision * 1.0)]
        else:
            return [0, 0]

    def coverage(self, train=None, test=None, k=200):
        train = train or self.train_data
        test = test or self.test_data
        recommend_items = set()
        all_items = set()
        for user in train.keys():
            for item in train[user].keys():
                all_items.add(item)
            rank = self.rank[k][user]
                   # or self.recommend(user, k=k, n_item=n_item)
            for item, w in rank.items():
                recommend_items.add(item)
        if len(all_items) != 0:
            cov = len(recommend_items) / (len(all_items) * 1.0)
            return cov
        else:
            return 0

    def popularity(self, train=None, test=None, k=200):
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
            rank = self.rank[k][user]
                   # or self.recommend(user, k=k, n_item=n_item)
            for item, w in rank.items():
                ret += math.log(1+item_popularity.get(item, 0))
                n += 1

        if n != 0:
            result = ret / (n * 1.0)
            return result
        else:
            return 0

    def diversity(self, train=None, test=None, k=200, item_sim=None):
        """
        Get the diversity
        """
        train = train or self.train_data
        test = test or self.test_data
        item_sim = item_sim or self.item_sim
        item_diversity = 0

        for user in train.keys():
            tmp_numerator = 0
            rank = self.rank[k][user]
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

