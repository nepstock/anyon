import pytest
from marshmallow.exceptions import ValidationError

from src.auth.serializer import USERNAME_ERROR_MESSAGE, SignInSchema


class TestSignInSerializer:
    def test_load_success(self, input_auth_post):
        schema = SignInSchema()
        schema.load(input_auth_post)

    def test_load_email_error(self):
        data = {
            "username": "example.com",
            "password": "P4ssw0rd",
            "client_id": "aasdfghjkl",
        }
        schema = SignInSchema()
        with pytest.raises(ValidationError) as e:
            schema.load(data)
        e.match(
            r"\{'username': \['" + USERNAME_ERROR_MESSAGE["invalid"] + r"'\]\}"
        )

    def test_load_password_error(self):
        data = {
            "username": "test@example.com",
            "password": "P4ssw",
            "client_id": "aasdfghjkl",
        }
        schema = SignInSchema()
        with pytest.raises(ValidationError) as e:
            schema.load(data)
        e.match(r"\{'password': \['Length must be between 8 and 27.'\]\}")
