from ipaddress import ip_address
from typing import Callable
from pathlib import Path

import redis.asyncio as redis
from fastapi import FastAPI, Request, status
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.routes import contacts, auth, users
from src.conf.config import settings

app = FastAPI()

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


# @app.middleware("http")
# async def ban_ips(request: Request, call_next: Callable):
#     """
#     The ban_ips function is a middleware function that checks if the client's IP address is in the banned_ips list.
#     If it is, then we return a JSONResponse with status code 403 and an error message. If not, then we call next(request)
#     and return its response.
    
#     :param request: Request: Get the client's ip address
#     :param call_next: Callable: Call the next function in the pipeline
#     :return: A response object
#     :doc-author: Trelent
#     """
#     ip = ip_address(request.client.host)
#     if ip in banned_ips:
#         return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
#     response = await call_next(request)
#     return response


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(contacts.router)


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app, like database connections or caches.
    
    :return: A future object, which is a coroutine
    :doc-author: Trelent
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, password=settings.redis_password)
    await FastAPILimiter.init(r)


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
    return {"message": "Contacts application"}