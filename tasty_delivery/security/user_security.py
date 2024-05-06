from datetime import timedelta

from adapter.database.db import get_db
from core.application.use_cases.user.user_case import UserCase
from core.domain.entities.user import User
from core.domain.exceptions.exception import DuplicateObject, ObjectNotFound
from security.base import create_access_token, Token, verify_password
from settings import settings


def get_user_token(user):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires,
    )
    return Token(**{"access_token": access_token, "token_type": "bearer"})


def handle_user_signup(user, current_user):
    result = UserCase(next(get_db())).get_by_cpf(user.cpf)
    if result:
        raise DuplicateObject("Usuário já existente na base de dados", 409)
    else:
        user = User(**user.model_dump(), username=user.email)
        user = UserCase(next(get_db())).create(user)

        return get_user_token(user)


def authenticate_user(form_data) -> Token:
    from core.application.use_cases.user.user_case import UserCase
    from core.application.use_cases.client.client_case import ClientCase

    if form_data.scopes and 'client' in form_data.scopes:
        user = ClientCase(next(get_db())).get_by_cpf(form_data.username)
    else:
        user = UserCase(next(get_db())).get_by_username(form_data.username)

        if not user or not verify_password(form_data.password, user.hashed_password):
            raise ObjectNotFound(status_code=400, msg="Usuário ou senha incorretos")

    return get_user_token(user)
