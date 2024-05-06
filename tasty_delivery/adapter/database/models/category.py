from datetime import datetime
from typing import List

from sqlalchemy import Column, String, BOOLEAN, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from adapter.database.db import Base
from adapter.database.models.product import Product


class Category(Base):
    __tablename__ = 'categories'

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
    is_active = Column(BOOLEAN)
    is_deleted = Column(BOOLEAN)
    created_at = Column(TIMESTAMP, default=datetime.utcnow())
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow())
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    updated_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    products: Mapped[List[Product]] = relationship()
