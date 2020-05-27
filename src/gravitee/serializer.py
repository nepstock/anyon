import datetime
import uuid

from marshmallow import (
    Schema,
    ValidationError,
    fields,
    post_load,
    validate,
    validates,
)
from marshmallow.decorators import pre_dump

from .constants import CLIENT_CREDENTIALS_SCOPES


class TokenSchema(Schema):
    access_token = fields.Str(required=True, allow_none=False)
    token_type = fields.String(required=True, allow_none=False)
    expires_in = fields.Int(required=True, allow_none=False)
    scope = fields.String(required=True, allow_none=False)
    id_token = fields.Str(allow_none=False)
    expires_date = fields.DateTime(
        required=False, missing=datetime.datetime.now()
    )

    @post_load
    def post_processing(self, data, **kwargs):
        data["expires_date"] = data["expires_date"] + datetime.timedelta(
            seconds=data["expires_in"] - 10
        )
        return data

    @validates("token_type")
    def token_validation(self, value):
        if value != "bearer":
            raise ValidationError("Invalid token type value.")

    @validates("scope")
    def scope_validation(context, value):
        values = set(value.split(" "))
        if not values.issubset(CLIENT_CREDENTIALS_SCOPES):
            raise ValidationError("Invalid scope value.")


class MetaSchema(Schema):
    resource_type = fields.Str(data_key="resourceType")
    created = fields.DateTime()
    modified = fields.DateTime(data_key="lastModified")
    location = fields.Url()

    @pre_dump
    def preprocess(self, data, **kwargs):
        for x in ("created", "lastModified"):
            if x in data and isinstance(data[x], str):
                data[x] = datetime.datetime.strptime(
                    data[x], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
        for x in (
            ("resourceType", "resource_type"),
            ("lastModified", "modified"),
        ):
            if x[0] in data:
                data[x[1]] = data[x[0]]
                del data[x[0]]
        return data


class EmailSchema(Schema):
    value = fields.Email(required=True)
    primary = fields.Boolean(required=True)


class NameSchema(Schema):
    family_name = fields.Str(data_key="familyName")
    given_name = fields.Str(data_key="givenName")

    @pre_dump
    def preprocess(self, data, **kwargs):
        for x in (
            ("familyName", "family_name"),
            ("givenName", "given_name"),
        ):
            if x[0] in data:
                data[x[1]] = data[x[0]]
                del data[x[0]]
        return data


class UserSchema(Schema):
    schemas = fields.List(fields.Str(required=True))
    id = fields.UUID(default=uuid.uuid4, required=True)
    external_id = fields.UUID(data_key="externalId", required=False)
    meta = fields.Nested(MetaSchema, dump_only=True)
    user_name = fields.Str(data_key="userName", required=True)
    name = fields.Nested(NameSchema, required=False)
    display_name = fields.Str(data_key="displayName")
    password = fields.Str(
        required=True, validate=validate.Length(min=8, max=27), load_only=True
    )
    active = fields.Boolean(missing=True)
    emails = fields.List(
        fields.Nested(EmailSchema), validate=validate.Length(min=1),
    )
    roles = fields.List(fields.Str())

    @pre_dump
    def preprocess(self, data, **kwargs):
        if "schemas" not in data or len(data["schemas"]) == 0:
            raise ValidationError(
                {"schemas": ["Shorter than minimum length 1."]}
            )
        for x in (
            ("externalId", "external_id"),
            ("userName", "user_name"),
            ("displayName", "display_name"),
        ):
            if x[0] in data:
                data[x[1]] = data[x[0]]
                del data[x[0]]

        return data
