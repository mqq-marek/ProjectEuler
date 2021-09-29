"""
The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.

Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.

"""

n = int(input())
total = 0
for i in range(1, n+1):
    total += pow(i, i, 10**10)
print(total%(10**10))