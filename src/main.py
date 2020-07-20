import datetime as dt

import pytz

from . import exceptions


TIMEZONE_BUDAPEST = pytz.timezone("Europe/Budapest")
CURRENT_TIMEZONE = TIMEZONE_BUDAPEST
WORKING_HOURS_START = dt.time(9)
WORKING_HOURS_END = dt.time(17)
ZERO_DURATION = dt.timedelta(seconds=0)


def main(submission_date, turnaround_time):
    is_submission_date_valid, reason = validate_submission_date(submission_date)
    if not is_submission_date_valid:
        return reason

    resolution_date = get_resolution_date(submission_date, turnaround_time)
    return resolution_date


def validate_submission_date(submission_date: dt.datetime, current_timezone=CURRENT_TIMEZONE):
    try:
        _validate_working_day(submission_date, current_timezone)
    except exceptions.NotWorkingDay as e:
        return False, e

    try:
        _validate_working_hours(submission_date, current_timezone)
    except exceptions.NotWorkingHours as e:
        return False, e

    return True, None


def _validate_working_day(submission_date: dt.datetime, current_timezone):
    # TODO: add timezone
    if submission_date.weekday() in [5, 6]:  # Monday is index 0
        raise exceptions.NotWorkingDay(f"Submission date <{submission_date}> is not a working day")


def _validate_working_hours(submission_date: dt.datetime, current_timezone):
    if not (WORKING_HOURS_START <= submission_date.astimezone(current_timezone).time() < WORKING_HOURS_END):
        raise exceptions.NotWorkingHours(f"Submission date <{submission_date}> falls outside of working hours")


def get_resolution_date(
    submission_date: dt.datetime, turnaround_time: dt.timedelta, current_timezone=CURRENT_TIMEZONE
):
    resolution_date = submission_date
    remaining_time = turnaround_time
    while True:
        if resolution_date.weekday() in [5, 6]:
            resolution_date += dt.timedelta(days=7 - resolution_date.weekday())
        end_of_working_day = resolution_date.replace(hour=WORKING_HOURS_END.hour, minute=WORKING_HOURS_END.minute)
        time_until_end_of_working_hours = end_of_working_day - resolution_date
        usable_remaining_time = min(remaining_time, time_until_end_of_working_hours)
        resolution_date += usable_remaining_time
        remaining_time -= usable_remaining_time

        if remaining_time > ZERO_DURATION:
            resolution_date += dt.timedelta(days=1)
            resolution_date = resolution_date.replace(hour=WORKING_HOURS_START.hour, minute=WORKING_HOURS_START.minute)
            if resolution_date.weekday() in [5, 6]:
                resolution_date += dt.timedelta(days=7 - resolution_date.weekday())
        else:
            if resolution_date.hour == WORKING_HOURS_END.hour and resolution_date.minute == WORKING_HOURS_END.minute:
                resolution_date += dt.timedelta(days=1)
                resolution_date = resolution_date.replace(
                    hour=WORKING_HOURS_START.hour, minute=WORKING_HOURS_START.minute
                )
            if resolution_date.weekday() in [5, 6]:
                resolution_date += dt.timedelta(days=7 - resolution_date.weekday())
            break

    print("Final res date", resolution_date)
    return resolution_date
