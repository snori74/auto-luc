#   
#   Supporting fuctions for bot-script.py
#

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

