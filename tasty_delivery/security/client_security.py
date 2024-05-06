from datetime import timedelta

from adapter.database.db import get_db
from core.application.use_cases.client.client_case import ClientCase
from core.domain.entities.client import Client
from core.domain.exceptions.exception import ObjectNotFound, DuplicateObject
from core.domain.value_objects.auth import Auth
from security.base import Token, create_access_token
from settings import settings


def get_client_token(client):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": client.cpf, "scopes": client.scopes},
        expires_delta=access_token_expires,
    )
    return Token(**{"access_token": access_token, "token_type": "bearer"})


def authenticate_client(cpf: str):
    client = ClientCase(next(get_db())).get_by_cpf(cpf)

    if not client:
        raise ObjectNotFound(status_code=400, msg="Usuário ou senha incorretos")

    return get_client_token(client)


def signup_client(client: Auth):
    client_db = ClientCase(next(get_db())).get_by_cpf(client.cpf)

    if client_db:
        raise DuplicateObject("Cliente já existente na base de dados", 409)
    else:
        client = Client(**client.model_dump())
        client = ClientCase(next(get_db())).create(client)

        return get_client_token(client)
