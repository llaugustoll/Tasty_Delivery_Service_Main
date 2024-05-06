from datetime import datetime, timedelta

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer
from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

from adapter.database.db import get_db
from logger import logger
from settings import settings

EXPIRATION_ERROR = "Credencial expirada"
CREDENTIAL_ERROR = "Não foi possível validar o token"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_token = HTTPBearer()


class AuthenticationError(HTTPException):
    def __init__(self, status_code: int, msg):
        super(AuthenticationError, self).__init__(status_code=status_code, detail=msg)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_current_user(token=Security(bearer_token)):
    from core.application.use_cases.user.user_case import UserCase
    from core.application.use_cases.client.client_case import ClientCase

    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except AttributeError:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    except ExpiredSignatureError:
        logger.warning(EXPIRATION_ERROR)
        raise AuthenticationError(status_code=status.HTTP_401_UNAUTHORIZED, msg=EXPIRATION_ERROR)

    except (JWTError, ValidationError):
        logger.warning(CREDENTIAL_ERROR)
        raise AuthenticationError(status_code=status.HTTP_401_UNAUTHORIZED, msg=CREDENTIAL_ERROR)

    username: str = payload.get("sub")
    if not username:
        raise AuthenticationError(status_code=status.HTTP_401_UNAUTHORIZED, msg=CREDENTIAL_ERROR)
    token_scopes = payload.get("scopes", [])
    token_data = TokenData(scopes=token_scopes, username=username)

    if 'client' in token_scopes:
        user = ClientCase(next(get_db())).get_by_cpf(cpf=token_data.username)
    else:
        user = UserCase(next(get_db())).get_by_username(user_name=token_data.username)
    if not user:
        logger.warning(CREDENTIAL_ERROR)
        raise AuthenticationError(status_code=status.HTTP_401_UNAUTHORIZED, msg=CREDENTIAL_ERROR)
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def has_permission(permission):
    def decorator(func):
        def wrapped_function(*args, **kwargs):
            if 'client' in permission or 'login' in permission:
                return func(*args, **kwargs)

            use_case = args[0]
            if not use_case.current_user:
                raise AuthenticationError(status_code=status.HTTP_403_FORBIDDEN, msg="Acesso negado")

            current_user = use_case.current_user

            if bool(set(permission) & set(current_user.scopes)):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    logger.warning(str(err))
                    raise err
            else:
                raise AuthenticationError(status_code=status.HTTP_403_FORBIDDEN, msg="Acesso negado")

        return wrapped_function

    return decorator
