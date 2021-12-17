"""

The 5-digit number, 16807=7**5, is also a fifth power.
Similarly, the 9-digit number, 134217728=8**9, is a ninth power.

How many n-digit positive integers exist which are also an nth power?


"""
import itertools


def show_powers(n):
    res = []
    range_start = 10 ** (n - 1)
    num_start = int(pow(range_start, 1 / n))
    range_stop = 10 * range_start
    for i in itertools.count(num_start):
        num = pow(i, n)
        if num < range_start:
            continue
        if num >= range_stop:
            break
        res.append(num)
    return res


def main_euler():
    # n = int(input())
    count = 0
    for i in range(1, 35):
        res = show_powers(i)
        print(i, len(res))
        count += len(res)
    print(count)


def main_hacker():
    n = int(input())
    for i in show_powers(n):
        print(i)


main_hacker()