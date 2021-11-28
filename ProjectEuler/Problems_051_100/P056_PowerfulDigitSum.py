"""

A googol (10**100) is a massive number: one followed by one-hundred zeros;
100**100 is almost unimaginably large: one followed by two-hundred zeros. Despite their size, the sum of the digits in each number is only 1.

Considering natural numbers of the form, a**b, where a, b < 100, what is the maximum digital sum?

"""


def digits(n):
    """Get number digits in reverse order."""
    yield n % 10
    n //= 10
    while n:
        yield n % 10
        n //= 10


def digit_sum(n):
    """Count sum of number digits"""
    return sum(digits(n))


def max_sum(n):
    """Find the highest sum of a**b where a, b < n."""
    best_sum = 0
    for a in range(2, n):
        num = 1
        for b in range(0, n):
            num *= a
            num_sum = digit_sum(num)
            if num_sum > best_sum:
                best_sum = num_sum
                print(best_sum, a, b+1)
    return best_sum


# print(max_sum(100))
exit()
n = int(input())
print(max_sum(n))