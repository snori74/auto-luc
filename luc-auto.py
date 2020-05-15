
import praw
import random
import string
import time 
from github import Github
from luc_settings import GITHUB_ACCESS_TOKEN

# -----------------------------setup globalss------------------------------------------------------

g = Github(GITHUB_ACCESS_TOKEN)
reddit = praw.Reddit('test')
repo = g.get_repo("snori74/linuxupskillchallenge")
subreddit = reddit.subreddit('linuxupskillchallange')

#------------------------------main----------------------------------------------------------------

def main():
"""
    * Check to see what weekday of the month it is
      (have provision for date on command line for testing)
    * Lookup table to see what to do on this day, 
      if 'nothing' , log and skip, else:
    * Process the list to be deleteed:
      - delete by title
    Process the list to be added:
      - first 'unpin' every existsing post
      - Grab the appropriate text from GitHub
      - Process the first line to get 'title'
      - post and pin
"""

    *















    # Open the subreddit and onfirm dedails
     # 
    info_on_subreddit(subreddit)

    # Take sticky off all posts
    #
    take_sticky_off(subreddit)

    # Create a new post, and sticky it
    #
    post_sticky(subreddit, post_title, post_text)

    # Now delete an old post...
    delete_submission(subreddit, "Testing-ibguZHVbgC")


# -----------------------------helper functions-----------------------------------------------------

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


if __name__ == "__main__":
    main()
