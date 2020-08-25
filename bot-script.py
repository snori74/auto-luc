#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
   bot-script.py - Intended to be run every day. Posts the lessons
                   for the Linux Upskill Challenge into the subreddit 
                   /r/linuxupskillchallenge - based on the text in 
                   github snori74/linuxupskillchallenge.

Note, need to be very careful not to run the script twice in one day, currently
it is not 'idempotent'
'''

import configparser
import os
import numpy as np
import sys
import json
import praw
import datetime
from github import Github
from luc_settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from luc_settings import REDDIT_USERNAME, REDDIT_PASSWORD
from luc_settings import GITHUB_ACCESS_TOKEN

def main():
    
    if len(sys.argv) < 2:
        sys.exit(
            "\n Usage: bot-script.py LIVE|TEST [<date>]"
            "\n "
            "\n e.g     bot-script LIVE             "  #   Production, today's date
            "\n         bot-script TEST             "  #   Test, today's date - posts to r/linuxupskillBotTest
            "\n         bot-script TEST 2020-11-01  "  #   Test of 1 Nov 2020 - posts to r/linuxupskillBotTest"
            "\n "
        )
    if sys.argv[1] == "LIVE":    
        today_date = datetime.date.today()
        print("OK, so we're working with today's date: ", today_date)
        subreddit = "linuxupskillchallenge"
        print("And posting to the LIVE r/upskillchallenge...")
    
    if sys.argv[1] == "TEST":
        subreddit = "linuxupskillBotTest"
        print("Posting to the TEST subreddit:  r/upskillBotTest...")
        
        if len(sys.argv) > 2:
            today_date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
            print("And using date: ", today_date)
        
        else:
            today_date = datetime.date.today()

    day_num, month_name, next_month = check_today(today_date)
    
    #DEBUG!!
    print("We're on day: ", day_num, " of the course")
    
    if day_num == 1:
        #    On this day, we pin the standard "Day 1"
        #    post - and the short video
        clear_all_pinned()
        title, body = get_lesson(day_num)
        post_and_pin_day(subreddit, title, body)
        post_and_pin("Day 1 - a short video")
        post("HOW THIS WORKS")  #   post, but don't pin (only two posts can be pinned) 
        #   clear last few of last month's lessons...
        del_day(20); del_day(19); del_day(18); del_day(17)
    
    elif day_num == 18:
        #   retrive, post and pin today's lesson as normal
        clear_all_pinned()
        post_and_pin("HOW THIS WORKS")
        title, body = get_lesson(day_num)
        post_and_pin_day(subreddit, title, body)
        del_day(day_num - 4)
 
        #    now retrieve custom 'advert' message for other subreddits,
        #    and post to those subreddits, alerting them to the new
        #    course starting on first Monday of the coming month
        advert_to_subreddit("linux")
        advert_to_subreddit("linux4noobs")
        advert_to_subreddit("linuxadmin")
        advert_to_subreddit("linuxmasterrace")
        advert_to_subreddit("sysadmin")
        
    else:
        clear_all_pinned()
        post_and_pin("HOW THIS WORKS")
        post_and_pin_day(day_num)
        del_day(day_num - 4)

# ------------------------------------------supporting functions------------------------

def check_today(thisdate):
    
    delta = datetime.timedelta(days=1)
    delta7 = datetime.timedelta(days=7)
    
    #   If we're on day 4 of the week (i.e. Thursday), save as "days_into_week"
    days_into_week = thisdate.isoweekday()    #    ISO weekday, 1=Monday
    
    print("We're on day #: ", days_into_week, " of the week, where 1=Monday", flush=True)

    #   Weekend?, exit with all nulls
    if days_into_week == 6: return(None, None, None)
    if days_into_week == 7: return(None, None, None)

    #   Find the Monday of that week 
    thismonday = thisdate - (delta * (days_into_week-1))
    #   The month of that is "month_num" in all cases. 
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
 
    #   Each week is five days of lessons - and then the few days of 
    #   the week we're in...
    day_num = ((weeks_back) * 5) + days_into_week
    #   ...but we only have 20 lessons...
    if day_num > 20: return(None, None, None)
    return([day_num,month_name, "June"])

def get_lesson(daynum):
    #   get daynum out of github
    g = Github(GITHUB_ACCESS_TOKEN)
    repo = g.get_repo("snori74/linuxupskillchallenge")
    contents = repo.get_contents("12.md")
    file_name = daynum, ".md"    # e.g "12.md"
    print("Raw contents of ", file_name, ": ", contents.decoded_content)
    print(contents.decoded_content)
    #   extract subject from body
    print("Will post with Subcet of: ", subject)
    return([title, body])

def post_and_pin(subreddit, title, body):
    post = subreddit.submit(title, selftext=body,
    url=None, flair_id=None, flair_text=None,
    resubmit=True, send_replies=True, nsfw=False, spoiler=False,
    collection_id=None)

    #   and "sticky" (pin) that post
    post.mod.sticky()

def clear_all_pinned():
    #   find list of all pinned
    #   fetch, unpin
    pass

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

def clear_all_pinned(sr):
    print('\nPosts: ')
    for post in sr.new(limit=25):
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

