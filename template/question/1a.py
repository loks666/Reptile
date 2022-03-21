#!/usr/bin/python
# coding:utf8

import itertools


def test():
    s_line1 = input()
    s_line2 = input()
    s_line3 = input()
    l_line1 = s_line1.split(" ")
    l_line2 = s_line2.split(" ")
    l_line3 = s_line3.split(" ")
    # 第一行参数
    k = int(l_line1[0])
    a_num = int(l_line1[1])
    b_num = int(l_line1[2])
    # 第二行参数
    a_scores = [int(i) for i in l_line2]
    # 第三行参数
    b_scores = [int(i) for i in l_line3]

    min_ab = []
    max_ab = []
    min_ab_num = min(len(a_scores), len(a_scores))

    if len(a_scores) == min_ab_num:
        min_ab = a_scores
        max_ab = b_scores
    else:
        min_ab = b_scores
        max_ab = a_scores

    fit_num = 0
    for i in itertools.permutations(max_ab, min_ab_num):
        fit_num = max(fit_num, len(list(filter(lambda x: x <= k, list(map(lambda x, y: abs(x - y), min_ab, list(i)))))))
    print(fit_num)


if __name__ == '__main__':
    test()
