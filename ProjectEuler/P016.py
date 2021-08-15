"""

What is the sum of the digits of the number  2**N?

"""

def digits_sum(n):
    pn = 2**n
    return sum(int(ch) for ch in str(pn))


def hacker_main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        result = digits_sum(n)
        print(result)


# print(digits_sum(1000))
hacker_main()