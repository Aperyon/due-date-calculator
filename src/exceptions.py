# TODO: proper error messages
class InvalidDate(Exception):
    pass


class NotWorkingDay(InvalidDate):
    pass


class NotWorkingHours(InvalidDate):
    pass