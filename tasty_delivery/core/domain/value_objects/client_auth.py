from typing import Annotated, List

from pydantic import Field

from core.domain.entities.base_entity import Base


class ClientAuth(Base):
    name: str = Field()
    email: str = Field()
    username: str = Field(max_length=11)
    scopes: Annotated[List, str] = Field([])
