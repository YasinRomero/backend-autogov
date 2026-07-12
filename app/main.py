from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.db.session import Base, engine
from app.api.router import api_router
from app.db.init_db import init_data

from app.models import *

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_data()
    yield

app = FastAPI(
    title="Tramites API",
    version="0.1.0",
    lifespan=lifespan
)

origins = [
    "http://localhost:4200",
    "https://tramitesmunicipalesweb.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")