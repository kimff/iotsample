from fastapi import FastAPI
from .database import engine
from . import models
from .routers import device, user, auth, stream
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(device.router)
app.include_router(stream.router)
app.include_router(user.router)
app.include_router(auth.router)
