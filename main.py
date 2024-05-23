import uvicorn

from ipaddress import ip_address
from typing import Callable
from pathlib import Path

import redis.asyncio as redis
from fastapi import FastAPI, Request, status, Depends, HTTPException
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

# from src.routes import contacts, auth, users
from src.conf.config import settings
from src.database.db import get_db
from routes import auth, user_option,images

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(user_option.router, prefix="/api")
app.include_router(images.router, prefix="/api")

banned_ips = [
    # ip_address("192.168.1.1"),
    # ip_address("192.168.1.2"),
]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router(auth.router)
# app.include_router(users.router)
# app.include_router(contacts.router)


# @app.on_event("startup")
# async def startup():
#     """
#     The startup function is called when the application starts up.
#     It's a good place to initialize things that are needed by your app, like database connections or caches.
    
#     :return: A future object, which is a coroutine
#     :doc-author: Trelent
#     """
#     r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, password=settings.redis_password)
#     await FastAPILimiter.init(r)


@app.get("/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.get("/")
def main_root():
    """
    The main_root function is the root of the API. It returns a JSON object with
    a message that says &quot;Contacts application&quot;. This function is called when you
    visit http://localhost:8000/. The main_root function does not take any
    arguments.
    
    :return: A dictionary
    :doc-author: Trelent
    """
    return {"message": "Pythongram started"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)