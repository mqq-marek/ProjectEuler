"""
You are given the following information, but you may prefer to do some research for yourself.

1 Jan 1900 was a Monday.
Thirty days has September,
April, June and November.
All the rest have thirty-one,
Saving February alone,
Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.

A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.

How many Sundays fell on the first of the month between two dates(both inclusive)?

"""
from collections import defaultdict

normal_leap_days_per_month = {0: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                              1: [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                              }

normal_leap_monthly_sundays = {0: {}, 1: {}}

NORMAL_WEEK_STEP = 365 % 7
LEAP_WEEK_STEP = 366 % 7


def is_leap(year):
    """ Return NORMAL or LEAP year. """
    if year % 400 == 0:
        return 1
    if year % 100 == 0:
        return 0
    if year % 4 == 0:
        return 1
    return 0


def start_month(year, month, day):
    if day != 1:
        month += 1
        if month == 13:
            month = 1
            year += 1
    return year, month


def day_of_week(year, month, day):
    """Return day of week. """
    days = 0
    h4, rem = divmod(year - 1900, 400)
    # In h4(400 years) we have 303 normal years and 97 leap
    days += h4 * (303 * NORMAL_WEEK_STEP + 97 * LEAP_WEEK_STEP)
    for y in range(1900, 1900 + rem):
        if is_leap(y):
            days += LEAP_WEEK_STEP
        else:
            days += NORMAL_WEEK_STEP
    days += sum(normal_leap_days_per_month[is_leap(year)][:month - 1])
    days += day - 1
    return days % 7


def init_sundays_per_year():
    """ Number of begin month sSundays based on day of week at year start.
    """
    def count_year(day, months):
        cnt = 0
        for ml in months:
            if day % 7 == 6:
                cnt += 1
            day += ml
        return cnt

    for start_day in range(7):
        normal_leap_monthly_sundays[0][start_day] = count_year(start_day, normal_leap_days_per_month[0])
        normal_leap_monthly_sundays[1][start_day] = count_year(start_day, normal_leap_days_per_month[1])


def sundays_in_range(ys, ms, y2, m2):
    """ Return number of Sundays at beginning of month. """
    day1 = day_of_week(ys, ms, 1)
    months_tab = normal_leap_days_per_month[is_leap(ys)]
    counter = 0
    while ys < y2 or (ys == y2 and ms <= m2):
        if day1 % 7 == 6:
            counter += 1
        day1 += months_tab[ms - 1]
        ms += 1
        if ms == 13:
            ms = 1
            ys += 1
            months_tab = normal_leap_days_per_month[is_leap(ys)]
    return counter


def sundays_in_years_range(ys, ye):
    """ Return day of week for begin of month in range."""
    day1 = day_of_week(ys, 1, 1) % 7
    counter = 0
    for y in range(ys, ye):
        test_leap = is_leap(y)
        counter += normal_leap_monthly_sundays[test_leap][day1]
        if test_leap:
            day1 = (day1 + LEAP_WEEK_STEP) % 7
        else:
            day1 = (day1 + NORMAL_WEEK_STEP) % 7
    return counter


def sundays(y1, m1, d1, y2, m2):
    """ Count Sundays between two dates. """
    y1, m1 = start_month(y1, m1, d1)
    if y1 == y2:
        return sundays_in_range(y1, m1, y2, m2)
    counter = sundays_in_range(y1, m1, y1, 12)
    counter += sundays_in_years_range(y1 + 1, y2)
    counter += sundays_in_range(y2, 1, y2, m2)
    return counter


if __name__ == '__main__':
    init_sundays_per_year()
    # print(sundays(1901, 1, 1, 2000, 12))
    t = int(input())
    for _ in range(t):
        ys, ms, ds = map(int, input().split())
        ye, me, de = map(int, input().split())
        print(sundays(ys, ms, ds, ye, me))
