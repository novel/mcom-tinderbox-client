import getopt
import sys

from tbclient.core import ObjectNotFound
from base import TBClientCommand

class TBQueueCommand(TBClientCommand):
    name = "queue"

    def __init__(self, *args, **kwargs):
        super(TBQueueCommand, self).__init__(*args, **kwargs)

    def help(self):
        return """queue command supports varios operations on tinderd queue

Queue Listing:

    Just use 'queue' command without arguments to list queue entries

Obtaining Detailed Info on Queue Entry:

    queue <entry_id>

    <entry_id>   id of an queue entry

Adding Entry to the Queue:

    queue add -b <build_id> [-e] [-p <priority>] category/port

    -b $build_id    id of the build we're working with
    -e              specifiy to email on completion (optional, default: false)
    -p <priority>   entry priority, supported values: from 1 to 10 (optional, default: 10)
    category/port   port we want to build, for example: security/gnutls
"""

    def start(self):
        super(TBQueueCommand, self).start()

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
            print ("%(id)3s %(username)s %(portdirectory)20s %(buildname)s %(priority)s "
               "%(status)s %(enqueued)s %(completed)s" ) % \
                    entry.__dict__

    def _get_queue_entry(self, entry_id):
        try:
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
        except ObjectNotFound:
            print "Error: there is no queue entry with id = %s" % entry_id

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
