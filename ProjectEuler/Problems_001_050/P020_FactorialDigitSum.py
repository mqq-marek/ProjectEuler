"""

Find the sum of the digits in the number n!

"""

import math


def digits_sum(n):
    fn = math.factorial(n)
    return sum(int(ch) for ch in str(fn))


def hacker_main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        result = digits_sum(n)
        print(result)


# print(digits_sum(100))
hacker_main()