import json
import os

import falcon

from src.helpers.common import get_new_uuid

from .serializer import SignUpSchema


class Collection(object):
    def __init__(self, api, credentials_store, domain: str, scope: str):
        self._api = api
        self._domain = domain
        self._credentials = credentials_store
        self._scope = scope

    def on_get(self, req, resp):
        # TODO
        resp.body = {}
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = SignUpSchema().load(req.media)
        user = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": get_new_uuid(),
            "userName": data["email"],
            "name": {"familyName": "", "givenName": ""},
            "password": data["password"],
            "active": True,
            "emails": [{"value": data["email"], "primary": True}],
        }
        access_token = self._credentials.get_token(self._domain, self._scope)
        user_data = self._api.create_user(self._domain, access_token, user)
        resp.body = json.dumps(user_data, ensure_ascii=False, sort_keys=True)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_201


class Item(object):
    def __init__(self, api, credentials_store, domain: str, scope: str):
        self._api = api
        self._domain = domain
        self._credentials = credentials_store
        self._scope = scope

    def on_get(self, req, resp, user_id: str):
        access_token = self._credentials.get_token(self._domain, self._scope)
        user_data = self._api.get_user(self._domain, access_token, user_id)
        resp.body = json.dumps(user_data, ensure_ascii=False, sort_keys=True)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200
