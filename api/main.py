from fastapi import FastAPI
from .routers import inventory
from .database import Base, engine

app = FastAPI(title="Inventory Analytics API")

Base.metadata.create_all(bind=engine)

app.include_router(inventory.router)
