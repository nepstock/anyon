from .auth.views import Collection as AuthCollection
from .users.views import Collection, Item


def routes(api, am, credentials, secrets, email) -> None:
    api.add_route(
        "/oauth/token", AuthCollection(am, secrets),
    )
    api.add_route(
        "/users", Collection(am, credentials, email),
    )
    api.add_route(
        "/users/{user_id}", Item(am, credentials),
    )
