#!/bin/python3
"""
The four adjacent digits in the 1000-digit number that have the greatest product are 9 × 9 × 8 × 9 = 5832.
Find the n adjacent digits in the given number that have the greatest product.
"""
import sys
from functools import reduce

NUMBER = """
73167176531330624919225119674426574742355349194934
96983520312774506326239578318016984801869478851843
85861560789112949495459501737958331952853208805511
12540698747158523863050715693290963295227443043557
66896648950445244523161731856403098711121722383113
62229893423380308135336276614282806444486645238749
30358907296290491560440772390713810515859307960866
70172427121883998797908792274921901699720888093776
65727333001053367881220235421809751254540594752243
52584907711670556013604839586446706324415722155397
53697817977846174064955149290862569321978468622482
83972241375657056057490261407972968652414535100474
82166370484403199890008895243450658541227588666881
16427171479924442928230863465674813919123162824586
17866458359124566529476545682848912883142607690042
24219022671055626321111109370544217506941658960408
07198403850962455444362981230987879927244284909188
84580156166097919133875499200524063689912560717606
05886116467109405077541002256983155200055935729725
71636269561882670428252483600823257530420752963450
"""


def make_product(digits, k, start):
    """
    Compute k numbers product from start position.
    :param digits:
    :param k:
    :param start:
    :return: (product, next_start)
    """
    index = 0
    product = 1
    while index < k and start + index < len(digits):
        if digits[start + index]:
            product *= digits[start + index]
            index += 1
        else:
            # if 0 found, change start to position after 0 and compute product again
            start += index + 1
            index = 0
            product = 1
    if index < k:
        # no k digit product without 0
        return 0, start
    else:
        # return k digit product starting at start position
        return product, start


def find_product(digits, k):
    """ Find max product of k consecutive digits."""
    max_product = 0
    start = 0
    while start + k <= len(digits):
        product, start = make_product(digits, k, start)
        if product > max_product:
            max_product = product
        start += 1
    return max_product


def hacker_main():
    t = int(input().strip())
    for a0 in range(t):
        n, k = map(int, input().split())
        num = input().strip()
        digits = [int(ch) for ch in num]
        product = find_product(digits, k)
        print(product)


def dev_main():
    digits = [int(ch) for ch in NUMBER.strip() if ch.isdigit()]
    product = find_product(digits, 4)
    print(product)
    product = find_product(digits, 13)
    print(product)


if __name__ == "__main__":
    hacker_main()