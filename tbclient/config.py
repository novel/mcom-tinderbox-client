import stat
import os.path
import ConfigParser

DEFAULT_CONFIG = "~/.tbc"

class MyConfig(ConfigParser.ConfigParser):
    profile = None

    def __init__(self, profile):
        self.profile = profile
        ConfigParser.ConfigParser.__init__(self)

    def get(self, option):
        return ConfigParser.ConfigParser.get(self, self.profile, option)


def get_config(profile="default"):
    config_path = os.path.expanduser(DEFAULT_CONFIG)

    if os.stat(config_path)[stat.ST_MODE] & \
            (stat.S_IRWXG | stat.S_IRWXO) != 0:
        raise RuntimeError("%s: permissions are too loose, set to 600" % \
                DEFAULT_CONFIG)

    conf = MyConfig(profile)
    conf.read(os.path.expanduser(config_path))
    
    return conf
