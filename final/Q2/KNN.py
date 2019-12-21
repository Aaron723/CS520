# -*- coding: utf-8 -*-
# @Time    : 12/15/19 16:49
# @Author  : Ziqi Wang
# @FileName: KNN.py
# @email    ：zw280@scarletmail.rutgers.edu
import numpy as np

pathA = 'ClassA.txt'
pathB = 'ClassB.txt'
pathM = 'Mystery.txt'


def readFile(path):
    class_list = []
    with open(path) as file:
        for line in file:
            newline = line.rstrip('\n').split('\t')
            if newline != ['']:
                class_list.append(newline)
    return np.array(class_list).astype('int').reshape((5, 5, 5))


cA = readFile(pathA)
cB = readFile(pathB)
cM = readFile(pathM)


def KNN(dataset, matrix):
    dist = 0
    for item in dataset:
        # the euclidean distance between the training data and the test data
        dist += np.sqrt(np.sum(np.square(item - matrix)))
    return dist / 5


def trad_KNN(dataset, matrix, K):
    dist = []
    vote_A, vote_B = 0, 0
    # the first five belong to A and the latter five belong to B
    for item in dataset:
        # the euclidean distance between the training data and the test data
        d = np.sqrt(np.sum(np.square(item - matrix)))
        dist.append(d)
    # sort the distance list. i < 5 means it belongs to A, otherwise B
    voteIndex = np.argsort(dist)
    for i in range(0, K):
        if voteIndex[i] < 5:
            vote_A += 1
        else:
            vote_B += 1
    print('matrix belongs to{clss}'.format(clss='A' if vote_A >= vote_B else 'B'))
    print(vote_A)
    print(vote_B)


# the test of the average distance KNN(not traditional KNN)
'''
dist_A = []
dist_B = []
for matrix in cM:
    dist_A, dist_B = KNN(cA, matrix), KNN(cB, matrix)
    if dist_A < dist_B:
        print('Class A')
    else:
        print('Class B')
    print('dist_A: {}, dist_B: {}'.format(dist_A, dist_B))
'''

# traditional KNN

K = 4
for matrix in cM:
    dataset = np.append(cA, cB, axis=0)
    trad_KNN(dataset, matrix, K)
