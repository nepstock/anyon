import pytest
from marshmallow.exceptions import ValidationError

from src.users.serializer import SignUpSchema


class TestSignUpSerializer:
    def test_load_success(self, input_users_post):
        schema = SignUpSchema()
        schema.load(input_users_post)

    def test_load_email_error(self):
        data = {"email": "example.com", "password": "P4ssw0rd"}
        schema = SignUpSchema()
        with pytest.raises(ValidationError) as e:
            schema.load(data)
        e.match(r"\{'email': \['Not a valid email address.'\]\}")

    def test_load_password_error(self):
        data = {"email": "test@example.com", "password": "P4ssw"}
        schema = SignUpSchema()
        with pytest.raises(ValidationError) as e:
            schema.load(data)
        e.match(r"\{'password': \['Length must be between 8 and 27.'\]\}")
