from typing import Optional

from requests.adapters import HTTPAdapter

from src.api.client import Client

from .oauth import Oauth
from .scim import SCIM


class AM:
    __slots__ = (
        "oauth",
        "scim",
    )

    def __init__(self, host: str, adapter: Optional[HTTPAdapter] = None):
        http = Client()
        if adapter is not None:
            http.add_adapter(host, adapter)
        self.oauth = Oauth(host, http)
        self.scim = SCIM(host, http)
