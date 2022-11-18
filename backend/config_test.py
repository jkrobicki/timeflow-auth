from fastapi import FastAPI, HTTPException, status, Request
from jose import JWTError, jwt
import requests
import os


def validate(token: str) -> None:
    """
    Validates the API key.

    Args:
        token (str): API key required to post the request to the endpoint.

    Raises:
        credentials_exception: when API key is missing or is invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials: incorrect API key",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
    except JWTError:
        raise credentials_exception


def authorize_request(request: Request):
    """
    Authorization dependency validation method.

    Args:
        request (Request): the Request with auth headers to be validated.
    """
    token = request.headers.get("apikey")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials are missing: missing API key",
        )
    validate(token=token)
