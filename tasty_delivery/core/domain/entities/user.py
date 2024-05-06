from typing import Annotated, List

from pydantic import Field, field_validator, validate_email

from core.domain.entities.base_entity import Base
from core.domain.exceptions.exception import InvalidEmail


class User(Base):
    name: str = Field()
    email: str = Field()
    cpf: str = Field(max_length=11)
    username: str = Field()
    password: str = Field(serialization_alias='hashed_password')
    scopes: Annotated[List, str] = Field([])

    @field_validator('email', mode='before')
    @classmethod
    def check_email(cls, v: str) -> str:
        try:
            validate_email(v)
        except Exception as err:
            raise InvalidEmail(str(err), 400)
        return v

    @field_validator('cpf', mode='before')
    @classmethod
    def check_cpf(cls, v: str) -> str:
        return v.replace(".", "").replace("-", "").zfill(11)

    @field_validator('password', mode='before')
    @classmethod
    def generate_password(cls, v: str):
        from security import get_password_hash

        return get_password_hash(v)


class UserOUT(User):
    password: str = Field(None, exclude=True)


class UserInDB(User):
    hashed_password: str = Field()


class UserUpdate(Base):
    name: str = Field(None)
    email: str = Field(None)
    cpf: str = Field(None, max_length=11)

    @field_validator('email')
    @classmethod
    def check_email(cls, v: str) -> str:
        try:
            validate_email(v)
        except Exception as err:
            raise InvalidEmail(str(err), 400)
        return v

    @field_validator('cpf', mode='before')
    @classmethod
    def check_cpf(cls, v: str) -> str:
        return v.replace(".", "").replace("-", "").zfill(11)
