import falcon
from marshmallow.exceptions import ValidationError
from requests.exceptions import HTTPError


def handle_validations(req, resp, error, params):
    raise falcon.HTTPInvalidParam(error.messages, error.field_name)


def handle_http(req, resp, error, params):
    error_item = error.response.json()
    if error.response.status_code == 400:
        raise falcon.HTTPBadRequest(
            title=error_item["scimType"], description=error_item["detail"],
        )
    elif error.response.status_code == 404:
        if "scimType" not in error_item:
            error_item["scimType"] = "NoContent"
        raise falcon.HTTPNotFound(
            title=error_item["scimType"], description=error_item["detail"],
        )
    elif error.response.status_code == 409:
        raise falcon.HTTPConflict(
            title=error_item["scimType"], description=error_item["detail"],
        )
    elif error.response.status_code >= 500:
        raise falcon.HTTPInternalServerError()
    else:
        raise falcon.HTTPServiceUnavailable()
