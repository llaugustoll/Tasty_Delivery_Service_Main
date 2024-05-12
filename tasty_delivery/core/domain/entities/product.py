from uuid import UUID

from pydantic import Field, BaseModel

from core.domain.entities.base_entity import Base
from core.domain.entities.category import CategoryOUT


class ProductIN(BaseModel):
    name: str = Field()
    description: str = Field()
    price: float = Field(gt=0)
    category_id: str = Field()

class ProductUpdateIN(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
    price: float | None = Field(gt=0)
    category_id: str | None = Field(None)


class ProductOUT(Base):
    name: str = Field()
    description: str = Field()
    price: float = Field(gt=0)
    category: CategoryOUT | None = Field(None)
