from typing import Dict, Optional, Tuple, Union

from .base import Base
from .constants import GRANT_TYPES, ContentTypes, GrantTypes, Services
from .helpers import add_content_type_to_header
from .serializer import ClientCredentialsTokenSchema, TokenSchema


class Oauth(Base):
    __slots__ = ()

    def _token(
        self,
        url: str,
        payload: Dict,
        auth: Tuple[str, str],
        schema: Union[TokenSchema, ClientCredentialsTokenSchema],
        scope: Optional[str] = None,
    ):
        if scope is not None:
            payload["scope"] = scope

        headers: Dict[str, str] = {}
        add_content_type_to_header(ContentTypes.Form_Urlencoded, headers)
        r = self._http.send(
            "post", url, data=payload, headers=headers, auth=auth
        )
        r.raise_for_status()
        if r.status_code == 200:
            return schema.load(r.json())
        return None

    def token(
        self,
        domain: str,
        client_id: str,
        client_secret: str,
        scope: Optional[str],
        **kwargs,
    ):
        url = self._create_url(domain, Services.Token)
        payload = {
            "grant_type": GRANT_TYPES[GrantTypes.Credentials],
        }
        schema: Union[
            TokenSchema, ClientCredentialsTokenSchema
        ] = ClientCredentialsTokenSchema()
        if "username" in kwargs and "password" in kwargs:
            payload = {
                "grant_type": GRANT_TYPES[GrantTypes.Password],
                "username": kwargs["username"],
                "password": kwargs["password"],
            }
            schema = TokenSchema()
        return self._token(
            url, payload, (client_id, client_secret), schema, scope
        )

    def revoke(
        self,
        domain: str,
        client_id: str,
        client_secret: str,
        token: str,
        token_type_hint: str = "access_token",
    ):
        url = self._create_url(domain, Services.Revoke)
        payload = {"token": token, "token_type_hint": token_type_hint}
        headers: Dict[str, str] = {}
        add_content_type_to_header(ContentTypes.Form_Urlencoded, headers)
        r = self._http.send(
            "post",
            url,
            data=payload,
            headers=headers,
            auth=(client_id, client_secret),
        )
        r.raise_for_status()
