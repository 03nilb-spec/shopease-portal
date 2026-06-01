from typing import List
from fastapi import APIRouter, Depends
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


@router.get("/", response_model=List[OrderResponse], status_code=200)
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    """Return all orders from the database."""
    return await fetch_all_orders(db)
