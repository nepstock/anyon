import re
from typing import Dict, Final, Pattern

import dns.resolver
from validate_email import exceptions, validate_email_or_fail

EMAIL_EXCEPTION_BODY: Final[Dict] = {
    "title": "validation_error",
    "description": "The email provided is not valid.",
}

LOCAL_PART: Final[Pattern] = re.compile(r"^.*?@", re.IGNORECASE)

WELCOME_TEMAPLATE = {
    "subject": "Nepstock: Bienvenido",
    "body": (
        "Ya has creado tu cuenta en nepestock" "<br />",
        "Puedes empezar a usarla de inmediato.",
    ),
}


def _get_mx_record(host: str) -> bool:
    try:
        records = dns.resolver.query(host, "MX")
        mxRecord = records[0].exchange
    except dns.resolver.NXDOMAIN:
        return False
    return True


def validate(email: str) -> bool:
    try:
        is_valid = validate_email_or_fail(
            email_address=email,
            check_regex=True,
            check_mx=True,
            smtp_timeout=10,
            dns_timeout=10,
            use_blacklist=True,
            debug=False,
        )
        return False if is_valid is None else is_valid
    except exceptions.AddressNotDeliverableError:
        host = re.sub(LOCAL_PART, "", email)
        return _get_mx_record(host)
    except Exception as e:
        # TODO - Add logger
        pass
    return False
