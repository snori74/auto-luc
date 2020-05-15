from datetime import datetime, date
import calendar

import sys


"""
this snippet might help:

    import datetime
    def next_weekday(d, weekday):
      days_ahead = weekday - d.weekday()
      if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

    d = datetime.date(2011, 7, 2)
    next_monday = next_weekday(d, 0) # 0 = Monday, 1=Tuesday, 2=Wednesday...
    print(next_monday)

"""
try:
    sys.argv[1]
except:
    today = date.today()
    today_str = today
    print("Today is: ", today_str, "i.e.: ", today.day, " of ", today.month)
else:
    today_str = sys.argv[1]
    print("'today' is deemed to be: ", today_str)
    today = datetime.strptime(today_str, '%Y-%m-%d')
"""
if args == sys.argv[1:] is None:
    today = date.today()
    today_str = str(date.today())
    print("Today's date:", today)
else:
    today = sys.argv[1]
"""

iso_tuple = today.isocalendar()
print("In year: ",iso_tuple[0])
print("In ISO week: ", iso_tuple[1])
print("And day #; ", iso_tuple[2], '(ISO, where 0=Sunday)')


first_weekday, num_days_in_month = calendar.monthrange(iso_tuple[0], today.month)
print("First weekday of this month is: ",first_weekday, calendar.day_name[first_weekday])

""" 
OK, so if first weekday = 3 (wed) then the next Mon the first one of thr month
amd DAY1 of  our course  weekday.day + (6-firstweekday)
"""
x = datetime(today.year,today.month, first_weekday + (6-first_weekday))
print("Dat one of the course:", x)
