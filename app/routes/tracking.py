from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import Tracking
from app.models.schema import TrackingResponse

router = APIRouter(prefix="/tracking", tags=["tracking"])


async def fetch_tracking(order_id: str, db: AsyncSession):
    """Return the tracking record for an order, or None if not found."""
    result = await db.execute(select(Tracking).where(Tracking.order_id == order_id))
    return result.scalar_one_or_none()


@router.get("/{order_id}", response_model=TrackingResponse, status_code=200)
async def get_tracking(order_id: str, db: AsyncSession = Depends(get_db)):
    """Return delivery tracking info for an order, or a friendly 404 if not found."""
    tracking = await fetch_tracking(order_id, db)
    if tracking is None:
        raise HTTPException(
            status_code=404,
            detail=f"We couldn't find tracking info for order {order_id}. It may still be processing — please check back soon!",
        )
    return tracking
