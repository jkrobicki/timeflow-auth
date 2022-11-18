from main import app
from fastapi import Header, Request
from data import SECRET_KEY, ALGORITHM
from pydantic import BaseModel
from jose import jwt


class Token(BaseModel):
    value: str


@app.post("/token")
async def test(user_id, author: str | None = Header(default=None)):
    """Working jwt encoding

    Args:
        user_id (int): User id to encode

    Returns:
        str: token
    """
    payload = {"userID": user_id, "expiry": 1}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(token)
    return token


@app.get("/items/")
async def read_items(request: Request):
    auth_header = request.headers.get("Authorization")
    return f"item is, auth header is {auth_header}"
