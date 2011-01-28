from base import TBClientCommand

class TBBuildPortCommand(TBClientCommand):
    name = "buildport"

    def __init__(self, *args, **kwargs):
        super(TBBuildPortCommand, self).__init__(*args, **kwargs)

    def help(self):
        return """TBD"""

    def start(self):
        super(TBBuildPortCommand, self).start()

        return self._list_current_buildports()

    def _list_current_buildports(self):
        buildport_format = "%(id)3s %(build_id)10s %(target_port)20s %(port_directory)20s"
        buildports = self.tinderboxclient.buildports()

        print buildport_format % {"id": "id",
                "build_id": "build_id", "target_port": "target port",
                "port_directory": "current port"}

        for buildport in buildports:
            print buildport_format % {"id": buildport["buildport"].id,
                            "build_id": buildport["build"].id,
                            "target_port": buildport["target_port"],
                            "port_directory": buildport["buildport"].directory
                            }
