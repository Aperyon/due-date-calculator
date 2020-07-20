import datetime as dt

import pytest
import pytz

from .main import CURRENT_TIMEZONE, validate_submission_date, get_resolution_date


UTC = pytz.utc


def test_earlier_timezone():
    now = dt.datetime.now()
    assert UTC.localize(now) > CURRENT_TIMEZONE.localize(now)


@pytest.mark.parametrize(
    "submission_date, current_timezone, expected_validity, expected_partial_error_message",
    [
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 12)), CURRENT_TIMEZONE, True, None),  # Wednesday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 9)), CURRENT_TIMEZONE, True, None),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 9)), UTC, False, "working hours"),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 10)), UTC, True, None),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 8, 59)), CURRENT_TIMEZONE, False, "working hours"),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 17)), CURRENT_TIMEZONE, False, "working hours"),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 17)), UTC, True, None),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 1, 16, 59)), CURRENT_TIMEZONE, True, None),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 2, 12)), CURRENT_TIMEZONE, True, None),  # Thursday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 3, 12)), CURRENT_TIMEZONE, True, None),  # Friday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 4, 12)), CURRENT_TIMEZONE, False, "working day"),  # Saturday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 5, 12)), CURRENT_TIMEZONE, False, "working day"),  # Sunday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 6, 12)), CURRENT_TIMEZONE, True, None),  # Monday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 1, 7, 12)), CURRENT_TIMEZONE, True, None),  # Tuesday
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 9)), CURRENT_TIMEZONE, True, None),  # DST
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 10)), CURRENT_TIMEZONE, True, None),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 10)), UTC, False, "working hours"),
        (CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 11)), UTC, True, None),
        (
            pytz.timezone("America/Whitehorse").localize(dt.datetime(2020, 1, 3, 16)),
            UTC,
            False,
            "working day",
        ),  # UTC-9
    ],
)
def test_validate_submission_date(
    submission_date, current_timezone, expected_validity, expected_partial_error_message
):
    is_valid, reason = validate_submission_date(submission_date, current_timezone)

    if expected_partial_error_message is not None:
        assert expected_partial_error_message in reason

    assert type(reason) in [type(None), str]
    assert is_valid is expected_validity, reason


@pytest.mark.parametrize(
    "submission_date, turnaround_time_in_hours, expected_resolution_date, current_timezone",
    [
        (
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 12)),
            1,
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 13)),
            CURRENT_TIMEZONE,
        ),
        (
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 12)),
            2,
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 14)),
            CURRENT_TIMEZONE,
        ),
        (
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 16)),
            1,
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 16, 9)),
            CURRENT_TIMEZONE,
        ),
        (
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 16)),
            2,
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 16, 10)),
            CURRENT_TIMEZONE,
        ),
        (
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 15, 16)),
            9,
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 17, 9)),
            CURRENT_TIMEZONE,
        ),
        (
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 19, 16)),
            1,
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 22, 9)),
            CURRENT_TIMEZONE,
        ),
        (
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 19, 16)),
            1,
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 22, 9)),
            CURRENT_TIMEZONE,
        ),
        (
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 19, 17)),
            1,
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 19, 18)),
            UTC,
        ),
        (
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 19, 17)),
            2,
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 22, 11)),
            UTC,
        ),
        (
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 19, 17)),
            9,
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 22, 18)),
            UTC,
        ),
        (
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 19, 17)),
            17,
            CURRENT_TIMEZONE.localize(dt.datetime(2020, 6, 23, 18)),
            UTC,
        ),
    ],
)
def test_getting_resolution_date(
    submission_date, turnaround_time_in_hours, expected_resolution_date, current_timezone
):
    assert get_resolution_date(submission_date, turnaround_time_in_hours, current_timezone) == expected_resolution_date
