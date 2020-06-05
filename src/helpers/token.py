import datetime
from typing import Optional


def check_token(item, **kwargs):
    return item["expires_date"] >= datetime.datetime.now()


class Credentials:
    __slots__ = (
        "_api",
        "_client_id",
        "_client_secret",
        "_store",
    )

    def __init__(self, store, api, client_id: str, client_secret: str):
        self._api = api
        self._client_id = client_id
        self._client_secret = client_secret
        self._store = store

    def get_token(self, domain: str, scope: Optional[str]):
        credentials = self._store.get()
        if credentials is None:
            credentials = self._api.token(
                domain, self._client_id, self._client_secret, scope
            )
            self._store.put(credentials)
        return credentials["access_token"]
