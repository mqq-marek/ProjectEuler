#!/bin/python3
"""
2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to N?
"""
import math


def smallest_multiple(n):
    """ Smallest multiple of all numbers from 2 to n. """
    multiple = 1
    for i in range(2, n+1):
        if multiple % i:
            multiple *= i // math.gcd(multiple, i)
    return multiple


t = int(input().strip())
for _ in range(t):
    n = int(input().strip())
    print(smallest_multiple(n))
