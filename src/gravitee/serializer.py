import datetime
import uuid
from typing import Final

from marshmallow import (
    INCLUDE,
    Schema,
    ValidationError,
    fields,
    post_load,
    validate,
    validates,
)
from marshmallow.decorators import pre_dump

from .constants import CLIENT_CREDENTIALS_SCOPES, CLIENT_SCOPE
from .helpers import change_dict_keys

CLIENT_SCOPE_SIZE: Final[int] = len(CLIENT_SCOPE)
CLIENT_CREDENTIALS_SCOPE_SIZE: Final[int] = len(CLIENT_CREDENTIALS_SCOPES)


class TokenSchema(Schema):
    access_token = fields.Str(required=True, allow_none=False)
    token_type = fields.String(required=True, allow_none=False)
    expires_in = fields.Int(required=True, allow_none=False)
    scope = fields.String(required=False, allow_none=False)
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
    def scope_validation(self, value):
        values = set(value.split(" "))
        values_size = len(values)
        if value.strip() and (
            values_size > CLIENT_SCOPE_SIZE
            or not values.issubset(CLIENT_SCOPE)
        ):
            raise ValidationError("Invalid scope value.")


class ClientCredentialsTokenSchema(TokenSchema):
    @validates("scope")
    def scope_validation(self, value):
        values = set(value.split(" "))
        values_size = len(values)
        if value.strip() and (
            values_size > CLIENT_CREDENTIALS_SCOPE_SIZE
            or not values.issubset(CLIENT_CREDENTIALS_SCOPES)
        ):
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
        change_dict_keys(
            (("resourceType", "resource_type"), ("lastModified", "modified"),),
            data,
        )
        return data


class EmailSchema(Schema):
    value = fields.Email(required=True)
    primary = fields.Boolean(required=True)


class NameSchema(Schema):
    family_name = fields.Str(data_key="familyName")
    given_name = fields.Str(data_key="givenName")

    @pre_dump
    def preprocess(self, data, **kwargs):
        change_dict_keys(
            (("familyName", "family_name"), ("givenName", "given_name"),), data
        )
        return data


class SCIMUserSchema(Schema):
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
        change_dict_keys(
            (
                ("externalId", "external_id"),
                ("userName", "user_name"),
                ("displayName", "display_name"),
            ),
            data,
        )
        return data


class AdditionalInformationSchema(Schema):
    class Meta:
        unknown = INCLUDE


class DomainUserSchema(Schema):
    username = fields.Str(data_key="userName", required=True)
    password = fields.Str(
        validate=validate.Length(min=8, max=27), load_only=True
    )
    email = fields.Email(required=True)
    first_name = fields.Str(data_key="firstName", required=True)
    last_name = fields.Str(data_key="lastName", required=True)
    external_id = fields.UUID(data_key="externalId", required=False)
    accountNonExpired = fields.Boolean()
    accountNonLocked = fields.Boolean()
    credentialsNonExpired = fields.Boolean()
    enabled = fields.Boolean()
    internal = fields.Boolean(missing=False)
    preRegistration = fields.Boolean(missing=True)
    registrationCompleted = fields.Boolean()
    domain = fields.Str()
    source = fields.Str()
    client = fields.Str()
    loginsCount = fields.Int()
    logged_at = fields.DateTime(
        data_key="loggedAt", required=False, missing=datetime.datetime.now()
    )
    additionalInformation = fields.Nested(AdditionalInformationSchema)
    created_at = fields.DateTime(
        data_key="createdAt", required=False, missing=datetime.datetime.now()
    )
    updated_at = fields.DateTime(
        data_key="updatedAt", required=False, missing=datetime.datetime.now()
    )
