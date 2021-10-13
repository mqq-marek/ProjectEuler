"""
The fraction  49/98 is a curious fraction.
An inexperienced mathematician while attempting to simplify it may incorrectly believe
that  49/98 = 4/8 is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

Which means fractions where trailing 0's are cancelled are trivial.
So we will ignore all the cases where we have to cancel 0's.

You will be given 2 integers  N and K.  N represents the number of digits in
Numerator and Denominator, and  K represents the exact number of digits to be "cancelled"
from Numerator and Denominator. Find every non-trivial fraction,
(1) where numerator is less than denominator,
(2) and the value of the reduced fraction is equal to the original fraction.

Sum all the Numerators and the Denominators of the original fractions, and print them separated by a space.

"""

from itertools import product, combinations
from time import perf_counter


def n_d_gen(n: int, k: int):
    pairs = set()
    min_ld = 10 ** (n - 1) + 1
    max_ld = 10 ** n - 1
    for long_denominator in range(min_ld, max_ld + 1):
        ld_str = str(long_denominator)
        for indexes_for_remove in combinations(list(range(n)), k):
            sd_str = ''.join(ch for i, ch in enumerate(ld_str) if i not in indexes_for_remove)
            skip_str = ''.join(ch for i, ch in enumerate(ld_str) if i in indexes_for_remove)
            if '0' in skip_str:
                continue
            short_denominator = int(sd_str)
            for short_numerator in range(1, short_denominator):
                # a/b = c/d if a * d = b * c
                sn_x_ld = short_numerator * long_denominator
                if sn_x_ld % short_denominator:
                    continue
                long_numerator = sn_x_ld // short_denominator
                if long_numerator < min_ld - 1:
                    continue
                ln_str = str(long_numerator)

                sn_str = ('0' * k + str(short_numerator))[-(n - k):]
                if sorted(ln_str) != sorted(sn_str+skip_str):
                    continue

                is_ok = False
                for for_remove in combinations(list(range(n)), k):
                    sn2_str = ''.join(ch for i, ch in enumerate(ln_str) if i not in for_remove)
                    if sn_str == sn2_str:
                        is_ok = True
                        break
                if not is_ok:
                    continue

                if (long_numerator, long_denominator) in pairs:
                    continue
                pairs.add((long_numerator, long_denominator))
                # print(long_numerator, '\t', long_denominator, '\t', short_numerator, '\t', short_denominator)
                yield long_numerator, long_denominator


def cancel(n, k):
    numerator_sum = 0
    denominator_sum = 0
    counter = 0
    for numerator, denominator in n_d_gen(n, k):
        counter += 1
        numerator_sum += numerator
        denominator_sum += denominator
    return numerator_sum, denominator_sum, counter


for n in range(3, 4):
    for k in range(1, n):
        start = perf_counter()
        a, b, c = cancel(n, k)
        tim = perf_counter() - start
        print(f'n={n}, k={k}, counter={c}, sum=({a},{b}), time={tim:.2f}')
n, k = map(int, input().split())
a, b, c = cancel(n, k)
print(a, b)
