from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import Order, Ticket
from app.models.schema import TicketCreate, TicketResponse

router = APIRouter(prefix="/tickets", tags=["tickets"])


async def fetch_all_tickets(db: AsyncSession) -> List[Ticket]:
    """Query the database and return all tickets sorted by newest first."""
    result = await db.execute(select(Ticket).order_by(Ticket.created_at.desc()))
    return result.scalars().all()


async def fetch_order(order_id: str, db: AsyncSession):
    """Return a single order by ID, or None if not found."""
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def generate_ticket_id(db: AsyncSession) -> str:
    """Generate the next sequential ticket ID in the format TKT001."""
    result = await db.execute(select(func.count()).select_from(Ticket))
    count = result.scalar()
    return f"TKT{count + 1:03d}"


async def insert_ticket(ticket_id: str, data: TicketCreate, db: AsyncSession) -> Ticket:
    """Insert a new ticket into the database and return the created record."""
    ticket = Ticket(
        id=ticket_id,
        order_id=data.order_id,
        issue=data.issue,
        status="open",
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.get("/", response_model=List[TicketResponse], status_code=200)
async def get_all_tickets(db: AsyncSession = Depends(get_db)):
    """Return all support tickets from the database."""
    return await fetch_all_tickets(db)


@router.post("/", response_model=TicketResponse, status_code=201)
async def create_ticket(data: TicketCreate, db: AsyncSession = Depends(get_db)):
    """Create a new support ticket after validating the linked order exists."""
    order = await fetch_order(data.order_id, db)
    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"We couldn't find order {data.order_id}. Please double-check the order ID and try again.",
        )
    ticket_id = await generate_ticket_id(db)
    return await insert_ticket(ticket_id, data, db)
