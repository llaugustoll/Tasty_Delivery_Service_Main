from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import Field, BaseModel

from core.domain.entities.client import Client
from core.domain.entities.product import ProductOUT


class OrderBase(BaseModel):
    id: int = Field(None)
    is_active: bool = Field(True)
    is_deleted: bool = Field(False)
    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
    created_by: UUID | None = Field(None)
    updated_by: UUID | None = Field(None)


class Product(BaseModel):
    product_id: UUID = Field()
    price: float | None = Field()
    quantity: int | None = Field()
    obs: str | None = Field(None)


class OrderIN(BaseModel):
    products: List[Product] = Field()
    discount: float | None = Field(0, gte=0)
    total: float = Field(gte=0)


class OrderUpdate(BaseModel):
    products: List[Product] | None = Field()
    discount: float | None = Field(gte=0)
    total: float | None = Field(gte=0)
    status: str | None = Field(None)


class OrderOUT(BaseModel):
    order_id: int = Field(..., alias="order_id")
    products: List[Product] | None = Field()
    discount: float | None = Field(gte=0)
    total: float | None = Field(gte=0)
    status: str | None = Field()
