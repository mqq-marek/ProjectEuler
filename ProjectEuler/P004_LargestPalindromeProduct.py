#!/bin/python3
"""
A palindromic number reads the same both ways.
The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 * 99.

Find the largest palindrome made from the product of two 3-digit numbers which is less than given number n.
"""


def is_3x3_digit_product(num):
    """Verify that number is product of two 3 digits numbers."""
    for j in range(100, 999 + 1):
        if num % j == 0 and 100 <= num // j <= 999:
            return True
    return False


def palindrome(n):
    """Build palindrome integer."""
    return int(str(n) + str(n)[::-1])


def find_palindrome(n):
    """Find palindrome not greater than n."""
    start = n // 1000
    # Search down
    for i in range(start, 100 - 1, -1):
        p = palindrome(i)
        if p < n and is_3x3_digit_product(p):
            return p


# print(find_palindrome(999999))
t = int(input().strip())
for _ in range(t):
    n = int(input().strip())
    print(find_palindrome(n))
