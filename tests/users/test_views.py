import json
import os
import uuid
from unittest.mock import patch

import falcon
import pytest

from src.users.views import Collection, Item


class TestItemSerializer:
    def test_item_success(
        self, client, output_am_get_user_response,
    ):
        url = f"/users/{output_am_get_user_response['id']}"
        response = client.simulate_get(url)
        client.mock_am.get_user.assert_called_with(
            os.getenv("AM_DOMAIN"),
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
        client.mock_am.create_user.assert_called_with(
            os.getenv("AM_DOMAIN"),
            client.mock_credentials.get_token(),
            new_user,
        )
        assert response.status == falcon.HTTP_201
        assert response.json == output_am_get_user_response
