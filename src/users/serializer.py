from marshmallow import Schema, fields, validate


class SignUpSchema(Schema):
    email = fields.Email(required=True, load_only=True)
    password = fields.Str(
        required=True, validate=validate.Length(min=8, max=27), load_only=True
    )
