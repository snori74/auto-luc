#!/usr/bin/env python

#   bot-script.py - Intended to be run every day, doing
#                   posts to reddit from data kept in github
#                   for the Linix Upskill Challenge.

'''
Note, need to be very careful regrads what happens if the script is run
twice on the same day for some reason. Think 'self-healling' or perhaps
'idempotent'.
'''

import praw
import configparser
import os
import numpy as np
import sys
import json
from pull_settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from pull_settings import REDDIT_USERNAME, REDDIT_PASSWORD


def main():
    
    cient_id = pull_settings()
    print("DEBUG: ", client_id)
    day_num, month_name, next_month = check-today()
    if day_num == 1:
        # on this day, we pin the standards "Day 1" post,
        # but also the short video
        clear_all_pinned()
        post_and_pin_day(day_num)
        del_day(
        pin_post("Day 1 - a short video")
    elif day_num == 18:
        # on this day we post a message to the other subreddits, alerting 
        # them to an new course starting on the upcoming Monday
        clear_all_pinned()
        post_and_pin_day(day_num)
        post_and_pin_day(daynum-1)
        post_to_linux("txt-for-linux-subreddit.md", next_month)
        post_to_linux_admin("txt-for-linuxsysadmin-subreddit.md", next_month)
        post_to_linux4noobs("linux4noobs-subbreddit.md", next_month)
        # etc
    else:
        clear_all_pinned()
        post_and_pin_day(day_num)
        post_and_pin_day(day_num-1)

# ------------------------------------------supporting functions------------------------

def check-today():
    '''
    DUMMY - real version will check today's date and return the
    correct values for:
     - day_num
     - month_name
     - next_month
     as a list - or NONE
     '''
     return([10,"May", "June"]
     

def post_and_pin_day(daynum):
    get daynum out of github
    extract subject from body
    post to reddit
    make mod
    make favorite/pinned
    make accepted

def clear_all_pinned():
    find list of asll pined
    feach, unpin

def post_to_linux():
    get fro github 'post_for_lixux.txt'
    extract subject?
    post text as md to r/linux 

def pull_setting();
    #    Pull settings, including 'secrets', from local dot file
    #
    config = configparser.ConfigParser()
    config_dir = os.path.expanduser('~/.luc-autoposter/')
    full_path = config_dir + 'config'

    try:
        config.read(full_path)
        key_itself = json.loads(config.get("Global", "User_agent"))
        client_id = {'api_key': key_itself}
    except:
        sys.exit(
            "\n[Error]: 'client_id' not found.\n"
            "\n   Script expects Reddit app's GUID in: ~/.luc-autoposter/config "
            "\n"
        )

    try:
        config.read(full_path)
        key_itself = json.loads(config.get("Global", "client_id"))
        client_id = {'api_key': key_itself}
    except:
        sys.exit(
            "\n[Error]: 'client_id' not found.\n"
            "\n   Script expects the Reddit script code key in: ~/.luc-autoposter/config "
            "\n"
        )

    try:
        config.read(full_path)
        EMAIL_FROM = json.loads(config.get("Global", "client_secret"))
    except:
    return(client_id)

def info_on_subreddit(sr):
    print("Is this reddit ReadOnly?:", reddit.read_only)  # Output: False
    subreddit = sr
    print("Selected subreddit: r/", subreddit)
    print("Checking my ID: ", reddit.user.me())
    print("display_name: ", subreddit.display_name)
    print("title; ", subreddit.title)
    print("description: ", subreddit.description)

def take_sticky_off(sr):
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
 
