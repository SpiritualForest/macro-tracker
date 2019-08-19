# Date handler
# We have to convert a given date to a unix epoch time
import datetime
import calendar

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
    year, month, day = _getToday()
    return year

def GetDaysAgo(n):
    # returns a datetime object whose date is <n> days ago from today
    today = _getToday()
    return datetime.datetime(*today) - datetime.timedelta(days=n)

def GetTimestampFromDate(datetimeObject):
    return datetimeObject.timestamp()

def GetDateFromTimestamp(timestamp):
    # Performs the opposite conversion: Unix epoch to a datetime object
    return datetime.datetime.fromtimestamp(timestamp)

def GetDateString(timestamp):
    # Get a string of the date: "15 January 2019", from a unix epoch
    datetimeObject = GetDateFromTimestamp(timestamp)
    month = calendar.month_name[datetimeObject.month]
    return "{} {} {}".format(datetimeObject.day, month, datetimeObject.year)
