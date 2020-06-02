import json
import os
from functools import lru_cache
from typing import Dict, Optional

from requests.adapters import HTTPAdapter

from src.api.auth import BearerAuth
from src.api.client import Client

from .constants import GRANT_TYPES, PATHS, GrantTypes, Services
from .serializer import TokenSchema, UserSchema
from marshmallow.exceptions import ValidationError


class AM:
    def __init__(self, host: str, adapter: Optional[HTTPAdapter] = None):
        self._host = host
        self._http = Client()
        if adapter is not None:
            self._http.add_adapter(self._host, adapter)

    @lru_cache(maxsize=5)
    def _create_url(self, domain: str, path_key: Services) -> str:
        return f"{self._host}/{domain}/{PATHS[path_key]}"

    def get_client_credentials(
        self,
        domain: str,
        client_id: str,
        client_secret: str,
        scope: Optional[str] = None,
    ):
        url = self._create_url(domain, Services.Token)
        payload = {
            "grant_type": GRANT_TYPES[GrantTypes.Credentials],
        }
        if scope is not None:
            payload["scope"] = scope

        r = self._http.send(
            "post", url, data=payload, auth=(client_id, client_secret),
        )
        r.raise_for_status()
        if r.status_code == 200:
            return TokenSchema().load(r.json())
        return None

    def get_user(self, domain: str, token: str, user_id: str):
        url = self._create_url(domain, Services.Users)
        r = self._http.send("get", f"{url}/{user_id}", auth=BearerAuth(token))
        r.raise_for_status()
        if r.status_code == 200:
            return UserSchema().dump(r.json())

    def create_user(self, domain: str, token: str, user):
        schema = UserSchema()
        errors = schema.validate(user)
        if errors:
            raise ValidationError(errors)
        url = self._create_url(domain, Services.Users)
        r = self._http.send(
            "post",
            url,
            data=json.dumps(user),
            headers={"Content-Type": "application/json"},
            auth=BearerAuth(token),
        )
        r.raise_for_status()
        if r.status_code == 201:
            return schema.dump(r.json())
