#!/usr/bin/python
# coding:utf8

import random

zuobi = False
b = random.randint(1, 10)
fg = False


def number_right(one, two):
    global b
    low = "too low"
    high = "too high"
    correct = "correct"
    pri_list = (low, high, correct)
    if one < two:
        print_result(low, pri_list)
        return False
    elif one > two:
        print_result(high, pri_list)
        return False
    else:
        print_result(correct, pri_list)
        return True


def print_result(out, pri_list):
    global zuobi
    result = random_run()
    if result:
        print(out)
    else:
        zuobi = True
        print(pri_list[random.randint(1, 3) - 1])


def random_run():
    probability = 1
    math = []
    for i in range(probability):
        math.append(1)
    for x in range(100 - probability):
        math.append(0)
    return random.choice(math)


while True:
    a = input()
    if '0' == a:
        if zuobi:
            print("yes")
        else:
            print("maybe")
            continue
    else:
        number_right(int(a), b)

if __name__ == '__main__':
    number_right()
