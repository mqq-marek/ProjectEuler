import pytest
from itertools import islice
from core import fibonacci, divisors, sequence_condition, prime_divisors, least_common_multiple


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
