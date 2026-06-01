from datetime import datetime
from typing import List
from pydantic import BaseModel


class OrderResponse(BaseModel):
    """Pydantic schema for a single order returned by the API."""

    id: str
    customer: str
    items: List[str]
    status: str
    total: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TicketCreate(BaseModel):
    """Pydantic schema for creating a new support ticket."""

    order_id: str
    issue: str


class TicketResponse(BaseModel):
    """Pydantic schema for a support ticket returned by the API."""

    id: str
    order_id: str
    issue: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
