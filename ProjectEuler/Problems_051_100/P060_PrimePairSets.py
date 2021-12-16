"""


The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes and concatenating them in any order
the result will always be prime. For example, taking 7 and 109, both 7109 and 1097 are prime.
The sum of these four primes, 792, represents the lowest sum for a set of four primes with this property.

Find the lowest sum for a set of five primes for which any two primes concatenate to produce another prime.

"""
import itertools
import math
import random
from bisect import bisect_left, bisect_right
from collections import defaultdict
from typing import List

prime_map = defaultdict(set)


def remove_key_refs(key):
    """Remove reference to prime being removed from map."""
    prime_map[key] = set()
    for value in prime_map.values():
        value.discard(key)


def remove_cross_refs(key: int, value: List[int], set_len: int):
    """Remove cross refs to primes not belonging to the same set."""
    modified = False
    refs_to_remove = []
    for elem in value:
        other = prime_map[elem]
        if len(value.intersection(other)) < set_len - 1:
            other.discard(key)
            refs_to_remove.append(elem)
    for elem in refs_to_remove:
        modified = True
        value.discard(elem)
    return modified


def clean_map(set_len):
    """Clean map by removing cross refs outside sets and pairs shorter than set_len."""
    while True:
        key_for_del = []
        modified = False
        for key, value in prime_map.items():
            if len(value) >= set_len:
                if remove_cross_refs(key, value, set_len):
                    modified = True
            if len(value) < set_len:
                key_for_del.append(key)
                remove_key_refs(key)
        for dkey in key_for_del:
            modified = True
            del prime_map[dkey]
        if not modified:
            break


def eratosthenes_sieve(n):
    """Return primes <= n."""

    def add_prime(k):
        """Add founded prime."""
        p = k + k + 3
        primes.append(p)
        pos = k + p
        while pos <= n:
            numbers[pos] = 1
            pos += p

    numbers = [0] * (n + 1)
    primes = [2]
    for i in range(n):
        if not numbers[i]:
            add_prime(i)
    return primes


def is_prime(num: int, primes: List[int] = None) -> bool:
    """
    Verify if num is prime
    :param num:
    :param primes:
    :return: True if prime, False otherwise
    """
    if num < 2:
        return False

    if num in [2, 3]:
        return True

    if num % 2 == 0 or num % 3 == 0:
        return False

    num_sqrt = int(math.sqrt(num))
    start = 5

    if primes and primes[-1] >= num_sqrt:
        if num <= primes[-1]:
            return primes[bisect_left(primes, num)] == num
        for prime in primes:
            if prime > num_sqrt:
                break
            if num % prime == 0:
                return False
        if primes[-1] % 6 == 1:
            start = primes[-1]
        else:
            start = primes[-1] + 2

        for n in range(start, 6, num_sqrt + 1):
            if num % n == 0 or num % (n + 4) == 0:
                return False
        return True
    else:
        return is_prime_Miller_Rabin(num, primes=primes[:20])


def is_prime_Miller_Rabin(num: int, *, primes: List[int] = None, tests: int = 5) -> bool:
    """
    Verify if num is prime
    :param num:
    :param primes: initial sorted primes table if exist (e.g. from Eratosthenes) - recommend up to the first 20 primes
    :param tests: number of additional rounds for big number testing
    :return: True if prime, False otherwise
    """
    if num < 2:
        return False
    if num < 13:
        #       2,    3,    4,     5,    6,     7,    8,     9,     10,    11,   12
        return [True, True, False, True, False, True, False, False, False, True, False][num - 2]

    sqrt_num = int(math.sqrt(num))
    for prime in primes:
        if prime > sqrt_num:
            return True
        if num % prime == 0:
            return False

    # Factor n-1 as d * 2 ** s
    s, d = 0, num - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # Make witnesses
    if num < 1373653:
        test_set = [2, 3]
    elif num < 25326001:
        test_set = [2, 3, 5]
    elif num < 118670087467:
        if num == 3215031751:
            return False
        test_set = [2, 3, 5, 7]
    elif num < 2152302898747:
        test_set = [2, 3, 5, 7, 11]
    else:
        test_set = [2, 3, 5, 7, 11, 13] + [random.randrange(17, num - 1) for _ in range(tests)]
    for a in test_set:
        x = pow(a, d, num)
        if x in [1, num - 1]:
            continue
        for _ in range(s):
            x = x * x % num
            if x == num - 1:
                break
        else:
            return False
    return True


def build_results(set_size):
    """Build result list."""
    def check_set() -> bool:
        """Verify if set is correct."""
        for num in items:
            if len(prime_map[num].intersection(all_items)) != set_size:
                return False
        return True

    results = []
    for k, v in prime_map.items():
        check_list = [i for i in v if i > k]
        if len(check_list) >= set_size:
            for items in itertools.combinations(check_list, set_size):
                all_items = set(items)
                all_items.add(k)
                if check_set():
                    results.append(sum(all_items))
    return sorted(list(results))


def prime_sets(max_prime: int, set_size: int):
    """Find and print prime sets."""
    primes = eratosthenes_sieve(min(10**7, max_prime*max_prime+1))
    # print('Primes generated')
    max_ndx = bisect_right(primes, max_prime)
    for ndx, p1 in enumerate(primes[1:max_ndx], start=1):
        p1str = str(p1)
        for p2 in primes[ndx:max_ndx]:
            p2str = str(p2)
            if is_prime(int(p1str+p2str), primes=primes) and is_prime(int(p2str+p1str), primes=primes):
                prime_map[p1].add(p2)
                prime_map[p2].add(p1)
    # print('Prime pairs generated')
    clean_map(set_size - 1)
    # print('Map cleaned')
    set_sums = build_results(set_size - 1)
    # print('result generated')
    for res in set_sums:
        print(res)


n, k = 20000,5
n, k = map(int, input().split())
prime_sets(n, k)
