import json
from typing import Dict, Optional, Tuple

from marshmallow.exceptions import ValidationError

from src.api.auth import BearerAuth

from .base import Base
from .constants import GRANT_TYPES, ContentTypes, GrantTypes, Services
from .helpers import add_content_type_to_header
from .serializer import SCIMUserSchema


class SCIM(Base):
    __slots__ = ()

    def get_user(self, domain: str, token: str, user_id: str):
        url = self._create_url(domain, Services.Users)
        r = self._http.send("get", f"{url}/{user_id}", auth=BearerAuth(token))
        r.raise_for_status()
        if r.status_code == 200:
            return SCIMUserSchema().dump(r.json())

    def create_user(self, domain: str, token: str, user):
        schema = SCIMUserSchema()
        errors = schema.validate(user)
        if errors:
            raise ValidationError(errors)
        url = self._create_url(domain, Services.Users)
        headers: Dict[str, str] = {}
        add_content_type_to_header(ContentTypes.Json, headers)
        r = self._http.send(
            "post",
            url,
            data=json.dumps(user),
            headers=headers,
            auth=BearerAuth(token),
        )
        r.raise_for_status()
        if r.status_code == 201:
            return schema.dump(r.json())
