# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from enum import Enum
import falcon
import io, os
from app_info import API_VERSION
from logic import Logic
import mimetypes

logic_instance = None

class GenerateLink:

    def on_post(self, req, resp):
        if not ServerStatus.check_status(resp):
            return
        
        request_body = req.get_media()

        if request_body is None or not "uri" in request_body:
            resp.status = falcon.HTTP_400
            resp.media = {"msg": "Invalid request."}
            return
        
        try:
            entry = logic_instance.gen_new_id(request_body["uri"].strip())
        except ValueError as e:
            print(f"WARNING: {e}")
            resp.status = falcon.HTTP_400
            resp.media = {"msg": "Invalid URI."}
            return

        if entry == None:
            resp.status = falcon.HTTP_500
            resp.media = {"msg": "Please try again later."}
            return

        payload = {
            "id": f"{entry.id}",
            "html_safe_uri": f"{entry.html_safe_uri}",
            "raw_uri": f"{entry.uri}",
            'encoded_uri': entry.encoded_uri,
        }

        resp.media = payload
    
    def process_response(self, req, resp, resource, req_succeeded):
        resp.content_type = mimetypes.types_map[".json"]

class RetrieveLink:
    def on_get(self, req, resp):
        if not ServerStatus.check_status(resp):
            return
        id_requested = req.get_param("id")

        # id not provided in query string
        if id_requested is None or id_requested == "":
            resp.status = falcon.HTTP_400
            resp.media = {"msg": "Undefined id."}
            return
        
        result = logic_instance.get_uri(id_requested.strip())
        # id does not exist in DB
        if result is None:
            resp.status = falcon.HTTP_404
            resp.media = {"msg": "ID not found."}
            return

        payload = {
            'html_safe_uri': result.html_safe_uri,
            'raw_uri': result.uri,
            'encoded_uri': result.encoded_uri,
        }
        resp.media = payload

    def process_response(self, req, resp, resource, req_succeeded):
        resp.content_type = mimetypes.types_map[".json"]

class ServerStatus:

    class ServerStatus(Enum):
        OK = "Ok"
        MAINTENANCE = "Maintenance"
        DOWN = "Down"
    
    status = ServerStatus.DOWN
    
    def on_get(self, req, resp):
        resp.media = {"status": ServerStatus.status.value}
    
    @staticmethod
    def check_status(resp):
        if logic_instance.is_db_up():
            ServerStatus.status = ServerStatus.ServerStatus.OK
        else:
            ServerStatus.status = ServerStatus.ServerStatus.DOWN

        if ServerStatus.status == ServerStatus.ServerStatus.OK:
            return True
        elif ServerStatus.status == ServerStatus.ServerStatus.MAINTENANCE:
            resp.status = falcon.HTTP_503
            resp.media = { "msg": "Server under maintenance, please try again later."}
            return False
        else:
            resp.status = falcon.HTTP_500
            resp.media = { "msg": "Server down, check API server log for more information."}
            return False

    def process_response(self, req, resp, resource, req_succeeded):
        resp.content_type = mimetypes.types_map[".json"]

class Doc:

    def __init__(self, storage_path):
        self._storage_path = os.path.abspath(storage_path)
        self._fopen = io.open

    def open(self, name="index.html"):
        filename = f"{self._storage_path}/{name}"

        stream = self._fopen(filename, "rb")
        content_length = os.path.getsize(filename)
        return stream, content_length

    def on_get(self, req, resp, name="index.html"):
        path = name
        resp.content_type = mimetypes.guess_type(path)[0]
        resp.stream, resp.content_length = self.open(path)

app = falcon.App(cors_enable=True)
logic_instance = Logic()
if logic_instance.maintenance_mode:
    ServerStatus.status = ServerStatus.ServerStatus.MAINTENANCE
elif logic_instance.init_ok:
    ServerStatus.status = ServerStatus.ServerStatus.OK
else:
    ServerStatus.status = ServerStatus.ServerStatus.DOWN

doc = Doc("../doc/build/")

app.add_static_route("/", doc._storage_path)
app.add_route("/", doc)

app.add_route(f'/api/{API_VERSION}/shorten', GenerateLink())
app.add_route(f'/api/{API_VERSION}/retrieve', RetrieveLink())
app.add_route(f'/api/{API_VERSION}/status', ServerStatus())
