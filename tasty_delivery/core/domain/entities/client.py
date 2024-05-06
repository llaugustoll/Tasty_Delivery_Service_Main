from typing import Annotated, List

from pydantic import Field, BaseModel

from core.domain.entities.base_entity import Base


class Client(Base):
    name: str = Field()
    email: str = Field()
    cpf: str = Field(max_length=11)
    scopes: Annotated[List, str] = Field([])


class ClientUpdate(BaseModel):
    name: str | None = Field(None)
    email: str | None = Field(None)
    cpf: str | None = Field(None, max_length=11)
