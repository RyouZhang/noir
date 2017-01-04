import calendar
import datetime
import time

def get_timestamp():
    return time.time() * 1000


# def get_now_ts():
#     now = datetime.datetime.utcnow()
#     timestamp = calendar.timegm(now.timetuple())
#
#     return timestamp