import os
from typing import Optional, TypedDict
from enum import Enum
from datetime import datetime

import json
from fastapi import Depends, HTTPException
import strawberry
from strawberry.extensions import Extension
from strawberry.fastapi.router import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from nasbio import settings
from nasbio.db import get_async_session, get_session


class Group(Enum):
    pass


class Role(Enum):
    user = 'user'
    admin = 'admin'


class Permission(Enum):
    pass


class Authorization(TypedDict):
    groups: list[Group]
    roles: list[Role]
    permissions: list[Permission]


class UserPayloadDict(TypedDict):
    authorization: Authorization
    iss: str
    sub: str
    aud: list[str]
    iat: int
    exp: int


class AuthExtension(Extension):
    def on_request_start(self):
        current_user: UserPayloadDict = self.execution_context.context.get('current_user')
        if (
            # Valid auth credentials.
            (current_user and current_user['sub'])
            or (
            # Development environment.
            os.environ.get('FASTAPI_ENV') == 'development'
            and (
                # Subgraph introspection by apollo gateway.
                self.execution_context.query == 'query __ApolloGetServiceDefinition__ { _service { sdl } }'
                or
                # Subgraph introspection by rover.
                self.execution_context.query == 'query SubgraphIntrospectQuery {\n    # eslint-disable-next-line'
                                                '\n    _service {\n        sdl\n    }\n}'
                or
                # GraphiQL request.
                self.execution_context.context.get('request').headers.get('referer')
                == f'https://localhost/api/{settings.SERVER_ID}/graphql'
            )
        )
            or
            # Test environment.
            os.environ.get('FASTAPI_ENV') == 'testing'
        ):
            return
        else:
            raise HTTPException(status_code=401, detail='Invalid credentials provided.')


class Context(TypedDict):
    db: Session
    async_db: AsyncSession
    current_user: Optional[UserPayloadDict]


async def get_context(
    request: Request,
    db=Depends(get_session),
    async_db=Depends(get_async_session),
) -> Context:
    current_user_header: str = request.headers.get('current-user')
    user_payload: Optional[UserPayloadDict] = json.loads(current_user_header) \
        if (current_user_header and current_user_header != 'undefined') else None

    return {
        'db': db,
        'async_db': async_db,
        'current_user': user_payload,
    }


# class IsAdmin(BasePermission):
#     message = 'Admin required.'
#
#     def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
#         return info.context['current_user']['admin']


DateTime = strawberry.scalar(
    datetime,
    serialize=lambda value: value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
    parse_value=lambda value: datetime.fromisoformat(value.rstrip('Z')),
)


@strawberry.interface
class MutationResponse:
    success: bool
    message: str
