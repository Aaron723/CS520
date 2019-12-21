# -*- coding: utf-8 -*-
# @Time    : 12/15/19 16:20
# @Author  : Ziqi Wang
# @FileName: Naive Bayesian.py
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


def NB_onepoint(point):
    isA = pA1[tuple(point)]
    isB = pB1[tuple(point)]
    return isA, isB


def NB_oneimage(image):
    point_list = np.argwhere(image == 1)
    result = 0
    A_p = []
    B_p = []
    for point in point_list:
        tempA, tempB = NB_onepoint(point)
        A_p.append(tempA)
        B_p.append(tempB)

    finalA = 1
    finalB = 1
    for i in range(len(point_list)):
        finalA *= A_p[i]
        finalB *= B_p[i]
    print('likelihood of A:', finalA, 'likelihood of B:', finalB)
    if finalA > finalB:
        return 'Class A'
    else:
        return 'Class B'


cA = readFile(pathA)
cB = readFile(pathB)
cM = readFile(pathM)

# the possibility of every points be 1(on every matrix)
#  + 1 mean we add some bias on this dataset
pA1 = (cA.sum(axis=0) + 1) / 6
pB1 = (cB.sum(axis=0) + 1) / 6

for ii in cM:
    print('prediction:', NB_oneimage(ii))
