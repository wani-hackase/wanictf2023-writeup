import random

k = 36
maxlength = 16


def f(x, cnt):
    cnt += 1
    r = 2**k
    if x == 0 or x == r:
        return -x, cnt
    if x * x % r != 0:
        return -x, cnt
    else:
        return -x * (x - r) // r, cnt


def g(x):
    ret = x * 2 + x // 3 * 10 - x // 5 * 10 + x // 7 * 10
    ret = ret - ret % 2 + 1
    return ret, x // 100 % 100


def digit(x):
    cnt = 0
    while x > 0:
        cnt += 1
        x //= 10
    return cnt


def pad(x, cnt):
    minus = False
    if x < 0:
        minus = True
        x, cnt = g(-x)
    sub = maxlength - digit(x)
    ret = x
    for i in range(sub - digit(cnt)):
        ret *= 10
        if minus:
            ret += pow(x % 10, x % 10 * i, 10)
        else:
            ret += pow(i % 10 - i % 2, i % 10 - i % 2 + 1, 10)
    ret += cnt * 10 ** (maxlength - digit(cnt))
    return ret


def int_generator(x):
    ret = -x
    x_, cnt = f(x, 0)
    while x_ > 0:
        ret = x_
        x_, cnt = f(x_, cnt)
    return pad(ret, cnt)


target1 = 1008844668800884
target2 = 2264663430088446
target3 = 6772814078400884

divisor = 2 ** (k // 2)
bound = 2 ** (k // 2 - 1)

for i in range(bound + 1):
    ni = int_generator(i * divisor)
    if ni == target1:
        print("flag1:{}".format(i * divisor))
    if ni == target2:
        print("flag2:{}".format(i * divisor))
    if ni == target3:
        print("flag3:{}".format(i * divisor))
