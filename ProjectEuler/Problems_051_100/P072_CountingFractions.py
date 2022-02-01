"""

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1,
it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d <= 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 21 elements in this set.

How many elements would be contained in the set of reduced proper fractions for d <= 1,000,000?

"""
"""
Euler's Totient function, phi(n), is used to determine the number of numbers
less than n which are relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and
relatively prime to nine, phi(9)=6.
n 	Relatively Prime 	phi(n) 	n/phi(n)
2 	1 	1 	2
3 	1,2 	2 	1.5
4 	1,3 	2 	2
5 	1,2,3,4 	4 	1.25
6 	1,5 	2 	3
7 	1,2,3,4,5,6 	6 	1.1666...
8 	1,3,5,7 	4 	2
9 	1,2,4,5,7,8 	6 	1.5
10 	1,3,7,9 	4 	2.5

It can be seen that n=6 produces a maximum n/phi(n) for n <= 10.

Find the value of n <= 1,000,000 for which n/phi(n) is a maximum.

"""


def rationals_sieve(n):
    """Return number of rationals in range m/n where m < n."""
    """Numbers of rationals with denominator d is equals totien(d)."""
    """Totient d is multiply of (pi**ki - pi**(ki-1)). Where d decomposition's multiply of p1**ki= """

    def add_prime_compute_totient(prime):
        """
        Add prime, update all multiples of prime.
        For prime and prime multiplies update numbers[pos] to have totiens value based on prime k.
        """
        pos = prime
        index = 1   # index = k means that pos can be power of k
        while pos <= n:
            multiply = prime
            if index == prime:
                index = 0
                num = pos // prime
                while num % prime == 0:
                    multiply *= prime
                    num //= prime
            numbers[pos] *= multiply - multiply // prime
            pos += prime
            index += 1

    numbers = [1] * (n + 2)
    numbers[1] = 0
    for i in range(2, n+1):
        if numbers[i] == 1:
            add_prime_compute_totient(i)
        # Rationals for i and rationals up to i-1
        numbers[i] += numbers[i - 1]
    return numbers


tot_array = rationals_sieve(10**6 + 1)
t = int(input())
for _ in range(t):
    n = int(input())
    print(tot_array[n])

