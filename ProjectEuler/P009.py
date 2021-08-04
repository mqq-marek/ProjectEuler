#!/bin/python3

import math

sqrt2 = math.sqrt(2)
# a**2 + b**2 = c**2, a <= b < c
s1 = 1 / (2 + sqrt2)        # 1 <= a <= s1 * (a + b + c) = n,  s1 * n < b < n //2
s2 = sqrt2 / (2 + sqrt2)    # s2 * n < c <= n//2


def triangle(n):
    product = -1
    for c in range(int(s2 * n), n // 2):
        c_sqr = c * c
        for b in range(min((n - c) // 2, int(s1 * n)), max(n // 2, c)):
            a = n - c - b
            if c_sqr == b ** 2 + a ** 2:
                p = c * b * a
                if p > product:
                    product = p
                    return product
    return product


def hacker_main():
    t = int(input().strip())
    for a0 in range(t):
        n = int(input().strip())
        print(triangle(n))


def dev_main():
    for i in range(12, 2000):
        p = triangle(i)


if __name__ == '__main__':
    hacker_main()
