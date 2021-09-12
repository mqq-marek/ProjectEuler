"""

Take the number 192 and multiply it by each of 1, 2, and 3:

192 * 1 = 192
192 * 2 = 384
192 * 3 = 576
By concatenating each product we get the 1 to 9 pandigital, 192384576.
We will call 192384576 the concatenated product of 192 and (1,2,3)

The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5,
giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

What is the largest 1 to 9 pandigital 9-digit number that can be formed
as the concatenated product of an integer with (1,2, ... , n) where n > 1?

The similar process can be shown for  to  pandigital also.  when multiplied by  gives  which is  pandigital.

You are given  N and K where K = 8 or 9, find the multipliers
for that given K below N and print them in ascending order.

"""

def is_pandigital(n_str, k):
    """Verify number is pandigital."""
    if len(n_str) == k and set(n_str) == set('123456789'[:k]):
        return True
    else:
        return False


def pandigital_product(n, k):
    """Verify product of n is pandigital."""
    num = ''
    for i in range(1, k):
        num += str(n * i)
        if len(num) >= k:
            break
    return num, is_pandigital(num, k)


def find_pandigital_product(n, k):
    """Get all pandigital in range."""
    for i in range(1, n + 1):
        num, is_ok = pandigital_product(i, k)
        if is_ok:
            yield num, i


#print(max(find_pandigital_product(10**5+1, 9))[0])
n, k = map(int, input().split())
pandigital = sorted(list(find_pandigital_product(n, k)), key=lambda x: x[1])
for pair in pandigital:
    print(pair[1])

