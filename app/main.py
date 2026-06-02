from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, notifications, orders, tickets, tracking

app = FastAPI(title="ShopEase Customer Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(notifications.router)
app.include_router(orders.router)
app.include_router(tickets.router)
app.include_router(tracking.router)
