from pydantic import Field, BaseModel

from core.domain.entities.base_entity import Base


class CategoryIN(BaseModel):
    name: str = Field(title="Descrição da categoria")


class CategoryOUT(Base):
    name: str = Field(title="Descrição da categoria")
