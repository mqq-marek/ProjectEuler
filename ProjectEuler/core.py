"""
Gems or core functionalities used in different problems.
"""
import itertools
from collections import Counter
from functools import reduce
from itertools import starmap
import math
from typing import Iterator, Sequence, TypeVar, Callable, Iterable, Tuple

GenT = TypeVar('GenT')


def moving_pairs(iterable: Iterable) -> Iterator:
    """
    Generate moving pair elements over iterable.
    e.g. (1, 2), (2, 3) from iterable 1, 2, 3.
    :param iterable:
    :yields: moving pair on iterable
    """
    iterator = iter(iterable)

    try:
        previous = next(iterator)
    except StopIteration:
        return

    for current in iterator:
        yield previous, current
        previous = current


def sequence_condition(condition: Callable[[GenT, GenT], bool], sequence: Iterable[GenT]) -> bool:
    """
    Verify if sequence fulfill operator condition between current and next element.
    :param condition: operator define condition between item[i] and item[i+1]
    :param sequence:
    :return: True if condition is True for all pairs (i, i+1)
    """
    # return all(condition(item1, item2) for item1, item2 in zip(sequence, sequence[1:]))
    # return all(condition(item1, item2) for item1, item2 in moving_pairs(sequence))
    return all(starmap(condition, moving_pairs(sequence)))


def fibonacci() -> Iterator[int]:
    """
    Fibonacci numbers generator.
    :yields: fibonacci sequence: 0, 1, 1, 2, 3, 5
    """
    f_current: int = 0
    f_next: int = 1
    while True:
        yield f_current
        f_current, f_next = f_next, f_current + f_next


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


IntPair = tuple[int, int]


def prime_factors_with_powers(num: int) -> list[IntPair]:
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


def is_prime(num: int) -> bool:
    """
    Verify if num is prime
    :param num:
    :return: True if prime, False otherwise
    """
    assert num >= 1

    if num == 1:
        return False

    if num == 2:
        return True

    if num % 2 == 0:
        return False

    for _ in divisors(num, start=3, step=2):
        # try to get first divisor
        return False

    # if no divisors, than prime
    return True


def partitions(n) -> Iterator[list[int]]:
    """
    Yields number n partitions.
    partitions(5) yields:
        [5]
        [1, 4]
        [2, 3]
        [1, 1, 3]
        [1, 2, 2]
        [1, 1, 1, 2]
        [1, 1, 1, 1, 1]
    """

    def next_partition() -> bool:
        """
        Update in-place partition to the next one with the same length.
        :return: True if next partition exist otherwise False
        """
        right_side_sum = 0
        for i in reversed(range(len(partition) - 1)):
            # Keep sum of elements skipped from right
            right_side_sum += partition[i + 1]
            # From the end look for the first element smaller than next
            if partition[i + 1] > partition[i]:
                # Borrow one
                partition[i + 1] -= 1
                # Find next which is smaller for increasing them
                for j in reversed(range(i + 1)):
                    if partition[j + 1] > partition[j]:
                        # Increase element j. Keep invariants that sum is n and numbers are monotonic
                        partition[j] += 1
                        # Now prepare for making minimal part on right of j
                        # all elements on right are equals partition[j] except last one which can be grater
                        right_j_sum = right_side_sum + (i - j) * partition[j + 1]
                        distance = len(partition) - j - 2
                        for k in range(distance):
                            partition[j + k + 1] = partition[j]
                        partition[-1] = right_j_sum - distance * partition[j] - 1
                        return True
        # Not found any place for generating next partition with:
        #   - the same sum
        #   - the same length
        #   - having elements in order: partition[0] <= partition[1] .... <= partition[len(partition)-1]
        return False

    # Build partitions in order based on partition length starting from 1 to n.
    # Elements in partition are always in non decreasing order
    # length == 1: [n]
    # length == 2: [1, n-1], [2, n-2], '''
    # length == 3: [1, 1, n-2], ...
    # ....
    # length == n: [1] * n
    for m in range(n):
        partition = [1] * m
        partition.append(n - m)
        yield partition[:]
        # Next partitions with the same size
        while next_partition():
            # assert all(a <= b for a, b in zip(partition, partition[1:])), partition
            # assert sum(partition) == n, partition
            yield partition[:]


def eratosthenes_sieve() -> Iterator[int]:
    # http://mypy-lang.org/examples.html example
    # An iterator of all prime numbers between 2 and
    # +infinity
    numbers = itertools.count(2)

    # Generate primes forever
    while True:
        # Get the first number from the iterator
        # (always a prime)
        prime = next(numbers)
        yield prime

        # This code iteratively builds up a chain
        # of filters...
        numbers = filter(prime.__rmod__, numbers)


def count_divisible_in_range(divisors: Iterable[int], stop: int):
    """Compute amount of numbers in range(1, stop) which are divisible by any of the divisors."""

    def has_divisors_in_list(num: int):
        for d in divisors_list:
            if num % d == 0:
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


def gen_primes(n: int) -> list[int]:
    def has_prime_divisiors(k):
        for p in primes:
            if k % p == 0:
                return True
        return False

    primes = []
    if n >= 2:
        primes.append(2)
    for i in range(3, n+1, 2):
        if not has_prime_divisiors(i):
            primes.append(i)
    return primes


    fo