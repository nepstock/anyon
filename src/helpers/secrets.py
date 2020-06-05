import datetime
from typing import Optional, Tuple, Dict


def check_secret(item, **kwargs):
    return item["client_id"] == kwargs["client_id"]


class Secrets:
    __slots__ = ("_store",)

    def __init__(self, store, data: Tuple[Dict[str, str]]) -> None:
        self._store = store
        for x in data:
            self._store.put(x)

    def get_secret(self, client_id: str):
        secret = self._store.get(client_id=client_id)
        if secret is None:
            return None
        self._store.put(secret)
        return secret["client_secret"]
