from pydantic import BaseModel, Field, field_validator, validate_email

from core.domain.exceptions.exception import InvalidEmail


class Auth(BaseModel):
    cpf: str = Field(max_length=11, min_length=11)
    name: str = Field(None)
    email: str = Field(None)
    admin: bool | None = Field(False)
    password: str | None = Field(None)

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
