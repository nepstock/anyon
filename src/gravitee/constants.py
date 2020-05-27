import os
from enum import Enum, unique


@unique
class Services(Enum):
    Users = 1
    Token = 2


@unique
class GrantTypes(Enum):
    Credentials = 1
    Token = 2


GRANT_TYPES = {GrantTypes.Credentials: "client_credentials"}

PATHS = {
    Services.Users: os.getenv("AM_PATH_USERS", ""),
    Services.Token: os.getenv("AM_PATH_TOKEN", ""),
}

CLIENT_CREDENTIALS_SCOPES = set(
    os.getenv("AM_CLIENT_CREDENTIALS_SCOPE", "").split(" ")
)
