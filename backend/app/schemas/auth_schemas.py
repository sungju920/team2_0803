""" Login Logout schemas."""

from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    id: str = Field(min_length=1, max_length=100)
    pwd: str = Field(min_length=4, max_length=100)


class LoginResponse(BaseModel):
    id: str
    name: str
    message: str


class LogoutResponse(BaseModel):
    message: str
