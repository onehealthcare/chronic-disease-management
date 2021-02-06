import datetime
import pytest
from utils.datetime_utils import _datetime


def test_datetime():
    sdt = '2021-01-01 12:01:03'
    dt = _datetime(sdt)

    assert dt == datetime.datetime.strptime(sdt, '%Y-%m-%d %H:%M:%S')

    with pytest.raises((ValueError, TypeError)):
        _datetime(1)

    with pytest.raises((ValueError, TypeError)):
        _datetime('a')
