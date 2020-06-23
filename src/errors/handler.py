from typing import Dict

import falcon
from marshmallow.exceptions import ValidationError
from requests.exceptions import HTTPError


def handle_validations(req, resp, error, params):
    raise falcon.HTTPInvalidParam(error.messages, error.field_name)


def _get_exception_title(error_item: Dict[str, str], status_code: int) -> str:
    if "scimType" not in error_item:
        if status_code == 404:
            return "NoContent"
        return "invalid_parameter"
    return error_item["scimType"]


def _get_exception_description(error_item: Dict[str, str]) -> str:
    if "detail" in error_item:
        return error_item["detail"]
    elif "error_description" not in error_item:
        return error_item["error_description"]
    return ""


def handle_http(req, resp, error, params):
    status_code = error.response.status_code
    exception_item = {
        "title": _get_exception_title(error.response.json(), status_code),
        "description": _get_exception_description(error.response.json()),
    }
    if status_code == 400:
        raise falcon.HTTPBadRequest(**exception_item)
    elif status_code == 404:
        raise falcon.HTTPNotFound(**exception_item)
    elif status_code == 409:
        raise falcon.HTTPConflict(**exception_item)
    elif status_code == 503:
        raise falcon.HTTPServiceUnavailable()
    raise falcon.HTTPInternalServerError()
