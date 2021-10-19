"""

By replacing the 1st digit of *3, it turns out that six of the nine possible values:
13, 23, 43, 53, 73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digits number is the first example
having seven primes among the ten generated numbers, yielding the family:
56003, 56113, 56333, 56443, 56663, 56773, and 56993.
Consequently 5603, being the first member of this family, is the smallest prime with this property.

Find the smallest N-digits prime which, by replacing K-digits of the number (not necessarily adjacent digits)
with the same digit, is part of an L prime value family.

Note1: It is guaranteed that solution does exist.
Note2: Leading zeros should not be considered.
Note3: If there are several solutions, choose the "lexicographically" smallest one
(one sequence is considered "lexicographically" smaller than another if its first element which does not match
the corresponding element in another sequence is smaller)

"""
import functools
import itertools
from bisect import bisect_left, bisect_right


def eratosthenes_sieve(n):
    """Return primes <= n."""

    def add_prime(k):
        """Add founded prime."""
        primes.append(k)
        pos = k + k
        while pos <= n:
            numbers[pos] = 1
            pos += k

    numbers = [0] * (n + 1)
    primes = [2]
    for i in range(3, n + 1, 2):
        if not numbers[i]:
            add_prime(i)
    return primes


def is_prime(primes, n):
    """Check if number is prime."""
    pos = bisect_left(primes, n)
    if pos < len(primes):  # n is in primes
        if primes[pos] == n:
            return True
    return False


def gen_patterns(n, k):
    """Build patterns for digits(n) and substitutions (*)"""
    pattern = 'd' * (n - k) + '*' * k
    founded = set()
    patterns = []
    for composition in itertools.permutations(pattern, n):
        if composition not in founded:
            founded.add(composition)
            digits_at = [i for i, ch in enumerate(composition) if ch == '*']
            patterns.append(digits_at)
    return patterns


def find_sequence(candidates, patterns, n, k, l):
    """Find reqired primes sequence from candidate list."""
    result = [10 ** n - 1] * l
    for candidate in candidates:
        for pattern in patterns:
            digits = [int(ch) for ch in str(candidate)]
            pattern_digits = [digits[index] for index in pattern]
            start_digit = pattern_digits[0]
            if len(set(pattern_digits)) > 1:
                # skip if not the same digits in '*' pattern
                continue
            if 10 - start_digit < l:
                # Skip if digits too high for having l primes
                continue
            primes_founded = [candidate]
            for digit in range(start_digit + 1, 10):
                for index in pattern:
                    digits[index] = digit
                next_candidate = functools.reduce(lambda x, y: 10 * x + y, digits)
                if is_prime(candidates, next_candidate):
                    primes_founded.append(next_candidate)
            if len(primes_founded) >= l:
                return primes_founded
    return result


def select(primes, n, k):
    """Select primes having n digits and k the same digits."""
    min_prime = 10 ** (n - 1)
    max_prime = 10 * min_prime
    start_index = bisect_left(primes, min_prime)
    end_index = bisect_right(primes, max_prime)
    if k == 1:
        candidates = primes[start_index:end_index]
    else:
        candidates = []
        for prime in primes[start_index:end_index]:
            if prime < min_prime or prime >= max_prime:
                assert False
            prime_digits = sorted(str(prime))
            unique_digits = set(prime_digits)
            for digit in unique_digits:
                counter = prime_digits.count(digit)
                if counter >= k:
                    candidates.append(prime)
                    break
    return candidates


def process(n, k, l):
    """Find n-digits prime sequence of length l having k the same digits."""
    primes = eratosthenes_sieve(10 ** n)
    candidates = select(primes, n, k)
    patterns = gen_patterns(n, k)
    if len(candidates) > 0:
        result = find_sequence(candidates, patterns, n, k, l)
        if result[0] < 10 ** n - 1:
            return result
    return ['Empty!']


# for n in range(2, 8):
#     for k in range(1, n + 1):
#         for l in range(1, 9):
#             print(n, k, l)
#             result = process(n, k, l)
#             print(*result[:l])
# exit()

n, k, l = [int(s) for s in input().split()]
result = process(n, k, l)
print(*result[:l])
