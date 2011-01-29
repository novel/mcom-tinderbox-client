import hashlib
import httplib
import time

try:
    import json
except ImportError:
    import simplejson as json

API_VERSION = "1.0"

class ServiceException(Exception): pass
class ObjectNotFound(ServiceException): pass
class MalformedResponse(ServiceException): pass

class Build(object):

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.status = kwargs["status"]
        self.description = kwargs["description"]
        self.updated = kwargs["updated"]
        self.currentport = kwargs["currentport"]
        self.remakecount = kwargs["remakecount"]
        self.jail_id = kwargs["jail"]["id"]
        self.portstree_id = kwargs["portstree"]["id"]

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_["build"])

class BuildPort(object):

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.directory = kwargs["directory"]


    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_["buildport"])

class QueueEntry(object):

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.username = kwargs["username"]
        self.status = kwargs["status"]
        self.portdirectory = kwargs["portdirectory"]
        self.priority = kwargs["priority"]
        self.buildname = kwargs["buildname"]
        self.user_id = kwargs["user"]["id"]
        self.build_id = kwargs["build"]["id"]
        self.enqueued = kwargs["enqueued"]
        self.completed = kwargs["completed"]

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_["entry"])

    @classmethod
    def construct_request_obj(cls, dict_):
        """Creates an encoded object for passing
        as request body."""

        entry_object = {"entry": dict_}

        return entry_object

class TinderboxClient(object):

    def __init__(self, url, username, passwd):
        self.url = url
        self.username = username
        self.password = passwd

        self.debug = False

    def _auth_token(self):
        token = hashlib.md5()

        md5_passwd = hashlib.md5(self.password).hexdigest()

        token.update(self.username)
        token.update(md5_passwd)

        return token.hexdigest()

    def _request(self, method, url, body=None, headers=None):
        all_headers = {"X-Tinderbox-User": self.username,
                "X-Tinderbox-Token": self._auth_token(),
                "X-Tinderbox-API-Version": API_VERSION}
        if headers is not None:
            all_headers.update(headers)

        conn = httplib.HTTPConnection(self.url)
        conn.request(method, "/api/" + url, body, all_headers)

        response = conn.getresponse()

        data = response.read()

        if self.debug:
            print "---- request ----"
            print url
            print "- %s %s -" % (response.status, response.reason)
            print "- response body -"
            print data
            print "----------------"
            print ""

        conn.close()

        if response.status == 404:
            raise ObjectNotFound("object not found at url: %s" % url)

        parsed_data = json.loads(data)

        if parsed_data['summary']['status'] != "ok":
            raise ServiceException(parsed_data['summary']['reason'])

        return parsed_data

    def builds(self, build_id=None):
        request_url = "build"
        if build_id is not None:
            request_url += "/%s" % build_id

        response = self._request("GET", request_url)

        builds = [] 

        for build in response["builds"]:
            builds.append(Build.from_dict(build))

        return builds

    def build(self, build_id):
        return self.builds(build_id=build_id)[0]

    def buildports(self, build_id=None):
        request_url = "buildport"
        
        response = self._request("GET", request_url)

        buildports = []
        for item in response["buildports"]:
            buildport = {}
            buildport["target_port"] = item["buildport"]["target_port"]
            buildport["build"] = Build.from_dict(item["buildport"]["build"])
            buildport["buildport"] = BuildPort.from_dict(item["buildport"]["buildport"])
            buildports.append(buildport)
        
        return buildports

    def queue_entries(self, entry_id=None):
        request_url = "queue"
        if entry_id is not None:
            request_url += "/%s" % entry_id

        response = self._request("GET", request_url)

        queue_entries = []
        for entry in response["entries"]:
            queue_entries.append(QueueEntry.from_dict(entry))

        return queue_entries

    def queue_entry(self, entry_id):
        return self.queue_entries(entry_id=entry_id)[0]

    def add_queue_entry(self, build_id, priority, portdir, email):
        request_url = "queue"
        queue_entry = QueueEntry.construct_request_obj({"build": {"id": build_id}, "portdirectory": portdir,
            "priority": priority,
            "email_on_completion": email})

        response = self._request("PUT", request_url,
                body=json.dumps(queue_entry))

        return True
