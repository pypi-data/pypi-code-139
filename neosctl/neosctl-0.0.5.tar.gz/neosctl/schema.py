import configparser
import dataclasses
import typing
from enum import Enum
from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel

from neosctl import constant


class FieldDataType(BaseModel):
    meta: Dict[str, Any]
    type: str


class FieldDefinition(BaseModel):
    name: str
    description: str | None = None
    type: str
    primary: bool
    optional: bool
    data_type: FieldDataType


class DataProductCreate(BaseModel):
    engine: str
    fields: List[FieldDefinition]


class RegisterCore(BaseModel):
    partition: str
    name: str


class RemoveCore(BaseModel):
    urn: str


class Auth(BaseModel):
    access_token: str = ""
    expires_in: int | None = None
    refresh_token: str = ""
    refresh_expires_in: int | None = None


class OptionalProfile(BaseModel):
    gateway_api_url: str = ""
    registry_api_url: str = ""
    iam_api_url: str = ""
    user: str = ""
    auth_flow: constant.AuthFlow = constant.AuthFlow.keycloak
    access_token: str = ""
    refresh_token: str = ""

    class Config:
        use_enum_values = True


class Profile(BaseModel):
    gateway_api_url: str
    registry_api_url: str
    iam_api_url: str
    user: str
    auth_flow: constant.AuthFlow
    access_token: str
    refresh_token: str

    class Config:
        use_enum_values = True


class EffectEnum(Enum):
    allow: str = "allow"
    deny: str = "deny"


class Statement(BaseModel):
    sid: str
    principal: typing.List[str]
    action: typing.List[str]
    resource: typing.List[str]
    condition: typing.List[str] | None = None
    effect: EffectEnum = EffectEnum.allow

    class Config:
        use_enum_values = True


class Statements(BaseModel):
    statements: typing.List[Statement]


class Policy(BaseModel):
    version: str = "2022-10-01"
    statements: list[Statement]


class UserPolicy(BaseModel):
    user: str
    policy: Policy


@dataclasses.dataclass
class Common:
    gateway_api_url: str
    registry_api_url: str
    iam_api_url: str
    profile_name: str
    config: configparser.ConfigParser
    profile: Profile | None

    def get_gateway_api_url(self):
        url = None
        if self.gateway_api_url:
            url = self.gateway_api_url
        elif self.profile and self.profile.gateway_api_url:
            url = self.profile.gateway_api_url
        return url

    def get_registry_api_url(self):
        url = None
        if self.registry_api_url:
            url = self.registry_api_url
        if self.profile and self.profile.registry_api_url:
            url = self.profile.registry_api_url
        return url

    def get_iam_api_url(self):
        url = None
        if self.iam_api_url:
            url = self.registry_api_url
        if self.profile and self.profile.iam_api_url:
            url = self.profile.iam_api_url
        return url
