from typing import Dict, Final

from marshmallow import Schema, fields, validate

USERNAME_ERROR_MESSAGE: Final[Dict[str, str]] = {
    "invalid": "Not a valid username."
}


class SignInSchema(Schema):
    client_id = fields.Str(required=True, load_only=True)
    username = fields.Email(
        required=True, load_only=True, error_messages=USERNAME_ERROR_MESSAGE,
    )
    password = fields.Str(
        required=True, validate=validate.Length(min=8, max=27), load_only=True
    )
