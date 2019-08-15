# Date handler
# We have to convert a given date to a unix epoch time
import datetime

def _getToday():
    today = datetime.date.today()
    return (today.year, today.month, today.day)

def GetToday():
    today = _getToday()
    # We only care about the date, not the time
    datetimeToday = datetime.datetime(*today)
    return datetimeToday.timestamp()

def GetDaysAgo(n):
    # Get the unix timestamp from n days ago
    today = _getToday()
    daysAgo = datetime.datetime(*today) - datetime.timedelta(days=n)
    return daysAgo.timestamp()
