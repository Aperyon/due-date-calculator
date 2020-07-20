import datetime as dt

import pytest
import pytz

from .main import CURRENT_TIMEZONE, validate_submission_date, get_resolution_date


UTC = pytz.utc


def test_earlier_timezone():
    now = dt.datetime.now()
    assert UTC.localize(now) > CURRENT_TIMEZONE.localize(now)


@pytest.mark.parametrize(
    "submission_date, current_timezone, expected_validity",
    [
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 12)), CURRENT_TIMEZONE, True),  # Wednesday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 9)), CURRENT_TIMEZONE, True),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 9)), UTC, False),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 10)), UTC, True),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 8, 59)), CURRENT_TIMEZONE, False),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 17)), CURRENT_TIMEZONE, False),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 17)), UTC, True),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 16, 59)), CURRENT_TIMEZONE, True),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 2, 12)), CURRENT_TIMEZONE, True),  # Thursday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 3, 12)), CURRENT_TIMEZONE, True),  # Friday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 4, 12)), CURRENT_TIMEZONE, False),  # Saturday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 5, 12)), CURRENT_TIMEZONE, False),  # Sunday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 6, 12)), CURRENT_TIMEZONE, True),  # Monday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 7, 12)), CURRENT_TIMEZONE, True),  # Tuesday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 9)), CURRENT_TIMEZONE, True),  # DST
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 10)), CURRENT_TIMEZONE, True),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 10)), UTC, False),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 11)), UTC, True),
    ],
)
def test_validate_submission_date(submission_date, current_timezone, expected_validity):
    is_valid, reason = validate_submission_date(submission_date, current_timezone)
    assert is_valid is expected_validity, reason


@pytest.mark.parametrize('submission_date, turnaround_time, expected_resolution_date', [
    CURRENT_TIMEZONE.localize(2020, 6, 15, 12), dt.timedelta(hours=1), CURRENT_TIMEZONE.localize(2020, 6, 15, 13)
])
def test_getting_resolution_date(submission_date, turnaround_time, expected_resolution_date):
    assert get_resolution_date(submission_date, turnaround_time) == expected_resolution_date
