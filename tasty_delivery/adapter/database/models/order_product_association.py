from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from adapter.database.db import Base


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), primary_key=True)
    quantity: Mapped[Integer] = Column(Integer)
    obs: Mapped[String] = Column(String, nullable=True)

    order: Mapped["Order"] = relationship('Order', back_populates="product_association")
    product: Mapped["Product"] = relationship('Product', back_populates="order_association")
