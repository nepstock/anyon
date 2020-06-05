import falcon

from src.errors.handler import (
    HTTPError,
    ValidationError,
    handle_http,
    handle_validations,
)

from .gravitee.am import AM
from .helpers.adapter import get_adapter
from .helpers.secrets import Secrets, check_secret
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
from .auth.views import Collection as AuthCollection


def create_app(am_api, credentials, secrets):
    api = falcon.API()

    api.add_route(
        "/oauth/token",
        AuthCollection(am_api, secrets, AM_DOMAIN, AM_CLIENT_SCOPE),
    )
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
    credentials = Credentials(
        Store(check_token), am, AM_CLIENT_ID, AM_CLIENT_SECRET
    )
    secrets = Secrets(
        Store(check_secret),
        ({"client_id": AM_CLIENT_ID, "client_secret": AM_CLIENT_SECRET},),
    )
    return create_app(am, credentials, secrets)
