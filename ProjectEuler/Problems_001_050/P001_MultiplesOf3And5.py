#!/bin/python3
"""
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9.
The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.
"""


def multiples_of_3_5(stop):
    """Compute sum numbers in range(1, stop) if numbers are divided by 3 or 5."""
    # numbers divided by 3 or 5 make cycle length 15.
    frames = (stop - 1) // 15
    # multiples for the first frame: 1-15
    multiples = [i for i in range(1, 15 + 1) if i % 3 == 0 or i % 5 == 0]
    frame_sum = sum(multiples)
    # every next frame has sum increase 15 for every sum element
    frame_increase = 15 * len(multiples)
    # compute 0*frame_increase + 1*frame_increase + .... + (frames - 1) * frame_increase
    # use equation for sum integers from 1 to n-1 which is n * (n - 1) /2
    s = frames * frame_sum + (frames - 1) * frames // 2 * frame_increase

    # add sum for ending part which is not full frame
    for k in range(frames * 15 + 1, stop):
        if k % 3 == 0 or k % 5 == 0:
            s += k

    return s


if __name__ == "__main__":
    # print(multiples_of_3_5(1000))
    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        print(multiples_of_3_5(n))
