"""공지사항 API의 요청과 응답 형식입니다."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoticeCreate(BaseModel):
    """공지사항 등록 요청입니다. 작성자는 현재 관리자 고정값으로 처리합니다."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=200, description="공지 제목")
    content: str = Field(..., min_length=1, description="공지 본문")


class NoticeUpdate(NoticeCreate):
    """공지사항 수정 요청입니다."""


class NoticeListItem(BaseModel):
    """목록 화면에 필요한 최소 공지 정보입니다."""

    id: int
    title: str


class NoticeDetail(BaseModel):
    """상세 화면에 표시할 공지 정보입니다."""

    id: int
    title: str
    content: str
    writer: str
    created_at: datetime
    updated_at: datetime


class NoticeDeleteResult(BaseModel):
    """공지 삭제 결과입니다."""

    message: str

