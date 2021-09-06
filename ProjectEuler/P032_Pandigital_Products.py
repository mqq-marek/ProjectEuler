"""

We shall say that an  N-digit number is pandigital if it makes use of all the digits 1 to N exactly once;
for example, the 5-digit number, 15234, is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand, multiplier,
and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity
can be written as a 1 through N pandigital.

HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.

"""
import operator
from functools import reduce
from itertools import permutations

DIGITS = [i+1 for i in range(9)]


def to_int(digits):
    return reduce(lambda x, y: x * 10 + y, digits)


def search(n: int):
    if n < 8:
        start = 2
    else:
        start = 4
    products = set()
    digits = DIGITS[:n]
    for item in permutations(digits):
        for i in range(start, 5):
            ab = to_int(item[:i])
            for j in range(i+1, n):
                b = to_int(item[i:j])
                a = to_int(item[j:])
                if ab == a * b:
                    products.add(ab)
    return sum(products)


n = int(input())
print(search(n))

