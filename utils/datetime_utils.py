import datetime
import time


def _datetime(d):
    # string 转成 datetime
    if isinstance(d, datetime.datetime):
        return d
    if isinstance(d, datetime.date):
        return datetime.datetime(d.year, d.month, d.day)
    try:
        n = datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            n = datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            try:
                n = datetime.datetime.strptime(d, '%Y-%m-%d')
            except ValueError:
                n = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M")
    return n


def _date(d):
    # date 和 string 转成 datetime
    if isinstance(d, datetime.date):
        return datetime.datetime(d.year, d.month, d.day)
    else:
        # string 类型的都在_datetime 方法判断
        d = _datetime(d)
        return datetime.datetime(d.year, d.month, d.day)


def _strftime(d):
    return d.strftime('%Y-%m-%d %H:%M:%S')


def str2date(d):
    # string 转成 date
    if isinstance(d, datetime.date):
        return d
    return _datetime(d).date()


def datetime_range(start, end, step=datetime.timedelta(days=1)):
    current = start
    while current < end:
        yield current
        current += step


def datetime_today(d=None):
    """获取今天0时0分0秒的datetime。"""
    if not d:
        d = datetime.date.today()
    return _date(d)


def this_hour(d):
    return datetime.datetime(d.year, d.month, d.day, d.hour)


def this_month(d):
    ''' 返回这个月的第一天
    '''
    return datetime.datetime(d.year, d.month, 1)


def next_month(d):
    ''' 返回下个月的第一天
    '''
    temp = this_month(d) + datetime.timedelta(days=45)
    return this_month(temp)


def prev_month(d):
    ''' 返回上个月的第一天 '''
    temp = this_month(d) - datetime.timedelta(days=15)
    return this_month(temp)


def month_range(start, end):
    time = this_month(start)
    while time < end:
        yield time
        time = next_month(time)


def this_week(date):
    ''' 返回date对应周的星期一 '''
    date = datetime_today(date)
    week_day = date.weekday()
    return date - datetime.timedelta(days=week_day)


def week_day(date, day):
    ''' 返回date对应周的星期X，day=0代表周一 '''
    date = this_week(date)
    return date + datetime.timedelta(days=day)


def next_week(date):
    ''' 返回date对应下周的星期一 '''
    date = datetime_today(date)
    return this_week(date) + datetime.timedelta(days=7)


truncate_week = this_week


truncate_month = this_month


def truncate_day(d):
    d = _datetime(d)
    return datetime.datetime(d.year, d.month, d.day)


def truncate_hour(d):
    d = _datetime(d)
    s = d.strftime("%Y-%m-%d %H")
    return datetime.datetime.strptime(s, '%Y-%m-%d %H')


def truncate_minute(d):
    d = _datetime(d)
    s = d.strftime("%Y-%m-%d %H:%M")
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M')


def truncate_second(d):
    d = _datetime(d)
    s = d.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def to_timestamp(d):
    d = _datetime(d)
    return time.mktime(d.timetuple())


def timestamp_to_datetime(t):
    return datetime.datetime.fromtimestamp(int(t))


def is_within_a_week(d, now=None):
    d = _datetime(d)
    now = datetime.datetime.now() if not now else _datetime(now)
    return abs(d - now) <= datetime.timedelta(days=7)
