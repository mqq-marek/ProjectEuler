#!/bin/python3
"""
The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?
"""

import math


def largest_prime_factor(n):
    """Find largest prime divisor."""

    def get_divisor(start, num):
        """Get divisor."""
        max_divisor = int(math.sqrt(num)) + 1
        for j in range(start, max_divisor + 1):
            if num % j == 0:
                return j
        return num

    ld = get_divisor(2, n)
    while ld != n:
        n //= ld
        ld = get_divisor(ld, n)
    return n


t = int(input().strip())
for _ in range(t):
    n = int(input().strip())
    print(largest_prime_factor(n))
