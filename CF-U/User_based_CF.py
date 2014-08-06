#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wenzhiquan'

import random
import math
from stdLib import *

class UserBasedCF:
    def __init__(self):
        self.test_data = dict()
        self.train_data = dict()
        self.user_sim = dict()
        self.item_users = dict()
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

        for u, item in self.train_data.items():
            for i in item.keys():
                self.item_users.setdefault(i, set())
                self.item_users[i].add(u)
        print "Data split finished..."

    def user_sim_data_read(self, filename=r"files/user_sim.dict"):
        self.user_sim = loadData(filename)

    def rank_read(self, filename=r"files/user_rank_20_cos.dict"):
        self.rank = loadData(filename)

    def user_similarity_whole(self,train = None):
        train = train or self.train_data
        self.userSimBest = dict()

        user_item_count = dict()
        count = dict()
        for item, users in item_users.items():
            for u in users:
                user_item_count.setdefault(u, 0)
                user_item_count[u] += 1
                for v in users:
                    if u == v:
                        continue
                    count.setdefault(u, {})
                    count[u].setdefault(v, 0)
                    count[u][v] += 1
        for u, related_users in count.items():
            self.userSimBest.setdefault(u, dict())
            for v, cuv in related_users.items():
                if cuv != 0:
                    self.userSimBest[u][v] = cuv / math.sqrt(user_item_count[u] * user_item_count[v] * 1.0)


    def user_similarity_cosine(self, knn=10):
        train = self.train_data

        average = dict()
        denominator = dict()
        user_sim = dict()

        for user, items in train.items():
            if len(items) != 0:
                for rating in items.values():
                    average.setdefault(user, 0)
                    average[user] += int(rating)
                average[user] /= len(items)
                for rating in items.values():
                    denominator.setdefault(user, 0)
                    denominator[user] += math.sqrt((int(rating) - average[user]) ** 2)
            else:
                average[user] = 0
        print "Average and denominator settled..."

        for u, ui in train.items():
            for v, vi in train.items():
                if u == v:
                    continue
                combine = set(ui.keys()) & set(vi.keys())
                if len(combine) != 0:
                    numerator = 0
                    for item in combine:
                        numerator += (int(ui[item]) - average[u]) * (int(vi[item]) - average[v]) * 1.0
                    denomin = (denominator[u] * denominator[v] * 1.0)
                    if numerator == 0 or denomin == 0:
                        continue
                    else:
                        user_sim.setdefault(u, {})
                        user_sim[u].setdefault(v, 0)
                        user_sim[u][v] = numerator / denomin * 1.0
            if u in user_sim.keys():
                user_sim[u] = dict(sorted(user_sim[u].items(), key=lambda x: x[1], reverse=True)[0:knn])
                print "Sim for ", u, "is settled."

        dumpData(user_sim, "files/user_sim_knn.dict")

    def recommend(self, train=None, n_item=20):
        user_sim =  self.user_sim
        train = train or self.train_data
        for user in train.keys():
            print "Recommending for user %s" % user
            ru = train.get(user, {})
            for i, pi in ru.items():
                if i in user_sim.keys():
                    for j, wj in user_sim[i].items():
                        if j in ru:
                            continue
                        self.rank.setdefault(user, {})
                        self.rank[user].setdefault(j, 0)
                        self.rank[user][j] += float(pi) * float(wj)
            self.rank[user] = dict(sorted(self.rank[user].items(), key=lambda x: x[1], reverse=True)[0:n_item])
        dumpData(self.rank, r"files/user_rank_20_cos.dict")
        return self.rank

    def recall_and_precision(self, train=None, test=None, n_item=20):
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
            rank = self.rank[user]
            for item, w in rank.items():
                if item in tu:
                    hit += 1
            recall += len(tu)
            precision += n_item

        if recall != 0 and precision != 0:
            return [hit / (recall * 1.0), hit / (precision * 1.0)]
        else:
            return [0, 0]

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