import falcon

from .gravitee.am import AM
from .handlers import handlers
from .helpers.adapter import get_adapter
from .helpers.secrets import Secrets, check_secret
from .helpers.token import Credentials, check_token
from .helpers.variables import Store
from .notify.email import Email
from .routes import routes
from .settings import AM_CLIENT_ID, AM_CLIENT_SECRET, AM_URL, SENDGRID_API_KEY


def create_app(am_api, credentials, secrets, email):
    api = falcon.API()

    routes(api, am_api, credentials, secrets, email)

    handlers(api)

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
    email = Email(SENDGRID_API_KEY)
    return create_app(am, credentials, secrets, email)
