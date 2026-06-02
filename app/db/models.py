from sqlalchemy import Column, String, Integer, TIMESTAMP, ARRAY, Text, Date, ForeignKey, Index
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    """SQLAlchemy model for the users table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="customer")


class Order(Base):
    """SQLAlchemy model for the orders table."""

    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    customer = Column(String, nullable=False)
    items = Column(ARRAY(Text), nullable=False)
    status = Column(String, nullable=False)
    total = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Ticket(Base):
    """SQLAlchemy model for the tickets table."""

    __tablename__ = "tickets"

    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    issue = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Tracking(Base):
    """SQLAlchemy model for the tracking table."""

    __tablename__ = "tracking"

    order_id = Column(String, ForeignKey("orders.id"), primary_key=True)
    location = Column(String, nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now())
    eta = Column(Date, nullable=True)
