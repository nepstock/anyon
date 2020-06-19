import falcon
import pytest

from src.auth.constants import AUTHORIZATION
from src.auth.helpers import transform_token_data
from src.settings import AM_CLIENT_ID, AM_CLIENT_SCOPE, AM_DOMAIN


class TestCollectionSerializer:
    def test_post_success(
        self, mock_env, client, input_auth_post, output_am_client_credentials,
    ):
        url = "/oauth/token"
        response = client.simulate_post(url, json=input_auth_post)
        client.mock_am.oauth.token.assert_called_with(
            AM_DOMAIN,
            input_auth_post["client_id"],
            client.mock_secrets.get_secret(),
            AM_CLIENT_SCOPE,
            username=input_auth_post["username"],
            password=input_auth_post["password"],
        )
        output_am_client_credentials = transform_token_data(
            output_am_client_credentials
        )
        assert response.status == falcon.HTTP_200
        assert response.json == output_am_client_credentials

    def test_delete_success(
        self, mock_env, client,
    ):
        url = "/oauth/token"
        token = "some_toke"
        response = client.simulate_delete(
            url, headers={AUTHORIZATION: f"bearer {token}"}
        )
        client.mock_am.oauth.revoke.assert_called_with(
            AM_DOMAIN, AM_CLIENT_ID, client.mock_secrets.get_secret(), token,
        )
        assert response.status == falcon.HTTP_204
