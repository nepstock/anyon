import falcon
import pytest

from src.settings import AM_CLIENT_SCOPE, AM_DOMAIN


class TestCollectionSerializer:
    def test_post_success(
        self, mock_env, client, input_auth_post, output_am_client_credentials,
    ):
        url = "/oauth/token"
        response = client.simulate_post(url, json=input_auth_post)
        client.mock_am.token.assert_called_with(
            AM_DOMAIN,
            input_auth_post["client_id"],
            client.mock_secrets.get_secret(),
            AM_CLIENT_SCOPE,
            username=input_auth_post["username"],
            password=input_auth_post["password"],
        )
        output_am_client_credentials["scope"] = output_am_client_credentials[
            "scope"
        ].replace("scim", "")
        assert response.status == falcon.HTTP_200
        assert response.json == output_am_client_credentials
