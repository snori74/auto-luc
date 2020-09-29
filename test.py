#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os
import sys
import datetime

#   Tests by running through the whole of year
#   of 2020 - with all output redirected to:
#       test.out
#       test.err
#
#   ...to allow checking. 
#
#   Note: You can watch and continuously refresh 
#   r/LinuxUpSkillBotTest/ to follow along.
#
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2021, 1, 1)

def daterange(start_date, end_date):
    print("Test for: ", start_date, " to ", end_date)
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

for single_date in daterange(start_date, end_date):
    day = single_date.strftime("%Y-%m-%d")    
    
    #   Test, with all output redirected to file
    os.system("rm test.out")
    os.system("rm test.err")
    os.system("touch test.out")
    os.system("touch test.err")
    #   Redirect just errors
    cmd = "./bot_script.py TEST " + day + " 2>>test.err"
    #   Redirect BOTH errors and stdout
    # cmd = "./bot_script.py TEST " + day + ">> test.out 2>>test.err"
    print("Command: ", cmd)
    os.system(cmd)
