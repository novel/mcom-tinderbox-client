from base import TBClientCommand

class TBBuildCommand(TBClientCommand):
    name = "build"

    def __init__(self, *args, **kwargs):
        super(TBBuildCommand, self).__init__(*args, **kwargs)

    def help(self):
        return "blah"

    def start(self):
        if len(self.clargs) == 0:
            # list all builds if not args given
            return self._list_builds()
        else:
            return self._get_build(self.clargs[0])
        

    def _list_builds(self):
        builds = self.tinderboxclient.builds()

        for build in builds:
            print ("%(id)3s %(name)16s %(status)s " 
            "%(currentport)s %(updated)s") % build.__dict__

    def _get_build(self, build_id):
        build = self.tinderboxclient.build(build_id)

        print """name: %(name)s
description: %(description)s
status: %(status)s
updated: %(updated)s
currentport: %(currentport)s
remake count: %(remakecount)s
jail id: %(jail_id)s
portstree_id: %(portstree_id)s
""" % build.__dict__
