__all__ = ['DateUtil']


def is_same_date(current, target):
    return current.year == target.year and current.month == target.month and current.day == target.day


def is_same_time(current, target):
    return current.hour == target.hour and current.minute == target.minute


def is_same_hour(current, target):
    return current.hour == target.hour and current.minute == target.minute
