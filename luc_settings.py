import configparser
import os
import json
import sys

config = configparser.ConfigParser()
config_dir = os.path.expanduser('~/.auto-luc/')
full_path = config_dir + 'config'

#    Pull settings, including 'secrets', from local dot file
#
def get_setting(setting):
    try:
        config.read(full_path)
        setting_value = json.loads(config.get("Global", setting))
        print(setting, "=", setting_value)

    except:
        sys.exit(
            "\n[Error]: ", setting, " not found.\n"
            "\n   The script expects settings to be stored"
            "\n   in the file: ~/.auto-luc/config "
            "\n"
        )

get_setting("GITHUB_ACCESS_TOKEN")
get_setting("REDDIT_CLIENT_SECRET")
get_setting("REDDITT_USER_AGENT")
get_setting("REDDIT_USERNAME")
get_setting("REDDIT_PASSWORD")




