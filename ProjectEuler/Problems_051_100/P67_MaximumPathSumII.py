"""
By starting at the top of the triangle and moving to adjacent numbers on the row below,
find the maximum total from top to bottom.
Find the maximum total from top to bottom of the triangle given in input.
"""

TRIANGLE = """75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23
"""


def extend(best):
    """ Extend current best sum for next triangle row offering best value from previous row.
    E.g. for triangle: 1 / 2, 3 / 4, 1, 5 best values second row are: 3, 4. Emit 3, 4, 4 for
    updating third row which gives best values as: 7, 5, 9, which gives 7, 7, 9, 9 for next row.
    :param best: current best value sum for previous row
    :return: select best value from previous row for current row
    """
    prev = 0
    for num in best:
        yield max(prev, num)
        prev = num
    yield prev


def best_value(arr):
    """ Find highest sum from top to bottom. """
    best_sum = [arr[0][0]]
    for a_row in arr[1:]:
        best_sum = [a + b for a, b in zip(a_row, extend(best_sum))]
    return max(best_sum)


def dev_main(data):
    lines = data.splitlines()
    arr = []
    for line in lines:
        row = list(map(int, line.split()))
        arr.append(row)
    best = best_value(arr)
    print(best)


def hacker_main():
    t = int(input())
    for t0 in range(t):
        n = int(input())
        arr = []
        for n0 in range(n):
            row = list(map(int, input().split()))
            assert len(row) == n0 + 1
            arr.append(row)
        best = best_value(arr)
        print(best)


def euler_main():
    with open('P067_Triangle.txt') as f:
        arr = []
        for line in f.readlines():
            row = list(map(int, line.split()))
            arr.append(row)
        best = best_value(arr)
        print(best)


if __name__ == "__main__":
    # euler_main()
    # dev_main(TRIANGLE)
    hacker_main()
