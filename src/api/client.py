from typing import Any, Dict, Optional, Tuple, Union

from requests import Session
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase


class Client(object):
    def __init__(self):
        self._http = Session()

    def add_adapter(self, host: str, http_adapter: HTTPAdapter) -> None:
        self._http.mount(host, http_adapter)

    def send(
        self,
        method: str,
        url: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[Union[AuthBase, Tuple[str, str]]] = None,
    ):
        send = getattr(self._http, method.lower())
        if method == "get":
            return send(url, params=data, headers=headers, auth=auth)
        return send(url, data=data, headers=headers, auth=auth)
