class TBClientCommand(object):
    """Base class for commands"""
    name = None

    def __init__(self, *args, **kwargs):
        self.clargs = kwargs['clargs']
        self.tinderboxclient = kwargs['tinderboxclient']

    def help(self):
        raise NotImplemented

    def start(self):
        raise NotImplemented

    def __unicode__(self):
        return "<TBClientCommand name: %s>" % self.name
