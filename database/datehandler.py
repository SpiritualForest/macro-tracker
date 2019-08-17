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

def GetDatetimeObject(day, month, year):
    # construct a datetime object and return it
    return datetime.datetime(year, month, day)

def GetYear():
    # returns the current year
    today = _getToday()
    return today.year

def GetDaysAgo(n):
    # Get the unix timestamp from n days ago
    today = _getToday()
    daysAgo = datetime.datetime(*today) - datetime.timedelta(days=n)
    return daysAgo.timestamp()

def GetTimestampFromDate(datetimeObject):
    return datetimeObject.timestamp()

def GetDateFromTimestamp(timestamp):
    # Performs the opposite conversion: Unix epoch to a datetime object
    return datetime.datetime.fromtimestamp(timestamp)
