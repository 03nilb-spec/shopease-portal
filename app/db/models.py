from sqlalchemy import Column, String, Integer, TIMESTAMP, ARRAY, Text
from sqlalchemy.sql import func
from app.db.database import Base


class Order(Base):
    """SQLAlchemy model for the orders table."""

    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    customer = Column(String, nullable=False)
    items = Column(ARRAY(Text), nullable=False)
    status = Column(String, nullable=False)
    total = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
