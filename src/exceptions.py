class InvalidDate(Exception):
    pass


class NotWorkDay(InvalidDate):
    pass


class NotWorkingHours(InvalidDate):
    pass
