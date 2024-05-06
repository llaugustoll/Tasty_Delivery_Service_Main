from datetime import datetime

from sqlalchemy import Column, String, BOOLEAN, TIMESTAMP, UUID, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from adapter.database.db import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    cpf = Column(String, unique=True)
    is_active = Column(BOOLEAN)
    is_deleted = Column(BOOLEAN)
    created_at = Column(TIMESTAMP, default=datetime.utcnow())
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow())
    updated_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    scopes = Column(ARRAY(String), nullable=True)
