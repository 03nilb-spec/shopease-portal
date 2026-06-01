from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import Order
from app.models.schema import OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])


async def fetch_all_orders(db: AsyncSession) -> List[Order]:
    """Query the database and return all orders sorted by newest first."""
    result = await db.execute(select(Order).order_by(Order.created_at.desc()))
    return result.scalars().all()


async def fetch_order_by_id(order_id: str, db: AsyncSession) -> Optional[Order]:
    """Query the database and return a single order by its ID, or None if not found."""
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


@router.get("/", response_model=List[OrderResponse], status_code=200)
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    """Return all orders from the database."""
    return await fetch_all_orders(db)


@router.get("/{order_id}", response_model=OrderResponse, status_code=200)
async def get_order(order_id: str, db: AsyncSession = Depends(get_db)):
    """Return a single order by ID, or a friendly 404 if it doesn't exist."""
    order = await fetch_order_by_id(order_id, db)
    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"We couldn't find your order {order_id}. Please double-check the order ID and try again.",
        )
    return order
