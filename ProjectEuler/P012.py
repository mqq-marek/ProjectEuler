"""
The sequence of triangle numbers is generated by adding the natural numbers.
So the 7th triangle number would be 1 + 2 + 3 + 4 + 5 + 6 + 7 = 28. The first ten terms would be:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

Let us list the factors of the first seven triangle numbers:

 1: 1
 3: 1,3
 6: 1,2,3,6
10: 1,2,5,10
15: 1,3,5,15
21: 1,3,7,21
28: 1,2,4,7,14,28
We can see that 28 is the first triangle number to have over five divisors.

What is the value of the first triangle number to have over five hundred divisors?

"""
import itertools
import math


def divisors(num):
    """Get number divisors."""
    counter = 0
    num_sqrt = int(math.sqrt(num))
    for j in range(1, num_sqrt + 1):
        div, rem = divmod(num, j)
        if rem == 0:
            yield j
            counter += 1
            if j != div:
                yield div
                counter += 1


def triangle_divisor(n=1):
    """
    Emit sequences of triangle number, triangle value, number  of divisors.
    n th triangle has value n*(n+1)/2. n and n+1 are co-primes. One of n, n+1 is divided by 2, so divisor number:
    divisor(n*(n+1)/2) = divisor(n//2)*divisor(n+1) for n even otherwise divisors(n)*divisors((n+1)//2)
    :param n: initial triangle number
    :return: yields (triangle number, triangle, value, triangle number of divisors)
    """
    if n % 2:
        # if n is odd, emit value for n and go to next
        yield n, n * (n + 1) // 2, len(list(divisors(n))) * len(list(divisors((n + 1) // 2)))
        n += 1

    # for n which is even
    odd = (n + 1)
    even = n // 2
    triangle = odd * even
    d_even = len(list(divisors(even)))

    while True:
        d_odd = len(list(divisors(odd)))
        yield n, triangle, d_odd * d_even

        # next element has the same odd part, even part is increased by 1 and triangle is increased by odd
        n += 1
        even += 1
        triangle += odd
        d_even = len(list(divisors(even)))
        yield n, triangle, d_odd * d_even
        # next element has the same even part, odd part is increased by 2 and triangle is increased by 2 * even
        n += 1
        odd += 2
        triangle += even + even


def find_triangular_with_divisors(n):
    """Brute-force finding triangular number with more than n divisors."""

    for i in itertools.count(start=1):
        j = i * (i + 1) // 2
        d = len(list(divisors(j)))
        if d > n:
            return j


def find_triangular_with_divisors_fast(n):
    """Fast finding triangular number with more than n divisors."""

    for i, j, d in triangle_divisor(1):
        if d > n:
            return j


def hacker_main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        first = find_triangular_with_divisors_fast(n)
        print(first)


def dev_main():
    for i, j, d in triangle_divisor(1):
        print(i, j, d)
        if i == 100:
            break


def test_main():
    max_divisors = {}
    max_d = 0
    for i in range(1, 10000):
        d = len(list(divisors(i*(i+1)//2)))
        if d > max_d:
            max_divisors.setdefault(d, i)
            max_d = d
    for k, v in max_divisors.items():
        print(f'{v:4}, {v*(v+1)//2:5}, {k:4}')
        v0d = list(divisors(v))
        v1d = list(divisors(v+1))
        if v % 2:
            vh = (v + 1) // 2
            vhd = list(divisors(vh))
            print(f'{v} has {len(v0d)} divisors {v0d}')
            print(f'{vh} has {len(vhd)} divisors {vhd}')
            dd = len(vhd) * len(v0d)
        else:
            vh = v // 2
            vhd = list(divisors(vh))
            print(f'{vh} has {len(vhd)} divisors {vhd}')
            print(f'{v + 1} has {len(v1d)} divisors {v1d}')
            dd = len(vhd) * len(v1d)
        if dd != k:
            print(f'Triangle divisor does not mach multiply of n, (n+1) elements')


if __name__ == "__main__":
    # print(find_triangular_with_divisors(500))
    dev_main()
