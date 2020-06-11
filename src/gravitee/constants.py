import os
from enum import Enum, unique
from typing import Dict, Final, FrozenSet


@unique
class ContentTypes(Enum):
    Form_Urlencoded = 1
    Json = 2


@unique
class GrantTypes(Enum):
    Credentials = 1
    Password = 2


@unique
class Services(Enum):
    Users = 1
    Token = 2
    Revoke = 3


@unique
class HeaderTypes(Enum):
    content_type = 1


CLIENT_CREDENTIALS_SCOPES: Final[FrozenSet] = frozenset(
    os.getenv("AM_CLIENT_CREDENTIALS_SCOPE", "").split(" ")
)

CONTENT_TYPES: Final[Dict[ContentTypes, str]] = {
    ContentTypes.Form_Urlencoded: (
        "application/x-www-form-urlencoded; charset=UTF-8"
    ),
    ContentTypes.Json: "application/json",
}

HEADERS: Final[Dict[HeaderTypes, str]] = {
    HeaderTypes.content_type: "Content-Type"
}

GRANT_TYPES: Final[Dict[GrantTypes, str]] = {
    GrantTypes.Credentials: "client_credentials",
    GrantTypes.Password: "password",
}

PATHS: Final[Dict[Services, str]] = {
    Services.Users: os.getenv("AM_PATH_USERS", ""),
    Services.Token: os.getenv("AM_PATH_TOKEN", ""),
    Services.Revoke: os.getenv("AM_PATH_REVOKE", ""),
}
