"""

An irrational decimal fraction is created by concatenating the positive integers:

0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If dn represents the nth digit of the fractional part, find the value of the following expression.
di1 * di2 *  .. * di7
For project euler:
d1 × d10 × d100 × d1000 × d10000 × d100000 × d1000000

"""
import operator
from bisect import bisect_left
from functools import reduce

numbers_len = [(i+1)*9*10**i for i in range(20)]
tab = [sum(numbers_len[0:i]) for i in range(20)]



def find_value(n):
    digits = bisect_left(tab, n)
    begin = tab[digits - 1]
    offset = n - begin
    num, digit = divmod(offset-1, digits)
    num += 10 ** (digits - 1)
    digit = digits - digit - 1
    result = (num // (10 ** digit)) % 10
    return result


print(reduce(operator.mul, (find_value(10**i) for i in range(7))))
t = int(input())
for _ in range(t):
    i = reduce(operator.mul, (find_value(i) for i in map(int, input().split())), 1)
    print(i)
