import urllib.parse

import pytest
import requests
from marshmallow.exceptions import ValidationError

from src.gravitee.am import AM
from src.gravitee.constants import GRANT_TYPES, PATHS, GrantTypes, Services
from src.gravitee.serializer import TokenSchema, UserSchema


class TestTokenSerializer:
    def _register_uri(
        self, method, url, requests_mock, mock_response, status_code
    ):
        requests_mock.register_uri(
            method, url, json=mock_response, status_code=status_code
        )

    def test_token_client_credentials_success(
        self,
        requests_mock,
        input_am_client_credentials,
        output_am_client_credentials,
    ):
        url = (
            f"{input_am_client_credentials['host']}/"
            f"{input_am_client_credentials['domain']}/{PATHS[Services.Token]}"
        )
        self._register_uri(
            "post", url, requests_mock, output_am_client_credentials, 200
        )
        am = AM(input_am_client_credentials["host"])
        r = am.token(
            input_am_client_credentials["domain"],
            input_am_client_credentials["client_id"],
            input_am_client_credentials["client_secret"],
            input_am_client_credentials["scope"],
        )
        payload = {
            "grant_type": GRANT_TYPES[GrantTypes.Credentials],
            "scope": input_am_client_credentials["scope"],
        }
        assert requests_mock.request_history[0].text == urllib.parse.urlencode(
            payload, doseq=True
        )
        reponse_schema = TokenSchema().load(output_am_client_credentials)
        r["expires_date"] = reponse_schema["expires_date"]
        assert reponse_schema == r

    def test_token_client_credentials_http_error(
        self, requests_mock, input_am_client_credentials
    ):
        url = (
            f"{input_am_client_credentials['host']}/"
            f"{input_am_client_credentials['domain']}/{PATHS[Services.Token]}"
        )
        self._register_uri("post", url, requests_mock, None, status_code=404)
        am = AM(input_am_client_credentials["host"])
        with pytest.raises(requests.exceptions.HTTPError):
            r = am.token(
                input_am_client_credentials["domain"],
                input_am_client_credentials["client_id"],
                input_am_client_credentials["client_secret"],
                input_am_client_credentials["scope"],
            )

    def test_token_password(
        self, requests_mock, input_am_password, output_am_client_credentials,
    ):
        url = (
            f"{input_am_password['host']}/"
            f"{input_am_password['domain']}/{PATHS[Services.Token]}"
        )
        self._register_uri(
            "post", url, requests_mock, output_am_client_credentials, 200
        )
        am = AM(input_am_password["host"])
        r = am.token(
            input_am_password["domain"],
            input_am_password["client_id"],
            input_am_password["client_secret"],
            input_am_password["scope"],
            username=input_am_password["username"],
            password=input_am_password["password"],
        )
        payload = {
            "grant_type": GRANT_TYPES[GrantTypes.Password],
            "username": input_am_password["username"],
            "password": input_am_password["password"],
            "scope": input_am_password["scope"],
        }
        assert requests_mock.request_history[0].text == urllib.parse.urlencode(
            payload, doseq=True
        )
        reponse_schema = TokenSchema().load(output_am_client_credentials)
        r["expires_date"] = reponse_schema["expires_date"]
        assert reponse_schema == r

    def test_token_password_http_error(self, requests_mock, input_am_password):
        url = (
            f"{input_am_password['host']}/"
            f"{input_am_password['domain']}/{PATHS[Services.Token]}"
        )
        self._register_uri("post", url, requests_mock, None, status_code=400)
        am = AM(input_am_password["host"])
        with pytest.raises(requests.exceptions.HTTPError):
            r = am.token(
                input_am_password["domain"],
                input_am_password["client_id"],
                input_am_password["client_secret"],
                input_am_password["scope"],
                username=input_am_password["username"],
                password=input_am_password["password"],
            )

    def test_get_user(
        self,
        requests_mock,
        input_am_client_credentials,
        output_am_client_credentials,
        output_am_get_user_response,
    ):
        url = (
            f"{input_am_client_credentials['host']}/"
            f"{input_am_client_credentials['domain']}/{PATHS[Services.Users]}"
            f"/{output_am_get_user_response['id']}"
        )
        self._register_uri(
            "get", url, requests_mock, output_am_get_user_response, 200
        )
        am = AM(input_am_client_credentials["host"])
        r = am.get_user(
            input_am_client_credentials["domain"],
            output_am_client_credentials["access_token"],
            output_am_get_user_response["id"],
        )
        output = UserSchema().dump(output_am_get_user_response)
        assert r == output

    def test_get_user_http_error(
        self,
        requests_mock,
        input_am_client_credentials,
        output_am_client_credentials,
        output_am_get_user_response,
    ):
        url = (
            f"{input_am_client_credentials['host']}/"
            f"{input_am_client_credentials['domain']}/{PATHS[Services.Users]}"
            f"/{output_am_get_user_response['id']}"
        )
        self._register_uri("get", url, requests_mock, None, 400)
        am = AM(input_am_client_credentials["host"])
        with pytest.raises(requests.exceptions.HTTPError):
            r = am.get_user(
                input_am_client_credentials["domain"],
                output_am_client_credentials["access_token"],
                output_am_get_user_response["id"],
            )

    def test_create_user(
        self,
        requests_mock,
        input_am_client_credentials,
        input_am_create_user,
        output_am_client_credentials,
        output_am_get_user_response,
    ):
        url = (
            f"{input_am_client_credentials['host']}/"
            f"{input_am_client_credentials['domain']}/{PATHS[Services.Users]}"
        )
        self._register_uri(
            "post", url, requests_mock, output_am_get_user_response, 201
        )
        am = AM(input_am_client_credentials["host"])
        r = am.create_user(
            input_am_client_credentials["domain"],
            output_am_client_credentials["access_token"],
            input_am_create_user,
        )
        output = UserSchema().dump(output_am_get_user_response)
        assert r == output

    def test_create_user_http_error(
        self,
        requests_mock,
        input_am_client_credentials,
        input_am_create_user,
        output_am_client_credentials,
        output_am_get_user_response,
    ):
        url = (
            f"{input_am_client_credentials['host']}/"
            f"{input_am_client_credentials['domain']}/{PATHS[Services.Users]}"
        )
        self._register_uri("post", url, requests_mock, None, 400)
        am = AM(input_am_client_credentials["host"])
        with pytest.raises(requests.exceptions.HTTPError):
            r = am.create_user(
                input_am_client_credentials["domain"],
                output_am_client_credentials["access_token"],
                input_am_create_user,
            )

    def test_create_user_validation_error(
        self,
        input_am_client_credentials,
        input_am_create_user,
        output_am_client_credentials,
        output_am_get_user_response,
    ):
        am = AM(input_am_client_credentials["host"])
        with pytest.raises(ValidationError):
            r = am.create_user(
                input_am_client_credentials["domain"],
                output_am_client_credentials["access_token"],
                {},
            )
