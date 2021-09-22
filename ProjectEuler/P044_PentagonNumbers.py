"""
Pentagonal numbers are generated by the formula, Pn=n(3n−1)/2. The first ten pentagonal numbers are:

1, 5, 12, 22, 35, 51, 70, 92, 117, 145, ...

It can be seen that P4 + P7 = 22 + 70 = 92 = P8. However, their difference, 70 − 22 = 48, is not pentagonal.

Find the pair of pentagonal numbers, Pj and Pk, for which their sum and difference are pentagonal
and D = |Pk − Pj| is minimised; what is the value of D?

Generalizing for a given K and N find all Pn (n < N) such that Pn - Pn-k  is pentagonal or Pn + Pn-k is pentagonal.

"""
import math


def pentagonal(i):
    """Pentagonal number."""
    return i * (3 * i - 1) // 2


def rev_pentagonal(n):
    """Reverse pentagonal. Return 0 for n < 0 or negate result is if is not positive integer result."""
    if n < 0:
        return 0
    delta = int(math.sqrt(1 + 24 * n))
    # delta is square and 1 + 24 * n % 6 == 0 so delta %6 == 5
    if delta * delta == 1 + 24 * n and delta % 6 == 5:
        return (delta + 1) // 6
    else:
        return - (delta + 1) // 6


def main_euler():
    best = 10000000000000

    for i in range(2, 1000000):
        pi = pentagonal(i)
        start = max(abs(rev_pentagonal(pi - best)) - 2, 1)

        for j in range(start, i):
            pj = j * (3 * j - 1) // 2
            if rev_pentagonal(pi + pj) > 0 and rev_pentagonal(pi - pj) > 0:
                if pi - pj < best:
                    best = pi - pj
                    print(i, j, best)
    return best


def main_hacker_rank(n, k):
    pentagonal_list = []
    for i in range(1, n - k):
        s1 = rev_pentagonal(pentagonal(i) + pentagonal(i + k))
        s2 = rev_pentagonal(-pentagonal(i) + pentagonal(i + k))
        if s1 > 0:
            pentagonal_list.append(pentagonal(i+k))
        if s2 > 0:
            pentagonal_list.append(pentagonal(i + k))

    return sorted(list(set((pentagonal_list))))


#main_euler()
n, k = map(int, input().split())

for num in main_hacker_rank(n, k):
    print(num)

