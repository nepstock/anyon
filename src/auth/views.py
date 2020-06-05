import json
import os

import falcon

from .serializer import SignInSchema


class Collection(object):
    def __init__(self, api, secrets_store, domain: str, scope: str):
        self._api = api
        self._domain = domain
        self._secrets_store = secrets_store
        self._scope = scope

    def on_post(self, req, resp):
        data = SignInSchema().load(req.media)
        secret = self._secrets_store.get_secret(data["client_id"])
        token_data = self._api.token(
            self._domain,
            data["client_id"],
            secret,
            self._scope,
            username=data["username"],
            password=data["password"],
        )
        del token_data["expires_date"]
        token_data["scope"] = token_data["scope"].replace("scim", "")
        resp.body = json.dumps(token_data, ensure_ascii=False, sort_keys=True)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200
