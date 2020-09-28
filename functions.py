#   Supporting fuctions for bot-script.py
#

import datetime
import praw
from github import Github
from settings import *
import time

def check_today(thisdate):
    """
    The course is described as:

    "...runs from the first Monday of the month, and lasts for four weeks..."

    Simple? Yes, but there are some surprising corner cases, e.g.:
     - sometimes the course doesn't start until the 7th of the month (e.g.September 2020)
     - the last day or two of <MONTH>'s course end up being in <MONTH+1> (e.g September 2020)
     - there's sometimes a whole week's gap at the end of a course (e.g. June 2020)

    """
    delta = datetime.timedelta(days=1)
    delta7 = datetime.timedelta(days=7)

    days_into_week = thisdate.isoweekday()  #    ISO weekday, 1=Monday

    print(
        "We're on day #: ", days_into_week, " of the week, where 1=Monday", flush=True
    )

    #   No lesson on the weekend
    if (days_into_week == 6) or (days_into_week == 7):
        return (None, None, None)

    #   Find the Monday of that week...
    thismonday = thisdate - (delta * (days_into_week - 1))
    #   ...the month of that is "month_num" in all cases.
    month_num = thismonday.month  #    January=1, December=12
    month_name = thismonday.strftime("%B")

    #   Now, from that Monday, step back 7 days each time, counting,
    #   until Month.(this_monday) <> month_num.
    weeks_back = 0
    while thismonday.month == month_num:
        thismonday = thismonday - (delta7)
        weeks_back = weeks_back + 1
    #   We've gone one week too far back, so...
    weeks_back = weeks_back - 1

    #   Each week has five days of lessons - and then the few days of
    #   the week we're in...
    day_num = ((weeks_back) * 5) + days_into_week

    #   ...but we only have 20 lessons...
    if day_num > 20:
        return (None, None, None)

    return [day_num, month_name, "June"]


def get_day(daynum):
    """
    Works out the filename for the day's lesson, then
    calls 'get_file' to pull directly from Github
    """
    import requests

    filename = str(daynum).zfill(2) + ".md"  #   Padding '1' to '01'
    title, body = get_file(filename)
    return [title, body]


def get_file(filename):
    """
    Given a filename, pulls lesson directly from Github (no API), in RAW
    format, then splits the title text off and tidies it - and returns
    both it and the now-trimmed body as a list.
    """
    import requests

    starturl = "https://raw.githubusercontent.com/snori74/linuxupskillchallenge/master/"
    url = starturl + filename
    r = requests.get(url, allow_redirects=True)
    #   comes back as type 'bytes', which we convert to string
    contents = r.content
    strcontent = contents.decode("utf-8")
    #   title line is everything before the newline...
    title = strcontent.partition("\n")[0]
    #   ...and the body is everything after.
    body = strcontent.partition("\n")[2]
    #   and then we trim the leading "# " off the title...
    title = title.partition("# ")[2]
    return [title, body]


def get_advert_file(filename):
    """
    Given an advert filename, pulls text directly from Github (no API), in RAW
    format, then splits the title text off and tidies it - and returns
    both it and the now-trimmed body as a list.
    """
    import requests

    starturl = "https://raw.githubusercontent.com/snori74/linuxupskillchallenge/master/"
    url = starturl + filename
    r = requests.get(url, allow_redirects=True)
    #   comes back as type 'bytes', which we convert to string
    contents = r.content
    strcontent = contents.decode("utf-8")
    #   title line is everything before the newline...
    title = strcontent.partition("\n")[0]
    #   ...and the body is everything after.
    body = strcontent.partition("\n")[2]
    #   and then we trim the leading "TITLE: " off the title...
    title = title.partition("TITLE: ")[2]
    return [title, body]

def insert_backlink(sr, body, day_num):
    #   go direct to the numbered lesson files
    if day_num == 1:
        print("No backlink in lesson 1")
    else:
        filename = str(day_num - 1).zfill(2) + ".md"  #   Padding '1' to '01'
        bl_title, bl_body = get_file(filename)
        bl_url = "<missing>"
        print("Previous post: ", bl_title)
        for post in sr.new(limit=25):
            print("Checking", post.title )
            if post.title.startswith(bl_title):
                print("Yup! foundit")
                bl_url = post.url
                break

        split_text = "Copyright 2012-2020 @snori74"
        top_of_body = body.partition(split_text)[0]
        bottom_of_body = body.partition(split_text)[2]
        backlink_text = (
            "\n\n## PREVIOUS DAY'S LESSON\n * [" + bl_title + "](" + bl_url + ")\n\n"
        )
        body = top_of_body + backlink_text + split_text + bottom_of_body

    return body

def get_post_pin_day(sr, day_num):
    title, body = get_day(day_num)
    body = insert_backlink(sr, body, day_num)
    print("Posting: ", title)
    post = sr.submit(
        title,
        selftext=body,
        url=None,
        flair_id=None,
        flair_text=None,
        resubmit=True,
        send_replies=True,
        nsfw=False,
        spoiler=False,
        collection_id=None,
    )

    #   and approve that post
    time.sleep(5)
    print("Approving...")
    try:
        post.mod.approve()
    except:
        print("Hmm, can't approve it for some reason...")
    
    #   and sticky/pin that post
    time.sleep(5)
    print("Stickying...")
    try:
        post.mod.sticky(state=True)
    except:
        print("Hmm, can't sticky it for some reason...")

    #
    #    and pop in a matching "Thoughts and comments" post...
    title, body = get_file("thoughts-and-comments.md")
    #   replace X with the day number
    title = title.partition("X")[0] + str(day_num) + title.partition("X")[2]
    post = sr.submit(
        title,
        selftext=body,
        url=None,
        flair_id=None,
        flair_text=None,
        resubmit=True,
        send_replies=True,
        nsfw=False,
        spoiler=False,
        collection_id=None,
    )


def get_post_pin_file(subreddit, filename):
    title, body = get_file(filename)
    print("Posting: ", title)
    post = subreddit.submit(
        title,
        selftext=body,
        url=None,
        flair_id=None,
        flair_text=None,
        resubmit=True,
        send_replies=True,
        nsfw=False,
        spoiler=False,
        collection_id=None,
    )

    #   and approve that post
    print("Approving...")
    try:
        post.mod.approve()
    except:
        print("Hmm, can't approve it for some reason...")

    #   and sticky that it
    print("Stickying...")
    try:
        post.mod.sticky(state=True)
    except:
        print("Hmm, can't sticky it for some reason...")

 

def get_post_file(subreddit, filename):
    title, body = get_file(filename)
    post = subreddit.submit(
        title,
        selftext=body,
        url=None,
        flair_id=None,
        flair_text=None,
        resubmit=True,
        send_replies=True,
        nsfw=False,
        spoiler=False,
        collection_id=None,
    )
    #   but don't sticky/pin this post


def get_post_advert(subreddit, subreddit_name):
    """
    We retrive a file for each of the subreddits that we want to
    advertise in, and post into each of those subreddits - unless
    we're in TEST mode (i.e. if our "subreddit" is set to the test
    location "LinuxUpSkillBotTest") - in which case we post the adverts
    there too.

    The 'advert' text files are named in a very specific way:

           txt-for-linux-subreddit.md
           txt-for-sysadminblogs-reddit.md

    """
    advert_file = "txt-for-" + subreddit_name + "-subreddit.md"
    print("Advert: ", advert_file)
    title, body = get_advert_file(advert_file)
    if title == "":
        print("Bugger! for some reason no 'title'")
        return

    print("Title and body: ", title, body)

    if subreddit == "linuxupskillBotTest":
        print("Posting advert to TEST subreddit")
        post = subreddit.submit(
            title,
            selftext=body,
            url=None,
            flair_id=None,
            flair_text=None,
            resubmit=True,
            send_replies=True,
            nsfw=False,
            spoiler=False,
            collection_id=None,
        )

    else:
        if subreddit == "linuxupskillChallenge":
            sr = reddit.subreddit(subreddit_name)
            print("Posting advert to ", sr, "LIVE subreddit")
            post = sr.submit(
                title,
                selftext=body,
                url=None,
                flair_id=None,
                flair_text=None,
                resubmit=True,
                send_replies=True,
                nsfw=False,
                spoiler=False,
                collection_id=None,
            )


def clear_all_pinned(subreddit):
    for post in subreddit.new(limit=25):
        if post.stickied:
            print("Unsticking...")
            try:
                post.mod.sticky(state=False)
                post.mod.distinguish(how="no")
            except:
                print("Hmm, can't sticky it for some reason...")


def delete_day(subreddit, day_num):
    title = "Day " + str(day_num) + " - "
    delete_title(subreddit, title)


def delete_title(subreddit, title):
    for post in subreddit.new(limit=25):
        if post.title.startswith(title):
            print("Deleting: ", post.title)
            post.delete()


def pin_title(subreddit, title):
    for post in subreddit.new(limit=25):
        if post.title.startswith(title):
            try:
                print("Distinguishing...")
                post.mod.distinguish(how="yes")
            except:
                print("Can't distiguish for some reason...")
            try:
                print("Approvng...")
                post.mod.approve()
            except:
                print("Can't approve for some reason...")
            try:
                print("Stickying...")
                post.mod.sticky(state=True)
            except:
                print("Not able to sticky for some reason")
                
