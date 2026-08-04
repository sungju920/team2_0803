"""고객 관리 요청 및 응답 스키마."""

from datetime import datetime

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    """고객 등록 및 회원가입 요청."""

    id: str = Field(min_length=1, max_length=100)
    pwd: str = Field(min_length=4, max_length=100)
    name: str = Field(min_length=1, max_length=100)


class CustomerUpdate(BaseModel):
    """고객 정보 수정 요청."""

    pwd: str | None = Field(default=None, min_length=4, max_length=100)
    name: str | None = Field(default=None, min_length=1, max_length=100)


class CustomerResponse(BaseModel):
    """비밀번호를 제외한 고객 응답."""

    id: str
    name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CustomerDeleteResponse(BaseModel):
    message: str
