import datetime as dt

import pytz

from . import exceptions


TIMEZONE_BUDAPEST = pytz.timezone("Europe/Budapest")
CURRENT_TIMEZONE = TIMEZONE_BUDAPEST
WORKING_HOURS_START = dt.time(9)
WORKING_HOURS_END = dt.time(17)
WEEKEND_DAY_INDICES = [5, 6]
ZERO_DURATION = dt.timedelta(seconds=0)


def main(submission_date, turnaround_time_in_hours):
    is_submission_date_valid, reason = validate_submission_date(submission_date)
    if not is_submission_date_valid:
        return reason

    resolution_date = get_resolution_date(submission_date, turnaround_time_in_hours)
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
    if submission_date.weekday() in WEEKEND_DAY_INDICES:
        raise exceptions.NotWorkingDay(f"Submission date <{submission_date}> is not a working day")


def _validate_working_hours(submission_date: dt.datetime, current_timezone):
    if not (WORKING_HOURS_START <= submission_date.astimezone(current_timezone).time() < WORKING_HOURS_END):
        raise exceptions.NotWorkingHours(f"Submission date <{submission_date}> falls outside of working hours")


def get_resolution_date(
    submission_date: dt.datetime, turnaround_time_in_hours: dt.timedelta, current_timezone=CURRENT_TIMEZONE
):
    original_timezone = submission_date.tzinfo
    resolution_date = submission_date.astimezone(current_timezone)
    remaining_time = dt.timedelta(hours=turnaround_time_in_hours)

    while remaining_time > ZERO_DURATION:
        end_of_working_day = resolution_date.replace(hour=WORKING_HOURS_END.hour, minute=WORKING_HOURS_END.minute)
        time_until_end_of_working_hours = end_of_working_day - resolution_date
        usable_remaining_time = min(remaining_time, time_until_end_of_working_hours)
        resolution_date += usable_remaining_time
        remaining_time -= usable_remaining_time

        if is_end_of_working_hours(resolution_date):
            resolution_date = _get_next_work_day_start(resolution_date, original_timezone)

    return resolution_date


def _get_next_work_day_start(initial_date, original_timezone):
    next_work_day = initial_date + dt.timedelta(days=1)
    if next_work_day.weekday() in WEEKEND_DAY_INDICES:
        next_work_day += dt.timedelta(days=7 - next_work_day.weekday())

    next_work_day_start = next_work_day.replace(hour=WORKING_HOURS_START.hour, minute=WORKING_HOURS_START.minute)
    next_work_day_start = next_work_day_start.replace(tzinfo=original_timezone)
    return next_work_day_start


def is_end_of_working_hours(datetime):
    return datetime.hour == WORKING_HOURS_END.hour and datetime.minute == WORKING_HOURS_END.minute
