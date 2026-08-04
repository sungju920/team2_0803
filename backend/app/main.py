from fastapi import FastAPI

from backend.app.routers import (
    auth_routers,
    cart_items_routers,
    customers_routers,
    notices_routers,
    products_routers,
)

app = FastAPI(title="Team 02 CRUD API", version="0.1.0")

app.include_router(customers_routers.router)
app.include_router(auth_routers.router)
app.include_router(products_routers.router)
app.include_router(cart_items_routers.router)
app.include_router(notices_routers.router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}

