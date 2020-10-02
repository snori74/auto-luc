A Python 'bot' to automate the posting of each daily lesson for https://LinuxUpskillChallenge.org - pulling them directly from GitHub, and using API calls to post to Reddit.

Core details:
 - Intended to be run daily from 'cron' or similar
 - Calculates which day of the course we're in
 - Grabs the corresponding lesson text from Github 
 - Posts this to the subreddit /r/linuxupskillchallenge
