"""
The prime 41, can be written as the sum of six consecutive primes:
    41 = 2 + 3 + 5 + 7 + 11 + 13
This is the longest sum of consecutive primes that adds to a prime below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.

Which prime, <=N, can be written as the sum of the most consecutive primes?
Note: You have to print prime as well as the length of consecutive chain whose sum is prime.
If such primes are more than 1, print the least.

"""
import math
from bisect import bisect_left, bisect_right


SIZE = 10 ** 7
NUMBERS = [0] * (SIZE + 1)


def eratosthenes_sieve(n):
    """Generate number with divisor counter. 0 for primes."""
    def add_prime(k):
        """Add founded prime."""
        primes.append(k)
        cum_primes.append(cum_primes[-1] + k)
        pos = k + k
        while pos < n:
            NUMBERS[pos] += 1
            pos += k

    primes = [2]
    cum_primes = [0, 2]
    for i in range(3, n, 2):
        if not NUMBERS[i]:
            add_prime(i)

    return primes, cum_primes


def gen_primes(n):
    """Generate primes up to n."""
    primes, cum_primes = eratosthenes_sieve(n)
    return primes, cum_primes


def is_prime(primes, n):
    """Check if number is prime."""
    pos = bisect_left(primes, n)
    if pos < len(primes):  # n is in primes
        if primes[pos] == n:
            return True
        else:
            return False
    else:  # n > primes[-1]
        n_sqrt = int(math.sqrt(n))
        for p in primes:  # checks for prime dividends
            if p <= n_sqrt:
                if n % p == 0:
                    return False
            else:
                break
        for k in range(primes[-1] + 2, n_sqrt + 1, 2):  # necessary if n > primes[-1]**2
            if n % k == 0:
                return False
        return True


def max_sum_len(cum_primes, n):
    """Find max sum len."""
    max_len = bisect_right(cum_primes, n) - 1
    return max_len


def longest(primes, cum_primes, n):
    """Find the longest sum."""
    max_len = max_sum_len(cum_primes, n)

    # Check for sum starting from 2
    cur_index = max_len
    cum_sum = cum_primes[cur_index]
    while not is_prime(primes, cum_sum):
        cur_index -= 1
        cum_sum -= primes[cur_index]
    best_len = cur_index
    best_prime = cum_sum
    best_start = 0

    # check for sum starting from next primes
    for i in range(1, len(primes)-max_len-1):
        cur_index = best_len + i + 1
        cum_sum = cum_primes[cur_index] - cum_primes[i]

        if cum_sum > n:
            break

        while cum_sum <= n:
            if cum_sum % 2 and is_prime(primes, cum_sum):
                best_len = cur_index - i
                best_prime = cum_sum
            cum_sum += primes[cur_index]
            cur_index += 1
    return best_prime, best_len


primes, cum_primes = gen_primes(SIZE)

# print(longest(primes, cum_primes, 1_000))
# print(longest(primes, cum_primes, 1_000_000)
# print(longest(primes, cum_primes, 100_000_000))
# print(longest(primes, cum_primes, 1_000_000_000_000))

t = int(input())
for _ in range(t):
    n = int(input())
    print(*longest(primes, cum_primes, n))



