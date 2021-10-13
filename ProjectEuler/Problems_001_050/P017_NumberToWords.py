"""

 Number to Words


"""
UP_TO_TWENTY = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten","Eleven",
                "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
HUNDRED = 'Hundred'
ZERO = "Zero"
THOUSAND = "Thousand"
MILLION = "Million"
BILLION = "Billion"
TRILLION = "Trillion"
MINUS = "Minus"


def up_to_100(n):
    words = []
    if n >= 20:
        words.append(TENS[n // 10])
        n = n % 10
    words.append(UP_TO_TWENTY[n])
    return words


def up_to_1000(n, and_support=False):
    words = []
    if n > 99:
        words.append(UP_TO_TWENTY[n // 100])
        words.append(HUNDRED)
        n = n % 100
        if n > 0:
            words += 'And'
    words += up_to_100(n)
    return words


def triple_part(n, part, suffix, and_support=False):
    nn = (n // 10 ** part) % 1000
    words = []
    if nn > 0:
        words = up_to_1000(nn, and_support=and_support)
        words.append(suffix)
    return words


def number_to_words(n, and_support=False):
    if n == 0:
        return ZERO
    words = []
    if n < 0:
        words.append(MINUS)
        n = -n
    words += triple_part(n, 12, TRILLION, and_support=and_support)
    words += triple_part(n, 9, BILLION, and_support=and_support)
    words += triple_part(n, 6, MILLION, and_support=and_support)
    words += triple_part(n, 3, THOUSAND, and_support=and_support)
    words += triple_part(n, 0, "", and_support=and_support)
    result = ' '.join([w for w in words if w])
    return result


def euler_main():
    total = 0
    for i in range(1, 1001):
        s = number_to_words(i,and_support=True)
        total += sum(1 for ch in s if ch.isalpha())
    return total


def hacker_main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        result = number_to_words(n)
        print(result)


print(number_to_words(101,and_support=True))
print(euler_main())
#print(number_to_words(104300513783))
# print(digits_sum(1000))
hacker_main()
