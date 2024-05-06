from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Base(BaseModel):
    id: UUID = Field(None)
    is_active: bool = Field(True)
    is_deleted: bool = Field(False)
    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
    created_by: UUID | None = Field(None)
    updated_by: UUID | None = Field(None)
