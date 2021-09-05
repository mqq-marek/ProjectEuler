import pytest
from itertools import islice
from core import (
    fibonacci,
    divisors,
    sequence_condition,
    prime_divisors,
    least_common_multiple,
    is_prime,
    partitions, normalized_prime_factors_with_powers,
)


def test_fibonacci():
    f_seq = [0, 1, 1, 2, 3, 5, 8, 13]
    assert list(islice(fibonacci(), len(f_seq))) == f_seq


divisors_table = [
    (1, 1, [1]),
    (1, 2, []),
    (2, 1, [1, 2]),
    (2, 2, []),
    (3, 1, [1, 3]),
    (3, 2, []),
    (4, 1, [1, 4, 2]),
    (4, 2, [2]),
    (5, 1, [1, 5]),
    (5, 2, []),
    (6, 1, [1, 6, 2, 3]),
    (6, 2, [2, 3]),
    (7, 1, [1, 7]),
    (7, 2, []),
    (8, 1, [1, 8, 2, 4]),
    (8, 2, [2, 4]),
    (8, 3, []),
    (9, 1, [1, 9, 3]),
    (9, 2, [3]),
    (9, 3, [3])
]


@pytest.mark.parametrize("number, start, expected", divisors_table)
def test_divisors(number, start, expected):
    result = list(divisors(number, start=start))
    assert result == expected
    result = list(divisors(number, start=start, ordered=True))
    assert result == sorted(expected)


seq_table = [
    (lambda x, y: x <= y, [], True),
    (lambda x, y: x <= y, [1], True),
    (lambda x, y: x <= y, [1, 1], True),
    (lambda x, y: x <= y, [1, 2], True),
    (lambda x, y: x <= y, [1, 2, 2, 3, 4, 4], True),
    (lambda x, y: x <= y, [1, 2, 2, 3, 4, 5], True),
    (lambda x, y: x <= y, [1, 0], False),
    (lambda x, y: x <= y, [1, 2, 0], False),
    (lambda x, y: x <= y, [1, 2, 2, 0], False),
    (lambda x, y: x <= y, [1, 0, 3], False),
    (lambda x, y: x <= y, [1, 0, 3, 3], False),

]


@pytest.mark.parametrize("operator, seq, expected", seq_table)
def test_sequence_condition(operator, seq, expected):
    assert sequence_condition(operator, seq) == expected


prime_divisor_table = [
    (1, [1]),
    (2, [2]),
    (3, [3]),
    (4, [2, 2]),
    (5, [5]),
    (6, [2, 3]),
    (7, [7]),
    (8, [2, 2, 2]),
    (9, [3, 3]),
    (10, [2, 5]),
    (11, [11]),
    (12, [2, 2, 3]),
]


@pytest.mark.parametrize("num, expected", prime_divisor_table)
def test_prime_divisors(num, expected):
    assert list(prime_divisors(num)) == expected


lcm_table = [
    ([2, 2], 2),
    ([3, 3, 3, 9], 9),
    ([2, 4, 6, 8], 24),
]


@pytest.mark.parametrize("nums, expected", lcm_table)
def test_least_common_multiple(nums, expected):
    assert least_common_multiple(nums) == expected


prime_table = [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (5, True),
    (6, False),
    (7, True),
    (8, False),
    (9, False),
    (10, False),
    (11, True),
    (12, False),
    (13, True),
    (14, False),
]


@pytest.mark.parametrize("num, expected", prime_table)
def test_is_prime(num, expected):
    assert is_prime(num) == expected


partition_table = [
    (1, [[1]]),
    (2, [[2], [1, 1]]),
    (3, [[3], [1, 2], [1, 1, 1]])
]


@pytest.mark.parametrize("num, expected", partition_table)
def test_partition(num, expected):
    assert list(partitions(num)) == expected

"""
    normalized_prime_divisors_with_powers(6) = [1, [(2,1), (3, 1)]
    normalized_prime_divisors_with_powers(12) = [1, [(2,2), (3, 1)]
    normalized_prime_divisors_with_powers(18) = [1, [(2,1), (3, 2)]
    normalized_prime_divisors_with_powers(36) = [2, [(2,1), (3, 1)]
    normalized_prime_divisors_with_powers(64) = [6, [(2,1)]
"""
normalized_prime_table = [
    (1, [1, [(1, 1)]]),
    (2, [1, [(2, 1)]]),
    (3, [1, [(3, 1)]]),
    (4, [2, [(2, 1)]]),
    (6, [1, [(2, 1), (3, 1)]]),
    (12, [1, [(2, 2), (3, 1)]]),
    (18, [1, [(2, 1), (3, 2)]]),
    (36, [2, [(2, 1), (3, 1)]]),
]

@pytest.mark.parametrize("num, expected", normalized_prime_table)
def test_normalized_prime_divisors_with_powers(num, expected):
    assert normalized_prime_factors_with_powers(num) == tuple(expected)

