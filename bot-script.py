#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''
   bot-script.py - Run every day. Pulls the lessons for the Linux Upskill 
                    Challenge from Github into the subreddit 

    Note 1: Don't run more that once a day - you'll risk multiple posting 
    Note 1a: Looks like we now have to generate a "Thoughts and comments 0 Day x" post too!
    Note 2: Now with the added trick, (thanks u/Danny007dan), of inserting 
    a "backlink" to the previous lesson just above the copyright notice,
    like this:

    ## PREVIOUS DAY'S LESSON
    * [Day 3 - Power trip!](https://www.reddit.com/r/linuxupskillchallenge/comments/ip257g/day_3_power_trip/)
    
    Which is cool, but how to we programattically get that link? Huh? Danny?
    
    '''

import praw
import datetime
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
        today_date = datetime.date.today()
        subreddit = reddit.subreddit("linuxupskillchallenge")
        print("Posting to: r/upskillchallenge - with today's date: ", today_date)
    
    if sys.argv[1] == "TEST":
        TEST = True
        subreddit = reddit.subreddit("LinuxUpSkillBotTest")
        print("In TESTing mode...")

        if len(sys.argv) > 2:
            today_date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
            print("Using BOGUS date of: ", today_date)
        
        else:
            today_date = datetime.date.today()
            print("And working with today's date: ", today_date)
   
    #   Which day of the course are we on?
    day_num, month_name, next_month = check_today(today_date)
    
    if day_num == 1:
        #    Post and pin the standard "Day 1" lesson - and the ditto the "short video"
        #    Repost "HOW THIS WORKS" text. Don't pin, cos only two can be at a time
        # 
        clear_all_pinned(subreddit)
        get_post_pin_day(subreddit, day_num)
        get_post_pin_file(subreddit, "day1-short-video.md")
        get_post_file(subreddit, "how-this-works.md")
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
        #   then pull in the current "How this Works", and pin
        get_post_pin_file(subreddit, "how-this-works.md")
        #
        #    ...and post custom 'advert' messages to subreddits
        get_post_advert(subreddit, "linux")
        get_post_advert(subreddit, "linux4noobs")
        get_post_advert(subreddit, "linuxadmin")
        get_post_advert(subreddit, "linuxmasterrace")
        get_post_advert(subreddit, "sysadminiblogs")
        
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

