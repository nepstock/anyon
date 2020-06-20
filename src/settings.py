import os
from typing import Final

APP_VERSION: Final[str] = os.getenv("APP_VERSION", "")

AM_URL: Final[str] = os.getenv("AM_URL", "")
AM_DOMAIN: Final[str] = os.getenv("AM_DOMAIN", "")
AM_CLIENT_CREDENTIALS_SCOPE: Final[str] = os.getenv(
    "AM_CLIENT_SCOPE", ""
).replace('"', "")
AM_CLIENT_ID: Final[str] = os.getenv("AM_CLIENT_ID", "")
AM_CLIENT_SECRET: Final[str] = os.getenv("AM_CLIENT_SECRET", "")
AM_CLIENT_SCOPE: Final[str] = os.getenv("AM_CLIENT_SCOPE", "").replace('"', "")

SENDGRID_API_KEY: Final[str] = os.getenv("SENDGRID_API_KEY", "")

EMAIL_FROM: Final[str] = os.getenv("EMAIL_FROM", "")
