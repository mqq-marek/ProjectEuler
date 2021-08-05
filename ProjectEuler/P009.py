#!/bin/python3
"""
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which, a**2 + b**2 = c**2
For example, 32 + 42 = 9 + 16 = 25 = 52.

For given sum of Pythagorean triplet (n = a + b + c) find the greatest product abc.
"""
import math

# Definition for triangle
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

# Definitions for triangle2
# Triangle is based on two parameters.
# For Pythagorean triangle a, b, c can be decomposed as k*(x**2-y**2), 2*k*x*y and k*(x**2+y**2).
# We still have that c < n // 2 this gives us that x ** 2 < n // 2 and y**2 < n // 4 (as x > y)


def triangle2(n):
    product = -1
    y_limit = int(math.sqrt(n) + 1) // 2
    x_limit = int(math.sqrt(n/2) + 1)
    for y in range(1, y_limit):
        y2 = y * y
        for x in range(y + 1, x_limit):
            x2 = x * x
            a_b_c = 2 * (x2 + x * y)
            if n % a_b_c:
                continue
            k = n // a_b_c
            p = 2 * x * y * (x2 + y2) * (x2 - y2) * k * k * k
            if p > product:
                product = p
    return product


def hacker_main():
    t = int(input().strip())
    for a0 in range(t):
        n = int(input().strip())
        print(triangle2(n))


def dev_main():
    for i in range(12, 2000):
        p = triangle(i)


if __name__ == '__main__':
    print(triangle2(1000))
    hacker_main()
