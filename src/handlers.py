from src.errors.handler import (
    HTTPError,
    ValidationError,
    handle_http,
    handle_validations,
)


def handlers(api) -> None:
    api.add_error_handler(HTTPError, handle_http)
    api.add_error_handler(ValidationError, handle_validations)
