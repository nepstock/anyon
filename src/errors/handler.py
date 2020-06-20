from typing import Dict

import falcon
from marshmallow.exceptions import ValidationError
from requests.exceptions import HTTPError


def handle_validations(req, resp, error, params):
    raise falcon.HTTPInvalidParam(error.messages, error.field_name)


def _get_exception_item(error_item: Dict[str, str], status_code: int) -> Dict:
    data = {}
    if "scimType" not in error_item and status_code == 404:
        data["title"] = "NoContent"
    elif "scimType" not in error_item:
        data["title"] = "invalid_parameter"
    else:
        data["title"] = error_item["scimType"]

    if "detail" not in error_item:
        data["description"] = error_item["error_description"]
    else:
        data["description"] = error_item["detail"]
    return data


def handle_http(req, resp, error, params):
    status_code = error.response.status_code
    exception_item = _get_exception_item(error.response.json(), status_code)
    if status_code == 400:
        raise falcon.HTTPBadRequest(**exception_item)
    elif status_code == 404:
        raise falcon.HTTPNotFound(**exception_item)
    elif status_code == 409:
        raise falcon.HTTPConflict(**exception_item)
    elif status_code == 503:
        raise falcon.HTTPServiceUnavailable()
    raise falcon.HTTPInternalServerError()
