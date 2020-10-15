
# TO INSTALL TO UBUNTU

Can be installed to a number of places, but let's assume that you
want to install to directory 'bot' in your own home directory. 

First, you need to install the ability to create Python 'virtual environments'
like this:

    sudo apt install virtualenv

_From now on, everything is done by you, with no need for 'sudo'_.

Here's how to setup the directory for the bot:

    cd 
    virtualenv -p python3 bot
    cd bot 
    source bin/activate
    pip install praw 

Here's how to setup the config file:

    mkdir ~/.auto-luc
    vim ~/.auto-luc/config

Note 1: You will need to edit the value of time_bump in 
bot_script.py based on the timezone of your server

Note 2: The format for _.auto-luc/config_ is given in _settings.py_.

To run the bot "manually", simply:

    cd ~/bot 
    source bin/activate
    python3 bot_script.py <params> >> /var/log/bot.log 2>> /var/log/bot-error.log

You may want to wrap this up as a shell script, and add some logging, e.g:

    #!/bin/bash
    cd ~/bot 
    source bin/activate
    python3 bot_script.py TEST >> /var/log/bot.log 2>> /var/log/bot-error.log


There are a couple of ways to call this daily at the correct time. If using 'crontab', 
a suitable entry would look like:

    SHELL=/bin/sh
    PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

    # m h dom mon dow command
    1 20	* * *	 /root/run-bot

To automate, first create a shell script like this 'run-bot':

    #!/bin/bash
    cd ~/bot 
    source bin/activate
    python3 bot_script.py 
    
Then create a cron entry (as an ordinary user, or as root) by _crontab -e_ with and entry like this:

    SHELL=/bin/sh
    PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

    # m h dom mon dow 	command
    1 20	* * *	 /root/run-bot

...which will run the script each day at 20:01 (8:01pm) - which is appropriate for a server running on UTC.

