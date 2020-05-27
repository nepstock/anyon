import falcon

from src.errors.handler import (
    HTTPError,
    ValidationError,
    handle_http,
    handle_validations,
)

from .gravitee.am import AM
from .helpers.adapter import get_adapter
from .helpers.token import Credentials, check_token
from .helpers.variables import Store
from .settings import (
    AM_CLIENT_ID,
    AM_CLIENT_SCOPE,
    AM_CLIENT_SECRET,
    AM_DOMAIN,
    AM_URL,
)
from .users.views import Collection, Item


def create_app(am_api, credentials):
    api = falcon.API()
    api.add_route(
        "/users", Collection(am_api, credentials, AM_DOMAIN, AM_CLIENT_SCOPE)
    )
    api.add_route(
        "/users/{user_id}",
        Item(am_api, credentials, AM_DOMAIN, AM_CLIENT_SCOPE),
    )

    api.add_error_handler(HTTPError, handle_http)
    api.add_error_handler(ValidationError, handle_validations)
    return api


def get_app():
    am = AM(AM_URL, get_adapter())
    store = Store(check_token)
    credentials = Credentials(store, am, AM_CLIENT_ID, AM_CLIENT_SECRET)
    return create_app(am, credentials)
