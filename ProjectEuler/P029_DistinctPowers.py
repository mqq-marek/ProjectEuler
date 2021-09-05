"""
Consider all integer combinations of  a**b for  2 <= a<= 5 and 2 <= b <=5.
If they are then placed in numerical order, with any repeats removed,
we get the sequence of 15 distinct terms.

How many distinct terms are in the sequence generated by a**b for  2 <= a, b <= N?

"""
import math
import operator
from collections import Counter, defaultdict
from functools import reduce
from typing import Iterator, Iterable, Sequence

IntPair = tuple[int, int]


def divisors(num: int, *, start: int = 2, ordered: bool = False, step: int = 1) -> Iterator[int]:
    """
    Get all number divisors starting from start.
    Faster (sqrt(n) operations) than scanning all numbers using:
        divisors = (i for i in range(start, n) if n % mod i == 0).
    :param step: step for verifying sequence of divisors (1= all numbers, 2 - odd numbers)
    :param num: number for which we yields divisors
    :param ordered: if True divisors yields in increasing order
        using list keeping half of the divisors.
        For ordered=True risk of memory overflow for huge numbers with few thousands digits
    :param start: starting number for divisor.
        Most frequent use:
            start=2 yields all divisors excluding 1 and n -  it will contains nothing for prime num
            start=1 yields all divisors including 1 and n -  it will contain 1 and num for prime num
            start is used for step by step number factorization
            (finding number representation as prime number product)
    :yields: num divisors
    """
    def _divisors():
        # Step 1:
        # Process divisible by 1 only when start == 1
        if start == 1:
            yield 1
            # prevent yield duplicate when num == 1
            if num > 1:
                yield num

        # Step 2:
        # Process divisibility in up to sqrt_num[+1]
        # - from 2 (1 already processed) or from start if greater then 2
        # - to sqrt_num if sqrt_num is exact square of num or once more otherwise
        for next_num in range(max(2, start), sqrt_num + no_int_sqrt, step):
            if num % next_num == 0:
                yield next_num
                yield num // next_num

        # Step 3:
        # Process when sqrt_num is exact sqrt of num except 1 which was already processed in step 1
        if no_int_sqrt == 0 and num > 1:
            yield sqrt_num

    def _sorted(iterable: Iterable[int]):
        # Divisor are not generated in sorted order. E.g. for 12 it is: 1, 12, 2, 6, 3, 4.
        # Odd elements are increasing, even elements are decreasing
        # Make stack for half of divisors if ordered list of divisors is requested
        divisors_stack: list[int] = []
        iterator = iter(iterable)

        try:
            previous = next(iterator)
        except StopIteration:
            return

        for current in iterator:
            if previous > current:
                # Send even element on stack
                divisors_stack.append(previous)
            else:
                # Yield odd element
                yield previous
            previous = current
        # Yield last ordered element
        yield previous

        # Yield elements from stack
        for divisor in reversed(divisors_stack):
            yield divisor

    assert num > 0, "divisors iterator works with num > 0"
    assert start > 0, "divisors iterator works with start > 0"

    # find divisors until sqrt(num)
    sqrt_num: int = int(math.sqrt(num))
    # Is exact num sqrt?
    if sqrt_num * sqrt_num == num:
        no_int_sqrt = 0
    else:
        no_int_sqrt = 1

    if ordered:
        yield from _sorted(_divisors())
    else:
        yield from _divisors()


def prime_divisors(num: int) -> Iterator[int]:
    """
    Get all num prime divisors.
    :param num: number for which we yields prime divisors
    :yields: num prime divisors
    """
    assert num > 0

    if num == 1:
        yield 1

    while num % 2 == 0:
        yield 2
        num >>= 1
    # start scan with 3 and step = 2
    scan_start: int = 3
    while num > 1:
        try:
            # try to get first prospect prime
            scan_start = next(divisors(num, start=scan_start, step=2))
        except StopIteration:
            # if no divisors, means num is prime
            scan_start = num
        yield scan_start
        num //= scan_start


def least_common_multiple(seq: Iterable[int]) -> int:
    """
    Least common multiple of positive integers.
    :param seq: sequence of numbers
    :return: LCM
    """
    def lcm(num1: int, num2: int) -> int:
        return num1 * num2 // math.gcd(num1, num2)

    return reduce(lcm, seq, 1)


def prime_factors_with_powers(num: int):
    """Return prime divisors of num as tuples (prime, counter)."""
    primes = Counter(prime_divisors(num))
    result = []
    for prime, power in sorted(primes.items()):
        result.append((prime, power))
    if not result:
        # num is prime
        result = [(num, 1)]
    return result


def normalized_prime_factors_with_powers(num: int) -> tuple[int, list[IntPair]]:
    """Return prime divisors of num as tuples (prime, power) with common power for all.
    normalized_prime_divisors_with_powers(6) = [1, [(2,1), (3, 1)]
    normalized_prime_divisors_with_powers(12) = [1, [(2,2), (3, 1)]
    normalized_prime_divisors_with_powers(18) = [1, [(2,1), (3, 2)]
    normalized_prime_divisors_with_powers(36) = [2, [(2,1), (3, 1)]
    normalized_prime_divisors_with_powers(64) = [6, [(2,1)]
    """
    prime_tuples = prime_factors_with_powers(num)
    gcd = math.gcd(*[p[1] for p in prime_tuples])
    prime_tuples = [(p[0], p[1] // gcd) for p in prime_tuples]
    return gcd, prime_tuples


def count_divisible_in_range(divisors: Iterable[int], stop: int):
    """Compute amount of numbers in range(1, stop) which are divisible by any of the divisors."""

    def has_divisors_in_list(num: int):
        for d in divisors_list:
            if d != 1 and num % d == 0:
                return True
        return False

    divisors_list = list(divisors)
    cycle = least_common_multiple(divisors_list)
    frames = (stop - 1) // cycle
    # multiples for the first frame
    multiples = [i for i in range(1, cycle + 1) if has_divisors_in_list(i)]
    frame_sum = len(multiples)
    # every next frame has the same amount of divisors
    total = frames * len(multiples)
    # add sum for ending part which is not full frame
    for k in range(frames * cycle + 1, stop):
        if has_divisors_in_list(k):
            total += 1
    return total


def distinct_powers_brute(num):
    """Compute distinct power using brute force."""
    total = set()
    for a in range(num, 1, -1):
        l0 = len(total)
        p = a * a
        for b in range(2, num+1):
            if p not in total:
                total.add(p)
            p *= a
    return len(total)


def distinct_powers(num):
    """
    Compute distinct power by rules using normalized prime factorization.
        Represent number a as (prime1**power1*prime2**power2...)**power using normalized_prime_factors_asPowers.
        a**b can match c**d only when they have same factorizations using primes but they have
        different factorization powers.
    """
    counter = 0
    for a in range(2, num+1):
        power, factors = normalized_prime_factors_with_powers(a)
        base_part = reduce(operator.mul, [a**b for a, b in factors], 1)
        # if there is no other number in range a..num with the same base_part then
        #   we will have num-1 new a**b elements
        increase = num - 1
        # next number with the same base_part will have power increased by 1
        next_power = power + 1
        next_common = a * base_part
        # collect all numbers in range a*base_power..num with the same base_part
        powers = []
        while next_common <= num:
            powers.append(next_power//math.gcd(power, next_power))
            next_power += 1
            next_common *= base_part
        if powers:
            # find all elements which will occurs in next number with the same base_part
            divisors = count_divisible_in_range(powers, num + 1)
            if power == 1:
                # Update amount of divisors the a has power 1
                divisors -= 1
                for p in powers:
                    if p % 2:
                        divisors -= 1
            else:
                for p, pp in enumerate(powers, power+1):
                    # p are powers of next numbers after a with the same base_part
                    # update amount of divisors
                    if p % 2 == 0 and p // 2 >= power:
                        divisors -= 1
                        break
            increase -= divisors
        counter += increase
    return counter


# print(distinct_powers(100))
n = int(input())
print(distinct_powers(n))
