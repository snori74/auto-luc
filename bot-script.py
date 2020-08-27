#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
   bot-script.py - Intended to be run every day. Posts the lessons
                   for the Linux Upskill Challenge into the subreddit 
                   /r/linuxupskillchallenge - based on the text in 
                   github snori74/linuxupskillchallenge.

    Note, you need to be very careful not to run the script twice in one day, 
    as currently it's not 'idempotent'

'''
import configparser
import os
import numpy as np
import sys
import json
import praw
import datetime
from github import Github

def main():
    
    if len(sys.argv) < 2:
        sys.exit(
            "\n Usage: bot-script.py LIVE|TEST [<date>]"
            "\n "
            "\n e.g     bot-script LIVE             "  #   Production, today's date
            "\n         bot-script TEST             "  #   Test, today, to r/linuxupskillBotTest
            "\n         bot-script TEST 2020-11-01  "  #   Test, 1Nov2020 to r/linuxupskillBotTest"
            "\n "
        )
    if sys.argv[1] == "LIVE":    
        subreddit = "linuxupskillchallenge"
        print("Posting to the LIVE r/upskillchallenge...")
        today_date = datetime.date.today()
        print("And working with today's date: ", today_date)
    
    if sys.argv[1] == "TEST":
        subreddit = "linuxupskillBotTest"
        print("Posting to the TEST subreddit:  r/upskillBotTest...")
        
        if len(sys.argv) > 2:
            today_date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
            print("And using date: ", today_date)
        
        else:
            today_date = datetime.date.today()
            print("And working with today's date: ", today_date)

    #   Get credentials
    REDDIT_CLIENT_ID = get_setting("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = get_setting("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = get_setting("REDDIT_USER_AGENT")
    REDDIT_USERNAME = get_setting("REDDIT_USERNAME")
    REDDIT_PASSWORD = get_setting("REDDIT_PASSWORD")
    GITHUB_ACCESS_TOKEN = get_setting("GITHUB_ACCESS_TOKEN")
    
    #   Which day of the course are we on?
    day_num, month_name, next_month = check_today(today_date)
    
    if day_num == 1:
        #    On this day, we post and pin the standard "Day 1"
        #    lesson - and the "short video" - and also repost
        #    the "HOW THIS WORKS" text - but don't pin this, 
        #    because only two posts can be pinned at a time.
        clear_all_pinned()
        get_post_pin_day(day_num)
        get_post_pin_title("Day 1 - a short video")
        get_post_title("HOW THIS WORKS")    #   New post, but not pinned  
        #   clear last few of last month's lessons...
        delete_day(20)
        delete_day(19)
        delete_day(18)
        delete_day(17)
        delete_day(16)
   
    elif day_num == 18:
        #   retrive, post and pin today's lesson as normal
        clear_all_pinned()
        get_post_pin_day(day_num)
        delete_day(day_num - 4)
        #   refresh the "How this Works" post
        get_post_pin_title("HOW THIS WORKS")
        #    ...and post custom 'advert' messages to subreddits
        get_post_advert("linux")
        get_post_advert("linux4noobs")
        get_post_advert("linuxadmin")
        get_post_advert("linuxmasterrace")
        get_post_advert("sysadminiblogs")
        
    else:
        clear_all_pinned(subreddit)
        pin_title("HOW THIS WORKS")
        get_post_pin_day(day_num)
        delete_day(day_num - 4)

# ------------------------------------------supporting functions------------------------

def check_today(thisdate):
    '''
    Course "...runs from the first Monday of the month, and lasts for four weeks..."
    Simple, but there are some surprising corner cases, e.g.:
     - the last day or two of <MONTH>'s course end up being in <MONTH+1> (e.g April 2020)
     - there's sometimes a whole week gap at the end of a course (e.g. June 2020)
    '''
    delta = datetime.timedelta(days=1)
    delta7 = datetime.timedelta(days=7)
    
    #   If we're on day 4 of the week (i.e. Thursday), save as "days_into_week"
    days_into_week = thisdate.isoweekday()    #    ISO weekday, 1=Monday
    
    print("We're on day #: ", days_into_week, " of the week, where 1=Monday", flush=True)

    #   No lesson on the weekend
    if days_into_week == 6: return(None, None, None)
    if days_into_week == 7: return(None, None, None)

    #   Find the Monday of that week... 
    thismonday = thisdate - (delta * (days_into_week-1))
    #   ...the month of that is "month_num" in all cases. 
    month_num = thismonday.month    #    January=1, December=12
    month_name = thismonday.strftime("%B")
    #   Now, from that Monday, step back 7 days each time, counting, 
    #   until Month.(this_monday) <> month_num. 
    weeks_back = 0
    while thismonday.month == month_num:
        thismonday = thismonday - (delta7)
        weeks_back = weeks_back + 1
    #   We've gone one week too far back, so...
    weeks_back = weeks_back -1
 
    #   Each week has five days of lessons - and then the few days of 
    #   the week we're in...
    day_num = ((weeks_back) * 5) + days_into_week

    #   ...but we only have 20 lessons...
    if day_num > 20: return(None, None, None)
    
    print("We're on day: ", day_num, " of the course")
    return([day_num,month_name, "June"])

def get_setting(setting):
    '''
    Pull settings, including 'secrets', from local dot file
    '''
    config = configparser.ConfigParser()
    config_dir = os.path.expanduser('~/.auto-luc/')
    full_path = config_dir + 'config'
    
    try:
        config.read(full_path)
        setting_value = json.loads(config.get("Global", setting))
        print(setting, "=", setting_value)
        return setting_value
    except:
        sys.exit(
            "\n[Error]: ", setting, " not found.\n"
            "\n   The script expects settings to be stored"
            "\n   in the file: ~/.auto-luc/config "
            "\n"
        )


'''
    Renamed, re-org'd functions:
        
        get_post_pin_day(12)
        get_post_pin_title("HOW THIS WORKS")
        get_post_title("HOW THIS WORKS")
        pin_title("HOW THIS WORKS")
        get_post_advert("sysadmin")
        clear_all_pinned()
        delete_day(12)

'''

def get_day(daynum):
    g = Github(GITHUB_ACCESS_TOKEN)
    repo = g.get_repo("snori74/linuxupskillchallenge")
    contents = repo.get_contents("12.md")
    file_name = daynum, ".md"    # e.g "12.md"
    print("Raw contents of ", file_name, ": ", contents.decoded_content)
    print(contents.decoded_content)
    #   extract subject from body
    print("Will post with Subcet of: ", subject)
    return([title, body])

def get_title(title):
    g = Github(GITHUB_ACCESS_TOKEN)
    repo = g.get_repo("snori74/linuxupskillchallenge")
    contents = repo.get_contents("12.md")
    file_name = daynum, ".md"    # e.g "12.md"
    print("Raw contents of ", file_name, ": ", contents.decoded_content)
    print(contents.decoded_content)
    #   extract subject from body
    print("Will post with Subcet of: ", subject)
    return([title, body])

def get_post_pin_day(day_num):
    title, body = get_day(day_num)
    post = subreddit.submit(title, selftext=body,
        url=None, flair_id=None, flair_text=None,
        resubmit=True, send_replies=True, nsfw=False, spoiler=False,
        collection_id=None)
    #   and sticky/pin that post
    post.mod.sticky()

def get_post_pin_title(title):
    title, body = get_title(title)
    post = subreddit.submit(title, selftext=body,
        url=None, flair_id=None, flair_text=None,
        resubmit=True, send_replies=True, nsfw=False, spoiler=False,
        collection_id=None)
    #   and sticky/pin that post
    post.mod.sticky()

def post_to_linux():
    # get fro github 'post_for_lixux.txt'
    # extract subject?
    # post text as md to r/linux 
    pass

def advert_to_subreddit(subreddit):
    '''
    Grab the matching advert text from Github, then
    post it to the subreddit
    '''
    # get from Github
    # split to title and body
    # post to subreddit

def info_on_subreddit(sr):
    print("Is this reddit ReadOnly?:", reddit.read_only)  # Output: False
    subreddit = sr
    print("Selected subreddit: r/", subreddit)
    print("Checking my ID: ", reddit.user.me())
    print("display_name: ", subreddit.display_name)
    print("title; ", subreddit.title)
    print("description: ", subreddit.description)

def clear_all_pinned():
    print('\nPosts: ')
    for post in subreddit.new(limit=25):
        print(post.title)
        if post.stickied:
            print('\tUnsticky-ing the one above')
            post.mod.sticky(state=False) # THIS works!
            post.mod.distinguish(how='no')

def post_sticky(sr, title, body):

    post = sr.submit(title, selftext=body)
    post.mod.distinguish(how='yes')
    post.mod.approve()
    post.mod.sticky(state=True)
    if not post.stickied:
        print("Hmmm, seems we haven't sticky'd: ", title)
        print("Pausing....")
        if post.stickied:
            print('Now done!')
        else:
            print('Still not showing as stickied')

def delete_submission(sr, title):
    print('\nLooking for one to delete...: ')
    for post in sr.new(limit=25):
        print(post.title)
        if post.title == title:
            print("Deleting: ", title)
            post.delete()

if __name__ == "__main__":
    main()

