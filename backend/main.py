from fastapi import APIRouter, Depends, Header
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from pydantic import BaseModel
from fastapi import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
import json
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import time
from fastapi.responses import JSONResponse
import os
from fastapi.middleware.cors import CORSMiddleware
from data import SECRET_KEY, ALGORITHM

### secret gen ###
import secrets

secret = secrets.token_hex(16)
### ###

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str) -> None:
    """
    Validates the API key.

    Args:
        token (str): API key required to post the request to the endpoint.

    Raises:
        credentials_exception: when API key is missing or is invalid.
    """
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials: incorrect API key",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return "token no work"
        # raise credentials_exception


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Middleware function adding headers to http calls

    Args:
        request (Request): sent Request class object
        call_next (_type_): call func

    Returns:
        object: response
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# @app.middleware("http")
# async def add_middleware_here(request: Request, call_next):
#     """verify token"""
#     token = request.headers["Authorization"]
#     try:
#         verification_of_token = verify_token(token)
#         if verification_of_token:
#             response = await call_next(request)
#             return response
#         else:
#             return JSONResponse(status_code=403)  # or 401
#     except:
#         return JSONResponse(status_code=401)


"""
steps:
1. create jwt
2. create get method
3. add to get method headers with token
4. validate get method using token
"""
