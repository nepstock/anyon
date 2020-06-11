import os
from enum import Enum, unique
from typing import Dict, Final, Set


@unique
class Services(Enum):
    Users = 1
    Token = 2
    Revoke = 3


@unique
class GrantTypes(Enum):
    Credentials = 1
    Password = 2


GRANT_TYPES: Final[Dict[GrantTypes, str]] = {
    GrantTypes.Credentials: "client_credentials",
    GrantTypes.Password: "password",
}

PATHS: Final[Dict[Services, str]] = {
    Services.Users: os.getenv("AM_PATH_USERS", ""),
    Services.Token: os.getenv("AM_PATH_TOKEN", ""),
    Services.Revoke: os.getenv("AM_PATH_REVOKE", ""),
}

CLIENT_CREDENTIALS_SCOPES: Final[Set] = set(
    os.getenv("AM_CLIENT_CREDENTIALS_SCOPE", "").split(" ")
)
