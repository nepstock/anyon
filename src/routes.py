from .auth.views import Collection as AuthCollection
from .settings import AM_CLIENT_ID, AM_CLIENT_SCOPE, AM_DOMAIN
from .users.views import Collection, Item


def routes(api, am, credentials, secrets, email) -> None:
    api.add_route(
        "/oauth/token",
        AuthCollection(am, AM_CLIENT_ID, secrets, AM_DOMAIN, AM_CLIENT_SCOPE),
    )
    api.add_route(
        "/users",
        Collection(am, credentials, AM_DOMAIN, AM_CLIENT_SCOPE, email),
    )
    api.add_route(
        "/users/{user_id}", Item(am, credentials, AM_DOMAIN, AM_CLIENT_SCOPE),
    )
