"""
The arithmetic sequence, 1487, 4817, 8147 in which each of the terms increases by 3330 is unusual in two ways:
(i) each of the three terms are prime, and,
(ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property.

You are given N and K, find all K size sequences where first element is less than N and K elements are permutations
of each other, are prime and are in AP(Arithmetic Progression).

Print the answer as concatenated integer formed by joining K terms.

2000 <= N <= 10**6
3 <= K <= 4

"""
from bisect import bisect_left, bisect_right
from itertools import permutations

NUMBERS = [0] * (2 * 10 ** 6 + 1)


def eratosthenes_sieve(n):
    """Generate number with divisor counter. 0 for primes."""
    def add_prime(k):
        """Add founded prime."""
        primes.append(k)
        pos = k + k
        while pos < n:
            NUMBERS[pos] += 1
            pos += k

    primes = [2]
    for i in range(3, n, 2):
        if not NUMBERS[i]:
            add_prime(i)
    return primes


def gen_primes(n):
    """Generate primes up to n."""
    primes = eratosthenes_sieve(n)
    return primes


def is_prime(primes, n):
    """Check if number is prime."""
    pos = bisect_left(primes, n)
    if pos < len(primes) and primes[pos] == n:
        return True
    return False


def get_perm_primes(primes, n):
    """Found all prime permutations not less than n."""
    founded = set()
    for p in permutations(str(n)):
        pn = int(''.join(p))
        if pn >= n and is_prime(primes, pn):
            founded.add(pn)
    founded = sorted(list(founded))
    return founded


def found_progression(founded, k, n):
    """Find all artihmetic sequences with length k when starting element is not greater than n."""
    def have_progression():
        """Verify if progression found based on the first two elements."""
        for ss in range(2, k):
            if founded[s] + ss * step not in founded:
                return False
        return True

    for s in range(0, len(founded)-k+1):
        if founded[s]>= n:
            break
        for index in range(s+1, len(founded) - k + 3):
            step = founded[index] - founded[s]
            if have_progression():
                result = []
                for i in range(k):
                    result.append(founded[s] + i * step)
                yield result


def find_prime_perm(n, k):
    """Find consecutive numbers."""
    tested = {}
    primes = gen_primes(10**6)
    p1487 = bisect_left(primes, 1487)
    pn = bisect_left(primes, n)

    result_list = []
    for i in primes[p1487:pn]:
        i_str = ''.join(sorted(str(i)))
        if tested.get(i_str) is None:
            tested[i_str] = True
            perm_primes = get_perm_primes(primes, i)
            if len(perm_primes) >= k:
                # print("PermPrimes", perm_primes)
                for result in found_progression(perm_primes, k, n):
                    result_list.append(int(''.join([str(i) for i in result])))
    result_list = sorted(result_list)
    return result_list


# print(find_prime_perm(10**6, 3))
n, k = map(int, input().split())
result = find_prime_perm(n, k)
print(*result, sep='\n')
