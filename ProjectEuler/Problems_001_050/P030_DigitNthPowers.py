"""
Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:
    1634 = 1**4 + 6**4 + 3**4 + 4**4
    8208
    9474

    The sum of these numbers is 19316.

    Find the sum of all the numbers that can be written as the sum of Nth powers of their digits.

"""
from itertools import product




def max_number_len(n):
    """Find max power of 10 which can be less or equals than sum of its digits power."""
    power_of_9 = 9**n
    k = 1
    while k*power_of_9 >= 10 ** k:
        k += 1
    return k


digits = [i for i in range(10)]
digit_power = [0] * 10
sum_powers = set()


def digits_product(k):
    nums = [0] * k
    while True:
        yield nums
        for i in range(k):
            nums[i] += 1
            if nums[i] != 10:
                for j in range(i):
                    if nums[j] < nums[i]:
                        nums[j] = nums[i]
                break
            nums[i] = 0
            if i == k-1:
                return


def number_to_digits(num):
    """Return sorted list of digits in number."""
    return sorted(int(ch) for ch in str(num))


def find_sum(n):
    for i in range(10):
        digit_power[i] = i ** n

    sum_len = 2
    while sum_len * digit_power[9] >= 10 ** (sum_len - 1):
        for p in digits_product(sum_len):
            p_sum = sum(digit_power[digit] for digit in p)
            if sorted(p) == number_to_digits(p_sum):
                sum_powers.add(p_sum)
        sum_len += 1
    return sum(sum_powers)


# print(find_sum(5))
n = int(input())
print(find_sum(n))

