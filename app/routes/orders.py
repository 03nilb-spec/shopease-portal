from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import Order
from app.models.schema import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])


async def fetch_all_orders(db: AsyncSession) -> List[Order]:
    """Query the database and return all orders sorted by newest first."""
    result = await db.execute(select(Order).order_by(Order.created_at.desc()))
    return result.scalars().all()


async def fetch_order_by_id(order_id: str, db: AsyncSession) -> Optional[Order]:
    """Query the database and return a single order by its ID, or None if not found."""
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


VALID_STATUSES = {"shipped", "pending", "delivered", "cancelled"}


async def generate_order_id(db: AsyncSession) -> str:
    """Generate the next sequential order ID in the format ORD001, ORD002, etc."""
    result = await db.execute(select(func.count()).select_from(Order))
    count = result.scalar_one()
    return f"ORD{count + 1:03d}"


async def insert_order(data: OrderCreate, db: AsyncSession) -> Order:
    """Persist a new order to the database and return the created instance."""
    order_id = await generate_order_id(db)
    order = Order(
        id=order_id,
        customer=data.customer,
        items=data.items,
        status=data.status,
        total=data.total,
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(payload: OrderCreate, db: AsyncSession = Depends(get_db)):
    """Create a new order and return the saved record with its assigned ID."""
    if payload.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Oops! '{payload.status}' isn't a valid status. Please use one of: shipped, pending, delivered, cancelled.",
        )
    return await insert_order(payload, db)


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
