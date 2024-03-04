from fastapi.middleware.cors import CORSMiddleware
from app import models, cliente
from app.database import engine
from fastapi import FastAPI

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8090",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cliente.router, tags=["Customer"], prefix="/customer")

@app.get("/api/healthchecker")
def root():
    return {"message": "The API is LIVE!!"}