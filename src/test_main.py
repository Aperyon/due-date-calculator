import datetime as dt

import pytest
import pytz

from .main import CURRENT_TIMEZONE, validate_submission_date


UTC = pytz.utc


def test_earlier_timezone():
    now = dt.datetime.now()
    assert UTC.localize(now) > CURRENT_TIMEZONE.localize(now)


@pytest.mark.parametrize('submission_date, current_timezone, is_valid', [
    (dt.datetime(2020, 1, 1, 12, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, True),  # Wednesday
    (dt.datetime(2020, 1, 1, 9, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, True),
    (dt.datetime(2020, 1, 1, 9, tzinfo=CURRENT_TIMEZONE), UTC, False),
    (dt.datetime(2020, 1, 1, 10, tzinfo=CURRENT_TIMEZONE), UTC, True),
    (dt.datetime(2020, 1, 1, 8, 59, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, True),
    (dt.datetime(2020, 1, 1, 17, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, False),
    (dt.datetime(2020, 1, 1, 17, tzinfo=CURRENT_TIMEZONE), UTC, True),
    (dt.datetime(2020, 1, 1, 16, 59, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, True),
    (dt.datetime(2020, 1, 2, 12, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, True),  # Thursday
    (dt.datetime(2020, 1, 3, 12, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, True),  # Friday
    (dt.datetime(2020, 1, 4, 12, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, False),  # Saturday
    (dt.datetime(2020, 1, 5, 12, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, False),  # Sunday
    (dt.datetime(2020, 1, 6, 12, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, True),  # Monday
    (dt.datetime(2020, 1, 7, 12, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, True),  # Tuesday
    (dt.datetime(2020, 6, 15, 9, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, True),  # DST
    (dt.datetime(2020, 6, 15, 10, tzinfo=CURRENT_TIMEZONE), CURRENT_TIMEZONE, True),  # DST
    (dt.datetime(2020, 6, 15, 10, tzinfo=CURRENT_TIMEZONE), UTC, False),
    (dt.datetime(2020, 6, 15, 11, tzinfo=CURRENT_TIMEZONE), UTC, True),
])
def test_validate_submission_date(submission_date, current_timezone, is_valid):
    assert validate_submission_date(submission_date, current_timezone) is is_valid
