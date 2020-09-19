
# TO INSTALL TO UBUNTU

Can be installed to a number of places, but let's assume that you
want to install to directory 'bot' in your own home directory. 


First, you need to install the ability to create Python 'virtual environments'
like this:

sudo apt install virtualenv

    From now on, everything is done by you, with no need for 'sudo'.

Here's how to setup the directory for the bot:

    cd 
    virtualenv -p python3 bot
    cd bot 
    source bin/activate
    pip install praw 

Here's how to setup the config file:

    mkdir ~./auto-luc
    vim .auto-luc/config

Note - you will need to edit the value of time_bump in 
bot_script.py based on your timezome

To run the bot:

    cd ~/bot 
    source bin/activate
    python3 bot_script <params>


