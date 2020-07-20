import datetime as dt
import pytz


TIMEZONE_BUDAPEST = pytz.timezone('Europe/Budapest')
CURRENT_TIMEZONE = TIMEZONE_BUDAPEST


def main(submission_date, turnaround_time):
    validate_submission_date(submission_date)
    resolution_date = get_resolution_date(submission_date, turnaround_time)
    return resolution_date


def validate_submission_date(submission_date, current_timezone=CURRENT_TIMEZONE):
    return True
