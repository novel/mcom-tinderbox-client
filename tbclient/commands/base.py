import getopt
import sys

class TBClientCommand(object):
    """Base class for commands"""
    name = None

    def __init__(self, *args, **kwargs):
        self.clargs = kwargs['clargs']
        self.tinderboxclient = kwargs['tinderboxclient']

    def help(self):
        raise NotImplemented

    def start(self):
        try:
            opts, args = getopt.getopt(self.clargs, "h")
        except getopt.GetoptError, err:
            print "Error: %s" % str(err)
            sys.exit(1)
    
        for o, a in opts:
            if o == "-h":
                print self.help()
                sys.exit(0)

    def __unicode__(self):
        return "<TBClientCommand name: %s>" % self.name
