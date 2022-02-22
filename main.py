from fastapi import FastAPI
from routers import *
from models import *

app = FastAPI()


# setup_db()

@app.on_event("startup")
def on_startup():
    setup_db()


app.include_router(users.router)
app.include_router(levels.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
