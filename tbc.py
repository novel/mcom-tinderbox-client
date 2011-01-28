#!/usr/bin/env python

import getopt
import sys

import ConfigParser

from tbclient.commands import commands
from tbclient.core import TinderboxClient
from tbclient.config import get_config

def usage(progname):
    print "usage: %s command" % progname
    print "valid commands are:\n\n%s\n" % \
            '\n'.join(supported_commands().keys())

def info_help(progname):
    print """%(progname)s [-a <service_address>] [-u <user>] [-p <passwd>] command
%(progname)s -h

    -h  displays this message
    -a  specifies service address (default: read from config file)
    -u  specifies username (default: read from config file)
    -p  specifies password (default: read from config file)

Valid commands are:

    %(commands)s

To get help on individual command, type:

    %(progname)s command -h
""" % {"progname": progname, "commands": ' '.join(supported_commands().keys())}

def supported_commands():
    commands_dict = {}
    
    for command in commands:
        commands_dict[command.name] = command

    return commands_dict

if __name__ == "__main__":
    tinderbox_client_kwargs = {}

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:hu:p:")
    except getopt.GetoptError, err:
        print str(err)
        usage(sys.argv[0])
        sys.exit(2)

    for o, a in opts:
        if o == "-a":
            tinderbox_client_kwargs["url"] = a
        elif o == "-h":
            info_help(sys.argv[0])
            sys.exit(0)
        elif o == "-u":
            tinderbox_client_kwargs["username"] = a
        elif o == "-p":
            tinderbox_client_kwargs["passwd"] = a

    if len(tinderbox_client_kwargs) == 0:
        # no command line options given, read config
        config = get_config()

        try:
            tinderbox_client_kwargs["url"] = config.get("apihost")
            tinderbox_client_kwargs["username"] = config.get("username")
            tinderbox_client_kwargs["passwd"] = config.get("passwd")
        except ConfigParser.NoOptionError, err:
            print "error: %s" % str(err)
            sys.exit(1)
    elif not ("url" and "username" and "passwd") in tinderbox_client_kwargs:
        usage(sys.argv[0])
        sys.exit(0)

    tinderboxclient = TinderboxClient(**tinderbox_client_kwargs)
   
    try:
        command_name = sys.argv[1]
        command = supported_commands()[command_name] \
                (clargs=sys.argv[2:],
                 tinderboxclient=tinderboxclient)
    except (IndexError, KeyError):
        usage(sys.argv[0])
        sys.exit(2)

    command.start()
