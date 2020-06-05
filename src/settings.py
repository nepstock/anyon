import os
from typing import Final

AM_URL: Final[str] = os.getenv("AM_URL", "")
AM_DOMAIN: Final[str] = os.getenv("AM_DOMAIN", "")
AM_CLIENT_ID: Final[str] = os.getenv("AM_CLIENT_ID", "")
AM_CLIENT_SECRET: Final[str] = os.getenv("AM_CLIENT_SECRET", "")
AM_CLIENT_SCOPE: Final[str] = os.getenv("AM_CLIENT_SCOPE", "")
