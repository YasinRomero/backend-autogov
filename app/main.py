from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import Base, engine
from app.api.router import api_router

from app.models import *

app = FastAPI(
    title="Tramites API",
    version="0.1.0"
)

origins = [
    "http://localhost:4200",
    "https://tramitesmunicipalesweb.onrender.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(api_router, prefix="/api/v1")