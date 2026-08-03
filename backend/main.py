from fastapi import FastAPI

from backend.app.routers import products_routers
from backend.app.routers import (
    auth_routers,
)
from backend.app.routers import cart_items_routers
from backend.app.routers import customers_routers
from backend.app.routers import notices_routers

app = FastAPI(title="Team 01 CRUD API", version="0.1.0")

app.include_router(customers_routers.router)
app.include_router(products_routers.router)
app.include_router(cart_items_routers.router)
app.include_router(notices_routers.router)
app.include_router(auth_routers.router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}

