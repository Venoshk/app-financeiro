from db.databese import Base 
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String, unique=True, index=True)
    description = Column(String)
    amount = Column(Float)
    category = Column(String)
    date = Column(DateTime)
    type = Column(String)
    item_id = Column(String)