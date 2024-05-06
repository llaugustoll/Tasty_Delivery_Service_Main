from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, BOOLEAN, TIMESTAMP, UUID, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from adapter.database.db import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    is_active = Column(BOOLEAN, default=True)
    is_deleted = Column(BOOLEAN, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow())
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow())
    category_id = Column(UUID, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products", viewonly=True)
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    updated_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)

    order_association = relationship('OrderProductAssociation', back_populates='product')
    orders = association_proxy("order_association", "order")
