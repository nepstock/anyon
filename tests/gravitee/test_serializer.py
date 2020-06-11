import uuid

import pytest
from marshmallow.exceptions import ValidationError

from src.gravitee.constants import CLIENT_CREDENTIALS_SCOPES
from src.gravitee.serializer import TokenSchema, UserSchema

SCOPE = next(iter(CLIENT_CREDENTIALS_SCOPES))


class TestTokenSerializer:
    def test_load_success(self, mock_env):
        token_data = {
            "scope": SCOPE,
            "expires_in": 7199,
            "id_token": "aKAhpjUMn_dYbH5jiDdJn8s0EdbtbMNqOTPhcI89T2g",
            "token_type": "bearer",
            "access_token": "2glZ7GYZaY3lD5ivIsgfDbQEBLEKHZNJ4UZWZEEbhEY",
        }
        schema = TokenSchema()
        schema.load(token_data)

    def test_load_scope_success(self):
        token_data = {
            "scope": "scim",
            "expires_in": 7199,
            "id_token": "aKAhpjUMn_dYbH5jiDdJn8s0EdbtbMNqOTPhcI89T2g",
            "token_type": "bearer",
            "access_token": "2glZ7GYZaY3lD5ivIsgfDbQEBLEKHZNJ4UZWZEEbhEY",
        }
        schema = TokenSchema()
        schema.load(token_data)

    def test_load_invalid_token_type(self):
        token_data = {
            "scope": SCOPE,
            "expires_in": 7199,
            "id_token": "aKAhpjUMn_dYbH5jiDdJn8s0EdbtbMNqOTPhcI89T2g",
            "token_type": "blablabla",
            "access_token": "2glZ7GYZaY3lD5ivIsgfDbQEBLEKHZNJ4UZWZEEbhEY",
        }
        schema = TokenSchema()
        with pytest.raises(ValidationError) as e:
            schema.load(token_data)
        e.match(r"\{'token_type': \['Invalid token type value.'\]\}")

    def test_load_invalid_scope(self):
        token_data = {
            "scope": "scim blablabla",
            "expires_in": 7199,
            "id_token": "aKAhpjUMn_dYbH5jiDdJn8s0EdbtbMNqOTPhcI89T2g",
            "token_type": "bearer",
            "access_token": "2glZ7GYZaY3lD5ivIsgfDbQEBLEKHZNJ4UZWZEEbhEY",
        }
        schema = TokenSchema()
        with pytest.raises(ValidationError) as e:
            schema.load(token_data)
        e.match(r"\{'scope': \['Invalid scope value.'\]\}")


class TestUserSerializer:
    def test_dump_success(self):
        user_data = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": "fe576610-a01f-4ae3-9766-10a01f9ae31c",
            "meta": {
                "resourceType": "User",
                "created": "2020-05-25T23:41:41.128Z",
                "lastModified": "2020-05-26T23:41:41.128Z",
                "location": (
                    "http://localhost/am/nepstock/scim/Users/"
                    "fe576610-a01f-4ae3-9766-10a01f9ae31c"
                ),
            },
            "userName": "test@example.com",
            "name": {"familyName": "", "givenName": ""},
            "displayName": " ",
            "active": False,
            "emails": [{"value": "test@example.com", "primary": True}],
        }
        schema = UserSchema()
        schema.dump(user_data)

    def test_dump_default_id_success(self):
        user_data = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "meta": {
                "resourceType": "User",
                "created": "2020-05-25T23:41:41.128Z",
                "lastModified": "2020-05-26T23:41:41.128Z",
                "location": (
                    "http://localhost/am/nepstock/scim/Users/"
                    "fe576610-a01f-4ae3-9766-10a01f9ae31c"
                ),
            },
            "userName": "test@example.com",
            "name": {"familyName": "", "givenName": ""},
            "displayName": " ",
            "active": False,
            "emails": [{"value": "test@example.com", "primary": True}],
        }
        schema = UserSchema()
        user = schema.dump(user_data)
        assert "id" in user and uuid.UUID(user["id"], version=4)

    def test_dump_invalid_schema(self):
        user_data = {
            "schemas": [],
            "meta": {
                "resourceType": "User",
                "created": "2020-05-25T23:41:41.128Z",
                "lastModified": "2020-05-26T23:41:41.128Z",
                "location": (
                    "http://localhost/am/nepstock/scim/Users/"
                    "fe576610-a01f-4ae3-9766-10a01f9ae31c"
                ),
            },
            "userName": "test@example.com",
            "name": {"familyName": "", "givenName": ""},
            "displayName": " ",
            "active": False,
            "emails": [{"value": "test@example.com", "primary": True}],
        }
        schema = UserSchema()
        with pytest.raises(ValidationError) as e:
            schema.dump(user_data)
        e.match(r"\{'schemas': \['Shorter than minimum length 1.'\]\}")

    def test_load_success(self):
        user_data = {
            "id": "fe576610-a01f-4ae3-9766-10a01f9ae31c",
            "userName": "test@example.com",
            "name": {"familyName": "", "givenName": ""},
            "displayName": " ",
            "password": "password",
            "active": True,
            "emails": [{"value": "test@example.com", "primary": True}],
        }
        schema = UserSchema()
        user = schema.load(user_data)

    def test_load_unknown_fields(self):
        user_data = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": "fe576610-a01f-4ae3-9766-10a01f9ae31c",
            "meta": {
                "resourceType": "User",
                "created": "2020-05-25T23:41:41.128Z",
                "lastModified": "2020-05-26T23:41:41.128Z",
                "location": (
                    "http://localhost/am/nepstock/scim/Users/"
                    "fe576610-a01f-4ae3-9766-10a01f9ae31c"
                ),
            },
            "userName": "test@example.com",
            "name": {"familyName": "", "givenName": ""},
            "password": "password",
            "displayName": " ",
            "active": False,
            "emails": [{"value": "test@example.com", "primary": True}],
        }
        schema = UserSchema()
        with pytest.raises(ValidationError) as e:
            schema.load(user_data)
        e.match(r"\{'meta': \['Unknown field.'\]\}")

    def test_load_invalid_emails(self):
        user_data = {
            "id": "fe576610-a01f-4ae3-9766-10a01f9ae31c",
            "userName": "test@example.com",
            "name": {"familyName": "", "givenName": ""},
            "displayName": " ",
            "password": "password",
            "active": False,
            "emails": [],
        }
        schema = UserSchema()
        with pytest.raises(ValidationError) as e:
            schema.load(user_data)
        e.match(r"\{'emails': \['Shorter than minimum length 1.'\]\}")

    def test_load_missing_fields(self):
        user_data = {
            "id": "fe576610-a01f-4ae3-9766-10a01f9ae31c",
            "userName": "test@example.com",
            "name": {"familyName": "", "givenName": ""},
            "displayName": " ",
            "active": False,
            "emails": [{"value": "test@example.com", "primary": True}],
        }
        schema = UserSchema()
        with pytest.raises(ValidationError) as e:
            schema.load(user_data)
        e.match(r"\{'password': \['Missing data for required field.'\]\}")
