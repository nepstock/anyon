import re
from typing import Dict

from .constants import SCOPE, TOKEN_TYPE


def remove_token_type(token: str) -> str:
    return re.sub(TOKEN_TYPE, "", token)


def transform_token_data(credentials: Dict[str, str]) -> Dict[str, str]:
    if "expires_date" in credentials:
        del credentials["expires_date"]
    credentials["scope"] = re.sub(SCOPE, "", credentials["scope"])
    return credentials
