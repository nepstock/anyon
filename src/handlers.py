from src.errors.handler import (
    ConnectionError,
    HTTPError,
    ValidationError,
    handle_http,
    handle_request_errors,
    handle_validations,
)


def handlers(api) -> None:
    api.add_error_handler(ConnectionError, handle_request_errors)
    api.add_error_handler(HTTPError, handle_http)
    api.add_error_handler(ValidationError, handle_validations)
