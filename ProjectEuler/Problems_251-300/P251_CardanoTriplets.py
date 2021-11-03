"""

A triplet of positive integers (a,b,c) is called a Cardano Triplet if it satisfies the condition:

(A+B*C**(1/2))**(1/3) +(A-B*C**(1/2))**(1/3) = 1

For example, (2,1,5) is a Cardano Triplet.

There exist 149 Cardano Triplets for which a+b+c ≤ 1000.

Find how many Cardano Triplets exist such that a+b+c ≤ 110,000,000.

"""

# [(A+B*C**(1/2))**(1/3) +(A-B*C**(1/2))**(1/3)]**3 = 1
# 2*A + 3 * (A+B*C**(1/2))**(1/3) * (A-B*C**(1/2))**(1/3) * ((A+B*C**(1/2))**(1/3) + (A-B*C**(1/2))**(1/3)) = 1
# 2*A + 3 * (A+B*C**(1/2))**(1/3) * (A-B*C**(1/2))**(1/3) * (1) = 1
# 27 * (A+B*C**(1/2))**(1/3) * (A-B*C**(1/2)) = (1 - 2*A) ** 3
# 8*A**3 + 15*A**2 + 6*A  - 27*B**2*C = 1
# 2,3 and 4th terms are divisible by 3 so 8*a**3 % 3 == 1 => a = 3*k+2
# 8*(3*k+2)**3+15*(3*k+2)**2+6*(3*k+2) - 1 = 27*B**2*C
# 27*(k+1)**2*(8k+5) = 27*B**2*C
#
# 8*(3*k+2)**3+15*(3*k+2)**2+6*(3*k+2) - 27*(k+1)**2*(8k+5) = 1, where a=3*k+2, b**2*c=(k+1)**2*(8*k+5), k=0, 1, ...
# (k+1)**2*(8*k+5) = 8*k**3 + 21*k**2 + 18*k + 5
# Solver: for given k, prime decompose k+1 and 8*k+5 for finding all pairs such that it can form b**2*c
# limit for a + b + c < n so a <= n so k <= (n - 1) / s, b, c < n so b**2*c < n**3, 8*k**3 + 21*k**2 + 18*k + 5 < n**3
# max k: (2**(1/3)+1/4**(1/3))*(8*x**3+21*x**2+18*x + 5)**(1/3) + 3*x + 2 - d = 0

import math
from typing import Iterator, Iterable


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


def extract_pairs(divisors_list: list[int]):
    pairs = []
    if divisors_list[0] > 1:
        pairs = [1]
    singles = []
    while divisors_list:
        first = divisors_list[0]
        count = divisors_list.count(first)
        p_count, s_count = divmod(count, 2)
        pairs += [first] * p_count
        singles += [first] * s_count
        divisors_list = divisors_list[count:]
    return pairs, singles


def b2c_less_d(d):
    alpha = pow(8*math.sqrt(16*d*d+d)+32*d+1, 1/3)
    k = int((alpha + 1 / alpha - 7)/8)
    return k


def find(n):
    count = (n - 8) // 12
    print('max k = ', count)
    k = count
    abc_sum = 0
    while True:
        if (8*k + 5) % 9 == 0:
            abc_sum = 6*k + 4 + (8*k + 5)//9
            if abc_sum <= n:
                print(f'k={k}, 8k+5 % 9 == 0. Sum: {abc_sum}')
            else:
                print(f'High from {k} for  8K+5 % 9, {abc_sum}')
                break
        k += 1
    k = count
    while True:
        if (8*k + 5) % 25 == 0:
            abc_sum = 8*k + 7 + (8*k + 5)//25
            if abc_sum <= n:
                print(f'k={k}, 8k+5 % 49 == 0. Sum: {abc_sum}')
            else:
                print(f'High from {k} for  8K+5 % 49, {abc_sum}')
                break
        k += 1
    #
    k = count
    while True:
        if (8*k + 5) % 49 == 0:
            abc_sum = 10*k + 9 + (8*k + 5)//49
            if abc_sum <= n:
                print(f'k={k}, 8k+5 % 29 == 0. Sum: {abc_sum}')
            else:
                print(f'High from {k} for  8K+5 % 25, {abc_sum}')
                break
        k += 1
#
    #
    k = count
    while True:
        if (8*k + 5) % 81 == 0:
            abc_sum = 12*k + 11 + (8*k + 5)//81
            if abc_sum <= n:
                print(f'k={k}, 8k+5 % 29 == 0. Sum: {abc_sum}')
            else:
                print(f'High from {k} for  8K+5 % 25, {abc_sum}')
                break
        k += 1


def b2c(k):
    return 5 + k * (18 + k * (21 + k * 8))


def find_solution(n):
    max_a, max_b, max_c = 0, 0, 0
    counter = 0
    max_k = n
    for i in range(1, max_k+2):
        max_k_for_c = b2c_less_d(n * i * i)
        cnt = 0
        for j in range(max_k_for_c+2):
            c, mod = divmod(b2c(j), i * i)
            if mod == 0:
                if 3 * j + 2 + i + c <= n:
                    if 3*j+2 > max_a:
                        max_a = 3 * j + 2
                    if i > max_b:
                        max_b = i
                    if c > max_c:
                        max_c = c
                    print(j, 3*j+2, i, c)
                    counter += 1
                    cnt += 1
        if cnt:
            print('^^^', i, max_k_for_c, cnt)
    print(n, counter, max_a, max_b, max_c)


find_solution(1000)







