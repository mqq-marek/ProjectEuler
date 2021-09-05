import pytest
from itertools import islice
from core import (
 count_divisible_in_range,
)


divisible_table = [
    ([2], 1, 0),
    ([2], 2, 0),
    ([2], 3, 1),
    ([2], 4, 1),
    ([2], 5, 2),
    ([2, 3], 3, 1),
    ([2, 3], 4, 2),
    ([2, 3], 5, 3),
    ([2, 3], 6, 3),
    ([2, 3], 7, 4),
]

@pytest.mark.parametrize("divisors, num, expected", divisible_table)
def test_count_divisible_in_range(divisors, num, expected):
    assert count_divisible_in_range(divisors, num) == expected
