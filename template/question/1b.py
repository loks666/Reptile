import math


def test():
    num = int(input())
    s = 0

    def f1(n):
        if n <= 1:
            return False
        else:
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True

    for i in range(1, num + 1):
        if f1(i) is True and f1(i + 2) is True and (i + 2) <= num:
            s += 1
    print(s)


if __name__ == '__main__':
    test()
