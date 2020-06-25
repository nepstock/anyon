import json

import falcon

from src.helpers.common import get_new_uuid
from src.settings import (
    AM_CLIENT_CREDENTIALS_SCOPE,
    AM_CLIENT_SCOPE,
    AM_DOMAIN,
    EMAIL_FROM,
)

from .email import EMAIL_EXCEPTION_BODY, WELCOME_TEMAPLATE, validate
from .serializer import SignUpSchema


class Collection:
    __slots__ = (
        "_api",
        "_credentials",
        "_domain",
        "_email",
        "_scope",
    )

    def __init__(self, api, credentials_store, email):
        self._api = api
        self._credentials = credentials_store
        self._domain = AM_DOMAIN
        self._email = email
        self._scope = f"{AM_CLIENT_CREDENTIALS_SCOPE} {AM_CLIENT_SCOPE}"

    def _send_email(self, email):
        try:
            self._email.send(
                EMAIL_FROM,
                email,
                WELCOME_TEMAPLATE["subject"],
                WELCOME_TEMAPLATE["body"],
            )
        except Exception as e:
            # TODO - add logger
            pass

    def on_post(self, req, resp):
        data = SignUpSchema().load(req.media)
        if not validate(data["email"]):
            raise falcon.errors.HTTPUnprocessableEntity(**EMAIL_EXCEPTION_BODY)
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
        user_data = self._api.scim.create_user(
            self._domain, access_token, user
        )
        self._send_email(data["email"])
        resp.body = json.dumps(user_data, ensure_ascii=False, sort_keys=True)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_201


class Item:
    __slots__ = (
        "_api",
        "_credentials",
        "_domain",
        "_scope",
    )

    def __init__(self, api, credentials_store):
        self._api = api
        self._credentials = credentials_store
        self._domain = AM_DOMAIN
        self._scope = f"{AM_CLIENT_CREDENTIALS_SCOPE} {AM_CLIENT_SCOPE}"

    def on_get(self, req, resp, user_id: str):
        access_token = self._credentials.get_token(self._domain, self._scope)
        user_data = self._api.scim.get_user(
            self._domain, access_token, user_id
        )
        resp.body = json.dumps(user_data, ensure_ascii=False, sort_keys=True)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200
