A Python 'bot' to automate the posting of each daily lesson 
for https://LinuxUpskillChallenge.org by making API
calls to Github and Reddit.


Core details:
 - Intended to be run daily from 'cron' or similar
 - Calculates which day of the course we're in
 - Grabs the corresponding lesson text from a Github repo
 - Posts this to the subreddit /r/linuxupskillchallenge
