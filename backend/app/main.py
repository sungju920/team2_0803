from fastapi import FastAPI

from app.routers.products_routers import router


app = FastAPI(title="Team 01 CRUD API", version="0.1.0")


app.include_router(router)