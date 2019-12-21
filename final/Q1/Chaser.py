#!/usr/bin/env python
# encoding: utf-8
# @project : Final
# @author: Ziqi Wang
# @file: Chaser.py
# @time: 2019-12-17 10:39:50

import numpy as np
import matplotlib.pyplot as plt
import time
import random


class Chase:
    def __init__(self):
        dots = np.random.choice(64, 3, replace=False)
        # dots = [32, 51, 7]
        self.sheep = Dot(dots[0])
        self.dog_1 = Dot(dots[1])
        self.dog_2 = Dot(dots[2])
        self.count = 0
        self.flag1 = False
        self.flag2 = False

    def check_neighbor(self):
        direct_list = [-8, -1, 1, 8]
        direct_list_temp = [-8, -1, 1, 8]
        for direct in direct_list_temp:
            if not self.check_move(0, direct):
                direct_list.remove(direct)
        return direct_list
    def check_move(self, num, direct):
        pos_list = [self.sheep.pos, self.dog_1.pos, self.dog_2.pos]
        new_pos = pos_list.pop(num) + direct
        if new_pos == pos_list[0] or new_pos == pos_list[1] or not self.check_valid(num, direct): return False
        return True

    def check_valid(self, num, direct):
        pos_list = [self.sheep.pos, self.dog_1.pos, self.dog_2.pos]
        if direct == -8 and pos_list[num] - 8 < 0: return False
        if direct == 8 and pos_list[num] + 8 > 63: return False
        if direct == -1 and (pos_list[num] - 1) % 8 == 7: return False
        if direct == 1 and (pos_list[num] + 1) % 8 == 0: return False
        return True

    def sheep_move(self):
        move_list = self.check_neighbor()
        if not move_list:
            return self.sheep.pos != 0
        pos = self.sheep.pos + np.random.choice(move_list)
        self.sheep = Dot(pos)
        return True

    def dog_move(self, num, direct):
        if self.check_move(num, direct):
            if num == 1:
                pos_1 = self.dog_1.pos + direct
                self.dog_1 = Dot(pos_1)
            elif num == 2:
                pos_2 = self.dog_2.pos + direct
                self.dog_2 = Dot(pos_2)
    def move_direct(self, num, dot, des):
        temp_list = [-1, -8]
        if dot.pos > des:
            if dot.i == des // 8 and self.check_move(num, -1):
                return -1
            elif dot.i > des // 8:
                if dot.j < des % 8 and self.check_move(num, 1):
                    return 1
                elif dot.j >= des % 8 and self.check_move(num, -8):
                    if dot.j == des % 8:
                        return -8
                    if self.check_move(num, -1):
                        return random.choice(temp_list)
        elif dot.pos < des:
            if dot.i == des // 8:
                if num == 1 and self.check_move(num, 1):
                    return 1
                elif num == 2 and self.check_move(num, 8):
                    return 8
            elif dot.i < des // 8 and self.check_move(num, 8):
                if dot.j < des % 8 and self.check_move(num, 1):
                    return 1
                elif num == 1 and dot.j == des % 8 and self.check_move(num, 1):
                    return 1
                elif dot.j >= des % 8 and self.check_move(num, 8):
                    return 8
        return 0

    def set_destiny(self):

        # move_list = self.check_neighbor()
        if self.sheep.pos + 8 == self.dog_2.pos:
            self.flag2 = True
        elif self.sheep.pos + 1 == self.dog_1.pos:
            self.flag1 = True

        if self.flag1 or self.flag2:
            return int(self.sheep.pos + 1), int(self.sheep.pos + 8)
        return int(self.sheep.pos + 8), int(self.sheep.pos + 1)

    def pic_plot(self):
        tmp_arr = np.zeros((8, 8))
        tmp_arr[0][0] = -1
        tmp_arr[int(self.sheep.pos // 8)][int(self.sheep.pos % 8)] = 2
        tmp_arr[int(self.dog_1.pos // 8)][int(self.dog_1.pos % 8)] = 1
        tmp_arr[int(self.dog_2.pos // 8)][int(self.dog_2.pos % 8)] = 1
        plt.figure(figsize=(5, 5))
        plt.pcolor(tmp_arr[::-1], edgecolors='black', cmap='seismic', linewidths=2)
        plt.xticks([]), plt.yticks([])
        plt.tight_layout()
        plt.show()

    def run(self):
        while self.sheep_move():
            des1, des2 = self.set_destiny()
            direct1 = self.move_direct(1, self.dog_1, des1)
            direct2 = self.move_direct(2, self.dog_2, des2)
            self.dog_move(1, direct1)
            self.dog_move(2, direct2)
            self.count += 1
            if self.count > 10000:
                # self.plot()
                move_list = self.check_neighbor()
                if self.sheep.pos == 63 and not move_list:
                    return -1
                elif self.sheep.pos == 56 and not move_list:
                    return -2
                # continue
                # return -1
            # print(self.count)
            # self.pic_plot()
            # time.sleep(0.5)
        return int(self.count)


class Dot:
    def __init__(self, pos):
        self.pos = pos
        self.i = pos // 8
        self.j = pos % 8


def test():
    chase = Chase()
    res = chase.run()
    # print(res)
    return res


file = "/Users/ziwan/PycharmProjects/final/Q1/result.txt"
if __name__ == '__main__':
    result, fail_1, fail_2 = 0, 0, 0
    for i in range(100000):
        temp = test()
        if temp != -1:
            result += temp
        elif temp == -1:
            fail_1 += 1
        else:
            fail_2 += 1
        with open('/Users/ziwan/PycharmProjects/final/Q1/result.txt', 'w') as f:
            f.write(str(result) + "," + str(result // (i + 1)) + "," + str(fail_1) + "," + str(fail_2))
