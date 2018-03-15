import datetime
import pytz


def get_delta_hour_to_us_east():
    native_dt = datetime.datetime.now()
    us_dt = datetime.datetime.now(pytz.timezone('US/Eastern'))
    delta_hour = datetime.datetime(native_dt.year, native_dt.month, native_dt.day, native_dt.hour, native_dt.minute, 0)\
                 - datetime.datetime(us_dt.year, us_dt.month, us_dt.day, us_dt.hour, us_dt.minute, 0)
    return delta_hour


def convert_to_us_east_dt(current_time):
    delta_hour = get_delta_hour_to_us_east()
    dt = current_time - delta_hour
    return dt
