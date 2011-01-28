import getopt
import sys

from base import TBClientCommand

class TBQueueCommand(TBClientCommand):
    name = "queue"

    def __init__(self, *args, **kwargs):
        super(TBQueueCommand, self).__init__(*args, **kwargs)

    def help(self):
        return "blah"

    def start(self):
        if len(self.clargs) == 0:
            return self._list_queue()
        else:
            if self.clargs[0] == "add":
                return self._add_queue_entry(self.clargs[1:]) 
            else:
                return self._get_queue_entry(self.clargs[0])
        

    def _list_queue(self):
        queue_entries = self.tinderboxclient.queue_entries()

        for entry in queue_entries:
            print ("%(id)3s %(portdirectory)20s %(buildname)s %(priority)s "
               "%(status)s %(enqueued)s %(completed)s" ) % \
                    entry.__dict__

    def _get_queue_entry(self, entry_id):
        entry = self.tinderboxclient.queue_entry(entry_id)

        print """id: %(id)s
username: %(username)s (id: %(user_id)s)
status: %(status)s
port directory: %(portdirectory)s
priority: %(priority)s
build: %(buildname)s (id: %(build_id)s)
enqueued at: %(enqueued)s
completed at: %(completed)s
""" % entry.__dict__

    def _add_queue_entry(self, args):
        try:
            opts, nargs = getopt.getopt(args, "b:ep:")
        except getopt.GetoptError, err:
            print str(err)
            sys.exit(2)

        build_id = None
        priority = 10
        email = False

        for o, a in opts:
            if o == "-b":
                build_id = a
            if o == "-e":
                email = True
            elif o == "-p":
                priority = a

        if build_id is None or len(nargs) == 0:
             print "error: build_id or port dir not specified"
             sys.exit(2)

        print self.tinderboxclient.add_queue_entry(build_id=build_id,
                priority=priority,
                portdir=nargs[0],
                email=email)
