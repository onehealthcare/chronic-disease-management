import datetime
import os
import shutil
from typing import Dict

import pytest
from config import LOG_PATH
from utils import file_logger as _logger
from utils.crypto import hmac_sha1_encode
from utils.datetime_utils import (
    _date,
    _datetime,
    _strftime,
    datetime_range,
    datetime_today,
    is_within_a_week,
    month_range,
    next_month,
    next_week,
    prev_month,
    str2date,
    this_hour,
    this_month,
    this_week,
    truncate_day,
    truncate_hour,
    truncate_minute,
    truncate_second,
    week_day,
)


def test_datetime():
    sdt = '2021-01-01 12:01:03'
    dt = _datetime(sdt)

    assert dt == datetime.datetime.strptime(sdt, '%Y-%m-%d %H:%M:%S')

    with pytest.raises((ValueError, TypeError)):
        _datetime(1)

    with pytest.raises((ValueError, TypeError)):
        _datetime('a')

    assert _strftime(dt) == sdt
    assert _datetime(dt.date()) == datetime.datetime(2021, 1, 1)


def test_date():
    sdt = '2021-01-01 12:01:03'
    dt = datetime.datetime(2021, 1, 1)

    assert _date(sdt) == dt
    assert _date(datetime.datetime(2021, 1, 1, 12, 30, 41)) == dt

    assert str2date(sdt) == dt.date()
    assert str2date(dt.date()) == dt.date()


def test_misc():
    sdt = '2021-01-01 12:01:03'
    dt = datetime.datetime(2021, 1, 1)
    now = datetime.datetime.today()
    assert datetime_today() == datetime.datetime(now.year, now.month, now.day)
    assert datetime_today(sdt) == dt
    assert truncate_day(sdt) == dt
    assert truncate_hour(sdt) == datetime.datetime(2021, 1, 1, 12)
    assert truncate_minute(sdt) == datetime.datetime(2021, 1, 1, 12, 1)
    assert truncate_second(sdt) == datetime.datetime(2021, 1, 1, 12, 1, 3)

    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2020, 1, 5)
    dts = list(datetime_range(start=start, end=end))
    assert len(dts) == 4
    assert dts[0] == start
    assert dts[-1] == end - datetime.timedelta(days=1)

    end = datetime.datetime(2021, 1, 5)
    months = list(month_range(start=start, end=end))
    assert len(months) == 13
    assert months[0] == start
    assert months[-1] == datetime.datetime(2021, 1, 1)

    dt = datetime.datetime(2021, 1, 4, 12, 3, 4)
    assert this_hour(dt) == datetime.datetime(2021, 1, 4, 12)
    assert this_month(dt) == datetime.datetime(2021, 1, 1)
    assert next_month(dt) == datetime.datetime(2021, 2, 1)
    assert prev_month(dt) == datetime.datetime(2020, 12, 1)
    assert this_week(dt) == datetime.datetime(2021, 1, 4)
    assert next_week(dt) == datetime.datetime(2021, 1, 11)
    assert week_day(dt, 1) == datetime.datetime(2021, 1, 5)

    # ts = 1609732984.0
    # assert to_timestamp(dt) == ts
    # assert timestamp_to_datetime(ts) == dt

    assert not is_within_a_week(dt, now)
    assert is_within_a_week(dt, datetime.datetime(2021, 1, 7, 12, 3, 4))
    assert not is_within_a_week(dt, datetime.datetime(2021, 2, 7, 12, 3, 4))


def test_logger():
    log_path = os.path.join(LOG_PATH, 'tests/test_utils')
    if os.path.exists(log_path):
        shutil.rmtree(log_path)

    logger = _logger('tests.test_utils')
    logger.info('test info')
    logger.warning('test warning')
    logger.error('test error')

    path = os.path.join(LOG_PATH, 'tests/test_utils/log')
    f = open(path)
    txt = f.read()

    assert 'INFO test info' in txt
    assert 'WARNING test warning' in txt
    assert 'ERROR test error' in txt

    f.close()

    logger2 = _logger('tests.test_utils')
    logger2.info('test info2')
    logger2.warning('test warning2')
    logger2.error('test error2')

    f = open(path)
    txt = f.read()

    assert 'INFO test info2' in txt
    assert 'WARNING test warning2' in txt
    assert 'ERROR test error2' in txt

    f.close()


def test_hmac_sha1():
    data: Dict[str, int] = {"b": 1, "a": 2}
    sign: str = hmac_sha1_encode(data)

    data = {"b": 1, "a": 2, "sign": 'xxxx'}
    assert hmac_sha1_encode(data) == sign
