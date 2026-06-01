from fastapi import FastAPI

from app.routes import orders, tickets, tracking

app = FastAPI(title="ShopEase Customer Portal")

app.include_router(orders.router)
app.include_router(tickets.router)
app.include_router(tracking.router)
