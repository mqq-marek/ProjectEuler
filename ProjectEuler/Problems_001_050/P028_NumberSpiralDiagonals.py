"""
Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:
        21 22 23 24 25
        20  7  8  9 10
        19  6  1  2 11
        18  5  4  3 12
        17 16 15 14 13

It can be verified that the sum of the numbers on the diagonals is 101.
What is the sum of the numbers on the diagonals in a N x N, (N is odd) spiral formed in the same way?
As the sum will be huge you have to print the result mod (10**9 + 7).

"""

"""
Upper right sequence is 1, 9, ... (2n+1)**2
Upper left sequence is 1, 7, ... (2n+1)**2 - 2*n
Down left sequence is 1, 5, ... (2n+1)**2 - 4n
Down right sequence is 1, 3, .. (2n+1)**2 - 6n 

Sum at distance n is 4 * (4*n**2 + n + 1)

"""


def diagonal_sum(square_size):
    n = (square_size - 1) // 2
    sum_1 = n
    sum_n = n * (n + 1) // 2
    sum_n_x_n = sum_n * (2 * n + 1) // 3
    result = (4 * (4*sum_n_x_n + sum_n + sum_1) + 1) % (10**9 + 7)
    return result


print(diagonal_sum(1001))
t = int(input())
for _ in range(t):
    n = int(input())
    print(diagonal_sum(n))
