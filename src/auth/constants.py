import re
from typing import Final, Pattern

AUTHORIZATION: Final[str] = "AUTHORIZATION"
SCOPE: Final[Pattern] = re.compile(
    r"(\s?(?:openId|scim)\s?){1,2}", re.IGNORECASE
)
TOKEN_TYPE: Final[Pattern] = re.compile(r"^bearer\s", re.IGNORECASE)
