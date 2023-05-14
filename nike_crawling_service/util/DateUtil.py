__all__ = ['DateUtil']


def is_same_date(self, current, target):
    return current.year == target.year and current.month == target.month and current.day == target.day


def is_same_time(self, current, target):
    return current.hour == target.hour and current.minute == target.minute
