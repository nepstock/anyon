import json
from typing import Optional

import falcon

from src.settings import AM_CLIENT_ID, AM_CLIENT_SCOPE, AM_DOMAIN

from .constants import AUTHORIZATION
from .helpers import remove_token_type, transform_token_data
from .serializer import SignInSchema


class Collection:
    __slots__ = (
        "_api",
        "_client_id",
        "_domain",
        "_scope",
        "_secrets_store",
    )

    def __init__(self, api, secrets_store):
        self._api = api
        self._client_id = AM_CLIENT_ID
        self._domain = AM_DOMAIN
        self._scope = AM_CLIENT_SCOPE
        self._secrets_store = secrets_store

    def on_post(self, req, resp):
        data = SignInSchema().load(req.media)
        secret = self._secrets_store.get_secret(data["client_id"])
        token_data = self._api.oauth.token(
            self._domain,
            data["client_id"],
            secret,
            self._scope,
            username=data["username"],
            password=data["password"],
        )
        token_data = transform_token_data(token_data)
        resp.body = json.dumps(token_data, ensure_ascii=False, sort_keys=True)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp):
        if AUTHORIZATION not in req.headers:
            raise falcon.HTTPBadRequest()
        token = remove_token_type(req.headers[AUTHORIZATION])
        secret = self._secrets_store.get_secret(self._client_id)
        self._api.oauth.revoke(self._domain, self._client_id, secret, token)
        resp.status = falcon.HTTP_204
