#!/usr/bin/env python3

'''
 The course:

    "runs from the first Monday of the month, for four weeks"

Seems pretty simple huh?

Yes, but there are some surprising results ('corner cases') like, sometimes:

 - the last few days of the course for <MONTH>, end up being in <MONTH+1> (e.g April 2020)
 - there is a whole week gap at the end of a course (e.g. June 2020)

One approach to a bot is to run it each day - and check what day of what course we're on
and then act accordingly. Basically, on "Day x" retreive and post the "Day x" lesson - but also 
delete that for "Day x'-5. On Day 16, post a message about next month course (and also to other 
subreddits), and on Day 1 clean out all the old lessons.But, the big trick is to (from today's date)figure out if the course is running at all, and if so, which day we're on.

So, the check_today() function is pretty important:

def check_today():
    return([10,"May", "June"])

This is my "4am logic" as to what should go in there:

    If we're on day 4 of the week (i.e. Thursday), save that value as "days_into_week" 
    then find the Monday of that week (i.e. date - days_into_week). The month of that 
    is "month_name" in all cases. Calculating "next_month" is of course trivial.
    Now, from that Monday, step back 7 days each time, counting, until 
    Month.(this_monday) <> month_name. Now (7 * weeks_back + days_into_week) gives us day_num

I'm pretty sure that covers all cases...

 - Steve  
'''
import datetime

def main():
    # define a range of dates that we'll test
    start_date = datetime.date(2019, 12, 1)
    end_date = datetime.date(2022, 3, 30)

    # and we'll step through a day at a time...
    delta = datetime.timedelta(days=1)

    while start_date <= end_date:
        daynum, monthnum, monthname = (check_today(start_date))
        print("Today is ", start_date, "lesson is Day", daynum, " of course for month ", monthnum)
        start_date += delta




# ------------------------end of main()-----------------------------------------

def check_today(thisdate):
    '''
    Logic:

    If we're on day 4 of the week (i.e. Thursday), save that value as "days_into_week"
    then find the Monday of that week (i.e. date - days_into_week). 
    The month of that is "month_name" in all cases. 
    Now, from that Monday, step back 7 days each time, counting, until 
    Month.(this_monday) <> month_name. 
    Now (7 * weeks_back + days_into_week) gives us day_num
    '''
    delta = datetime.timedelta(days=1)
    delta7 = datetime.timedelta(days=7)
    
    #   If we're on day 4 of the week (i.e. Thursday), save that value
    #   as "days_into_week"
    days_into_week = thisdate.isoweekday()    #    ISO weekday, 1=Monday
    
    #   If we're on a weekend day then we exit with all nulls
    if days_into_week == 6: return(None, None, None)
    if days_into_week == 7: return(None, None, None)

    #   then find the Monday of that week (i.e. date - days_into_week). 
    thismonday = thisdate - (delta * days_into_week)

    #   The month of that is "month_num" in all cases. 
    month_num = thismonday.month    #    January=1, December=12

    #   Now, from that Monday, step back 7 days each time, counting, 
    #   until Month.(this_monday) <> month_num. 
    weeks_back = 0
    while thismonday.month == month_num:
        thismonday = thismonday - (delta7)
        weeks_back = weeks_back + 1

    # Now (5 * weeks_back + days_into_week) gives us day_num
    day_num = (5*weeks_back) + days_into_week -5
    #  But we only have 20 lessons...
    if day_num > 20: return(None, None, None)
    return([day_num,month_num, "June"])

if __name__ == "__main__":
    main()


