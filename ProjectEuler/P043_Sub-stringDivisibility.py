"""
The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.

Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, we note the following:

d2d3d4=406 is divisible by 2
d3d4d5=063 is divisible by 3
d4d5d6=635 is divisible by 5
d5d6d7=357 is divisible by 7
d6d7d8=572 is divisible by 11
d7d8d9=728 is divisible by 13
d8d9d10=289 is divisible by 17
Find the sum of all 0 to N pandigital numbers with this property.

"""
from functools import reduce
from itertools import permutations


def pandigitals(n: int):
    """Yields 0..n pandigitals."""
    for num in permutations([0, 1, 2, 3, 4, 5, 6, 7, 8, 9][:n+1]):
        yield num


def value(tab, i):
    """Return 3 digit value starting at position i[index starts from 1]."""
    return tab[i - 1] * 100 + tab[i] * 10 + tab[i + 1]


def full_value(tab):
    """Return pandigital value."""
    return reduce(lambda x, y: x * 10 + y, tab)


def substring(n):
    """ Find substrings."""
    for num in pandigitals(n):
        if n >= 9 and value(num, 8) % 17:
            continue
        if n >= 8 and value(num, 7) % 13:
            continue
        if n >= 7 and value(num, 6) % 11:
            continue
        if n >= 6 and value(num, 5) % 7:
            continue
        if n >= 5 and value(num, 4) % 5:
            continue
        if n >= 4 and value(num, 3) % 3:
            continue
        if n >= 3 and value(num, 2) % 2:
            continue
        yield full_value(num)



# print(sum(substring(9)))


n = int(input())
print(sum(substring(n)))