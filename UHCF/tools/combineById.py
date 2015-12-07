#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: combineById.py
@time: 15/12/7 15:06
@description: null
"""

filename = r"../result/sortedRatings.txt"
read = open(filename, 'r')
data = read.readlines()
read.close()

filename = r"../data/movies.dat"
read = open(filename, 'r')
movies = read.readlines()
read.close()

movieDict = {}

for i in movies:
    tmp = i.split("::")
    id = tmp[0]
    labels = tmp[2]
    movieDict.setdefault(id, labels)

outfile = r"../result/ratingWithLabel.txt"
out = open(outfile, 'w')

for i in data:
    tmp = i.split("::")
    movieId = tmp[1]
    tmp[3] = tmp[3][:-1]
    tmp.append(movieDict[movieId])
    out.write("::".join(tmp))

out.close()