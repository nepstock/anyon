from functools import lru_cache

from .constants import PATHS, Services


class Base:
    __slots__ = (
        "_host",
        "_http",
    )

    def __init__(self, host: str, http_client) -> None:
        self._host = host
        self._http = http_client

    @lru_cache(maxsize=5)
    def _create_url(self, domain: str, path_key: Services) -> str:
        return f"{self._host}/{domain}/{PATHS[path_key]}"
