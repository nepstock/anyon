import json
import uuid
from unittest.mock import patch

import falcon
import pytest

from src.settings import AM_DOMAIN, EMAIL_FROM
from src.users.email import WELCOME_TEMAPLATE


class TestItemSerializer:
    def test_item_success(
        self, mock_env, client, output_am_get_user_response,
    ):
        url = f"/users/{output_am_get_user_response['id']}"
        response = client.simulate_get(url)
        client.mock_credentials.get_token.assert_called_with(
            AM_DOMAIN, "scim openid"
        )
        client.mock_am.scim.get_user.assert_called_with(
            AM_DOMAIN,
            client.mock_credentials.get_token(),
            output_am_get_user_response["id"],
        )
        assert response.status == falcon.HTTP_200
        assert response.json == output_am_get_user_response


class TestCollectionSerializer:
    @patch("src.users.views.get_new_uuid")
    def test_post_success(
        self,
        get_new_uuid,
        mock_env,
        client,
        input_users_post,
        output_am_get_user_response,
    ):
        url = "/users"
        get_new_uuid.return_value = output_am_get_user_response["id"]
        response = client.simulate_post(url, json=input_users_post)
        new_user = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": output_am_get_user_response["id"],
            "userName": input_users_post["email"],
            "name": {"familyName": "", "givenName": ""},
            "password": input_users_post["password"],
            "active": True,
            "emails": [{"value": input_users_post["email"], "primary": True}],
        }
        client.mock_credentials.get_token.assert_called_with(
            AM_DOMAIN, "scim openid"
        )
        client.mock_am.scim.create_user.assert_called_with(
            AM_DOMAIN, client.mock_credentials.get_token(), new_user,
        )
        client.mock_email.send.assert_called_with(
            EMAIL_FROM,
            input_users_post["email"],
            WELCOME_TEMAPLATE["subject"],
            WELCOME_TEMAPLATE["body"],
        )
        assert response.status == falcon.HTTP_201
        assert response.json == output_am_get_user_response
