"""

It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits,
but in a different order.

Given N, find all the positive integers, x <=N, such that x, 2*x, ..., K * N  contain the same digits.
125_875 <= N <= 2_000_000
2 <= K <= 6


"""
def find(n, k):
    results = []
    i = 1
    while i <= n:
        i_str = sorted(str(i))
        if k * int(i_str[0]) > 9:
            i = 10 ** len(i_str)
        else:
            for j in range(2, k + 1):
                j_str = sorted(str(i * j))
                if j_str != i_str:
                    break
            else:
                results.append(i)
            i += 1
    return results


# n = 2_000_000
# for k in range(2, 7):
#     results  = find(n, k)
#     for result in results:
#         print(*[i * result for i in range(1, k + 1)])


n, k = [int(s) for s in input().split()]
results = find(n, k)
for result in results:
    print(*[i * result for i in range(1, k + 1)])