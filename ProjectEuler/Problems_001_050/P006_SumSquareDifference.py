#!/bin/python3
"""
The sum of the squares of the first ten natural numbers is:
    1**2 + 2**2 + ... + 10**2 = 385

The square of the sum of the first ten natural numbers is:
    (1 + 2 + ... + 10)**2 = 3025

Hence the difference between the sum of the squares
of the first ten natural numbers and the square of the sum is: 3025-385 = 2640

Find the difference between the sum of the squares of the first N natural numbers and the square of the sum.
"""


def sum_square_vs_square_sum_diff(n):
    s1 = n * (n + 1) * (2 * n + 1) // 6
    s2 = (n * (n + 1) // 2) ** 2
    return abs(s1 - s2)


# print(sum_square_vs_square_sum_diff(100))
t = int(input().strip())
for _ in range(t):
    n = int(input().strip())
    print(sum_square_vs_square_sum_diff(n))
