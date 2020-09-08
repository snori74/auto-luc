#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''
   bot-script.py - Intended to be run every day. Posts the lessons
                   for the Linux Upskill Challenge into the subreddit 
                   /r/linuxupskillchallenge - based on the text in 
                   github snori74/linuxupskillchallenge.

    Note, don't run more that once a day, or you'll risk multple posting 
    

'''
import configparser
import os
import numpy as np
import sys
import json
import praw
import datetime
from github import Github
from functions import *
from settings import *


subreddit = None
    
def main():
    
    reddit = praw.Reddit(
            user_agent=REDDIT_USER_AGENT,
            client_id=REDDIT_CLIENT_ID, 
            client_secret=REDDIT_CLIENT_SECRET,
            username=REDDIT_USERNAME, 
            password=REDDIT_PASSWORD
            )

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
        subreddit = reddit.subreddit("linuxupskillchallenge")
        print("Posting to the LIVE r/upskillchallenge...")
        today_date = datetime.date.today()
        print("And working with today's date: ", today_date)
    
    if sys.argv[1] == "TEST":
        subreddit = reddit.subreddit("linuxupskillBotTest")
        advert_subreddit = reddit.subreddit("linuxupskillBotTest")
        print("In TESTing mode...")

        if len(sys.argv) > 2:
            today_date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
            print("And using date: ", today_date)
        
        else:
            today_date = datetime.date.today()
            print("And working with today's date: ", today_date)
   
    #   Which day of the course are we on?
    day_num, month_name, next_month = check_today(today_date)
    
    if day_num == 1:
        #    On this day, we post and pin the standard "Day 1"
        #    lesson - and the "short video" - and also repost
        #    the "HOW THIS WORKS" text - but don't pin this, 
        #    because only two posts can be pinned at a time.
        # 
        clear_all_pinned(subreddit)
        get_post_pin_day(subreddit, day_num)
        get_post_pin_file(subreddit, "day1-short-video.md")
        get_post_file(subreddit, "how-this-works.md")    #   New post, but not pinned  
        #
        #   clear last few of last month's lessons...
        delete_day(subreddit, 20)
        delete_day(subreddit, 19)
        delete_day(subreddit, 18)
        delete_day(subreddit, 17)
        delete_day(subreddit, 16)
   
    elif day_num == 18:
        #
        #   retrive, post and pin today's lesson as normal
        clear_all_pinned(subreddit)
        get_post_pin_day(subreddit, day_num)
        delete_day(subreddit, day_num - 4)
        #
        #   refresh the "How this Works" post
        get_post_pin_file(subreddit, "how-this-works.md")
        #
        #    ...and post custom 'advert' messages to subreddits
        get_post_advert(advert_subreddit, "linux")
        get_post_advert(advert_subreddit, "linux4noobs")
        get_post_advert(advert_subreddit, "linuxadmin")
        get_post_advert(advert_subreddit, "linuxmasterrace")
        get_post_advert(advert_subreddit, "sysadminiblogs")
        
    elif day_num == None:
        print("No lesson today...")
        pass

    else:
        #   a 'normal' weekday...
        clear_all_pinned(subreddit)
        pin_title(subreddit, "HOW THIS WORKS")
        get_post_pin_day(subreddit, day_num)
        delete_day(subreddit, day_num - 4)

if __name__ == "__main__":
    main()

