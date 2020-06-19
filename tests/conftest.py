import datetime
from unittest.mock import MagicMock

import pytest
from falcon import testing

from src.app import create_app
from src.gravitee.constants import CLIENT_CREDENTIALS_SCOPES

DOMAIN = "mock_domain"
CLIENT_ID = "mock_client_id"
CLIENT_SECRET = "mock_client_secret"
EMAIL_FROM = "mock@example.com"
SCOPE = next(iter(CLIENT_CREDENTIALS_SCOPES))


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("AM_DOMAIN", DOMAIN)
    monkeypatch.setenv("AM_CLIENT_ID", CLIENT_ID)
    monkeypatch.setenv("AM_CLIENT_SECRET", CLIENT_SECRET)
    monkeypatch.setenv("AM_CLIENT_SCOPE", SCOPE)
    monkeypatch.setenv("EMAIL_FROM", EMAIL_FROM)


@pytest.fixture
def mock_am():
    return MagicMock()


@pytest.fixture
def mock_credentials():
    return MagicMock()


@pytest.fixture
def mock_email():
    return MagicMock()


@pytest.fixture
def mock_secrets():
    return MagicMock()


@pytest.fixture
def input_am_client_credentials():
    return {
        "host": "http://test.com",
        "domain": DOMAIN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE,
    }


@pytest.fixture
def output_am_client_credentials():
    return {
        "access_token": "TOwCpefZQG32HvrCQ5e89zRTrnCMOXk-xkp1yfCIaog",
        "token_type": "bearer",
        "expires_in": 7199,
        "scope": SCOPE,
    }


@pytest.fixture
def input_am_password():
    return {
        "host": "http://test.com",
        "domain": DOMAIN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": "test@example.com",
        "password": "P4$$w0rd",
        "scope": SCOPE,
    }


@pytest.fixture
def output_am_get_user_response():
    return {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "565417db-6883-45ee-9417-db688305ee4e",
        "externalId": "39a3094a-b4d1-41e2-a309-4ab4d141e2fd",
        "meta": {
            "resourceType": "User",
            "created": "2020-05-25T02:24:13.647Z",
            "lastModified": "2020-05-25T23:40:32.805Z",
            "location": (
                "http://localhost/am/nepstock/scim/"
                "Users/565417db-6883-45ee-9417-db688305ee4e"
            ),
        },
        "userName": "test@example.com",
        "name": {"familyName": "", "givenName": ""},
        "displayName": "testo testi",
        "active": True,
        "emails": [{"value": "test@example.com", "primary": True}],
        "roles": [],
    }


@pytest.fixture
def input_am_create_user():
    return {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "565417db-6883-45ee-9417-db688305ee4e",
        "userName": "test@example.com",
        "name": {"familyName": "", "givenName": ""},
        "password": "P4$$w0rd",
        "active": True,
        "emails": [{"value": "test@example.com", "primary": True}],
    }


@pytest.fixture
def input_users_post():
    return {
        "email": "test@test.com",
        "password": "P4$$w0rd",
    }


@pytest.fixture
def input_auth_post():
    return {
        "username": "test@test.com",
        "password": "P4$$w0rd",
        "client_id": CLIENT_ID,
    }


@pytest.fixture
def output_view_am_client_credentials():
    return {
        "access_token": "TOwCpefZQG32HvrCQ5e89zRTrnCMOXk-xkp1yfCIaog",
        "token_type": "bearer",
        "expires_in": 7199,
        "scope": SCOPE,
        "expires_date": datetime.datetime.now(),
    }


@pytest.fixture
def client(
    mock_am,
    mock_credentials,
    mock_email,
    mock_secrets,
    output_view_am_client_credentials,
    output_am_get_user_response,
):
    mock_am.oauth.token.return_value = output_view_am_client_credentials
    mock_am.scim.get_user.return_value = output_am_get_user_response
    mock_am.scim.create_user.return_value = output_am_get_user_response
    # mock_email.send.return_value =
    api = create_app(mock_am, mock_credentials, mock_secrets, mock_email)
    t = testing.TestClient(api)
    t.mock_am = mock_am
    t.mock_credentials = mock_credentials
    t.mock_email = mock_email
    t.mock_secrets = mock_secrets
    return t
