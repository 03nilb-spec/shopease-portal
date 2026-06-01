from fastapi import FastAPI

from app.routes import orders

app = FastAPI(title="ShopEase Customer Portal")

app.include_router(orders.router)
