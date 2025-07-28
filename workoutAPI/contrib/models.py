from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
import uuid


#Classe pai o qual os models irão herdar
class BaseModel(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid.uuid4, nullable=False, primary_key=True)