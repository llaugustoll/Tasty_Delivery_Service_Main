from datetime import datetime

from sqlalchemy import Column, String, Float, Boolean, TIMESTAMP, Integer, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from adapter.database.db import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)
    client_id: Mapped[UUID] = mapped_column(ForeignKey("clients.id"), nullable=True)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    total = Column(Float)
    discount = Column(Float)
    status = Column(String)

    # product_association = relationship('OrderProductAssociation', back_populates='order')
    # products = association_proxy("product_association", "product")
