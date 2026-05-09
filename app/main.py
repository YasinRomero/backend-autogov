from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.router import api_router

from app.models import *

app = FastAPI(
    title="Tramites API",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)
app.include_router(api_router, prefix="/api/v1")