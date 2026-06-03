from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, cart, customer_profile, notifications, orders, products, tickets, tracking

app = FastAPI(title="ShopEase Customer Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cart.router)
app.include_router(customer_profile.router)
app.include_router(products.router)
app.include_router(notifications.router)
app.include_router(orders.router)
app.include_router(tickets.router)
app.include_router(tracking.router)
